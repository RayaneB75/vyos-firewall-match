"""Tests for the VyOS hierarchical boot config parser."""

from __future__ import annotations

import pytest

from vyfwmatch.adapters.config_parser import parse_config


class TestParseEmpty:
    def test_empty_string(self):
        assert parse_config("") == {}

    def test_whitespace_only(self):
        assert parse_config("   \n\n  \t  ") == {}


class TestParseSingleNode:
    def test_single_empty_block(self):
        result = parse_config("firewall { }")
        assert result == {"firewall": {}}

    def test_single_leaf(self):
        result = parse_config("hostname router1")
        assert result == {"hostname": "router1"}


class TestParseNestedNodes:
    def test_two_levels(self):
        config = """\
        firewall {
            ipv4 {
            }
        }
        """
        result = parse_config(config)
        assert result == {"firewall": {"ipv4": {}}}

    def test_three_levels(self):
        config = """\
        firewall {
            ipv4 {
                forward {
                    filter {
                        default-action accept
                    }
                }
            }
        }
        """
        result = parse_config(config)
        assert result["firewall"]["ipv4"]["forward"]["filter"]["default-action"] == "accept"

    def test_sibling_blocks(self):
        config = """\
        firewall {
            ipv4 {
            }
            ipv6 {
            }
        }
        """
        result = parse_config(config)
        assert "ipv4" in result["firewall"]
        assert "ipv6" in result["firewall"]


class TestParseTagNodes:
    def test_rule_tag_node(self):
        config = """\
        rule 10 {
            action drop
        }
        """
        result = parse_config(config)
        assert result == {"rule": {"10": {"action": "drop"}}}

    def test_multiple_tag_nodes(self):
        config = """\
        rule 10 {
            action drop
        }
        rule 20 {
            action accept
        }
        """
        result = parse_config(config)
        assert result["rule"]["10"]["action"] == "drop"
        assert result["rule"]["20"]["action"] == "accept"

    def test_named_chain(self):
        config = """\
        name CONN_FILTER {
            default-action return
            rule 10 {
                action accept
            }
        }
        """
        result = parse_config(config)
        assert result["name"]["CONN_FILTER"]["default-action"] == "return"
        assert result["name"]["CONN_FILTER"]["rule"]["10"]["action"] == "accept"


class TestParseMultiValueLeaves:
    def test_repeated_address(self):
        config = """\
        address-group SERVERS {
            address 198.51.100.101
            address 198.51.100.102
        }
        """
        result = parse_config(config)
        addrs = result["address-group"]["SERVERS"]["address"]
        assert isinstance(addrs, list)
        assert "198.51.100.101" in addrs
        assert "198.51.100.102" in addrs

    def test_repeated_network(self):
        config = """\
        network-group NET {
            network 192.168.0.0/24
            network 192.168.1.0/24
        }
        """
        result = parse_config(config)
        nets = result["network-group"]["NET"]["network"]
        assert isinstance(nets, list)
        assert len(nets) == 2

    def test_repeated_interface(self):
        config = """\
        interface-group LAN {
            interface eth1
            interface eth2
            interface eth3
        }
        """
        result = parse_config(config)
        ifaces = result["interface-group"]["LAN"]["interface"]
        assert isinstance(ifaces, list)
        assert len(ifaces) == 3


class TestParseQuotedValues:
    def test_single_quoted(self):
        result = parse_config("network '192.168.0.0/24'")
        assert result["network"] == "192.168.0.0/24"

    def test_double_quoted(self):
        result = parse_config('description "My firewall rule"')
        assert result["description"] == "My firewall rule"


class TestParseValuelessNodes:
    def test_state_valueless(self):
        config = """\
        state {
            established
            related
        }
        """
        result = parse_config(config)
        assert "established" in result["state"]
        assert "related" in result["state"]

    def test_disable_flag(self):
        config = """\
        rule 10 {
            action drop
            disable
        }
        """
        result = parse_config(config)
        assert "disable" in result["rule"]["10"]


class TestParseComments:
    def test_line_comments_stripped(self):
        config = """\
        // This is a comment
        firewall {
            // Another comment
            ipv4 {
            }
        }
        """
        result = parse_config(config)
        assert result == {"firewall": {"ipv4": {}}}

    def test_hash_comments_stripped(self):
        config = """\
        # Comment
        hostname router1
        """
        result = parse_config(config)
        assert result == {"hostname": "router1"}


class TestParseFullQuickstart:
    """Parse the full quickstart config and validate structure."""

    def test_parse_structure(self):
        from tests.conftest import QUICKSTART_CONFIG

        result = parse_config(QUICKSTART_CONFIG)
        fw = result["firewall"]

        # Global options
        assert "global-options" in fw
        sp = fw["global-options"]["state-policy"]
        assert sp["established"]["action"] == "accept"
        assert sp["invalid"]["action"] == "drop"

        # Groups
        assert "group" in fw
        assert "WAN" in fw["group"]["interface-group"]
        assert "LAN" in fw["group"]["interface-group"]

        # IPv4 forward
        forward = fw["ipv4"]["forward"]["filter"]
        assert "rule" in forward
        assert "10" in forward["rule"]
        assert forward["rule"]["10"]["action"] == "jump"

        # Named chains
        assert "CONN_FILTER" in fw["ipv4"]["name"]
        assert "OUTSIDE-IN" in fw["ipv4"]["name"]
        assert "VyOS_MANAGEMENT" in fw["ipv4"]["name"]
