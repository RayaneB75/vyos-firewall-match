"""Rule Loader Service.

Loads firewall rules and configuration from VyOS config using the adapter.
"""

from typing import Any, Optional

from vyfwmatch.adapters.vyos_config import VyOSConfigAdapter
from vyfwmatch.domain.models import (
    Chain,
    FirewallConfig,
    FirewallGroup,
    InterfaceCriteria,
    Rule,
    SourceDestCriteria,
    StatePolicy,
)


class RuleLoaderService:
    """Service for loading firewall configuration from VyOS config."""

    def __init__(self, adapter: VyOSConfigAdapter):
        """Initialize the rule loader with a config adapter.

        Args:
            adapter: VyOS configuration adapter
        """
        self.adapter = adapter

    def load_firewall_config(self) -> FirewallConfig:
        """Load complete firewall configuration.

        Returns:
            FirewallConfig object with all rules, chains, and groups
        """
        config = FirewallConfig()
        fw_tree = self.adapter.get_firewall_config()

        if not fw_tree:
            return config

        # Load groups
        self._load_groups(fw_tree.get("group", {}), config)

        # Load global options (state-policy)
        self._load_state_policies(fw_tree.get("global-options", {}), config)

        # Load IPv4 chains
        self._load_family_chains(fw_tree.get("ipv4", {}), "ipv4", config)

        # Load IPv6 chains
        self._load_family_chains(fw_tree.get("ipv6", {}), "ipv6", config)

        return config

    def _load_groups(self, group_node: Any, config: FirewallConfig) -> None:
        """Load all firewall groups."""
        if not isinstance(group_node, dict):
            return

        group_mappings = {
            "address-group": ("address", "address"),
            "network-group": ("network", "network"),
            "port-group": ("port", "port"),
            "interface-group": ("interface", "interface"),
            "mac-group": ("mac", "mac-address"),
            "domain-group": ("domain", "address"),
            "ipv6-address-group": ("ipv6-address", "address"),
            "ipv6-network-group": ("ipv6-network", "network"),
        }

        for group_key, (group_type, member_key) in group_mappings.items():
            groups_dict = group_node.get(group_key, {})
            if not isinstance(groups_dict, dict):
                continue

            for name, body in groups_dict.items():
                if not isinstance(body, dict):
                    continue

                members = self._as_list(body.get(member_key, []))
                description = body.get("description", "")
                if isinstance(description, list):
                    description = description[0] if description else ""

                group = FirewallGroup(
                    group_type=group_type,
                    name=name,
                    members=members,
                    description=str(description),
                )
                config.groups[f"{group_type}:{name}"] = group

    def _load_state_policies(self, global_opts: Any, config: FirewallConfig) -> None:
        """Load global state policies."""
        if not isinstance(global_opts, dict):
            return

        sp_node = global_opts.get("state-policy", {})
        if not isinstance(sp_node, dict):
            return

        for state_name in ("established", "related", "invalid"):
            entry = sp_node.get(state_name, {})
            if not isinstance(entry, dict):
                continue

            action = entry.get("action", "")
            if action:
                log_val = "log" in entry
                config.state_policies.append(
                    StatePolicy(state=state_name, action=str(action), log=log_val)
                )

    def _load_family_chains(
        self, family_node: Any, family: str, config: FirewallConfig
    ) -> None:
        """Load chains for one address family (ipv4 or ipv6)."""
        if not isinstance(family_node, dict):
            return

        chains = config.ipv4_chains if family == "ipv4" else config.ipv6_chains

        # Load base chains: forward, input, output
        for hook in ("forward", "input", "output"):
            hook_node = family_node.get(hook, {})
            if not isinstance(hook_node, dict):
                continue

            filter_node = hook_node.get("filter", {})
            if not isinstance(filter_node, dict):
                continue

            default_action = str(filter_node.get("default-action", "accept"))
            chain = Chain(
                name=f"{hook}-filter",
                family=family,
                hook=hook,
                default_action=default_action,
            )
            self._load_rules(filter_node, chain)
            chains[chain.name] = chain

        # Load custom named chains
        named_node = family_node.get("name", {})
        if isinstance(named_node, dict):
            for chain_name, chain_body in named_node.items():
                if not isinstance(chain_body, dict):
                    continue

                default_action = str(chain_body.get("default-action", "drop"))
                chain = Chain(
                    name=chain_name,
                    family=family,
                    hook="custom",
                    default_action=default_action,
                    description=str(chain_body.get("description", "")),
                )
                self._load_rules(chain_body, chain)
                chains[chain_name] = chain

    def _load_rules(self, node: dict, chain: Chain) -> None:
        """Load rules from a chain/filter node."""
        rules_node = node.get("rule", {})
        if not isinstance(rules_node, dict):
            return

        for rule_num_str, rule_body in rules_node.items():
            if not isinstance(rule_body, dict):
                continue

            try:
                rule_num = int(rule_num_str)
            except ValueError:
                continue

            rule = Rule(number=rule_num)
            rule.action = str(rule_body.get("action", "drop"))
            rule.description = str(rule_body.get("description", ""))
            rule.disabled = "disable" in rule_body
            rule.protocol = self._get_optional(rule_body, "protocol")
            rule.jump_target = self._get_optional(rule_body, "jump-target")
            rule.log = "log" in rule_body

            # Source and destination
            rule.source = self._load_source_dest(rule_body.get("source", {}))
            rule.destination = self._load_source_dest(rule_body.get("destination", {}))

            # Interfaces
            rule.inbound_interface = self._load_interface(
                rule_body.get("inbound-interface", {})
            )
            rule.outbound_interface = self._load_interface(
                rule_body.get("outbound-interface", {})
            )

            # State
            state_node = rule_body.get("state", {})
            if isinstance(state_node, dict):
                rule.state = list(state_node.keys())
            elif isinstance(state_node, list):
                rule.state = [str(s) for s in state_node]
            elif isinstance(state_node, str):
                rule.state = [state_node] if state_node else []

            # ICMP
            icmp_node = rule_body.get("icmp", {})
            if isinstance(icmp_node, dict):
                rule.icmp_type_name = self._get_optional(icmp_node, "type-name")
                type_val = self._get_optional(icmp_node, "type")
                if type_val is not None:
                    try:
                        rule.icmp_type = int(type_val)
                    except ValueError:
                        pass
                code_val = self._get_optional(icmp_node, "code")
                if code_val is not None:
                    try:
                        rule.icmp_code = int(code_val)
                    except ValueError:
                        pass

            # ICMPv6
            icmpv6_node = rule_body.get("icmpv6", {})
            if isinstance(icmpv6_node, dict):
                rule.icmp_type_name = self._get_optional(icmpv6_node, "type-name")

            chain.rules.append(rule)

    def _load_source_dest(self, node: Any) -> SourceDestCriteria:
        """Load source or destination match criteria."""
        criteria = SourceDestCriteria()
        if not isinstance(node, dict):
            return criteria

        criteria.address = self._get_optional(node, "address")
        criteria.address_mask = self._get_optional(node, "address-mask")
        criteria.fqdn = self._get_optional(node, "fqdn")
        criteria.port = self._get_optional(node, "port")
        criteria.mac_address = self._get_optional(node, "mac-address")

        # Group references
        group_node = node.get("group", {})
        if isinstance(group_node, dict):
            criteria.address_group = self._get_optional(group_node, "address-group")
            criteria.network_group = self._get_optional(group_node, "network-group")
            criteria.port_group = self._get_optional(group_node, "port-group")
            criteria.mac_group = self._get_optional(group_node, "mac-group")
            criteria.domain_group = self._get_optional(group_node, "domain-group")
            criteria.ipv6_address_group = self._get_optional(group_node, "ipv6-address-group")
            criteria.ipv6_network_group = self._get_optional(group_node, "ipv6-network-group")

        return criteria

    def _load_interface(self, node: Any) -> InterfaceCriteria:
        """Load interface match criteria."""
        iface = InterfaceCriteria()
        if not isinstance(node, dict):
            return iface

        iface.name = self._get_optional(node, "name")
        iface.group = self._get_optional(node, "group")
        return iface

    @staticmethod
    def _as_list(value: Any) -> list[str]:
        """Coerce a value to a list of strings."""
        if isinstance(value, list):
            return [str(v) for v in value]
        if isinstance(value, str) and value:
            return [value]
        return []

    @staticmethod
    def _get_optional(node: dict, key: str) -> Optional[str]:
        """Get a string value or None from a dict node."""
        val = node.get(key)
        if val is None:
            return None
        if isinstance(val, list):
            return str(val[0]) if val else None
        return str(val) if val != "" else None
