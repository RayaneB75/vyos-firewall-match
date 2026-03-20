Architecture
============

This document describes the modular architecture of VyFwMatch and how it
processes VyOS boot configurations to evaluate firewall rules.

## Overview

VyFwMatch follows a layered, modular architecture designed for maintainability,
testability, and future integration with the official VyOS codebase (`vyos-1x`).

## Directory Layout

### Core Package (`vyfwmatch/`)

```
vyfwmatch/
├── __init__.py           # Package initialization
├── main.py               # Main entry point
├── cli/                  # Command-line interface
│   ├── argument_parser.py
│   └── output_formatter.py
├── adapters/             # External integrations
│   └── vyos_config.py    # VyOS config adapter
├── services/             # Business logic
│   ├── rule_loader.py    # Load firewall config
│   └── decision_engine.py # Match rules against traffic
└── domain/               # Core models
    └── models.py         # Domain objects
```

### Legacy Modules (Internal Use)

```
parser/                   # Config parsing (used by adapter)
├── config_parser.py      # VyOS config tokenizer
├── firewall_extractor.py # Legacy extractor
└── models.py             # Legacy models

matcher/                  # Matching helpers
├── helpers.py            # IP/port matching utilities
└── engine.py             # Legacy matching engine

ui/                       # Legacy CLI (deprecated)
├── cli.py
└── output.py
```

## Execution Flow

1. **CLI Entry** (`vyfwmatch/main.py`)
   - Parse command-line arguments
   - Validate inputs (IP addresses, ports, etc.)

2. **Configuration Loading** (`vyfwmatch/adapters/vyos_config.py`)
   - Load VyOS config file
   - Currently bridges to legacy `parser/config_parser.py`
   - Future: Direct integration with `vyos-1x` API

3. **Rule Loading** (`vyfwmatch/services/rule_loader.py`)
   - Extract firewall configuration from config tree
   - Parse groups (address, network, port, interface)
   - Build domain models (chains, rules, policies)

4. **Traffic Matching** (`vyfwmatch/services/decision_engine.py`)
   - Determine hook (forward/input/output)
   - Determine address family (IPv4/IPv6)
   - Evaluate rules top-down (first-match-wins)
   - Handle jump/continue/return actions
   - Apply default-action if no rule matches

5. **Output Formatting** (`vyfwmatch/cli/output_formatter.py`)
   - Format result as table or JSON
   - Include evaluation trace for debugging

## Layer Responsibilities

### CLI Layer (`vyfwmatch/cli/`)

**Purpose**: Handle user interaction

- Argument parsing and validation
- Output formatting (table, JSON)
- Error messages and help text

**Key Files**:
- `argument_parser.py` - Parse and validate CLI arguments
- `output_formatter.py` - Format match results for display

### Adapter Layer (`vyfwmatch/adapters/`)

**Purpose**: Interface with external systems (VyOS config)

- Abstract config access
- Bridge to legacy parser (temporary)
- Future: Direct vyos-1x integration

**Key Files**:
- `vyos_config.py` - VyOS configuration adapter

**Design Goal**: Replace bridge with direct `vyos-1x` API calls once dependencies
are resolved (`libvyosconfig.so`, `cracklib` module).

### Service Layer (`vyfwmatch/services/`)

**Purpose**: Business logic and orchestration

- Load firewall configuration
- Execute matching logic
- Minimal decision engine

**Key Files**:
- `rule_loader.py` - Extract and transform firewall config
- `decision_engine.py` - Evaluate rules against traffic tuples

### Domain Layer (`vyfwmatch/domain/`)

**Purpose**: Core business models

- Firewall rules and chains
- Traffic tuples
- Match results
- Groups (address, network, port, interface)

**Key Files**:
- `models.py` - Domain objects with minimal logic

## Configuration Parsing

The adapter uses a bridge pattern to access VyOS config:

```
VyOS Config File
      ↓
parser/config_parser.py (tokenizer)
      ↓
ConfigTree (nested dict structure)
      ↓
vyfwmatch/services/rule_loader.py (extractor)
      ↓
Domain Models (FirewallConfig, Chain, Rule)
```

### Config Tree Structure

The parser preserves VyOS hierarchical structure:

```
firewall {
  ipv4 {
    forward {
      filter {
        rule 10 {
          action accept
          state established
        }
      }
    }
  }
}
```

Becomes:

```python
{
  'firewall': {
    'ipv4': {
      'forward': {
        'filter': {
          'rule': {
            '10': {
              'action': 'accept',
              'state': {'established': {}}
            }
          }
        }
      }
    }
  }
}
```

## Domain Models

### FirewallConfig

Container for the entire firewall configuration:
- Groups (address, network, port, interface)
- Chains (forward, input, output, named)
- State policies (global state-based actions)

### Chain

Represents a firewall chain:
- Name (e.g., "forward-filter")
- Hook (forward, input, output)
- Family (ipv4, ipv6)
- Rules (ordered list)
- Default action

### Rule

Individual firewall rule:
- Number (for ordering)
- Action (accept, drop, reject, jump, continue, return)
- Criteria (source, destination, protocol, port, interface, state)
- Jump target (for jump actions)
- Disabled flag

### TrafficTuple

Input representing network traffic:
- Inbound/outbound interfaces
- Source/destination IP addresses
- Protocol and port
- Connection state
- Hook

### MatchResult

Output of the matching process:
- Matched rule (or default action)
- Chain information
- Evaluation trace
- Action to take

## Matching Engine Logic

### Hook Determination

```
if hook specified: use specified hook
else if outbound_interface: hook = forward
else: hook = input
```

### Address Family

Determined from source/destination IP addresses:
- IPv4 addresses → ipv4 family
- IPv6 addresses → ipv6 family

### Chain Selection

```
chain_name = f"{family} {hook}-filter"
```

### Rule Evaluation

For each rule in the chain (ordered by number):

1. Check if rule is disabled → skip
2. Evaluate all criteria (AND semantics):
   - Protocol match
   - Source IP/network/group match
   - Destination IP/network/group match
   - Source port match
   - Destination port match
   - Inbound interface match
   - Outbound interface match
   - Connection state match
3. If all criteria match:
   - Execute action (accept, drop, reject, jump, continue, return)
4. If jump:
   - Evaluate target chain recursively
5. If continue:
   - Skip to next rule
6. If return:
   - Return to calling chain

If no rule matches, apply chain's default-action.

### Group Resolution

Groups are resolved via `FirewallConfig.get_group()`:

- `address-group` → list of IP addresses
- `network-group` → list of CIDR networks
- `port-group` → list of port numbers or ranges
- `interface-group` → list of interface names

For IPv6 rules, the matcher attempts IPv6-specific group types:
- `ipv6-address-group`
- `ipv6-network-group`

### State Matching

Global state-policy is evaluated only if no chain rule matched:

```python
if state_policy and traffic.state in state_policy:
    return state_policy[traffic.state]  # accept or drop
```

## Output Formatting

### Table Format

```
==================================================
  Policy Match Result
==================================================

  Chain:        ipv4 forward-filter
  Rule:         10
  Action:       accept
  Description:  Allow established connections

  Match Criteria:
    State:              established

--------------------------------------------------
  RESULT: ACCEPT
--------------------------------------------------

  Evaluation Trace:
    Hook determined: forward
    Evaluating chain: ipv4 forward-filter
      Rule 10: MATCHED -> action=accept
```

### JSON Format

```json
{
  "matched": true,
  "action": "accept",
  "chain": {
    "name": "forward-filter",
    "family": "ipv4",
    "hook": "forward"
  },
  "rule_number": 10,
  "is_default_action": false,
  "trace": [...]
}
```

## Future Enhancements

### Direct vyos-1x Integration

Replace `parser/config_parser.py` bridge with direct vyos-1x API:

```python
from vyos.config import Config
from vyos.configsource import ConfigSourceString

# Future implementation
config = Config(session_env=session)
fw_config = config.get_config_dict(['firewall'])
```

This requires resolving dependencies:
- `libvyosconfig.so` (VyOS C library)
- `cracklib` module (password strength checking)

### Additional Features

- Zone-based firewall support
- Connection tracking
- NAT rule evaluation
- Performance optimizations for large rulesets
