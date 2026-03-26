"""Tests for VyOS validator wrappers.

Tests the vyos_validators module that wraps both shell-based and Python-based
validators from VyOS.
"""

# pylint: disable=protected-access

from vyfwmatch.services import vyos_validators


class TestIPv4AddressValidation:
    """Test IPv4 address validation."""

    def test_valid_ipv4(self):
        """Valid IPv4 addresses should pass."""
        assert vyos_validators.validate_ipv4_address("192.168.1.1")
        assert vyos_validators.validate_ipv4_address("10.0.0.1")
        assert vyos_validators.validate_ipv4_address("172.16.0.1")
        assert vyos_validators.validate_ipv4_address("8.8.8.8")

    def test_invalid_ipv4(self):
        """Invalid IPv4 addresses should fail."""
        assert not vyos_validators.validate_ipv4_address("256.1.1.1")
        assert not vyos_validators.validate_ipv4_address("192.168.1.300")
        assert not vyos_validators.validate_ipv4_address("not-an-ip")
        assert not vyos_validators.validate_ipv4_address("192.168.1")
        assert not vyos_validators.validate_ipv4_address("")

    def test_ipv4_with_prefix_fails(self):
        """IPv4 with CIDR prefix should fail (use validate_ipv4_prefix)."""
        assert not vyos_validators.validate_ipv4_address("192.168.1.0/24")


class TestIPv6AddressValidation:
    """Test IPv6 address validation."""

    def test_valid_ipv6(self):
        """Valid IPv6 addresses should pass."""
        assert vyos_validators.validate_ipv6_address("2001:db8::1")
        assert vyos_validators.validate_ipv6_address("fe80::1")
        assert vyos_validators.validate_ipv6_address("::1")
        assert vyos_validators.validate_ipv6_address("2001:0db8:0000:0000:0000:0000:0000:0001")

    def test_invalid_ipv6(self):
        """Invalid IPv6 addresses should fail."""
        assert not vyos_validators.validate_ipv6_address("gggg::1")
        assert not vyos_validators.validate_ipv6_address("192.168.1.1")
        assert not vyos_validators.validate_ipv6_address("not-an-ip")
        assert not vyos_validators.validate_ipv6_address("")

    def test_ipv6_with_prefix_fails(self):
        """IPv6 with CIDR prefix should fail (use validate_ipv6_prefix)."""
        assert not vyos_validators.validate_ipv6_address("2001:db8::/32")


class TestIPv4PrefixValidation:
    """Test IPv4 prefix (CIDR) validation."""

    def test_valid_ipv4_prefix(self):
        """Valid IPv4 prefixes should pass."""
        assert vyos_validators.validate_ipv4_prefix("192.168.1.0/24")
        assert vyos_validators.validate_ipv4_prefix("10.0.0.0/8")
        assert vyos_validators.validate_ipv4_prefix("172.16.0.0/12")
        assert vyos_validators.validate_ipv4_prefix("0.0.0.0/0")
        assert vyos_validators.validate_ipv4_prefix("192.168.1.1/32")

    def test_invalid_ipv4_prefix(self):
        """Invalid IPv4 prefixes should fail."""
        assert not vyos_validators.validate_ipv4_prefix("192.168.1.0/33")
        assert not vyos_validators.validate_ipv4_prefix("192.168.1.0/")
        assert not vyos_validators.validate_ipv4_prefix("192.168.1.0")
        assert not vyos_validators.validate_ipv4_prefix("not-a-prefix")
        assert not vyos_validators.validate_ipv4_prefix("")


class TestIPv6PrefixValidation:
    """Test IPv6 prefix (CIDR) validation."""

    def test_valid_ipv6_prefix(self):
        """Valid IPv6 prefixes should pass."""
        assert vyos_validators.validate_ipv6_prefix("2001:db8::/32")
        assert vyos_validators.validate_ipv6_prefix("fe80::/10")
        assert vyos_validators.validate_ipv6_prefix("::/0")
        assert vyos_validators.validate_ipv6_prefix("2001:db8::1/128")

    def test_invalid_ipv6_prefix(self):
        """Invalid IPv6 prefixes should fail."""
        assert not vyos_validators.validate_ipv6_prefix("2001:db8::/129")
        assert not vyos_validators.validate_ipv6_prefix("2001:db8::/")
        assert not vyos_validators.validate_ipv6_prefix("2001:db8::")
        assert not vyos_validators.validate_ipv6_prefix("not-a-prefix")
        assert not vyos_validators.validate_ipv6_prefix("")


class TestIPv4RangeValidation:
    """Test IPv4 range validation."""

    def test_valid_ipv4_range(self):
        """Valid IPv4 ranges should pass."""
        assert vyos_validators.validate_ipv4_range("192.168.1.1-192.168.1.10")
        assert vyos_validators.validate_ipv4_range("10.0.0.1-10.0.0.255")
        assert vyos_validators.validate_ipv4_range("172.16.0.1-172.16.0.1")  # Same IP

    def test_invalid_ipv4_range(self):
        """Invalid IPv4 ranges should fail."""
        assert not vyos_validators.validate_ipv4_range("192.168.1.10-192.168.1.1")  # Reversed
        assert not vyos_validators.validate_ipv4_range("192.168.1.1-256.1.1.1")  # Invalid end
        assert not vyos_validators.validate_ipv4_range("not-a-range")
        assert not vyos_validators.validate_ipv4_range("192.168.1.1")
        assert not vyos_validators.validate_ipv4_range("")


class TestIPv6RangeValidation:
    """Test IPv6 range validation."""

    def test_valid_ipv6_range(self):
        """Valid IPv6 ranges should pass."""
        assert vyos_validators.validate_ipv6_range("2001:db8::1-2001:db8::10")
        assert vyos_validators.validate_ipv6_range("fe80::1-fe80::ffff")
        assert vyos_validators.validate_ipv6_range("::1-::1")  # Same IP

    def test_invalid_ipv6_range(self):
        """Invalid IPv6 ranges should fail."""
        assert not vyos_validators.validate_ipv6_range("2001:db8::10-2001:db8::1")  # Reversed
        assert not vyos_validators.validate_ipv6_range("not-a-range")
        assert not vyos_validators.validate_ipv6_range("2001:db8::1")
        assert not vyos_validators.validate_ipv6_range("")


class TestMACAddressValidation:
    """Test MAC address validation."""

    def test_valid_mac(self):
        """Valid MAC addresses should pass."""
        assert vyos_validators.validate_mac_address("00:11:22:33:44:55")
        assert vyos_validators.validate_mac_address("AA:BB:CC:DD:EE:FF")
        assert vyos_validators.validate_mac_address("aa:bb:cc:dd:ee:ff")
        assert vyos_validators.validate_mac_address("12:34:56:78:9a:bc")

    def test_invalid_mac(self):
        """Invalid MAC addresses should fail."""
        assert not vyos_validators.validate_mac_address("00:11:22:33:44")  # Too short
        assert not vyos_validators.validate_mac_address("00:11:22:33:44:55:66")  # Too long
        assert not vyos_validators.validate_mac_address("00-11-22-33-44-55")  # Wrong separator
        assert not vyos_validators.validate_mac_address("GG:11:22:33:44:55")  # Invalid hex
        assert not vyos_validators.validate_mac_address("not-a-mac")
        assert not vyos_validators.validate_mac_address("")


class TestFQDNValidation:
    """Test FQDN validation."""

    def test_valid_fqdn(self):
        """Valid FQDNs should pass."""
        assert vyos_validators.validate_fqdn("example.com")
        assert vyos_validators.validate_fqdn("subdomain.example.com")
        assert vyos_validators.validate_fqdn("multiple.sub.domains.example.com")
        assert vyos_validators.validate_fqdn("example123.com")
        assert vyos_validators.validate_fqdn("ex-ample.com")

    def test_invalid_fqdn(self):
        """Invalid FQDNs should fail."""
        assert not vyos_validators.validate_fqdn("-example.com")  # Leading hyphen
        assert not vyos_validators.validate_fqdn("example-.com")  # Trailing hyphen
        assert not vyos_validators.validate_fqdn("example..com")  # Double dot
        assert not vyos_validators.validate_fqdn(".example.com")  # Leading dot
        assert not vyos_validators.validate_fqdn("example.com.")  # Trailing dot (depends on RFC interpretation)
        assert not vyos_validators.validate_fqdn("")


class TestIPProtocolValidation:
    """Test IP protocol validation."""

    def test_valid_protocol_numbers(self):
        """Valid protocol numbers should pass."""
        assert vyos_validators.validate_ip_protocol("0")
        assert vyos_validators.validate_ip_protocol("6")  # TCP
        assert vyos_validators.validate_ip_protocol("17")  # UDP
        assert vyos_validators.validate_ip_protocol("1")  # ICMP
        assert vyos_validators.validate_ip_protocol("255")

    def test_invalid_protocol_numbers(self):
        """Invalid protocol numbers should fail."""
        assert not vyos_validators.validate_ip_protocol("256")
        assert not vyos_validators.validate_ip_protocol("-1")
        assert not vyos_validators.validate_ip_protocol("999")

    def test_valid_protocol_names(self):
        """Valid protocol names should pass."""
        assert vyos_validators.validate_ip_protocol("tcp")
        assert vyos_validators.validate_ip_protocol("udp")
        assert vyos_validators.validate_ip_protocol("icmp")
        assert vyos_validators.validate_ip_protocol("esp")
        assert vyos_validators.validate_ip_protocol("ah")
        assert vyos_validators.validate_ip_protocol("gre")
        assert vyos_validators.validate_ip_protocol("tcp_udp")

    def test_invalid_protocol_names(self):
        """Invalid protocol names should fail."""
        assert not vyos_validators.validate_ip_protocol("invalid")
        assert not vyos_validators.validate_ip_protocol("notaprotocol")
        assert not vyos_validators.validate_ip_protocol("")


class TestPortRangeValidation:
    """Test port range validation."""

    def test_valid_single_ports(self):
        """Valid single port numbers should pass."""
        assert vyos_validators.validate_port_range("1")
        assert vyos_validators.validate_port_range("80")
        assert vyos_validators.validate_port_range("443")
        assert vyos_validators.validate_port_range("8080")
        assert vyos_validators.validate_port_range("65535")

    def test_invalid_single_ports(self):
        """Invalid single port numbers should fail."""
        assert not vyos_validators.validate_port_range("0")
        assert not vyos_validators.validate_port_range("65536")
        assert not vyos_validators.validate_port_range("-1")
        assert not vyos_validators.validate_port_range("99999")

    def test_valid_port_ranges(self):
        """Valid port ranges should pass."""
        assert vyos_validators.validate_port_range("80-443")
        assert vyos_validators.validate_port_range("1-1024")
        assert vyos_validators.validate_port_range("8000-9000")
        assert vyos_validators.validate_port_range("1-65535")

    def test_invalid_port_ranges(self):
        """Invalid port ranges should fail."""
        assert not vyos_validators.validate_port_range("443-80")  # Reversed
        assert not vyos_validators.validate_port_range("0-100")  # Invalid start
        assert not vyos_validators.validate_port_range("100-70000")  # Invalid end
        assert not vyos_validators.validate_port_range("100-")  # Missing end
        assert not vyos_validators.validate_port_range("-100")  # Missing start

    def test_valid_service_names(self):
        """Valid service names should pass."""
        assert vyos_validators.validate_port_range("http")
        assert vyos_validators.validate_port_range("https")
        assert vyos_validators.validate_port_range("ssh")
        assert vyos_validators.validate_port_range("ftp")
        assert vyos_validators.validate_port_range("dns")
        assert vyos_validators.validate_port_range("smtp")

    def test_invalid_service_names(self):
        """Invalid service names should fail."""
        assert not vyos_validators.validate_port_range("invalid-service")
        assert not vyos_validators.validate_port_range("notaservice")
        assert not vyos_validators.validate_port_range("")


class TestPortMultiValidation:
    """Test comma-separated port list validation."""

    def test_valid_port_multi(self):
        assert vyos_validators.validate_port_multi("80,443")
        assert vyos_validators.validate_port_multi("53,67-68")
        assert vyos_validators.validate_port_multi("!22,80,443")
        assert vyos_validators.validate_port_multi("http,https")
        assert vyos_validators.validate_port_multi("imap,imaps,smtp,smtps,pop3,pop3s,587")

    def test_invalid_port_multi(self):
        assert not vyos_validators.validate_port_multi("80,")
        assert not vyos_validators.validate_port_multi(",443")
        assert not vyos_validators.validate_port_multi("80,99999")
        assert not vyos_validators.validate_port_multi("80,not-a-service")


class TestBinaryDiscovery:
    """Test binary discovery mechanism."""

    def test_init_binaries_runs(self):
        """Binary initialization should run without error."""
        # This is already called on module import, but test it explicitly
        vyos_validators._init_binaries()
        # No assertion needed - just checking it doesn't crash

    def test_binary_paths_set(self):
        """Binary paths should be set (or None if not found)."""
        # After initialization, the globals should be set
        assert vyos_validators._STATE["binaries_checked"] is True
        # Binary paths will be None on macOS without building,
        # which is expected and handled by fallbacks


class TestServicesParsing:
    """Test /etc/services parser used by port fallback."""

    def test_parse_services_text(self):
        text = (
            "smtp 25/tcp mail\n"
            "submission 587/tcp\n"
            "imaps 993/tcp imap4-ssl\n"
            "# comment\n"
        )
        parsed = vyos_validators._parse_services_text(text)
        assert "smtp" in parsed
        assert "mail" in parsed
        assert "submission" in parsed
        assert "imaps" in parsed
        assert "imap4-ssl" in parsed
