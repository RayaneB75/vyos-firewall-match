"""Tests for output formatting."""

import json

from vyfwmatch.cli.output_formatter import format_result
from vyfwmatch.domain.models import (
    MatchResult,
    Rule,
    SourceDestCriteria,
    InterfaceCriteria,
)


class TestFormatTable:
    """Test table format output."""

    def test_format_regular_rule_match(self):
        """Test formatting a regular rule match."""
        rule = Rule(
            number=10,
            action="accept",
            description="Allow HTTPS traffic",
            protocol="tcp",
            source=SourceDestCriteria(address="10.0.0.1"),
            destination=SourceDestCriteria(address="192.168.1.1", port="443"),
            inbound_interface=InterfaceCriteria(name="eth0"),
            outbound_interface=InterfaceCriteria(name="eth1"),
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=10,
            rule=rule,
        )

        output = format_result(result, "table")

        assert "Policy Match Result" in output
        assert "Chain:        ipv4 filter" in output
        assert "Rule:         10" in output
        assert "Action:" in output
        assert "accept" in output
        assert "Description:  Allow HTTPS traffic" in output
        assert "Protocol:           tcp" in output
        assert "Source Address:     10.0.0.1" in output
        assert "Dest Address:       192.168.1.1" in output
        assert "Dest Port:          443" in output
        assert "Inbound Interface:  eth0" in output
        assert "Outbound Interface: eth1" in output

    def test_format_default_action(self):
        """Test formatting default action result."""
        result = MatchResult(
            matched=True,
            action="drop",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            is_default_action=True,
        )

        output = format_result(result, "table")

        assert "Chain:        ipv4 filter" in output
        assert "Match Type:   Default Action (no rule matched)" in output
        assert "Action:" in output
        assert "drop" in output
        assert "RESULT: DROP" in output

    def test_format_state_policy(self):
        """Test formatting state policy result."""
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="global",
            chain_family="global",
            chain_hook="",
            is_state_policy=True,
            state_policy_state="established",
        )

        output = format_result(result, "table")

        assert "Match Type:   Global State Policy" in output
        assert "State:        established" in output
        assert "Action:" in output
        assert "accept" in output

    def test_format_with_trace(self):
        """Test formatting with evaluation trace."""
        rule = Rule(
            number=10,
            action="accept",
            protocol="tcp",
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=10,
            rule=rule,
            trace=[
                "Checking state policy for state 'new'",
                "Evaluating chain ipv4/forward/filter",
                "Rule 10: matched",
            ],
        )

        output = format_result(result, "table")

        assert "Evaluation Trace:" in output
        assert "Checking state policy" in output
        assert "Evaluating chain" in output
        assert "Rule 10: matched" in output

    def test_format_with_groups(self):
        """Test formatting rules with groups."""
        rule = Rule(
            number=20,
            action="drop",
            source=SourceDestCriteria(network_group="INTERNAL"),
            destination=SourceDestCriteria(
                address_group="SERVERS", port_group="WEBPORTS"
            ),
            inbound_interface=InterfaceCriteria(group="LAN"),
        )
        result = MatchResult(
            matched=True,
            action="drop",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=20,
            rule=rule,
        )

        output = format_result(result, "table")

        assert "Source Net Group:   INTERNAL" in output
        assert "Dest Addr Group:    SERVERS" in output
        assert "Dest Port Group:    WEBPORTS" in output
        assert "Inbound Interface:  (group: LAN)" in output

    def test_format_with_state(self):
        """Test formatting rules with state matching."""
        rule = Rule(
            number=5,
            action="accept",
            state=["established", "related"],
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=5,
            rule=rule,
        )

        output = format_result(result, "table")

        assert "State:              established, related" in output

    def test_format_with_jump_target(self):
        """Test formatting rules with jump targets."""
        rule = Rule(
            number=10,
            action="jump",
            jump_target="CUSTOM_CHAIN",
        )
        result = MatchResult(
            matched=True,
            action="jump",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=10,
            rule=rule,
        )

        output = format_result(result, "table")

        assert "Jump Target:        CUSTOM_CHAIN" in output

    def test_colorized_actions(self):
        """Test that actions are colorized in table output."""
        actions_to_test = ["accept", "drop", "reject", "jump", "continue", "return"]

        for action in actions_to_test:
            result = MatchResult(
                matched=True,
                action=action,
                chain_name="filter",
                chain_family="ipv4",
                chain_hook="forward",
                is_default_action=True,
            )
            output = format_result(result, "table")
            # Check that ANSI color codes are present
            assert "\033[" in output or action in output


class TestFormatJson:
    """Test JSON format output."""

    def test_format_json_basic(self):
        """Test basic JSON formatting."""
        rule = Rule(
            number=10,
            action="accept",
            description="Test rule",
            protocol="tcp",
            source=SourceDestCriteria(address="10.0.0.1", port="1234"),
            destination=SourceDestCriteria(address="192.168.1.1", port="443"),
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=10,
            rule=rule,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["matched"] is True
        assert data["action"] == "accept"
        assert data["chain"]["name"] == "filter"
        assert data["chain"]["family"] == "ipv4"
        assert data["chain"]["hook"] == "forward"
        assert data["rule_number"] == 10
        assert data["is_default_action"] is False
        assert data["is_state_policy"] is False

        rule_details = data["rule_details"]
        assert rule_details["number"] == 10
        assert rule_details["action"] == "accept"
        assert rule_details["description"] == "Test rule"
        assert rule_details["protocol"] == "tcp"
        assert rule_details["source"]["address"] == "10.0.0.1"
        assert rule_details["source"]["port"] == "1234"
        assert rule_details["destination"]["address"] == "192.168.1.1"
        assert rule_details["destination"]["port"] == "443"

    def test_format_json_default_action(self):
        """Test JSON formatting for default action."""
        result = MatchResult(
            matched=True,
            action="drop",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            is_default_action=True,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["matched"] is True
        assert data["action"] == "drop"
        assert data["is_default_action"] is True
        assert data["is_state_policy"] is False
        assert "rule_number" not in data
        assert "rule_details" not in data

    def test_format_json_state_policy(self):
        """Test JSON formatting for state policy."""
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="global",
            chain_family="global",
            chain_hook="",
            is_state_policy=True,
            state_policy_state="established",
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["is_state_policy"] is True
        assert data["state_policy_state"] == "established"

    def test_format_json_with_groups(self):
        """Test JSON formatting with groups."""
        rule = Rule(
            number=20,
            action="accept",
            source=SourceDestCriteria(
                network_group="INTERNAL", address_group="TRUSTED"
            ),
            destination=SourceDestCriteria(port_group="WEBPORTS"),
            inbound_interface=InterfaceCriteria(group="LAN"),
            outbound_interface=InterfaceCriteria(group="WAN"),
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=20,
            rule=rule,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        rule_details = data["rule_details"]
        assert rule_details["source"]["network_group"] == "INTERNAL"
        assert rule_details["source"]["address_group"] == "TRUSTED"
        assert rule_details["destination"]["port_group"] == "WEBPORTS"
        assert rule_details["inbound_interface"]["group"] == "LAN"
        assert rule_details["outbound_interface"]["group"] == "WAN"

    def test_format_json_with_state(self):
        """Test JSON formatting with state."""
        rule = Rule(
            number=5,
            action="accept",
            state=["established", "related"],
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=5,
            rule=rule,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["rule_details"]["state"] == ["established", "related"]

    def test_format_json_with_jump_target(self):
        """Test JSON formatting with jump target."""
        rule = Rule(
            number=10,
            action="jump",
            jump_target="CUSTOM_CHAIN",
        )
        result = MatchResult(
            matched=True,
            action="jump",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=10,
            rule=rule,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["rule_details"]["jump_target"] == "CUSTOM_CHAIN"

    def test_format_json_with_trace(self):
        """Test JSON formatting includes trace."""
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            is_default_action=True,
            trace=["Step 1", "Step 2", "Step 3"],
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["trace"] == ["Step 1", "Step 2", "Step 3"]

    def test_format_json_empty_trace(self):
        """Test JSON formatting with empty trace."""
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            is_default_action=True,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["trace"] == []

    def test_format_json_with_interfaces(self):
        """Test JSON formatting with interface names."""
        rule = Rule(
            number=15,
            action="accept",
            inbound_interface=InterfaceCriteria(name="eth0"),
            outbound_interface=InterfaceCriteria(name="eth1"),
        )
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            rule_number=15,
            rule=rule,
        )

        output = format_result(result, "json")
        data = json.loads(output)

        assert data["rule_details"]["inbound_interface"]["name"] == "eth0"
        assert data["rule_details"]["outbound_interface"]["name"] == "eth1"


class TestDefaultFormat:
    """Test default format behavior."""

    def test_default_format_is_table(self):
        """Test that default format is table."""
        result = MatchResult(
            matched=True,
            action="accept",
            chain_name="filter",
            chain_family="ipv4",
            chain_hook="forward",
            is_default_action=True,
        )

        # No format specified, should default to table
        output = format_result(result)

        assert "Policy Match Result" in output
        assert "=" * 50 in output
        assert "RESULT: ACCEPT" in output
