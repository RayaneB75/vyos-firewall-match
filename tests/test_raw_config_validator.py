"""Tests for raw firewall configuration validator."""

from vyfwmatch.services.raw_config_validator import (
    ConfigValidationError,
    RawConfigValidator,
)


def test_valid_minimal_config_passes() -> None:
    """A minimal valid config should pass validation."""
    config = {
        "group": {
            "network-group": {
                "INSIDE": {"network": ["10.0.0.0/8"]},
            },
            "interface-group": {
                "WAN": {"interface": ["eth0"]},
            },
        },
        "ipv4": {
            "forward": {
                "filter": {
                    "default-action": "drop",
                    "rule": {
                        "10": {
                            "action": "accept",
                            "protocol": "tcp",
                            "destination": {"port": "443"},
                        }
                    },
                }
            },
            "CONN_FILTER": {
                "default-action": "return",
                "rule": {
                    "10": {
                        "action": "accept",
                        "state": {"established": {}, "related": {}},
                    }
                },
            },
        },
    }

    validator = RawConfigValidator()
    validator.validate(config)


def test_invalid_values_collect_multiple_errors() -> None:
    """Validator should collect all errors before raising."""
    config = {
        "group": {
            "network-group": {
                "BAD_NET": {"network": ["10.0.0.0/99"]},
            },
            "port-group": {
                "BAD_PORTS": {"port": ["70000"]},
            },
            "interface-group": {
                "EMPTY_IFACE": {"interface": []},
            },
        },
        "ipv4": {
            "forward": {
                "filter": {
                    "default-action": "invalid-action",
                    "rule": {
                        "10": {
                            "action": "jump",
                            "protocol": "notaprotocol",
                            "jump-target": "MISSING_CHAIN",
                            "source": {"address": "300.1.1.1"},
                            "destination": {"port": "99999"},
                        }
                    },
                }
            }
        },
    }

    validator = RawConfigValidator()

    try:
        validator.validate(config)
        assert False, "Expected ConfigValidationError"
    except ConfigValidationError as exc:
        assert len(exc.errors) >= 6
        messages = [error.message for error in exc.errors]
        assert any("Invalid network prefix" in msg for msg in messages)
        assert any("Invalid port" in msg for msg in messages)
        assert any("Invalid action" in msg for msg in messages)
        assert any("Invalid protocol" in msg for msg in messages)
        assert any("Jump target" in msg for msg in messages)


def test_jump_action_requires_jump_target() -> None:
    """Jump action without jump-target should fail."""
    config = {
        "ipv4": {
            "forward": {
                "filter": {
                    "rule": {
                        "10": {
                            "action": "jump",
                        }
                    }
                }
            }
        }
    }

    validator = RawConfigValidator()

    try:
        validator.validate(config)
        assert False, "Expected ConfigValidationError"
    except ConfigValidationError as exc:
        messages = [error.message for error in exc.errors]
        assert any("requires jump-target" in msg for msg in messages)


def test_valid_ipv6_rules_pass() -> None:
    """A valid IPv6 config should pass validation."""
    config = {
        "ipv6": {
            "input": {
                "filter": {
                    "default-action": "drop",
                    "rule": {
                        "10": {
                            "action": "accept",
                            "protocol": "icmpv6",
                            "source": {"address": "2001:db8::/32"},
                        }
                    },
                }
            }
        }
    }

    validator = RawConfigValidator()
    validator.validate(config)


def test_port_multi_and_trimmed_address_pass() -> None:
    """Validator accepts port-multi and trims accidental whitespace."""
    config = {
        "group": {
            "network-group": {
                "TEST": {"network": ["10.4.13.6/32"]},
            }
        },
        "ipv4": {
            "forward": {
                "filter": {
                    "rule": {
                        "10": {
                            "action": "accept",
                            "destination": {"port": "80,443"},
                            "source": {"address": "89.234.162.249 "},
                        }
                    }
                }
            }
        },
    }

    validator = RawConfigValidator()
    validator.validate(config)
