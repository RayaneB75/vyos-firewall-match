"""Tests for the firewall rule/group extractor."""

from __future__ import annotations

from tests.conftest import (
    DETAILED_CONFIG,
    GROUPS_CONFIG,
    MINIMAL_DROP_WITH_STATE_RULE_CONFIG,
    QUICKSTART_CONFIG,
    build_config,
)


class TestExtractGroups:
    """Test extraction of firewall groups."""

    def test_extract_address_group(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("address", "SERVERS")
        assert grp is not None
        assert "198.51.100.101" in grp.members
        assert "198.51.100.102" in grp.members

    def test_extract_address_group_with_range(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("address", "ADR-INSIDE-v4")
        assert grp is not None
        assert "192.168.0.1" in grp.members
        assert "10.0.0.1-10.0.0.8" in grp.members

    def test_extract_network_group(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("network", "TRUSTEDv4")
        assert grp is not None
        assert "192.0.2.0/30" in grp.members
        assert "203.0.113.128/25" in grp.members

    def test_extract_network_group_multi(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("network", "NET-INSIDE-v4")
        assert grp is not None
        assert len(grp.members) == 2

    def test_extract_port_group(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("port", "PORT-TCP-SERVER1")
        assert grp is not None
        assert "http" in grp.members
        assert "443" in grp.members
        assert "5000-5010" in grp.members

    def test_extract_interface_group(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("interface", "LAN")
        assert grp is not None
        assert "eth2.2001" in grp.members
        assert "bon0" in grp.members
        assert "eth3" in grp.members

    def test_extract_ipv6_network_group(self):
        config = build_config(GROUPS_CONFIG)
        grp = config.get_group("ipv6-network", "TRUSTEDv6")
        assert grp is not None
        assert "2001:db8::/64" in grp.members

    def test_no_groups_returns_empty(self):
        config = build_config("firewall { ipv4 { } }")
        assert len(config.groups) == 0


class TestExtractStatePolicy:
    """Test extraction of global state policies."""

    def test_extract_global_state_policy(self):
        config = build_config(QUICKSTART_CONFIG)
        assert len(config.state_policies) == 3
        states = {sp.state: sp.action for sp in config.state_policies}
        assert states["established"] == "accept"
        assert states["related"] == "accept"
        assert states["invalid"] == "drop"

    def test_no_state_policy(self):
        config = build_config(GROUPS_CONFIG)
        assert len(config.state_policies) == 0


class TestExtractChains:
    """Test extraction of firewall chains."""

    def test_extract_forward_chain(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains.get("forward-filter")
        assert chain is not None
        assert chain.hook == "forward"
        assert chain.family == "ipv4"
        assert chain.default_action == "accept"

    def test_extract_input_chain(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains.get("input-filter")
        assert chain is not None
        assert chain.hook == "input"
        assert chain.default_action == "drop"

    def test_extract_named_chain(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains.get("CONN_FILTER")
        assert chain is not None
        assert chain.hook == "custom"
        assert chain.default_action == "return"
        assert len(chain.rules) == 2

    def test_extract_named_chain_outside_in(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains.get("OUTSIDE-IN")
        assert chain is not None
        assert chain.default_action == "drop"
        assert len(chain.rules) == 0  # No rules, just default drop

    def test_extract_ipv6_chain(self):
        config = build_config(GROUPS_CONFIG)
        chain = config.ipv6_chains.get("input-filter")
        assert chain is not None
        assert chain.family == "ipv6"
        assert chain.default_action == "drop"
        assert len(chain.rules) == 1

    def test_forward_chain_rule_count(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        assert len(chain.rules) == 2  # rule 10 and rule 100

    def test_input_chain_rule_count(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains["input-filter"]
        assert len(chain.rules) == 5  # rules 10, 20, 30, 40, 50


class TestExtractRules:
    """Test extraction of firewall rules."""

    def test_extract_rule_with_source_dest(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains["input-filter"]
        rules = chain.sorted_rules()
        # Rule 40: accept DNS from NET-INSIDE-v4
        rule_40 = next(r for r in rules if r.number == 40)
        assert rule_40.action == "accept"
        assert rule_40.protocol == "tcp_udp"
        assert rule_40.destination.port == "53"
        assert rule_40.source.network_group == "NET-INSIDE-v4"

    def test_extract_rule_with_groups(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rules = chain.sorted_rules()
        # Rule 100: jump OUTSIDE-IN for WAN→NET-INSIDE-v4
        rule_100 = next(r for r in rules if r.number == 100)
        assert rule_100.action == "jump"
        assert rule_100.jump_target == "OUTSIDE-IN"
        assert rule_100.inbound_interface.group == "WAN"
        assert rule_100.destination.network_group == "NET-INSIDE-v4"

    def test_extract_rule_with_interface_name(self):
        config = build_config(DETAILED_CONFIG)
        chain = config.ipv4_chains["input-filter"]
        rules = chain.sorted_rules()
        rule_10 = next(r for r in rules if r.number == 10)
        assert rule_10.inbound_interface.group == "TRUSTED"

    def test_extract_rule_with_state(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains["CONN_FILTER"]
        rules = chain.sorted_rules()
        rule_10 = next(r for r in rules if r.number == 10)
        assert "established" in rule_10.state
        assert "related" in rule_10.state

    def test_extract_jump_rule(self):
        config = build_config(QUICKSTART_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rules = chain.sorted_rules()
        rule_10 = next(r for r in rules if r.number == 10)
        assert rule_10.action == "jump"
        assert rule_10.jump_target == "CONN_FILTER"

    def test_extract_disabled_rule(self):
        config = build_config(DETAILED_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rules = chain.sorted_rules()
        rule_100 = next(r for r in rules if r.number == 100)
        assert rule_100.disabled is True

    def test_extract_rule_with_address_range(self):
        config = build_config(DETAILED_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rules = chain.sorted_rules()
        rule_50 = next(r for r in rules if r.number == 50)
        assert rule_50.source.address == "192.0.2.10-192.0.2.20"

    def test_extract_rule_with_negation(self):
        config = build_config(DETAILED_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rules = chain.sorted_rules()
        rule_70 = next(r for r in rules if r.number == 70)
        assert rule_70.source.address == "!10.0.0.0/8"

    def test_rules_sorted_by_number(self):
        config = build_config(DETAILED_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rules = chain.sorted_rules()
        numbers = [r.number for r in rules]
        assert numbers == sorted(numbers)

    def test_extract_ipv6_forward_rules(self):
        config = build_config(DETAILED_CONFIG)
        chain = config.ipv6_chains.get("forward-filter")
        assert chain is not None
        assert chain.default_action == "drop"
        assert len(chain.rules) == 3

    def test_extract_state_as_repeated_leaf(self):
        """State specified as repeated leaves (not inside a block) produces a list."""
        config = build_config(MINIMAL_DROP_WITH_STATE_RULE_CONFIG)
        chain = config.ipv4_chains["forward-filter"]
        rule = chain.sorted_rules()[0]
        assert "established" in rule.state
        assert "related" in rule.state
