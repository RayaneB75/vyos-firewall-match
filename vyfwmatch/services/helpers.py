"""Matching utility functions for IP addresses, ports, interfaces, and services.

All functions here are pure and operate on primitive types (strings, ints).
They handle negation (! prefix), wildcards, ranges, and CIDR notation.

This module provides IP and protocol matching utilities using original VyOS
implementations from vyos-1x.
"""

import fnmatch
import ipaddress
import socket
from typing import Optional

from vyfwmatch.adapters.vyos_utils import is_ipv4, is_ipv6

# Re-export VyOS functions for use by other modules
__all__ = [
    "is_ipv4",
    "is_ipv6",
    "resolve_service",
    "is_negated",
    "protocol_matches",
    "port_matches",
    "ip_matches",
    "ip_matches_with_mask",
    "interface_matches",
]


# ---------------------------------------------------------------------------
# Well-known service name → (port, protocol) mapping
# ---------------------------------------------------------------------------

_SERVICE_MAP: dict[str, tuple[int, str]] = {
    "http": (80, "tcp"),
    "https": (443, "tcp"),
    "ssh": (22, "tcp"),
    "telnet": (23, "tcp"),
    "ftp": (21, "tcp"),
    "ftp-data": (20, "tcp"),
    "smtp": (25, "tcp"),
    "dns": (53, "udp"),
    "domain": (53, "udp"),
    "dhcp": (67, "udp"),
    "bootps": (67, "udp"),
    "bootpc": (68, "udp"),
    "tftp": (69, "udp"),
    "pop3": (110, "tcp"),
    "ntp": (123, "udp"),
    "imap": (143, "tcp"),
    "snmp": (161, "udp"),
    "ldap": (389, "tcp"),
    "syslog": (514, "udp"),
    "rtsp": (554, "tcp"),
    "imaps": (993, "tcp"),
    "pop3s": (995, "tcp"),
    "openvpn": (1194, "udp"),
    "l2tp": (1701, "udp"),
    "pptp": (1723, "tcp"),
    "nfs": (2049, "tcp"),
    "mysql": (3306, "tcp"),
    "rdp": (3389, "tcp"),
    "sip": (5060, "udp"),
    "http-alt": (8080, "tcp"),
    "bgp": (179, "tcp"),
    "ospf": (89, "tcp"),
}


def resolve_service(name: str) -> tuple[Optional[int], Optional[str]]:
    """Resolve a service name or port number to (port, protocol).

    Returns:
        (port_number, protocol) - protocol may be None for numeric-only input.

    Examples:
        resolve_service("http")  -> (80, "tcp")
        resolve_service("dns")   -> (53, "udp")
        resolve_service("443")   -> (443, None)
        resolve_service("ssh")   -> (22, "tcp")
    """
    # Try numeric first
    try:
        return (int(name), None)
    except ValueError:
        pass

    lower = name.lower()
    if lower in _SERVICE_MAP:
        return _SERVICE_MAP[lower]

    # Fallback: try system socket resolution
    try:
        port = socket.getservbyname(lower)
        return (port, None)
    except OSError:
        return (None, None)


# ---------------------------------------------------------------------------
# Negation handling
# ---------------------------------------------------------------------------


def is_negated(value: str) -> tuple[bool, str]:
    """Check if a value is negated (! prefix) and strip it.

    Returns:
        (is_negated, stripped_value)
    """
    if value.startswith("!"):
        return True, value[1:]
    return False, value


# ---------------------------------------------------------------------------
# IP address matching
# ---------------------------------------------------------------------------


def ip_matches(ip_str: str, spec: str) -> bool:
    """Check if an IP address matches a specification.

    The spec can be:
      - A single IP: "10.0.0.1"
      - A CIDR network: "10.0.0.0/24"
      - A range: "10.0.0.1-10.0.0.100"
      - Negated: "!10.0.0.0/24"

    Works for both IPv4 and IPv6.
    """
    negated, spec_clean = is_negated(spec)

    try:
        result = _ip_matches_positive(ip_str, spec_clean)
    except (ValueError, TypeError):
        return False

    return (not result) if negated else result


def _ip_matches_positive(ip_str: str, spec: str) -> bool:
    """Positive (non-negated) IP match."""
    ip = ipaddress.ip_address(ip_str)

    # Range: 10.0.0.1-10.0.0.100
    if "-" in spec and "/" not in spec:
        return ip_in_range(ip_str, spec)

    # CIDR: 10.0.0.0/24
    if "/" in spec:
        network = ipaddress.ip_network(spec, strict=False)
        return ip in network

    # Exact match
    return ip == ipaddress.ip_address(spec)


def ip_in_range(ip_str: str, range_str: str) -> bool:
    """Check if IP is within a range like '10.0.0.1-10.0.0.100'."""
    parts = range_str.split("-", 1)
    if len(parts) != 2:
        return False
    try:
        ip = ipaddress.ip_address(ip_str)
        start = ipaddress.ip_address(parts[0].strip())
        end = ipaddress.ip_address(parts[1].strip())
        return start <= ip <= end
    except ValueError:
        return False


def ip_matches_with_mask(ip_str: str, address: str, mask: str) -> bool:
    """Check if an IP matches an address with a bitmask.

    VyOS ``address-mask`` works like netfilter ``--src-mask`` / ``--dst-mask``:
    the packet IP is bitwise-ANDed with the mask and compared to (address AND mask).

    For example:
      - address="89.234.162.249", mask="255.255.255.255" → exact match
      - address="10.0.0.0", mask="255.0.0.0" → matches 10.x.x.x

    Supports negation on the address (! prefix).
    """
    negated, addr_clean = is_negated(address)

    try:
        ip = ipaddress.ip_address(ip_str)
        addr = ipaddress.ip_address(addr_clean)
        mask_addr = ipaddress.ip_address(mask)

        ip_int = int(ip)
        addr_int = int(addr)
        mask_int = int(mask_addr)

        result = (ip_int & mask_int) == (addr_int & mask_int)
    except (ValueError, TypeError):
        return False

    return (not result) if negated else result


# ---------------------------------------------------------------------------
# Port matching
# ---------------------------------------------------------------------------


def port_matches(port: int, spec: str) -> bool:
    """Check if a port number matches a specification.

    The spec can be:
      - A single port: "443"
      - A named port: "http"
      - A range: "5000-5010"
      - A comma-separated list: "http,443,8080-8090"
      - Negated: "!http", "!443"
    """
    negated, spec_clean = is_negated(spec)
    result = _port_matches_positive(port, spec_clean)
    return (not result) if negated else result


def _port_matches_positive(port: int, spec: str) -> bool:
    """Positive (non-negated) port match."""
    # Comma-separated list
    parts = [p.strip() for p in spec.split(",")]
    for part in parts:
        if "-" in part:
            # Range: 5000-5010
            range_parts = part.split("-", 1)
            try:
                low = _resolve_port(range_parts[0].strip())
                high = _resolve_port(range_parts[1].strip())
                if low is not None and high is not None and low <= port <= high:
                    return True
            except (ValueError, TypeError):
                continue
        else:
            resolved = _resolve_port(part)
            if resolved is not None and port == resolved:
                return True
    return False


def _resolve_port(name_or_num: str) -> Optional[int]:
    """Resolve a port name or number to an integer."""
    try:
        return int(name_or_num)
    except ValueError:
        pass
    lower = name_or_num.lower()
    if lower in _SERVICE_MAP:
        return _SERVICE_MAP[lower][0]
    try:
        return socket.getservbyname(lower)
    except OSError:
        return None


# ---------------------------------------------------------------------------
# Interface matching
# ---------------------------------------------------------------------------


def interface_matches(iface: str, pattern: str) -> bool:
    """Check if an interface name matches a pattern.

    Supports:
      - Exact match: "eth0"
      - Wildcard: "eth*", "eth3*"
      - Negation: "!eth0", "!eth*"
    """
    negated, pattern_clean = is_negated(pattern)
    result = fnmatch.fnmatch(iface, pattern_clean)
    return (not result) if negated else result


# ---------------------------------------------------------------------------
# Protocol matching
# ---------------------------------------------------------------------------


def protocol_matches(proto: str, spec: str) -> bool:
    """Check if a protocol matches a specification.

    Supports:
      - Exact match: "tcp", "udp", "icmp"
      - Special: "all" matches everything, "tcp_udp" matches tcp or udp
      - Negation: "!tcp"
    """
    negated, spec_clean = is_negated(spec)
    result = _protocol_matches_positive(proto.lower(), spec_clean.lower())
    return (not result) if negated else result


def _protocol_matches_positive(proto: str, spec: str) -> bool:
    """Positive protocol match."""
    if spec == "all":
        return True
    if spec == "tcp_udp":
        return proto in ("tcp", "udp")
    return proto == spec
