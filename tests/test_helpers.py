"""Tests for matching helper functions (IP, port, interface, protocol)."""

from __future__ import annotations

from vyfwmatch.services.helpers import (
    interface_matches,
    ip_in_range,
    ip_matches,
    ip_matches_with_mask,
    is_negated,
    port_matches,
    protocol_matches,
    resolve_service,
)


# ---------------------------------------------------------------------------
# is_negated
# ---------------------------------------------------------------------------


class TestIsNegated:
    """Test is_negated() function."""

    def test_negated(self):
        assert is_negated("!10.0.0.0/8") == (True, "10.0.0.0/8")

    def test_not_negated(self):
        assert is_negated("10.0.0.0/8") == (False, "10.0.0.0/8")

    def test_empty(self):
        assert is_negated("") == (False, "")


# ---------------------------------------------------------------------------
# IP matching
# ---------------------------------------------------------------------------


class TestIpMatches:
    """Test ip_matches() function."""

    def test_exact_match(self):
        assert ip_matches("198.51.100.101", "198.51.100.101") is True

    def test_exact_no_match(self):
        assert ip_matches("198.51.100.102", "198.51.100.101") is False

    def test_cidr_match(self):
        assert ip_matches("192.168.0.50", "192.168.0.0/24") is True

    def test_cidr_no_match(self):
        assert ip_matches("10.0.0.1", "192.168.0.0/24") is False

    def test_cidr_boundary(self):
        assert ip_matches("192.168.0.0", "192.168.0.0/24") is True
        assert ip_matches("192.168.0.255", "192.168.0.0/24") is True
        assert ip_matches("192.168.1.0", "192.168.0.0/24") is False

    def test_negation_cidr(self):
        # !10.0.0.0/8 means "anything NOT in 10.0.0.0/8"
        assert ip_matches("10.0.0.1", "!10.0.0.0/8") is False
        assert ip_matches("192.168.0.1", "!10.0.0.0/8") is True

    def test_negation_exact(self):
        assert ip_matches("10.0.0.1", "!10.0.0.1") is False
        assert ip_matches("10.0.0.2", "!10.0.0.1") is True

    def test_range_match(self):
        assert ip_matches("10.0.0.5", "10.0.0.1-10.0.0.8") is True

    def test_range_boundary(self):
        assert ip_matches("10.0.0.1", "10.0.0.1-10.0.0.8") is True
        assert ip_matches("10.0.0.8", "10.0.0.1-10.0.0.8") is True

    def test_range_no_match(self):
        assert ip_matches("10.0.0.9", "10.0.0.1-10.0.0.8") is False
        assert ip_matches("10.0.0.0", "10.0.0.1-10.0.0.8") is False

    def test_ipv6_cidr(self):
        assert ip_matches("2001:db8::100", "2001:db8::/64") is True
        assert ip_matches("2001:db9::1", "2001:db8::/64") is False

    def test_ipv6_exact(self):
        assert ip_matches("2001:db8::1", "2001:db8::1") is True
        assert ip_matches("2001:db8::2", "2001:db8::1") is False

    def test_ipv6_negation(self):
        assert ip_matches("2001:db8::1", "!2001:db8::/64") is False
        assert ip_matches("2001:db9::1", "!2001:db8::/64") is True

    def test_wide_cidr(self):
        assert ip_matches("192.0.2.1", "192.0.2.0/30") is True
        assert ip_matches("192.0.2.3", "192.0.2.0/30") is True
        assert ip_matches("192.0.2.4", "192.0.2.0/30") is False

    def test_slash_25(self):
        assert ip_matches("203.0.113.200", "203.0.113.128/25") is True
        assert ip_matches("203.0.113.100", "203.0.113.128/25") is False


class TestIpInRange:
    """Test ip_in_range() function."""

    def test_in_range(self):
        assert ip_in_range("10.0.0.5", "10.0.0.1-10.0.0.8") is True

    def test_out_of_range(self):
        assert ip_in_range("10.0.0.9", "10.0.0.1-10.0.0.8") is False

    def test_invalid_format(self):
        assert ip_in_range("10.0.0.1", "invalid") is False


class TestIpMatchesWithMask:
    """Test ip_matches_with_mask() function."""

    def test_exact_match_full_mask(self):
        """255.255.255.255 mask = exact match."""
        assert ip_matches_with_mask("89.234.162.249", "89.234.162.249", "255.255.255.255") is True

    def test_exact_no_match_full_mask(self):
        assert ip_matches_with_mask("89.234.162.250", "89.234.162.249", "255.255.255.255") is False

    def test_class_a_mask(self):
        """255.0.0.0 mask = match first octet."""
        assert ip_matches_with_mask("10.1.2.3", "10.0.0.0", "255.0.0.0") is True
        assert ip_matches_with_mask("11.1.2.3", "10.0.0.0", "255.0.0.0") is False

    def test_class_c_mask(self):
        """255.255.255.0 mask = match first 3 octets."""
        assert ip_matches_with_mask("192.168.1.50", "192.168.1.0", "255.255.255.0") is True
        assert ip_matches_with_mask("192.168.2.50", "192.168.1.0", "255.255.255.0") is False

    def test_zero_mask_matches_everything(self):
        """0.0.0.0 mask = match everything."""
        assert ip_matches_with_mask("1.2.3.4", "200.200.200.200", "0.0.0.0") is True

    def test_negated_address(self):
        """Negated address with mask."""
        assert ip_matches_with_mask("89.234.162.249", "!89.234.162.249", "255.255.255.255") is False
        assert ip_matches_with_mask("89.234.162.250", "!89.234.162.249", "255.255.255.255") is True

    def test_invalid_ip(self):
        """Invalid IP returns False."""
        assert ip_matches_with_mask("not-an-ip", "10.0.0.0", "255.0.0.0") is False


# ---------------------------------------------------------------------------
# Port matching
# ---------------------------------------------------------------------------


class TestPortMatches:
    """Test port_matches() function."""

    def test_exact_numeric(self):
        assert port_matches(443, "443") is True
        assert port_matches(80, "443") is False

    def test_named_port(self):
        assert port_matches(80, "http") is True
        assert port_matches(443, "https") is True
        assert port_matches(22, "ssh") is True

    def test_range(self):
        assert port_matches(5005, "5000-5010") is True
        assert port_matches(5000, "5000-5010") is True
        assert port_matches(5010, "5000-5010") is True
        assert port_matches(4999, "5000-5010") is False
        assert port_matches(5011, "5000-5010") is False

    def test_comma_list(self):
        assert port_matches(80, "http,443,8080-8090") is True
        assert port_matches(443, "http,443,8080-8090") is True
        assert port_matches(8085, "http,443,8080-8090") is True
        assert port_matches(22, "http,443,8080-8090") is False

    def test_negation(self):
        assert port_matches(80, "!http") is False
        assert port_matches(443, "!http") is True

    def test_negation_numeric(self):
        assert port_matches(443, "!443") is False
        assert port_matches(80, "!443") is True


# ---------------------------------------------------------------------------
# Interface matching
# ---------------------------------------------------------------------------


class TestInterfaceMatches:
    """Test interface_matches() function."""

    def test_exact(self):
        assert interface_matches("eth0", "eth0") is True
        assert interface_matches("eth1", "eth0") is False

    def test_wildcard(self):
        assert interface_matches("eth0", "eth*") is True
        assert interface_matches("eth1", "eth*") is True
        assert interface_matches("bond0", "eth*") is False

    def test_specific_wildcard(self):
        assert interface_matches("eth3", "eth3*") is True
        assert interface_matches("eth31", "eth3*") is True
        assert interface_matches("eth2", "eth3*") is False

    def test_negation(self):
        assert interface_matches("eth0", "!eth0") is False
        assert interface_matches("eth1", "!eth0") is True

    def test_negation_wildcard(self):
        assert interface_matches("eth0", "!bond*") is True
        assert interface_matches("bond0", "!bond*") is False


# ---------------------------------------------------------------------------
# Protocol matching
# ---------------------------------------------------------------------------


class TestProtocolMatches:
    """Test protocol_matches() function."""

    def test_exact(self):
        assert protocol_matches("tcp", "tcp") is True
        assert protocol_matches("udp", "udp") is True
        assert protocol_matches("tcp", "udp") is False

    def test_all(self):
        assert protocol_matches("tcp", "all") is True
        assert protocol_matches("udp", "all") is True
        assert protocol_matches("icmp", "all") is True

    def test_tcp_udp(self):
        assert protocol_matches("tcp", "tcp_udp") is True
        assert protocol_matches("udp", "tcp_udp") is True
        assert protocol_matches("icmp", "tcp_udp") is False

    def test_negation(self):
        assert protocol_matches("tcp", "!tcp") is False
        assert protocol_matches("udp", "!tcp") is True

    def test_case_insensitive(self):
        assert protocol_matches("TCP", "tcp") is True
        assert protocol_matches("tcp", "TCP") is True


# ---------------------------------------------------------------------------
# Service resolution
# ---------------------------------------------------------------------------


class TestResolveService:
    """Test resolve_service() function."""

    def test_http(self):
        port, proto = resolve_service("http")
        assert port == 80
        assert proto == "tcp"

    def test_https(self):
        port, proto = resolve_service("https")
        assert port == 443
        assert proto == "tcp"

    def test_ssh(self):
        port, proto = resolve_service("ssh")
        assert port == 22
        assert proto == "tcp"

    def test_dns(self):
        port, proto = resolve_service("dns")
        assert port == 53
        assert proto == "udp"

    def test_numeric(self):
        port, proto = resolve_service("8080")
        assert port == 8080
        assert proto is None

    def test_numeric_443(self):
        port, proto = resolve_service("443")
        assert port == 443
        assert proto is None

    def test_unknown(self):
        port, _ = resolve_service("nonexistent_service_xyz")
        assert port is None
