"""Data models for VyOS firewall configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FirewallGroup:
    """A named firewall group (address, network, port, interface, etc.)."""

    group_type: str  # address, network, port, interface, mac, domain,
    #                  ipv6-address, ipv6-network
    name: str
    members: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class SourceDestMatch:
    """Match criteria for source or destination in a firewall rule."""

    address: Optional[str] = None          # IP, CIDR, range, or !negated
    address_mask: Optional[str] = None     # address mask
    fqdn: Optional[str] = None            # FQDN match
    port: Optional[str] = None            # port spec: number, range, list
    mac_address: Optional[str] = None     # MAC address, supports !negation
    # Group references (by name)
    address_group: Optional[str] = None
    network_group: Optional[str] = None
    port_group: Optional[str] = None
    mac_group: Optional[str] = None
    domain_group: Optional[str] = None
    ipv6_address_group: Optional[str] = None
    ipv6_network_group: Optional[str] = None


@dataclass
class InterfaceMatch:
    """Match criteria for inbound or outbound interface."""

    name: Optional[str] = None   # interface name, wildcard (eth*), or !negated
    group: Optional[str] = None  # interface-group name, or !negated


@dataclass
class FirewallRule:
    """A single firewall rule within a chain."""

    number: int
    action: str = "drop"                           # accept, drop, reject, jump, continue, return
    description: str = ""
    disabled: bool = False
    protocol: Optional[str] = None                 # tcp, udp, icmp, icmpv6, tcp_udp, all, !negated
    source: SourceDestMatch = field(default_factory=SourceDestMatch)
    destination: SourceDestMatch = field(default_factory=SourceDestMatch)
    inbound_interface: InterfaceMatch = field(default_factory=InterfaceMatch)
    outbound_interface: InterfaceMatch = field(default_factory=InterfaceMatch)
    state: list[str] = field(default_factory=list)  # established, related, new, invalid
    jump_target: Optional[str] = None
    log: bool = False
    icmp_type_name: Optional[str] = None           # e.g. echo-request
    icmp_type: Optional[int] = None
    icmp_code: Optional[int] = None


@dataclass
class FirewallChain:
    """A firewall chain (base hook or custom named chain)."""

    name: str                      # e.g. "forward-filter", "input-filter", or custom name
    family: str = "ipv4"           # ipv4, ipv6
    hook: str = "custom"           # forward, input, output, custom
    default_action: str = "accept" # accept, drop, reject, return
    rules: list[FirewallRule] = field(default_factory=list)
    description: str = ""

    def sorted_rules(self) -> list[FirewallRule]:
        """Return rules sorted by rule number (ascending)."""
        return sorted(self.rules, key=lambda r: r.number)


@dataclass
class StatePolicy:
    """Global state policy entry."""

    state: str       # established, related, invalid
    action: str      # accept, drop, reject
    log: bool = False


@dataclass
class FirewallConfig:
    """Complete parsed firewall configuration."""

    groups: dict[str, FirewallGroup] = field(default_factory=dict)
    # Key format: "type:name" e.g. "address:SERVERS", "network:NET-INSIDE-v4"

    ipv4_chains: dict[str, FirewallChain] = field(default_factory=dict)
    # Keys: "forward-filter", "input-filter", "output-filter", or custom name

    ipv6_chains: dict[str, FirewallChain] = field(default_factory=dict)
    # Same key format as ipv4_chains

    state_policies: list[StatePolicy] = field(default_factory=list)

    def get_group(self, group_type: str, name: str) -> Optional[FirewallGroup]:
        """Look up a group by type and name."""
        key = f"{group_type}:{name}"
        return self.groups.get(key)
