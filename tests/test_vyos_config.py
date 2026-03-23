"""Tests for VyOS configuration adapter."""

import pytest

from tests.conftest import MINIMAL_DROP_CONFIG, MINIMAL_DROP_WITH_SIMPLE_RULE_CONFIG
from vyfwmatch.adapters.vyos_config import VyOSConfigAdapter


# pylint: disable=too-many-public-methods,protected-access
class TestVyOSConfigAdapter:
    """Test VyOSConfigAdapter class."""

    def test_init_with_valid_config(self, tmp_path):
        """Test initialization with valid config file."""
        config_content = """\
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
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        assert adapter.config_path == str(config_file)
        assert adapter._config_tree is not None

    def test_init_with_nonexistent_file(self):
        """Test initialization with non-existent file."""
        with pytest.raises(FileNotFoundError) as exc_info:
            VyOSConfigAdapter("/nonexistent/config.boot")

        assert "Config file not found" in str(exc_info.value)

    def test_init_with_invalid_config(self, tmp_path):
        """Test initialization with empty config."""
        config_file = tmp_path / "config.boot"
        config_file.write_text("")

        # Empty config should work (just has no firewall rules)
        adapter = VyOSConfigAdapter(str(config_file))
        assert adapter._config_tree is not None

    def test_get_firewall_config(self, tmp_path):
        """Test getting firewall config."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
    ipv6 {
        input {
            filter {
                default-action accept
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        fw_config = adapter.get_firewall_config()

        assert isinstance(fw_config, dict)
        assert "ipv4" in fw_config
        assert "ipv6" in fw_config

    def test_get_firewall_config_empty(self, tmp_path):
        """Test getting firewall config when none exists."""
        config_content = """\
interfaces {
    ethernet eth0 {
        address 192.168.1.1/24
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        fw_config = adapter.get_firewall_config()

        assert isinstance(fw_config, dict)
        assert len(fw_config) == 0

    def test_get_subtree_simple_path(self, tmp_path):
        """Test getting a subtree with simple path."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_CONFIG)

        adapter = VyOSConfigAdapter(str(config_file))
        subtree = adapter.get_subtree(["firewall", "ipv4"])

        assert subtree is not None
        assert "forward" in subtree

    def test_get_subtree_deep_path(self, tmp_path):
        """Test getting a subtree with deep path."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_WITH_SIMPLE_RULE_CONFIG)

        adapter = VyOSConfigAdapter(str(config_file))
        subtree = adapter.get_subtree(
            ["firewall", "ipv4", "forward", "filter", "rule", "10"]
        )

        assert subtree is not None
        assert "action" in subtree

    def test_get_subtree_nonexistent_path(self, tmp_path):
        """Test getting a subtree for non-existent path."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_CONFIG)

        adapter = VyOSConfigAdapter(str(config_file))
        subtree = adapter.get_subtree(["firewall", "ipv6", "input"])

        assert subtree is None

    def test_get_subtree_invalid_intermediate(self, tmp_path):
        """Test getting a subtree when intermediate path is not a dict."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_CONFIG)

        adapter = VyOSConfigAdapter(str(config_file))
        # Try to traverse through a leaf value
        subtree = adapter.get_subtree(
            ["firewall", "ipv4", "forward", "filter", "default-action", "something"]
        )

        assert subtree is None

    def test_exists_true(self, tmp_path):
        """Test exists() when path exists."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        assert adapter.exists(["firewall", "ipv4", "forward"])
        assert adapter.exists(["firewall", "ipv4", "forward", "filter"])

    def test_exists_false(self, tmp_path):
        """Test exists() when path doesn't exist."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        assert not adapter.exists(["firewall", "ipv6"])
        assert not adapter.exists(["firewall", "ipv4", "input"])

    def test_list_nodes(self, tmp_path):
        """Test listing child nodes."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
        input {
            filter {
                default-action accept
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        nodes = adapter.list_nodes(["firewall", "ipv4"])

        assert "forward" in nodes
        assert "input" in nodes
        assert len(nodes) == 2

    def test_list_nodes_empty(self, tmp_path):
        """Test listing nodes when path doesn't exist."""
        config_file = tmp_path / "config.boot"
        config_file.write_text(MINIMAL_DROP_CONFIG)

        adapter = VyOSConfigAdapter(str(config_file))
        nodes = adapter.list_nodes(["firewall", "ipv6"])

        assert not nodes

    def test_list_nodes_not_dict(self, tmp_path):
        """Test listing nodes when path points to non-dict."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        nodes = adapter.list_nodes(
            ["firewall", "ipv4", "forward", "filter", "default-action"]
        )

        assert not nodes

    def test_return_value_string(self, tmp_path):
        """Test return_value() for string value."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        value = adapter.return_value(
            ["firewall", "ipv4", "forward", "filter", "default-action"]
        )

        assert value == "drop"

    def test_return_value_none(self, tmp_path):
        """Test return_value() when path doesn't exist."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        value = adapter.return_value(["firewall", "ipv6", "input"])

        assert value is None

    def test_return_value_list(self, tmp_path):
        """Test return_value() for list value (returns first item)."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    state established
                    state related
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        value = adapter.return_value(
            ["firewall", "ipv4", "forward", "filter", "rule", "10", "state"]
        )

        # Should return first item from list
        assert value == "established"

    def test_return_value_empty_list(self, tmp_path):
        """Test return_value() for empty list."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    state
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        value = adapter.return_value(
            ["firewall", "ipv4", "forward", "filter", "rule", "10", "state"]
        )

        assert value is None

    def test_return_value_dict(self, tmp_path):
        """Test return_value() for dict (should return None)."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    action accept
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        value = adapter.return_value(
            ["firewall", "ipv4", "forward", "filter", "rule", "10"]
        )

        # Should return None for dict
        assert value is None

    def test_return_values_list(self, tmp_path):
        """Test return_values() for list."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    state established
                    state related
                    state new
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        values = adapter.return_values(
            ["firewall", "ipv4", "forward", "filter", "rule", "10", "state"]
        )

        assert isinstance(values, list)
        assert "established" in values
        assert "related" in values
        assert "new" in values

    def test_return_values_string(self, tmp_path):
        """Test return_values() for string (returns single-item list)."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        values = adapter.return_values(
            ["firewall", "ipv4", "forward", "filter", "default-action"]
        )

        assert values == ["drop"]

    def test_return_values_none(self, tmp_path):
        """Test return_values() when path doesn't exist."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                default-action drop
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        values = adapter.return_values(["firewall", "ipv6", "input"])

        assert values == []

    def test_return_values_dict(self, tmp_path):
        """Test return_values() for dict (returns empty list)."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    action accept
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        values = adapter.return_values(
            ["firewall", "ipv4", "forward", "filter", "rule", "10"]
        )

        assert values == []

    def test_return_value_empty_string(self, tmp_path):
        """Test return_value() for empty string."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    disable
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        value = adapter.return_value(
            ["firewall", "ipv4", "forward", "filter", "rule", "10", "disable"]
        )

        # Empty string should return None
        assert value is None

    def test_return_values_empty_string(self, tmp_path):
        """Test return_values() for empty string."""
        config_content = """\
firewall {
    ipv4 {
        forward {
            filter {
                rule 10 {
                    disable
                }
            }
        }
    }
}
"""
        config_file = tmp_path / "config.boot"
        config_file.write_text(config_content)

        adapter = VyOSConfigAdapter(str(config_file))
        values = adapter.return_values(
            ["firewall", "ipv4", "forward", "filter", "rule", "10", "disable"]
        )

        # Empty string should return empty list
        assert values == []
