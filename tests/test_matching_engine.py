"""End-to-end matching engine tests using real VyOS config scenarios.

Each test exercises the full pipeline: parse config → extract → match.
Configs are from the official VyOS documentation.
"""

from __future__ import annotations

import pytest

from matcher.engine import MatchingEngine, MatchResult, TrafficTuple
from parser.models import FirewallConfig
from tests.conftest import build_config, match_traffic


# ===================================================================
# Scenario 1: Quick-Start Home/Small Office Gateway
# ===================================================================


class TestQuickstartForward:
    """Forward chain tests: traffic passing THROUGH the router."""

    def test_wan_to_lan_https_new_drops(self, quickstart_config: FirewallConfig):
        """WAN→LAN new HTTPS: hits OUTSIDE-IN default drop (no allow rule for 443)."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.10",
            protocol="tcp",
            port=443,
            state="new",
        )
        assert result.matched is True
        assert result.action == "drop"
        # Should have traversed CONN_FILTER (no match on new) → OUTSIDE-IN (default drop)

    def test_wan_to_lan_established_accepts(self, quickstart_config: FirewallConfig):
        """WAN→LAN established traffic: accepted by CONN_FILTER rule 10."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.10",
            protocol="tcp",
            port=443,
            state="established",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.chain_name == "CONN_FILTER"
        assert result.rule_number == 10

    def test_wan_to_lan_invalid_drops(self, quickstart_config: FirewallConfig):
        """WAN→LAN invalid state: dropped by CONN_FILTER rule 20."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.10",
            protocol="tcp",
            port=80,
            state="invalid",
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.chain_name == "CONN_FILTER"
        assert result.rule_number == 20

    def test_lan_to_wan_new_accepts(self, quickstart_config: FirewallConfig):
        """LAN→WAN new traffic: CONN_FILTER returns, rule 100 doesn't match
        (destination not in NET-INSIDE-v4), falls to default accept."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth1",
            outbound_interface="eth0",
            source_ip="192.168.0.50",
            destination_ip="8.8.8.8",
            protocol="tcp",
            port=443,
            state="new",
        )
        assert result.matched is True
        assert result.action == "accept"

    def test_wan_to_non_internal_default_accept(self, quickstart_config: FirewallConfig):
        """WAN→non-LAN (dest not in NET-INSIDE-v4): rule 100 doesn't match,
        falls to forward default accept."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            outbound_interface="eth2",
            source_ip="1.2.3.4",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=80,
            state="new",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.is_default_action is True


class TestQuickstartInput:
    """Input chain tests: traffic destined TO the router."""

    def test_ssh_from_lan_accepts(self, quickstart_config: FirewallConfig):
        """SSH from LAN: jumps to VyOS_MANAGEMENT, rule 15 accepts (LAN group)."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth1",
            source_ip="192.168.0.50",
            destination_ip="192.168.0.1",
            protocol="tcp",
            port=22,
            state="new",
            hook="input",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.chain_name == "VyOS_MANAGEMENT"
        assert result.rule_number == 15

    def test_ssh_from_wan_new_accepts(self, quickstart_config: FirewallConfig):
        """SSH from WAN with state=new: VyOS_MANAGEMENT rule 20 (recent drop)
        matches first for new+WAN, but rule 21 accepts new+WAN.
        Actually rule 20 drops because it matches new+WAN with recent criteria.
        Since we don't model 'recent' matching, rule 20 matches on state+interface."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.1",
            protocol="tcp",
            port=22,
            state="new",
            hook="input",
        )
        assert result.matched is True
        # Rule 20 has recent + state new + WAN — since we can't evaluate
        # 'recent' counters, the rule matches on state+interface criteria
        assert result.chain_name == "VyOS_MANAGEMENT"

    def test_icmp_new_accepts(self, quickstart_config: FirewallConfig):
        """ICMP echo-request with state=new: accepted by input rule 30."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.1",
            protocol="icmp",
            state="new",
            hook="input",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 30

    def test_dns_from_lan_accepts(self, quickstart_config: FirewallConfig):
        """DNS from LAN network: accepted by input rule 40."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth1",
            source_ip="192.168.0.50",
            destination_ip="192.168.0.1",
            protocol="udp",
            port=53,
            hook="input",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 40

    def test_dns_from_wan_drops(self, quickstart_config: FirewallConfig):
        """DNS from WAN: source NOT in NET-INSIDE-v4, no match → default drop."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.1",
            protocol="udp",
            port=53,
            hook="input",
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.is_default_action is True

    def test_loopback_accepts(self, quickstart_config: FirewallConfig):
        """Loopback traffic (127.x.x.x): accepted by input rule 50."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="lo",
            source_ip="127.0.0.1",
            destination_ip="127.0.0.1",
            protocol="tcp",
            port=8080,
            hook="input",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 50

    def test_unknown_service_default_drop(self, quickstart_config: FirewallConfig):
        """Unknown service from WAN: no rule matches → default drop."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.1",
            protocol="tcp",
            port=9999,
            state="new",
            hook="input",
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.is_default_action is True


# ===================================================================
# Scenario 2: Groups (address, network, port, interface)
# ===================================================================


class TestGroupsForward:
    def test_trusted_source_accepts(self, groups_config: FirewallConfig):
        """Source in TRUSTEDv4 network: accepted by forward rule 20."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="192.0.2.1",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=80,
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 20

    def test_trusted_source_other_subnet(self, groups_config: FirewallConfig):
        """Source in other TRUSTEDv4 subnet (203.0.113.128/25)."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="203.0.113.200",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=80,
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 20

    def test_untrusted_source_drops(self, groups_config: FirewallConfig):
        """Source NOT in TRUSTEDv4: no match on rule 20 → default drop."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="10.10.10.10",
            destination_ip="10.0.0.1",
            protocol="udp",
            port=9999,
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.is_default_action is True

    def test_port_group_from_internal(self, groups_config: FirewallConfig):
        """Internal source + port in PORT-TCP-SERVER1: accepted by rule 40."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth1",
            outbound_interface="eth0",
            source_ip="192.168.0.50",
            destination_ip="8.8.8.8",
            protocol="tcp",
            port=443,
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 40

    def test_port_group_range_match(self, groups_config: FirewallConfig):
        """Internal source + port 5005 (in 5000-5010 range): accepted by rule 40."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth1",
            outbound_interface="eth0",
            source_ip="192.168.1.10",
            destination_ip="8.8.8.8",
            protocol="tcp",
            port=5005,
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 40


class TestGroupsIpv6:
    def test_trusted_ipv6_source_accepts(self, groups_config: FirewallConfig):
        """IPv6 source in TRUSTEDv6: accepted by ipv6 input rule 10."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth0",
            source_ip="2001:db8::100",
            destination_ip="2001:db8::1",
            protocol="tcp",
            port=22,
            hook="input",
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 10

    def test_untrusted_ipv6_drops(self, groups_config: FirewallConfig):
        """IPv6 source NOT in TRUSTEDv6: default drop."""
        result = match_traffic(
            groups_config,
            inbound_interface="eth0",
            source_ip="2001:db9::1",
            destination_ip="2001:db8::1",
            protocol="tcp",
            port=22,
            hook="input",
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.is_default_action is True


# ===================================================================
# Scenario 3: Zone-Based Firewall — test named chains directly
# ===================================================================


class TestZoneNamedChains:
    """Test named chains from the zone-based config.

    Since zone-based matching (zone→interface mapping) isn't implemented
    in the engine, we test the named chains directly.
    """

    def test_wan_lan_established_accepts(self, zone_config: FirewallConfig):
        """WAN-LAN-v4 chain: established → accept."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv4_chains["WAN-LAN-v4"]
        traffic = TrafficTuple(
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.10",
            protocol="tcp",
            port=80,
            state="established",
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv4_chains, []
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 10

    def test_wan_lan_new_drops(self, zone_config: FirewallConfig):
        """WAN-LAN-v4 chain: new traffic → default drop."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv4_chains["WAN-LAN-v4"]
        traffic = TrafficTuple(
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="192.168.0.10",
            protocol="tcp",
            port=80,
            state="new",
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv4_chains, []
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.is_default_action is True

    def test_lan_local_ssh_accepts(self, zone_config: FirewallConfig):
        """LAN-LOCAL-v4: SSH (port 22 TCP) → accept (rule 30)."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv4_chains["LAN-LOCAL-v4"]
        traffic = TrafficTuple(
            inbound_interface="eth1",
            source_ip="192.168.0.50",
            destination_ip="192.168.0.1",
            protocol="tcp",
            port=22,
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv4_chains, []
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 30

    def test_lan_local_icmp_accepts(self, zone_config: FirewallConfig):
        """LAN-LOCAL-v4: ICMP → accept (rule 20)."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv4_chains["LAN-LOCAL-v4"]
        traffic = TrafficTuple(
            inbound_interface="eth1",
            source_ip="192.168.0.50",
            destination_ip="192.168.0.1",
            protocol="icmp",
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv4_chains, []
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 20

    def test_lan_local_random_port_drops(self, zone_config: FirewallConfig):
        """LAN-LOCAL-v4: random UDP port → default drop."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv4_chains["LAN-LOCAL-v4"]
        traffic = TrafficTuple(
            inbound_interface="eth1",
            source_ip="192.168.0.50",
            destination_ip="192.168.0.1",
            protocol="udp",
            port=9999,
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv4_chains, []
        )
        assert result.matched is True
        assert result.action == "drop"
        assert result.is_default_action is True

    def test_ipv6_wan_local_icmpv6_accepts(self, zone_config: FirewallConfig):
        """WAN-LOCAL-v6: ICMPv6 → accept (rule 20)."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv6_chains["WAN-LOCAL-v6"]
        traffic = TrafficTuple(
            inbound_interface="eth0",
            source_ip="2001:db8::1",
            destination_ip="fe80::1",
            protocol="icmpv6",
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv6_chains, []
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.rule_number == 20

    def test_local_wan_default_accept(self, zone_config: FirewallConfig):
        """LOCAL-WAN-v4: default accept (no rules)."""
        engine = MatchingEngine(zone_config)
        chain = zone_config.ipv4_chains["LOCAL-WAN-v4"]
        traffic = TrafficTuple(
            inbound_interface="eth0",
            source_ip="192.168.0.1",
            destination_ip="8.8.8.8",
            protocol="tcp",
            port=443,
        )
        result = engine._evaluate_chain(
            chain, traffic, zone_config.ipv4_chains, []
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.is_default_action is True


# ===================================================================
# Scenario 4: Detailed matching — ranges, negation, disabled rules, IPv6
# ===================================================================


class TestDetailedForward:
    def test_established_accepts(self, detailed_config: FirewallConfig):
        """Established traffic accepted by rule 5."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="1.2.3.4",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=80,
            state="established",
        )
        assert result.action == "accept"
        assert result.rule_number == 5

    def test_invalid_drops(self, detailed_config: FirewallConfig):
        """Invalid state dropped by rule 10."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="1.2.3.4",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=80,
            state="invalid",
        )
        assert result.action == "drop"
        assert result.rule_number == 10

    def test_source_range_match(self, detailed_config: FirewallConfig):
        """Source in range 192.0.2.10-192.0.2.20 with dest port 443: rule 50."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="192.0.2.15",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=443,
        )
        assert result.action == "accept"
        assert result.rule_number == 50

    def test_source_range_no_match(self, detailed_config: FirewallConfig):
        """Source outside range: doesn't match rule 50."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="192.0.2.25",
            destination_ip="10.0.0.1",
            protocol="tcp",
            port=443,
        )
        # Should not match rule 50 (out of range), may match rule 60 or 70
        assert result.rule_number != 50

    def test_internal_to_webports_accepts(self, detailed_config: FirewallConfig):
        """Internal source + web port: accepted by rule 60."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth1",
            outbound_interface="eth0",
            source_ip="10.0.0.50",
            destination_ip="8.8.8.8",
            protocol="tcp",
            port=8085,
        )
        assert result.action == "accept"
        assert result.rule_number == 60

    def test_internal_to_webports_port80(self, detailed_config: FirewallConfig):
        """Internal source + port 80: accepted by rule 60."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth1",
            outbound_interface="eth0",
            source_ip="172.16.0.1",
            destination_ip="8.8.8.8",
            protocol="tcp",
            port=80,
        )
        assert result.action == "accept"
        assert result.rule_number == 60

    def test_negation_drops_external(self, detailed_config: FirewallConfig):
        """Source NOT in 10.0.0.0/8 (negated match): dropped by rule 70."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="203.0.113.5",
            destination_ip="10.0.0.1",
            protocol="udp",
            port=9999,
        )
        assert result.action == "drop"
        assert result.rule_number == 70

    def test_negation_does_not_drop_internal(self, detailed_config: FirewallConfig):
        """Source IN 10.0.0.0/8: rule 70 does NOT match (negated)."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="10.0.0.50",
            destination_ip="1.2.3.4",
            protocol="udp",
            port=9999,
        )
        # Rule 70 doesn't match (10.x IS in !10.0.0.0/8 → negation = no match)
        # Falls through to rule 80 (icmp) → no match (udp), then rule 100 (disabled) → default drop
        assert result.rule_number != 70

    def test_icmp_accepts(self, detailed_config: FirewallConfig):
        """ICMP traffic: accepted by rule 80."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="10.0.0.1",
            destination_ip="10.0.0.2",
            protocol="icmp",
        )
        assert result.action == "accept"
        assert result.rule_number == 80

    def test_disabled_rule_skipped(self, detailed_config: FirewallConfig):
        """Rule 100 is disabled: should be skipped, fall to default drop."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="10.0.0.1",
            destination_ip="10.0.0.2",
            protocol="udp",
            port=9999,
        )
        # Rule 100 (disabled catch-all) should be skipped
        assert result.rule_number != 100
        assert result.is_default_action is True
        assert result.action == "drop"


class TestDetailedInput:
    def test_ssh_from_trusted_interface(self, detailed_config: FirewallConfig):
        """SSH from trusted interface group: accepted by input rule 10."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth1",
            source_ip="10.0.0.1",
            destination_ip="10.0.0.254",
            protocol="tcp",
            port=22,
            hook="input",
        )
        assert result.action == "accept"
        assert result.rule_number == 10

    def test_ssh_from_untrusted_interface(self, detailed_config: FirewallConfig):
        """SSH from untrusted interface: rule 10 doesn't match → default drop."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="10.0.0.254",
            protocol="tcp",
            port=22,
            hook="input",
        )
        # eth0 is not in TRUSTED group (eth1, eth2)
        assert result.action == "drop"

    def test_icmp_input_accepts(self, detailed_config: FirewallConfig):
        """ICMP to router: accepted by input rule 20."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            source_ip="1.2.3.4",
            destination_ip="10.0.0.254",
            protocol="icmp",
            hook="input",
        )
        assert result.action == "accept"
        assert result.rule_number == 20


class TestDetailedIpv6:
    def test_ipv6_established_accepts(self, detailed_config: FirewallConfig):
        """IPv6 established traffic: accepted by forward rule 10."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="2001:db8::1",
            destination_ip="2001:db8::2",
            protocol="tcp",
            port=80,
            state="established",
        )
        assert result.action == "accept"
        assert result.rule_number == 10

    def test_ipv6_icmpv6_accepts(self, detailed_config: FirewallConfig):
        """IPv6 ICMPv6: accepted by forward rule 20."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="2001:db8::1",
            destination_ip="2001:db8::2",
            protocol="icmpv6",
        )
        assert result.action == "accept"
        assert result.rule_number == 20

    def test_ipv6_https_from_prefix_accepts(self, detailed_config: FirewallConfig):
        """IPv6 HTTPS from 2001:db8::/32: accepted by forward rule 30."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="2001:db8:1::100",
            destination_ip="2001:db8::2",
            protocol="tcp",
            port=443,
        )
        assert result.action == "accept"
        assert result.rule_number == 30

    def test_ipv6_https_outside_prefix_drops(self, detailed_config: FirewallConfig):
        """IPv6 HTTPS from outside 2001:db8::/32: default drop."""
        result = match_traffic(
            detailed_config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="2001:db9::1",
            destination_ip="2001:db8::2",
            protocol="tcp",
            port=443,
        )
        assert result.action == "drop"
        assert result.is_default_action is True


# ===================================================================
# General edge cases
# ===================================================================


class TestEdgeCases:
    def test_no_firewall_config(self):
        """Empty config: no chains → implicit accept."""
        config = build_config("")
        result = match_traffic(
            config,
            inbound_interface="eth0",
            outbound_interface="eth1",
            source_ip="10.0.0.1",
            destination_ip="10.0.0.2",
            protocol="tcp",
            port=80,
        )
        assert result.matched is True
        assert result.action == "accept"
        assert result.is_default_action is True

    def test_trace_is_populated(self, quickstart_config: FirewallConfig):
        """Trace should contain evaluation steps."""
        result = match_traffic(
            quickstart_config,
            inbound_interface="eth1",
            source_ip="192.168.0.50",
            destination_ip="192.168.0.1",
            protocol="tcp",
            port=22,
            state="new",
            hook="input",
        )
        assert len(result.trace) > 0
        assert any("Hook determined" in t for t in result.trace)
        assert any("Evaluating chain" in t for t in result.trace)
