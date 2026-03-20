"""Shared test fixtures with real VyOS configuration examples.

All configurations are based on examples from the official VyOS documentation
(https://docs.vyos.io/en/latest/configuration/firewall/).
"""

from __future__ import annotations

import pytest

from vyfwmatch.services.decision_engine import DecisionEngine
from vyfwmatch.domain.models import TrafficTuple, FirewallConfig, MatchResult
from vyfwmatch.adapters.config_parser import parse_config
from vyfwmatch.services.rule_loader import RuleLoaderService
from vyfwmatch.adapters.vyos_config import VyOSConfigAdapter
import tempfile
import os


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def build_config(text: str) -> FirewallConfig:
    """Parse config text and extract firewall config in one step."""
    # Write config text to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.boot', delete=False) as f:
        f.write(text)
        temp_path = f.name
    
    try:
        # Use the VyOSConfigAdapter and RuleLoaderService
        adapter = VyOSConfigAdapter(temp_path)
        loader = RuleLoaderService(adapter)
        return loader.load_firewall_config()
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def match_traffic(config: FirewallConfig, **kwargs) -> MatchResult:
    """Build a traffic tuple and run the matching engine."""
    traffic = TrafficTuple(**kwargs)
    engine = DecisionEngine(config)
    return engine.match(traffic)


# ---------------------------------------------------------------------------
# Fixture: Quick-Start Home/Small Office Gateway
# From: https://docs.vyos.io/en/latest/quick-start.html
# ---------------------------------------------------------------------------


QUICKSTART_CONFIG = """\
firewall {
    global-options {
        state-policy {
            established {
                action accept
            }
            related {
                action accept
            }
            invalid {
                action drop
            }
        }
    }
    group {
        interface-group WAN {
            interface eth0
        }
        interface-group LAN {
            interface eth1
        }
        network-group NET-INSIDE-v4 {
            network 192.168.0.0/24
        }
    }
    ipv4 {
        forward {
            filter {
                default-action accept
                rule 10 {
                    action jump
                    jump-target CONN_FILTER
                }
                rule 100 {
                    action jump
                    jump-target OUTSIDE-IN
                    inbound-interface {
                        group WAN
                    }
                    destination {
                        group {
                            network-group NET-INSIDE-v4
                        }
                    }
                }
            }
        }
        input {
            filter {
                default-action drop
                rule 10 {
                    action jump
                    jump-target CONN_FILTER
                }
                rule 20 {
                    action jump
                    jump-target VyOS_MANAGEMENT
                    destination {
                        port 22
                    }
                    protocol tcp
                }
                rule 30 {
                    action accept
                    icmp {
                        type-name echo-request
                    }
                    protocol icmp
                    state {
                        new
                    }
                }
                rule 40 {
                    action accept
                    destination {
                        port 53
                    }
                    protocol tcp_udp
                    source {
                        group {
                            network-group NET-INSIDE-v4
                        }
                    }
                }
                rule 50 {
                    action accept
                    source {
                        address 127.0.0.0/8
                    }
                }
            }
        }
        name CONN_FILTER {
            default-action return
            rule 10 {
                action accept
                state {
                    established
                    related
                }
            }
            rule 20 {
                action drop
                state {
                    invalid
                }
            }
        }
        name OUTSIDE-IN {
            default-action drop
        }
        name VyOS_MANAGEMENT {
            default-action return
            rule 15 {
                action accept
                inbound-interface {
                    group LAN
                }
            }
            rule 20 {
                action drop
                recent {
                    count 4
                    time minute
                }
                state {
                    new
                }
                inbound-interface {
                    group WAN
                }
            }
            rule 21 {
                action accept
                state {
                    new
                }
                inbound-interface {
                    group WAN
                }
            }
        }
    }
}
"""


# ---------------------------------------------------------------------------
# Fixture: Groups with Address/Network/Port/Interface
# From: https://docs.vyos.io/en/latest/configuration/firewall/groups.html
# ---------------------------------------------------------------------------


GROUPS_CONFIG = """\
firewall {
    group {
        address-group SERVERS {
            address 198.51.100.101
            address 198.51.100.102
        }
        address-group ADR-INSIDE-v4 {
            address 192.168.0.1
            address 10.0.0.1-10.0.0.8
        }
        network-group TRUSTEDv4 {
            network 192.0.2.0/30
            network 203.0.113.128/25
        }
        network-group NET-INSIDE-v4 {
            network 192.168.0.0/24
            network 192.168.1.0/24
        }
        interface-group LAN {
            interface eth2.2001
            interface bon0
            interface eth3
        }
        port-group PORT-TCP-SERVER1 {
            port http
            port 443
            port 5000-5010
        }
        ipv6-network-group TRUSTEDv6 {
            network 2001:db8::/64
        }
    }
    ipv4 {
        output {
            filter {
                default-action accept
                rule 10 {
                    action accept
                    outbound-interface {
                        group !LAN
                    }
                }
            }
        }
        forward {
            filter {
                default-action drop
                rule 20 {
                    action accept
                    source {
                        group {
                            network-group TRUSTEDv4
                        }
                    }
                }
                rule 30 {
                    action accept
                    destination {
                        group {
                            address-group SERVERS
                        }
                    }
                    destination {
                        port 443
                    }
                    protocol tcp
                }
                rule 40 {
                    action accept
                    destination {
                        group {
                            port-group PORT-TCP-SERVER1
                        }
                    }
                    protocol tcp
                    source {
                        group {
                            network-group NET-INSIDE-v4
                        }
                    }
                }
            }
        }
    }
    ipv6 {
        input {
            filter {
                default-action drop
                rule 10 {
                    action accept
                    source {
                        group {
                            network-group TRUSTEDv6
                        }
                    }
                }
            }
        }
    }
}
"""


# ---------------------------------------------------------------------------
# Fixture: Zone-Based Firewall (LAN / WAN / LOCAL)
# From: https://docs.vyos.io/en/latest/configuration/firewall/zone.html
# ---------------------------------------------------------------------------


ZONE_CONFIG = """\
firewall {
    ipv4 {
        name WAN-LAN-v4 {
            default-action drop
            rule 10 {
                action accept
                state {
                    established
                    related
                }
            }
            rule 20 {
                action drop
                state {
                    invalid
                }
            }
        }
        name LAN-WAN-v4 {
            default-action accept
            rule 10 {
                action accept
                state {
                    established
                    related
                }
            }
            rule 20 {
                action drop
                state {
                    invalid
                }
            }
        }
        name LAN-LOCAL-v4 {
            default-action drop
            rule 10 {
                action accept
                state {
                    established
                    related
                }
            }
            rule 20 {
                action accept
                protocol icmp
            }
            rule 30 {
                action accept
                destination {
                    port 22
                }
                protocol tcp
            }
        }
        name WAN-LOCAL-v4 {
            default-action drop
            rule 10 {
                action accept
                state {
                    established
                    related
                }
            }
            rule 20 {
                action drop
                state {
                    invalid
                }
            }
        }
        name LOCAL-WAN-v4 {
            default-action accept
        }
    }
    ipv6 {
        name WAN-LOCAL-v6 {
            default-action drop
            rule 10 {
                action accept
                state {
                    established
                    related
                }
            }
            rule 20 {
                action accept
                protocol icmpv6
            }
            rule 30 {
                action drop
                state {
                    invalid
                }
            }
        }
    }
}
"""


# ---------------------------------------------------------------------------
# Fixture: Detailed matching — address ranges, disabled rules, negation
# From: https://docs.vyos.io/en/latest/configuration/firewall/ipv4.html
# ---------------------------------------------------------------------------


DETAILED_CONFIG = """\
firewall {
    group {
        network-group INTERNAL {
            network 10.0.0.0/8
            network 172.16.0.0/12
            network 192.168.0.0/16
        }
        port-group WEBPORTS {
            port 80
            port 443
            port 8080-8090
        }
        interface-group TRUSTED {
            interface eth1
            interface eth2
        }
    }
    ipv4 {
        forward {
            filter {
                default-action drop
                rule 5 {
                    action accept
                    state {
                        established
                        related
                    }
                }
                rule 10 {
                    action drop
                    state {
                        invalid
                    }
                }
                rule 50 {
                    action accept
                    source {
                        address 192.0.2.10-192.0.2.20
                    }
                    protocol tcp
                    destination {
                        port 443
                    }
                }
                rule 60 {
                    action accept
                    source {
                        group {
                            network-group INTERNAL
                        }
                    }
                    destination {
                        group {
                            port-group WEBPORTS
                        }
                    }
                    protocol tcp
                }
                rule 70 {
                    action drop
                    source {
                        address !10.0.0.0/8
                    }
                    description "Drop traffic not from 10.0.0.0/8"
                }
                rule 80 {
                    action accept
                    protocol icmp
                }
                rule 100 {
                    action drop
                    description "Disabled catch-all"
                    disable
                }
            }
        }
        input {
            filter {
                default-action drop
                rule 10 {
                    action accept
                    inbound-interface {
                        group TRUSTED
                    }
                    protocol tcp
                    destination {
                        port 22
                    }
                }
                rule 20 {
                    action accept
                    protocol icmp
                }
            }
        }
    }
    ipv6 {
        forward {
            filter {
                default-action drop
                rule 10 {
                    action accept
                    state {
                        established
                        related
                    }
                }
                rule 20 {
                    action accept
                    protocol icmpv6
                }
                rule 30 {
                    action accept
                    source {
                        address 2001:db8::/32
                    }
                    destination {
                        port 443
                    }
                    protocol tcp
                }
            }
        }
    }
}
"""


# ---------------------------------------------------------------------------
# Pytest fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def quickstart_config() -> FirewallConfig:
    return build_config(QUICKSTART_CONFIG)


@pytest.fixture
def groups_config() -> FirewallConfig:
    return build_config(GROUPS_CONFIG)


@pytest.fixture
def zone_config() -> FirewallConfig:
    return build_config(ZONE_CONFIG)


@pytest.fixture
def detailed_config() -> FirewallConfig:
    return build_config(DETAILED_CONFIG)
