"""Extract typed firewall objects from a parsed VyOS config tree.

Takes the nested dict produced by config_parser.parse_config() and builds
FirewallConfig with groups, chains, rules, and global state-policy.
"""

from __future__ import annotations

from typing import Any, Optional

from parser.config_parser import ConfigTree
from parser.models import (
    FirewallChain,
    FirewallConfig,
    FirewallGroup,
    FirewallRule,
    InterfaceMatch,
    SourceDestMatch,
    StatePolicy,
)


def extract_firewall(config: ConfigTree) -> FirewallConfig:
    """Extract full firewall configuration from parsed config tree."""
    fw = config.get("firewall", {})
    if not isinstance(fw, dict):
        return FirewallConfig()

    result = FirewallConfig()

    # Extract groups
    _extract_groups(fw.get("group", {}), result)

    # Extract global state-policy
    _extract_state_policy(fw.get("global-options", {}), result)

    # Extract IPv4 chains
    _extract_family_chains(fw.get("ipv4", {}), "ipv4", result)

    # Extract IPv6 chains
    _extract_family_chains(fw.get("ipv6", {}), "ipv6", result)

    return result


# ---------------------------------------------------------------------------
# Group extraction
# ---------------------------------------------------------------------------

_GROUP_TYPE_MAP = {
    "address-group": "address",
    "network-group": "network",
    "port-group": "port",
    "interface-group": "interface",
    "mac-group": "mac",
    "domain-group": "domain",
    "ipv6-address-group": "ipv6-address",
    "ipv6-network-group": "ipv6-network",
}

# The member key differs per group type
_GROUP_MEMBER_KEY = {
    "address-group": "address",
    "network-group": "network",
    "port-group": "port",
    "interface-group": "interface",
    "mac-group": "mac-address",
    "domain-group": "address",
    "ipv6-address-group": "address",
    "ipv6-network-group": "network",
}


def _extract_groups(group_node: Any, result: FirewallConfig) -> None:
    """Extract all firewall group definitions."""
    if not isinstance(group_node, dict):
        return

    for group_key, type_name in _GROUP_TYPE_MAP.items():
        groups_dict = group_node.get(group_key, {})
        if not isinstance(groups_dict, dict):
            continue
        member_key = _GROUP_MEMBER_KEY[group_key]

        for name, body in groups_dict.items():
            if not isinstance(body, dict):
                continue
            members = _as_list(body.get(member_key, []))
            desc = body.get("description", "")
            if isinstance(desc, list):
                desc = desc[0]
            grp = FirewallGroup(
                group_type=type_name,
                name=name,
                members=members,
                description=str(desc),
            )
            result.groups[f"{type_name}:{name}"] = grp


# ---------------------------------------------------------------------------
# State policy extraction
# ---------------------------------------------------------------------------


def _extract_state_policy(global_opts: Any, result: FirewallConfig) -> None:
    """Extract global-options state-policy."""
    if not isinstance(global_opts, dict):
        return
    sp = global_opts.get("state-policy", {})
    if not isinstance(sp, dict):
        return

    for state_name in ("established", "related", "invalid"):
        entry = sp.get(state_name, {})
        if not isinstance(entry, dict):
            continue
        action = entry.get("action", "")
        if action:
            log_val = "log" in entry
            result.state_policies.append(
                StatePolicy(state=state_name, action=str(action), log=log_val)
            )


# ---------------------------------------------------------------------------
# Chain / rule extraction
# ---------------------------------------------------------------------------

_BASE_HOOKS = ("forward", "input", "output")


def _extract_family_chains(
    family_node: Any, family: str, result: FirewallConfig
) -> None:
    """Extract base chains and named chains for one address family."""
    if not isinstance(family_node, dict):
        return

    chains = result.ipv4_chains if family == "ipv4" else result.ipv6_chains

    # Base chains: forward/input/output → filter
    for hook in _BASE_HOOKS:
        hook_node = family_node.get(hook, {})
        if not isinstance(hook_node, dict):
            continue
        filter_node = hook_node.get("filter", {})
        if not isinstance(filter_node, dict):
            continue

        default_action = str(filter_node.get("default-action", "accept"))
        chain = FirewallChain(
            name=f"{hook}-filter",
            family=family,
            hook=hook,
            default_action=default_action,
        )
        _extract_rules(filter_node, chain)
        chains[chain.name] = chain

    # Custom named chains: name/<chain-name>
    named_node = family_node.get("name", {})
    if isinstance(named_node, dict):
        for chain_name, chain_body in named_node.items():
            if not isinstance(chain_body, dict):
                continue
            default_action = str(chain_body.get("default-action", "drop"))
            chain = FirewallChain(
                name=chain_name,
                family=family,
                hook="custom",
                default_action=default_action,
                description=str(chain_body.get("description", "")),
            )
            _extract_rules(chain_body, chain)
            chains[chain_name] = chain


def _extract_rules(node: dict, chain: FirewallChain) -> None:
    """Extract rules from a chain/filter node."""
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

        rule = FirewallRule(number=rule_num)
        rule.action = str(rule_body.get("action", "drop"))
        rule.description = str(rule_body.get("description", ""))
        rule.disabled = "disable" in rule_body
        rule.protocol = _get_optional(rule_body, "protocol")
        rule.jump_target = _get_optional(rule_body, "jump-target")
        rule.log = "log" in rule_body

        # Source and destination
        rule.source = _extract_source_dest(rule_body.get("source", {}))
        rule.destination = _extract_source_dest(rule_body.get("destination", {}))

        # Interfaces
        rule.inbound_interface = _extract_interface(
            rule_body.get("inbound-interface", {})
        )
        rule.outbound_interface = _extract_interface(
            rule_body.get("outbound-interface", {})
        )

        # State
        state_node = rule_body.get("state", {})
        if isinstance(state_node, dict):
            rule.state = [k for k in state_node.keys()]
        elif isinstance(state_node, list):
            rule.state = [str(s) for s in state_node]
        elif isinstance(state_node, str):
            rule.state = [state_node] if state_node else []

        # ICMP
        icmp_node = rule_body.get("icmp", {})
        if isinstance(icmp_node, dict):
            rule.icmp_type_name = _get_optional(icmp_node, "type-name")
            type_val = _get_optional(icmp_node, "type")
            if type_val is not None:
                try:
                    rule.icmp_type = int(type_val)
                except ValueError:
                    pass
            code_val = _get_optional(icmp_node, "code")
            if code_val is not None:
                try:
                    rule.icmp_code = int(code_val)
                except ValueError:
                    pass

        # ICMPv6 (same structure, different key)
        icmpv6_node = rule_body.get("icmpv6", {})
        if isinstance(icmpv6_node, dict):
            rule.icmp_type_name = _get_optional(icmpv6_node, "type-name")

        chain.rules.append(rule)


def _extract_source_dest(node: Any) -> SourceDestMatch:
    """Extract source or destination match criteria."""
    match = SourceDestMatch()
    if not isinstance(node, dict):
        return match

    match.address = _get_optional(node, "address")
    match.address_mask = _get_optional(node, "address-mask")
    match.fqdn = _get_optional(node, "fqdn")
    match.port = _get_optional(node, "port")
    match.mac_address = _get_optional(node, "mac-address")

    # Group references
    group_node = node.get("group", {})
    if isinstance(group_node, dict):
        match.address_group = _get_optional(group_node, "address-group")
        match.network_group = _get_optional(group_node, "network-group")
        match.port_group = _get_optional(group_node, "port-group")
        match.mac_group = _get_optional(group_node, "mac-group")
        match.domain_group = _get_optional(group_node, "domain-group")
        match.ipv6_address_group = _get_optional(group_node, "ipv6-address-group")
        match.ipv6_network_group = _get_optional(group_node, "ipv6-network-group")

    return match


def _extract_interface(node: Any) -> InterfaceMatch:
    """Extract interface match (name or group)."""
    iface = InterfaceMatch()
    if not isinstance(node, dict):
        return iface
    iface.name = _get_optional(node, "name")
    iface.group = _get_optional(node, "group")
    return iface


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _as_list(value: Any) -> list[str]:
    """Coerce a value to a list of strings."""
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def _get_optional(node: dict, key: str) -> Optional[str]:
    """Get a string value or None from a dict node."""
    val = node.get(key)
    if val is None:
        return None
    if isinstance(val, list):
        return str(val[0]) if val else None
    return str(val) if val != "" else None
