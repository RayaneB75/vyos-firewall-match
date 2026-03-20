"""Output formatters for VyFwMatch."""

import json
from typing import Any

from vyfwmatch.domain.models import MatchResult, Rule


def format_result(result: MatchResult, output_format: str = "table") -> str:
    """Format a match result for display.

    Args:
        result: The match result from the decision engine.
        output_format: "table" or "json".

    Returns:
        Formatted string for display.
    """
    if output_format == "json":
        return _format_json(result)
    return _format_table(result)


def _format_table(result: MatchResult) -> str:
    """Format result as a human-readable table."""
    lines: list[str] = []
    lines.append("")
    lines.append("=" * 50)
    lines.append("  Policy Match Result")
    lines.append("=" * 50)
    lines.append("")

    if result.is_state_policy:
        lines.append("  Match Type:   Global State Policy")
        lines.append(f"  State:        {result.state_policy_state}")
        lines.append(f"  Action:       {_colorize_action(result.action)}")
    elif result.is_default_action:
        lines.append(f"  Chain:        {result.chain_family} {result.chain_name}")
        lines.append("  Match Type:   Default Action (no rule matched)")
        lines.append(f"  Action:       {_colorize_action(result.action)}")
    else:
        lines.append(f"  Chain:        {result.chain_family} {result.chain_name}")
        lines.append(f"  Rule:         {result.rule_number}")
        lines.append(f"  Action:       {_colorize_action(result.action)}")

        if result.rule and result.rule.description:
            lines.append(f"  Description:  {result.rule.description}")

        if result.rule:
            _append_rule_details(lines, result.rule)

    lines.append("")
    lines.append("-" * 50)
    lines.append(f"  RESULT: {result.action.upper()}")
    lines.append("-" * 50)

    # Trace
    if result.trace:
        lines.append("")
        lines.append("  Evaluation Trace:")
        for entry in result.trace:
            lines.append(f"    {entry}")

    lines.append("")
    return "\n".join(lines)


def _append_rule_details(lines: list[str], rule: Rule) -> None:
    """Append detailed rule match criteria to output lines."""
    lines.append("")
    lines.append("  Match Criteria:")

    if rule.protocol:
        lines.append(f"    Protocol:           {rule.protocol}")

    if rule.inbound_interface.name or rule.inbound_interface.group:
        iface_str = rule.inbound_interface.name or ""
        if rule.inbound_interface.group:
            iface_str += f" (group: {rule.inbound_interface.group})"
        lines.append(f"    Inbound Interface:  {iface_str.strip()}")

    if rule.outbound_interface.name or rule.outbound_interface.group:
        iface_str = rule.outbound_interface.name or ""
        if rule.outbound_interface.group:
            iface_str += f" (group: {rule.outbound_interface.group})"
        lines.append(f"    Outbound Interface: {iface_str.strip()}")

    if rule.source.address:
        lines.append(f"    Source Address:     {rule.source.address}")
    if rule.source.network_group:
        lines.append(f"    Source Net Group:   {rule.source.network_group}")
    if rule.source.address_group:
        lines.append(f"    Source Addr Group:  {rule.source.address_group}")
    if rule.source.port:
        lines.append(f"    Source Port:        {rule.source.port}")

    if rule.destination.address:
        lines.append(f"    Dest Address:       {rule.destination.address}")
    if rule.destination.network_group:
        lines.append(f"    Dest Net Group:     {rule.destination.network_group}")
    if rule.destination.address_group:
        lines.append(f"    Dest Addr Group:    {rule.destination.address_group}")
    if rule.destination.port:
        lines.append(f"    Dest Port:          {rule.destination.port}")
    if rule.destination.port_group:
        lines.append(f"    Dest Port Group:    {rule.destination.port_group}")

    if rule.state:
        lines.append(f"    State:              {', '.join(rule.state)}")

    if rule.jump_target:
        lines.append(f"    Jump Target:        {rule.jump_target}")


def _colorize_action(action: str) -> str:
    """Add ANSI color to action for terminal display."""
    colors = {
        "accept": "\033[92maccept\033[0m",   # green
        "drop": "\033[91mdrop\033[0m",        # red
        "reject": "\033[91mreject\033[0m",    # red
        "jump": "\033[93mjump\033[0m",        # yellow
        "continue": "\033[94mcontinue\033[0m",  # blue
        "return": "\033[94mreturn\033[0m",    # blue
    }
    return colors.get(action.lower(), action)


def _format_json(result: MatchResult) -> str:
    """Format result as JSON."""
    data: dict[str, Any] = {
        "matched": result.matched,
        "action": result.action,
        "chain": {
            "name": result.chain_name,
            "family": result.chain_family,
            "hook": result.chain_hook,
        },
        "is_default_action": result.is_default_action,
        "is_state_policy": result.is_state_policy,
    }

    if result.rule_number is not None:
        data["rule_number"] = result.rule_number

    if result.state_policy_state:
        data["state_policy_state"] = result.state_policy_state

    if result.rule:
        data["rule_details"] = _rule_to_dict(result.rule)

    data["trace"] = result.trace

    return json.dumps(data, indent=2)


def _rule_to_dict(rule: Rule) -> dict[str, Any]:
    """Convert a Rule to a JSON-serializable dict."""
    d: dict[str, Any] = {
        "number": rule.number,
        "action": rule.action,
    }
    if rule.description:
        d["description"] = rule.description
    if rule.protocol:
        d["protocol"] = rule.protocol
    if rule.state:
        d["state"] = rule.state
    if rule.jump_target:
        d["jump_target"] = rule.jump_target

    # Source
    src: dict[str, str] = {}
    if rule.source.address:
        src["address"] = rule.source.address
    if rule.source.port:
        src["port"] = rule.source.port
    if rule.source.network_group:
        src["network_group"] = rule.source.network_group
    if rule.source.address_group:
        src["address_group"] = rule.source.address_group
    if src:
        d["source"] = src

    # Destination
    dst: dict[str, str] = {}
    if rule.destination.address:
        dst["address"] = rule.destination.address
    if rule.destination.port:
        dst["port"] = rule.destination.port
    if rule.destination.network_group:
        dst["network_group"] = rule.destination.network_group
    if rule.destination.address_group:
        dst["address_group"] = rule.destination.address_group
    if rule.destination.port_group:
        dst["port_group"] = rule.destination.port_group
    if dst:
        d["destination"] = dst

    # Interfaces
    if rule.inbound_interface.name or rule.inbound_interface.group:
        d["inbound_interface"] = {
            "name": rule.inbound_interface.name,
            "group": rule.inbound_interface.group,
        }
    if rule.outbound_interface.name or rule.outbound_interface.group:
        d["outbound_interface"] = {
            "name": rule.outbound_interface.name,
            "group": rule.outbound_interface.group,
        }

    return d
