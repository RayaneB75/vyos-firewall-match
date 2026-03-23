"""Domain models for firewall configuration and matching.

Minimal business objects representing firewall entities.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FirewallGroup:
    """A named firewall group (address, network, port, interface)."""

    group_type: str  # address, network, port, interface, ipv6-address, ipv6-network
    name: str
    members: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class SourceDestCriteria:
    """Source or destination matching criteria."""

    address: Optional[str] = None  # IP, CIDR, range, or !negated
    address_mask: Optional[str] = None
    fqdn: Optional[str] = None
    port: Optional[str] = None
    mac_address: Optional[str] = None

    # Group references
    address_group: Optional[str] = None
    network_group: Optional[str] = None
    port_group: Optional[str] = None
    mac_group: Optional[str] = None
    domain_group: Optional[str] = None
    ipv6_address_group: Optional[str] = None
    ipv6_network_group: Optional[str] = None


@dataclass
class InterfaceCriteria:
    """Interface matching criteria."""

    name: Optional[str] = None  # interface name, wildcard (eth*), or !negated
    group: Optional[str] = None  # interface-group name, or !negated


@dataclass
class Rule:
    """A single firewall rule."""

    number: int
    action: str = "drop"  # accept, drop, reject, jump, continue, return
    description: str = ""
    disabled: bool = False

    protocol: Optional[str] = None
    source: SourceDestCriteria = field(default_factory=SourceDestCriteria)
    destination: SourceDestCriteria = field(default_factory=SourceDestCriteria)
    inbound_interface: InterfaceCriteria = field(default_factory=InterfaceCriteria)
    outbound_interface: InterfaceCriteria = field(default_factory=InterfaceCriteria)

    state: list[str] = field(default_factory=list)  # established, related, new, invalid
    jump_target: Optional[str] = None
    log: bool = False

    # ICMP
    icmp_type_name: Optional[str] = None
    icmp_type: Optional[int] = None
    icmp_code: Optional[int] = None


@dataclass
class Chain:
    """A firewall chain (base hook or custom named chain)."""

    name: str
    family: str = "ipv4"  # ipv4, ipv6
    hook: str = "custom"  # forward, input, output, custom
    default_action: str = "accept"
    rules: list[Rule] = field(default_factory=list)
    description: str = ""

    def sorted_rules(self) -> list[Rule]:
        """Return rules sorted by rule number (ascending)."""
        return sorted(self.rules, key=lambda r: r.number)


@dataclass
class StatePolicy:
    """Global state policy entry."""

    state: str  # established, related, invalid
    action: str  # accept, drop, reject
    log: bool = False


@dataclass
class FirewallConfig:
    """Complete firewall configuration."""

    groups: dict[str, FirewallGroup] = field(default_factory=dict)
    ipv4_chains: dict[str, Chain] = field(default_factory=dict)
    ipv6_chains: dict[str, Chain] = field(default_factory=dict)
    state_policies: list[StatePolicy] = field(default_factory=list)

    def get_group(self, group_type: str, name: str) -> Optional[FirewallGroup]:
        """Look up a group by type and name."""
        key = f"{group_type}:{name}"
        return self.groups.get(key)


@dataclass
class TrafficTuple:
    """Traffic to match against firewall rules."""

    inbound_interface: str
    outbound_interface: Optional[str] = None
    source_ip: str = ""
    destination_ip: str = ""
    protocol: Optional[str] = None
    port: Optional[int] = None
    state: Optional[str] = None
    hook: Optional[str] = None


@dataclass
class MatchResult:
    """Result of a firewall match evaluation."""

    matched: bool = False
    action: str = ""
    chain_name: str = ""
    chain_family: str = ""
    chain_hook: str = ""
    rule_number: Optional[int] = None
    rule: Optional[Rule] = None
    is_default_action: bool = False
    is_state_policy: bool = False
    state_policy_state: str = ""
    trace: list[str] = field(default_factory=list)
