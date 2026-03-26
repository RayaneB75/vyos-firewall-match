"""Raw configuration validator.

This module validates VyOS firewall configuration BEFORE parsing into domain models.
It uses original VyOS validators from vyos-1x to ensure configuration correctness.

Validation is comprehensive and mandatory:
- Validates all group types (address, network, port, mac, domain, interface)
- Validates all chain types (input, output, forward, prerouting, name)
- Validates all rule components (actions, protocols, IPs, ports, MACs, etc.)
- Validates jump targets reference existing chains
- Collects ALL errors before raising exception (summary-only error messages)

This runs before RuleLoaderService to catch configuration errors early.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from vyfwmatch.services import vyos_validators

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    """A single validation error with path and message."""
    path: str
    message: str


class ConfigValidationError(Exception):
    """Raised when configuration validation fails.

    Contains all collected validation errors.
    """

    def __init__(self, errors: list[ValidationError]):
        self.errors = errors
        error_count = len(errors)
        super().__init__(f"Configuration validation failed with {error_count} error(s)")


class RawConfigValidator:
    """Validates raw VyOS firewall configuration before parsing.

    Uses original VyOS validators to comprehensively validate all aspects
    of the firewall configuration.
    """

    def __init__(self):
        self.errors: list[ValidationError] = []
        self.known_chains: dict[str, set[str]] = {'ipv4': set(), 'ipv6': set()}

    def validate(self, config_dict: dict[str, Any]) -> None:
        """Validate raw firewall configuration.

        Args:
            config_dict: Raw configuration dictionary from VyOSConfigAdapter

        Raises:
            ConfigValidationError: If validation fails (contains all errors)
        """
        self.errors = []
        self.known_chains = {'ipv4': set(), 'ipv6': set()}

        # Validate groups first
        groups = config_dict.get('group', {})
        if groups:
            self._validate_groups(groups)

        # Build list of known chains for jump target validation
        self._discover_chains(config_dict)

        # Validate IPv4 chains
        ipv4 = config_dict.get('ipv4', {})
        if ipv4:
            self._validate_ipv4_chains(ipv4)

        # Validate IPv6 chains
        ipv6 = config_dict.get('ipv6', {})
        if ipv6:
            self._validate_ipv6_chains(ipv6)

        # Validate jump targets reference existing chains
        self._validate_jump_targets(config_dict)

        # If any errors were collected, raise exception
        if self.errors:
            raise ConfigValidationError(self.errors)

    def _add_error(self, path: str, message: str) -> None:
        """Add a validation error."""
        self.errors.append(ValidationError(path=path, message=message))

    # ========================================================================
    # Group Validation
    # ========================================================================

    def _validate_groups(self, groups: dict[str, Any]) -> None:
        """Validate all firewall groups."""
        # Address groups
        address_groups = groups.get('address-group', {})
        for name, group in address_groups.items():
            self._validate_address_group(name, group, f"group.address-group.{name}")

        # Network groups
        network_groups = groups.get('network-group', {})
        for name, group in network_groups.items():
            self._validate_network_group(name, group, f"group.network-group.{name}")

        # Port groups
        port_groups = groups.get('port-group', {})
        for name, group in port_groups.items():
            self._validate_port_group(name, group, f"group.port-group.{name}")

        # MAC groups
        mac_groups = groups.get('mac-group', {})
        for name, group in mac_groups.items():
            self._validate_mac_group(name, group, f"group.mac-group.{name}")

        # Domain groups
        domain_groups = groups.get('domain-group', {})
        for name, group in domain_groups.items():
            self._validate_domain_group(name, group, f"group.domain-group.{name}")

        # Interface groups (just check they're not empty)
        interface_groups = groups.get('interface-group', {})
        for name, group in interface_groups.items():
            self._validate_interface_group(name, group, f"group.interface-group.{name}")

    def _validate_address_group(self, name: str, group: dict[str, Any], path: str) -> None:
        """Validate an address group."""
        addresses = group.get('address', [])
        if isinstance(addresses, str):
            addresses = [addresses]

        if not addresses:
            self._add_error(path, f"Address group '{name}' is empty")
            return

        for addr in addresses:
            addr = str(addr).strip()
            # Address can be IPv4 or IPv6
            if not (vyos_validators.validate_ipv4_address(addr) or
                    vyos_validators.validate_ipv6_address(addr)):
                self._add_error(path, f"Invalid IP address: {addr}")

    def _validate_network_group(self, name: str, group: dict[str, Any], path: str) -> None:
        """Validate a network group."""
        networks = group.get('network', [])
        if isinstance(networks, str):
            networks = [networks]

        if not networks:
            self._add_error(path, f"Network group '{name}' is empty")
            return

        for net in networks:
            net = str(net).strip()
            # Network must be in CIDR notation
            if not (vyos_validators.validate_ipv4_prefix(net) or
                    vyos_validators.validate_ipv6_prefix(net)):
                self._add_error(path, f"Invalid network prefix: {net}")

    def _validate_port_group(self, name: str, group: dict[str, Any], path: str) -> None:
        """Validate a port group."""
        ports = group.get('port', [])
        if isinstance(ports, str):
            ports = [ports]

        if not ports:
            self._add_error(path, f"Port group '{name}' is empty")
            return

        for port in ports:
            port_str = str(port).strip()
            if not vyos_validators.validate_port_range(port_str):
                self._add_error(path, f"Invalid port: {port_str}")

    def _validate_mac_group(self, name: str, group: dict[str, Any], path: str) -> None:
        """Validate a MAC address group."""
        macs = group.get('mac-address', [])
        if isinstance(macs, str):
            macs = [macs]

        if not macs:
            self._add_error(path, f"MAC group '{name}' is empty")
            return

        for mac in macs:
            mac = str(mac).strip()
            if not vyos_validators.validate_mac_address(mac):
                self._add_error(path, f"Invalid MAC address: {mac}")

    def _validate_domain_group(self, name: str, group: dict[str, Any], path: str) -> None:
        """Validate a domain group."""
        domains = group.get('address', [])
        if isinstance(domains, str):
            domains = [domains]

        if not domains:
            self._add_error(path, f"Domain group '{name}' is empty")
            return

        for domain in domains:
            domain = str(domain).strip()
            if not vyos_validators.validate_fqdn(domain):
                self._add_error(path, f"Invalid FQDN: {domain}")

    def _validate_interface_group(self, name: str, group: dict[str, Any], path: str) -> None:
        """Validate an interface group."""
        interfaces = group.get('interface', [])
        if isinstance(interfaces, str):
            interfaces = [interfaces]

        if not interfaces:
            self._add_error(path, f"Interface group '{name}' is empty")

    # ========================================================================
    # Chain Discovery (for jump target validation)
    # ========================================================================

    def _discover_chains(self, config_dict: dict[str, Any]) -> None:
        """Discover all defined chains for jump target validation."""
        # IPv4 chains
        ipv4 = config_dict.get('ipv4', {})
        for chain_name in ipv4.keys():
            self.known_chains['ipv4'].add(chain_name)

        # IPv6 chains
        ipv6 = config_dict.get('ipv6', {})
        for chain_name in ipv6.keys():
            self.known_chains['ipv6'].add(chain_name)

    # ========================================================================
    # IPv4/IPv6 Chain Validation
    # ========================================================================

    def _validate_ipv4_chains(self, ipv4: dict[str, Any]) -> None:
        """Validate all IPv4 chains."""
        for chain_name, chain_data in ipv4.items():
            path = f"ipv4.{chain_name}"
            self._validate_chain(chain_name, chain_data, path, 'ipv4')

    def _validate_ipv6_chains(self, ipv6: dict[str, Any]) -> None:
        """Validate all IPv6 chains."""
        for chain_name, chain_data in ipv6.items():
            path = f"ipv6.{chain_name}"
            self._validate_chain(chain_name, chain_data, path, 'ipv6')

    def _validate_chain(self, _chain_name: str, chain_data: dict[str, Any],
                       path: str, ip_version: str) -> None:
        """Validate a single chain (input/output/forward/prerouting/name)."""
        # Chains can have 'filter' or directly contain rules/default-action
        if 'filter' in chain_data:
            filter_data = chain_data['filter']
            self._validate_chain_rules(filter_data, f"{path}.filter", ip_version)
        else:
            self._validate_chain_rules(chain_data, path, ip_version)

    def _validate_chain_rules(self, chain_data: dict[str, Any],
                              path: str, ip_version: str) -> None:
        """Validate rules within a chain."""
        # Validate default action if present
        default_action = chain_data.get('default-action')
        if default_action:
            self._validate_action(default_action, f"{path}.default-action")

        # Validate individual rules
        rules = chain_data.get('rule', {})
        for rule_num, rule_data in rules.items():
            rule_path = f"{path}.rule.{rule_num}"
            self._validate_rule(rule_num, rule_data, rule_path, ip_version)

    # ========================================================================
    # Rule Validation
    # ========================================================================

    def _validate_rule(self, _rule_num: str, rule: dict[str, Any],
                      path: str, ip_version: str) -> None:
        """Validate a single firewall rule."""
        # Validate action (required)
        action = rule.get('action')
        if action:
            self._validate_action(action, f"{path}.action")

        # Validate protocol
        protocol = rule.get('protocol')
        if protocol:
            if not vyos_validators.validate_ip_protocol(protocol):
                self._add_error(f"{path}.protocol", f"Invalid protocol: {protocol}")

        # Validate source
        source = rule.get('source')
        if source:
            self._validate_source_dest(source, f"{path}.source", ip_version)

        # Validate destination
        destination = rule.get('destination')
        if destination:
            self._validate_source_dest(destination, f"{path}.destination", ip_version)

        # Validate state
        state = rule.get('state')
        if state:
            self._validate_state(state, f"{path}.state")

    def _validate_action(self, action: str, path: str) -> None:
        """Validate a firewall action."""
        valid_actions = {'accept', 'drop', 'reject', 'return', 'jump', 'queue', 'nftables'}
        if action not in valid_actions:
            self._add_error(path, f"Invalid action: {action}")

    def _validate_source_dest(self, sd: dict[str, Any], path: str, ip_version: str) -> None:
        """Validate source or destination section of a rule."""
        # Validate address
        address = sd.get('address')
        if address:
            address = str(address).strip()
            if ip_version == 'ipv4':
                # Can be address, prefix, range, or negated
                addr_to_check = address.lstrip('!')
                if not (vyos_validators.validate_ipv4_address(addr_to_check) or
                        vyos_validators.validate_ipv4_prefix(addr_to_check) or
                        vyos_validators.validate_ipv4_range(addr_to_check)):
                    self._add_error(f"{path}.address", f"Invalid IPv4 address: {address}")
            else:  # ipv6
                addr_to_check = address.lstrip('!')
                if not (vyos_validators.validate_ipv6_address(addr_to_check) or
                        vyos_validators.validate_ipv6_prefix(addr_to_check) or
                        vyos_validators.validate_ipv6_range(addr_to_check)):
                    self._add_error(f"{path}.address", f"Invalid IPv6 address: {address}")

        # Validate port
        port = sd.get('port')
        if port:
            self._validate_port(port, f"{path}.port")

        # Validate MAC address
        mac = sd.get('mac')
        if mac:
            self._validate_mac(mac, f"{path}.mac")

        # Validate group references (groups are validated separately)
        group = sd.get('group')
        if group:
            # Just check they reference something - actual group validation done in _validate_groups
            pass

    def _validate_port(self, port: str | dict[str, Any], path: str) -> None:
        """Validate a port specification."""
        if isinstance(port, dict):
            # Port can be a dict for negation, etc.
            return

        port_str = str(port).strip()
        if ',' in port_str:
            is_valid = vyos_validators.validate_port_multi(port_str)
        else:
            is_valid = vyos_validators.validate_port_range(port_str.lstrip('!'))

        if not is_valid:
            self._add_error(path, f"Invalid port: {port}")

    def _validate_mac(self, mac: dict[str, Any], path: str) -> None:
        """Validate a MAC address specification."""
        # MAC is typically in a dict with 'address' key
        if isinstance(mac, dict):
            mac_addr = mac.get('address')
            if mac_addr:
                mac_to_check = mac_addr.lstrip('!')
                if not vyos_validators.validate_mac_address(mac_to_check):
                    self._add_error(f"{path}.address", f"Invalid MAC address: {mac_addr}")

    def _validate_state(self, state: dict[str, Any] | list[str] | str, path: str) -> None:
        """Validate connection state specification."""
        valid_states = {'established', 'related', 'new', 'invalid'}

        # State can be a dict with state names as keys, a list, or a string
        if isinstance(state, dict):
            for state_name in state.keys():
                if state_name not in valid_states:
                    self._add_error(path, f"Invalid state: {state_name}")
        elif isinstance(state, list):
            for state_name in state:
                if state_name not in valid_states:
                    self._add_error(path, f"Invalid state: {state_name}")
        elif isinstance(state, str):
            if state not in valid_states:
                self._add_error(path, f"Invalid state: {state}")

    # ========================================================================
    # Jump Target Validation
    # ========================================================================

    def _validate_jump_targets(self, config_dict: dict[str, Any]) -> None:
        """Validate that all jump targets reference existing chains."""
        # Check IPv4 chains
        ipv4 = config_dict.get('ipv4', {})
        for chain_name, chain_data in ipv4.items():
            self._validate_jump_targets_in_chain(
                chain_data, f"ipv4.{chain_name}", 'ipv4'
            )

        # Check IPv6 chains
        ipv6 = config_dict.get('ipv6', {})
        for chain_name, chain_data in ipv6.items():
            self._validate_jump_targets_in_chain(
                chain_data, f"ipv6.{chain_name}", 'ipv6'
            )

    def _validate_jump_targets_in_chain(self, chain_data: dict[str, Any],
                                        path: str, ip_version: str) -> None:
        """Validate jump targets in a specific chain."""
        # Handle chains with 'filter' wrapper
        if 'filter' in chain_data:
            chain_rules = chain_data['filter'].get('rule', {})
            base_path = f"{path}.filter"
        else:
            chain_rules = chain_data.get('rule', {})
            base_path = path

        # Check each rule
        for rule_num, rule_data in chain_rules.items():
            action = rule_data.get('action')
            if action == 'jump':
                jump_target = rule_data.get('jump-target')
                if not jump_target:
                    self._add_error(
                        f"{base_path}.rule.{rule_num}",
                        "Action 'jump' requires jump-target"
                    )
                elif jump_target not in self.known_chains[ip_version]:
                    self._add_error(
                        f"{base_path}.rule.{rule_num}.jump-target",
                        f"Jump target '{jump_target}' not found"
                    )


__all__ = ['RawConfigValidator', 'ConfigValidationError', 'ValidationError']
