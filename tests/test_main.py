"""Tests for main entry point."""

import json
from io import StringIO
from unittest.mock import patch

from tests.conftest import (
    MINIMAL_ACCEPT_CONFIG,
    MINIMAL_DROP_WITH_DNS_RULE_CONFIG,
    MINIMAL_DROP_WITH_GROUP_RULE_CONFIG,
    MINIMAL_DROP_WITH_HTTP_RULE_CONFIG,
    MINIMAL_DROP_WITH_RULE_CONFIG,
    MINIMAL_INPUT_ICMP_CONFIG,
    MINIMAL_STATE_POLICY_CONFIG,
)
from vyfwmatch.main import main


class TestMainFunction:
    """Test the main() function."""

    def test_main_with_valid_config(self, tmp_path):
        """Test main with a valid configuration."""
        # Create a minimal config file
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action accept
                rule 10 {
                    action accept
                    protocol tcp
                    destination {
                        port 443
                    }
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        # Test successful execution
        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
            "--port",
            "443",
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ret = main(argv)

        assert ret == 0
        output = mock_stdout.getvalue()
        assert "Policy Match Result" in output

    def test_main_config_file_not_found(self):
        """Test main with non-existent config file."""
        argv = [
            "--config",
            "/nonexistent/config.boot",
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
        ]

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            ret = main(argv)

        assert ret == 1
        assert "Error: Config file not found" in mock_stderr.getvalue()

    def test_main_invalid_config_file(self, tmp_path):
        """Test main with invalid/corrupted config file."""
        config_file = tmp_path / "config.boot"
        # Write completely empty content
        config_file.write_text("")

        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
        ]

        # Empty config should still work, just with no rules
        with patch("sys.stdout", new_callable=StringIO):
            ret = main(argv)

        # Should succeed but with default action
        assert ret == 0

    def test_main_json_output(self, tmp_path):
        """Test main with JSON output format."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_WITH_RULE_CONFIG)

        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
            "--format",
            "json",
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ret = main(argv)

        assert ret == 0
        output = mock_stdout.getvalue()
        # Should be valid JSON
        data = json.loads(output)
        assert "matched" in data
        assert "action" in data
        assert "chain" in data

    def test_main_with_state_policy(self, tmp_path):
        """Test main with global state policy."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_STATE_POLICY_CONFIG)

        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
            "--state",
            "established",
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ret = main(argv)

        assert ret == 0
        output = mock_stdout.getvalue()
        assert "State Policy" in output or "established" in output

    def test_main_with_hook(self, tmp_path):
        """Test main with specific hook."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_INPUT_ICMP_CONFIG)

        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "icmp",
            "--hook",
            "input",
        ]

        with patch("sys.stdout", new_callable=StringIO):
            ret = main(argv)

        assert ret == 0

    def test_main_with_all_options(self, tmp_path):
        """Test main with all CLI options specified."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_WITH_GROUP_RULE_CONFIG)

        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--outbound-interface",
            "eth1",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
            "--port",
            "443",
            "--state",
            "new",
            "--hook",
            "forward",
            "--format",
            "table",
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ret = main(argv)

        assert ret == 0
        output = mock_stdout.getvalue()
        assert "Policy Match Result" in output

    def test_main_default_action_result(self, tmp_path):
        """Test main when default action is returned."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_WITH_DNS_RULE_CONFIG)

        # Traffic that doesn't match any rule should get default action
        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--protocol",
            "tcp",
            "--port",
            "80",
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            ret = main(argv)

        assert ret == 0
        output = mock_stdout.getvalue()
        assert "Default Action" in output or "drop" in output.lower()

    def test_main_no_argv(self, tmp_path):
        """Test main() when called from __main__ block (argv=None)."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_ACCEPT_CONFIG)

        # Simulate command line args via sys.argv
        with patch(
            "sys.argv",
            [
                "vyfwmatch",
                "--config",
                str(config_file),
                "--inbound-interface",
                "eth0",
                "--source",
                "10.0.0.1",
                "--destination",
                "192.168.1.1",
                "--protocol",
                "tcp",
            ],
        ):
            with patch("sys.stdout", new_callable=StringIO):
                ret = main(argv=None)

        assert ret == 0

    def test_main_service_resolution(self, tmp_path):
        """Test main with service name instead of port."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_WITH_HTTP_RULE_CONFIG)

        argv = [
            "--config",
            str(config_file),
            "--inbound-interface",
            "eth0",
            "--source",
            "10.0.0.1",
            "--destination",
            "192.168.1.1",
            "--service",
            "http",
        ]

        with patch("sys.stdout", new_callable=StringIO):
            ret = main(argv)

        assert ret == 0
