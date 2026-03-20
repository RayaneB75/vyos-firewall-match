API Reference
=============

VyFwMatch is primarily a command-line tool, but its modules can be used
programmatically. This document describes both the CLI interface and the
internal Python API.

## Command-Line Interface

### Installation

```bash
pip install -e .
```

This installs the `vyfwmatch` command.

### Usage

```bash
vyfwmatch [OPTIONS]
```

**Required Arguments:**

- `--config PATH` - Path to VyOS boot configuration file
- `--inbound-interface NAME` - Inbound interface name (e.g., eth0, bond0)
- `--source IP` - Source IP address
- `--destination IP` - Destination IP address
- At least one of:
  - `--service NAME` - Service name (e.g., http, ssh, dns)
  - `--protocol NAME` - Protocol (e.g., tcp, udp, icmp)

**Optional Arguments:**

- `--outbound-interface NAME` - Outbound interface name
- `--hook {forward,input,output}` - Firewall hook (default: auto-detect)
- `--port NUMBER` - Destination port (requires `--protocol`)
- `--state {new,established,related,invalid}` - Connection state
- `--format {table,json}` - Output format (default: table)

### Examples

```bash
# Test forwarded HTTPS traffic
vyfwmatch --config config.boot --inbound-interface eth0 \
  --source 10.0.0.1 --destination 192.168.0.10 --service https

# Test input traffic with specific state
vyfwmatch --config config.boot --inbound-interface eth0 \
  --source 1.2.3.4 --destination 192.168.0.1 --protocol tcp \
  --port 22 --state new --hook input

# JSON output for scripting
vyfwmatch --config config.boot --inbound-interface eth0 \
  --source 10.0.0.1 --destination 8.8.8.8 --protocol icmp \
  --format json
```

## Python API

### High-Level Usage

```python
from vyfwmatch.adapters.vyos_config import VyOSConfigAdapter
from vyfwmatch.services.rule_loader import RuleLoaderService
from vyfwmatch.services.decision_engine import DecisionEngine
from vyfwmatch.domain.models import TrafficTuple

# Load VyOS configuration
adapter = VyOSConfigAdapter("config.boot")

# Load firewall rules
loader = RuleLoaderService(adapter)
fw_config = loader.load_firewall_config()

# Create traffic tuple
traffic = TrafficTuple(
    inbound_interface="eth0",
    outbound_interface="eth1",
    source_ip="10.0.0.1",
    destination_ip="192.168.0.10",
    protocol="tcp",
    port=443,
    state="new",
    hook=None  # Auto-detect
)

# Match against firewall rules
engine = DecisionEngine(fw_config)
result = engine.match(traffic)

# Check result
print(f"Action: {result.action}")
print(f"Chain: {result.chain_name}")
print(f"Rule: {result.rule_number}")
```

### Module Reference

## vyfwmatch.adapters.vyos_config

### VyOSConfigAdapter

**Purpose:** Interface to VyOS configuration files

```python
class VyOSConfigAdapter:
    def __init__(self, config_path: str):
        """Load VyOS configuration from file.
        
        Args:
            config_path: Path to VyOS boot config file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
        """
    
    def get_firewall_config(self) -> dict:
        """Get firewall configuration tree.
        
        Returns:
            Nested dict representing firewall config
        """
    
    def get_groups(self) -> dict:
        """Get firewall groups configuration.
        
        Returns:
            Dict of group definitions
        """
    
    def get_global_options(self) -> dict:
        """Get global firewall options.
        
        Returns:
            Dict of global settings (state-policy, etc.)
        """
```

## vyfwmatch.services.rule_loader

### RuleLoaderService

**Purpose:** Load and parse firewall configuration

```python
class RuleLoaderService:
    def __init__(self, adapter: VyOSConfigAdapter):
        """Initialize with a config adapter.
        
        Args:
            adapter: VyOS configuration adapter
        """
    
    def load_firewall_config(self) -> FirewallConfig:
        """Load complete firewall configuration.
        
        Returns:
            FirewallConfig with groups, chains, and policies
        """
```

## vyfwmatch.services.decision_engine

### DecisionEngine

**Purpose:** Evaluate firewall rules against traffic

```python
class DecisionEngine:
    def __init__(self, config: FirewallConfig):
        """Initialize with firewall configuration.
        
        Args:
            config: Firewall configuration to evaluate
        """
    
    def match(self, traffic: TrafficTuple) -> MatchResult:
        """Match traffic against firewall rules.
        
        Args:
            traffic: Traffic tuple to match
            
        Returns:
            MatchResult with action and details
        """
```

## vyfwmatch.domain.models

### TrafficTuple

Represents network traffic to be evaluated:

```python
@dataclass
class TrafficTuple:
    inbound_interface: str
    source_ip: str
    destination_ip: str
    protocol: Optional[str] = None
    port: Optional[int] = None
    outbound_interface: Optional[str] = None
    state: Optional[str] = None
    hook: Optional[str] = None  # forward, input, output
```

### MatchResult

Result of firewall rule evaluation:

```python
@dataclass
class MatchResult:
    matched: bool
    action: str  # accept, drop, reject
    chain_name: str
    chain_family: str  # ipv4, ipv6
    chain_hook: str  # forward, input, output
    rule_number: Optional[int] = None
    rule: Optional[Rule] = None
    is_default_action: bool = False
    is_state_policy: bool = False
    state_policy_state: Optional[str] = None
    trace: List[str] = field(default_factory=list)
```

### FirewallConfig

Container for firewall configuration:

```python
@dataclass
class FirewallConfig:
    groups: Dict[str, FirewallGroup] = field(default_factory=dict)
    chains: Dict[str, Chain] = field(default_factory=dict)
    state_policy: Optional[StatePolicy] = None
    
    def get_group(self, name: str, family: str = "ipv4") -> Optional[FirewallGroup]:
        """Get a firewall group by name.
        
        Args:
            name: Group name
            family: Address family (ipv4 or ipv6)
            
        Returns:
            FirewallGroup or None if not found
        """
```

### Chain

Firewall chain definition:

```python
@dataclass
class Chain:
    name: str
    family: str  # ipv4, ipv6
    hook: str  # forward, input, output
    default_action: str = "accept"
    rules: List[Rule] = field(default_factory=list)
```

### Rule

Individual firewall rule:

```python
@dataclass
class Rule:
    number: int
    action: str  # accept, drop, reject, jump, continue, return
    description: str = ""
    protocol: Optional[str] = None
    source: SourceDestCriteria = field(default_factory=SourceDestCriteria)
    destination: SourceDestCriteria = field(default_factory=SourceDestCriteria)
    inbound_interface: InterfaceCriteria = field(default_factory=InterfaceCriteria)
    outbound_interface: InterfaceCriteria = field(default_factory=InterfaceCriteria)
    state: List[str] = field(default_factory=list)
    jump_target: Optional[str] = None
    disabled: bool = False
```

### FirewallGroup

Group definition (address, network, port, interface):

```python
@dataclass
class FirewallGroup:
    name: str
    group_type: str  # address-group, network-group, port-group, interface-group
    members: List[str] = field(default_factory=list)
```

## vyfwmatch.cli.output_formatter

### format_result

Format match result for display:

```python
def format_result(result: MatchResult, output_format: str = "table") -> str:
    """Format a match result for display.
    
    Args:
        result: Match result from decision engine
        output_format: "table" or "json"
        
    Returns:
        Formatted string for display
    """
```

## Legacy API (Internal Use)

The following modules are used internally and maintained for backward
compatibility:

### parser.config_parser

```python
def parse_config(text: str) -> ConfigTree:
    """Parse VyOS boot config text.
    
    Args:
        text: VyOS configuration in curly-brace format
        
    Returns:
        Nested dict structure (ConfigTree)
    """

def parse_config_file(path: str) -> ConfigTree:
    """Parse VyOS boot config from file.
    
    Args:
        path: Path to config file
        
    Returns:
        Nested dict structure (ConfigTree)
    """
```

### matcher.helpers

Utility functions for matching:

```python
def ip_matches(rule_addr: str, traffic_ip: str, groups: dict, family: str) -> bool:
    """Check if traffic IP matches rule address criteria."""

def port_matches(rule_port: str, traffic_port: int, groups: dict) -> bool:
    """Check if traffic port matches rule port criteria."""

def interface_matches(rule_iface: str, traffic_iface: str, groups: dict) -> bool:
    """Check if traffic interface matches rule interface criteria."""

def resolve_service(service: str) -> Tuple[Optional[int], Optional[str]]:
    """Resolve service name to port and protocol.
    
    Args:
        service: Service name (e.g., "http", "ssh")
        
    Returns:
        (port, protocol) tuple or (None, None) if unknown
    """
```

## Error Handling

All modules raise standard Python exceptions:

- `FileNotFoundError` - Config file not found
- `ValueError` - Invalid configuration or arguments
- `KeyError` - Missing required configuration

Example error handling:

```python
try:
    adapter = VyOSConfigAdapter("config.boot")
    loader = RuleLoaderService(adapter)
    config = loader.load_firewall_config()
except FileNotFoundError:
    print("Configuration file not found")
except ValueError as e:
    print(f"Invalid configuration: {e}")
```

## Type Hints

All new modules use comprehensive type hints for better IDE support and
type checking. Use `mypy` for static type checking:

```bash
mypy vyfwmatch/
```

## Testing

Use pytest to test your integrations:

```python
from vyfwmatch.adapters.vyos_config import VyOSConfigAdapter
from vyfwmatch.services.rule_loader import RuleLoaderService
from vyfwmatch.services.decision_engine import DecisionEngine
from vyfwmatch.domain.models import TrafficTuple

def test_firewall_matching():
    adapter = VyOSConfigAdapter("tests/fixtures/sample_config.boot")
    loader = RuleLoaderService(adapter)
    config = loader.load_firewall_config()
    
    engine = DecisionEngine(config)
    traffic = TrafficTuple(
        inbound_interface="eth0",
        source_ip="10.0.0.1",
        destination_ip="192.168.0.10",
        protocol="tcp",
        port=443
    )
    
    result = engine.match(traffic)
    assert result.action == "accept"
```
