"""Tests for CLI argument parsing and validation."""

from __future__ import annotations

import pytest

from vyfwmatch.cli.argument_parser import parse_args


class TestRequiredArgs:
    def test_all_required_args(self):
        """Valid invocation with all required args."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
        ])
        assert args.config == "config.boot"
        assert args.inbound_interface == "eth0"
        assert args.source == "10.0.0.1"
        assert args.destination == "192.168.0.10"
        assert args.resolved_port == 443
        assert args.resolved_protocol == "tcp"

    def test_missing_inbound_interface(self):
        """Error when --inbound-interface is omitted."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--service", "443",
            ])

    def test_missing_source(self):
        """Error when --source is omitted."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--destination", "192.168.0.10",
                "--service", "443",
            ])

    def test_missing_destination(self):
        """Error when --destination is omitted."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--service", "443",
            ])

    def test_missing_config(self):
        """Error when --config is omitted."""
        with pytest.raises(SystemExit):
            parse_args([
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--service", "443",
            ])

    def test_source_must_be_ip(self):
        """Error when --source is an FQDN."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "example.com",
                "--destination", "192.168.0.10",
                "--service", "443",
                "--protocol", "tcp",
            ])

    def test_destination_must_be_ip(self):
        """Error when --destination is an FQDN."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "example.com",
                "--service", "443",
                "--protocol", "tcp",
            ])


class TestServiceProtocolValidation:
    def test_missing_service_and_protocol(self):
        """Error when neither --service nor --protocol is given."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
            ])

    def test_service_only_resolves_protocol(self):
        """--service=http without --protocol → protocol auto-resolved to tcp."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "http",
        ])
        assert args.resolved_port == 80
        assert args.resolved_protocol == "tcp"

    def test_service_dns_resolves_udp(self):
        """--service=dns without --protocol → protocol auto-resolved to udp."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "dns",
        ])
        assert args.resolved_port == 53
        assert args.resolved_protocol == "udp"

    def test_protocol_only(self):
        """--protocol=icmp without --service → valid, no port."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--protocol", "icmp",
        ])
        assert args.resolved_protocol == "icmp"
        assert args.resolved_port is None

    def test_protocol_and_port(self):
        """--protocol=tcp with --port=443 is valid."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--protocol", "tcp",
            "--port", "443",
        ])
        assert args.resolved_protocol == "tcp"
        assert args.resolved_port == 443

    def test_port_requires_protocol(self):
        """--port without --protocol should error."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--port", "443",
            ])

    def test_both_service_and_protocol(self):
        """Both --service=443 and --protocol=tcp → valid."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
        ])
        assert args.resolved_port == 443
        assert args.resolved_protocol == "tcp"

    def test_service_numeric_no_protocol_resolution(self):
        """--service=8080 (numeric) → port resolved, no protocol auto-set."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "8080",
            "--protocol", "tcp",
        ])
        assert args.resolved_port == 8080
        assert args.resolved_protocol == "tcp"

    def test_service_and_port_mutually_exclusive(self):
        """--service and --port cannot be used together."""
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--service", "https",
                "--port", "443",
                "--protocol", "tcp",
            ])


class TestOutputFormat:
    def test_format_table(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
            "--format", "table",
        ])
        assert args.output_format == "table"

    def test_format_json(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
            "--format", "json",
        ])
        assert args.output_format == "json"

    def test_invalid_format(self):
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--service", "443",
                "--format", "xml",
            ])

    def test_default_format_is_table(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
        ])
        assert args.output_format == "table"


class TestOptionalArgs:
    def test_outbound_interface(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--outbound-interface", "eth1",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
        ])
        assert args.outbound_interface == "eth1"

    def test_no_outbound_interface(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--protocol", "icmp",
        ])
        assert args.outbound_interface is None

    def test_state_argument(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--protocol", "tcp",
            "--service", "80",
            "--state", "new",
        ])
        assert args.state == "new"

    def test_state_established(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--protocol", "tcp",
            "--service", "80",
            "--state", "established",
        ])
        assert args.state == "established"

    def test_invalid_port(self):
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--protocol", "tcp",
                "--port", "0",
            ])

    def test_port_out_of_range(self):
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--protocol", "tcp",
                "--port", "70000",
            ])

    def test_invalid_state(self):
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--protocol", "tcp",
                "--service", "80",
                "--state", "bogus",
            ])


class TestHookArgument:
    def test_hook_forward(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
            "--hook", "forward",
        ])
        assert args.hook == "forward"

    def test_hook_input(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
            "--hook", "input",
        ])
        assert args.hook == "input"

    def test_hook_output(self):
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
            "--hook", "output",
        ])
        assert args.hook == "output"

    def test_hook_default_none(self):
        """When --hook is not specified, it defaults to None."""
        args = parse_args([
            "--config", "config.boot",
            "--inbound-interface", "eth0",
            "--source", "10.0.0.1",
            "--destination", "192.168.0.10",
            "--service", "443",
            "--protocol", "tcp",
        ])
        assert args.hook is None

    def test_invalid_hook(self):
        with pytest.raises(SystemExit):
            parse_args([
                "--config", "config.boot",
                "--inbound-interface", "eth0",
                "--source", "10.0.0.1",
                "--destination", "192.168.0.10",
                "--service", "443",
                "--protocol", "tcp",
                "--hook", "prerouting",
            ])
