"""VyOS validator wrappers.

This module provides wrapper functions for VyOS validators from vyos-1x/src/validators/.
It handles both shell-based validators (that call external binaries) and Python-based
validators (that can be imported directly).

For shell validators:
- ipv4-address, ipv6-address, etc. call ipaddrcheck binary
- mac-address, fqdn, etc. call validate-value binary

For Python validators:
- ip-protocol, port-range are imported and executed directly

Binary Discovery:
Binaries are searched in the following locations:
1. ipaddrcheck/src/ipaddrcheck (built from submodule)
2. vyos-utils/_build/default/src/validate_value.exe (built from submodule)
3. System PATH (/usr/local/bin, /usr/bin, etc.)

If binaries are not found, validation returns False (strict mode).
"""

import ipaddress
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Setup logging
logger = logging.getLogger(__name__)

# Binary paths
_IPADDRCHECK_BINARY: Optional[str] = None
_VALIDATE_VALUE_BINARY: Optional[str] = None
_BINARIES_CHECKED = False

# Project root (vyfwmatch/)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def _find_binary(name: str, search_paths: list[Path]) -> Optional[str]:
    """Find a binary by searching in order: submodule build dirs, then system PATH.
    
    Args:
        name: Binary name to search for
        search_paths: List of paths to check in submodules
        
    Returns:
        Full path to binary if found, None otherwise
    """
    # Check submodule paths first
    for path in search_paths:
        if path.exists() and os.access(path, os.X_OK):
            logger.debug(f"Found {name} at {path}")
            return str(path)
    
    # Check system PATH
    system_binary = shutil.which(name)
    if system_binary:
        logger.debug(f"Found {name} in system PATH at {system_binary}")
        return system_binary
    
    logger.warning(f"Binary {name} not found in submodules or system PATH")
    return None


def _init_binaries() -> None:
    """Initialize binary paths by searching for them."""
    global _IPADDRCHECK_BINARY, _VALIDATE_VALUE_BINARY, _BINARIES_CHECKED
    
    if _BINARIES_CHECKED:
        return
    
    _BINARIES_CHECKED = True
    
    # Search for ipaddrcheck
    ipaddrcheck_paths = [
        PROJECT_ROOT / "ipaddrcheck" / "src" / "ipaddrcheck",
    ]
    _IPADDRCHECK_BINARY = _find_binary("ipaddrcheck", ipaddrcheck_paths)
    
    # Search for validate-value (OCaml build output has .exe extension on all platforms)
    validate_value_paths = [
        PROJECT_ROOT / "vyos-utils" / "_build" / "default" / "src" / "validate_value.exe",
    ]
    _VALIDATE_VALUE_BINARY = _find_binary("validate-value", validate_value_paths)
    
    if not _IPADDRCHECK_BINARY:
        logger.warning(
            "ipaddrcheck binary not found. IP validation will fail. "
            "Build it with: cd ipaddrcheck && autoreconf -i && ./configure && make"
        )
    
    if not _VALIDATE_VALUE_BINARY:
        logger.warning(
            "validate-value binary not found. Regex validation will fail. "
            "Build it with: cd vyos-utils && dune build"
        )


def _call_ipaddrcheck(flag: str, value: str) -> bool:
    """Execute ipaddrcheck binary with a specific flag.
    
    Args:
        flag: ipaddrcheck flag (e.g., '--is-ipv4-single')
        value: Value to validate
        
    Returns:
        True if validation passed, False otherwise
    """
    _init_binaries()
    
    if not _IPADDRCHECK_BINARY:
        return False
    
    try:
        result = subprocess.run(
            [_IPADDRCHECK_BINARY, flag, value],
            capture_output=True,
            timeout=5
        )
        # Exit code 0 = valid, 1 = invalid, 2 = error
        return result.returncode == 0
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logger.error("Error calling ipaddrcheck: %s", e)
        return False


def _call_validate_value(regex: str, value: str) -> bool:
    """Execute validate-value binary with a regex pattern.
    
    Args:
        regex: Regular expression pattern
        value: Value to validate
        
    Returns:
        True if validation passed, False otherwise
    """
    _init_binaries()
    
    if not _VALIDATE_VALUE_BINARY:
        return False
    
    try:
        result = subprocess.run(
            [_VALIDATE_VALUE_BINARY, "--regex", regex, "--value", value],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        logger.error("Error calling validate-value: %s", e)
        return False


# ============================================================================
# IP Address Validators
# ============================================================================

def validate_ipv4_address(addr: str) -> bool:
    """Validate an IPv4 address (no prefix/mask).
    
    Args:
        addr: IPv4 address string
        
    Returns:
        True if valid IPv4 address, False otherwise
    """
    # Try binary first
    result = _call_ipaddrcheck("--is-ipv4-single", addr)
    if result or _IPADDRCHECK_BINARY:
        return result
    
    # Fallback to Python ipaddress module
    try:
        ipaddress.IPv4Address(addr)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_ipv6_address(addr: str) -> bool:
    """Validate an IPv6 address (no prefix/mask).
    
    Args:
        addr: IPv6 address string
        
    Returns:
        True if valid IPv6 address, False otherwise
    """
    # Try binary first
    result = _call_ipaddrcheck("--is-ipv6-single", addr)
    if result or _IPADDRCHECK_BINARY:
        return result
    
    # Fallback to Python ipaddress module
    try:
        ipaddress.IPv6Address(addr)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_ipv4_prefix(prefix: str) -> bool:
    """Validate an IPv4 prefix in CIDR notation (e.g., 192.168.1.0/24).
    
    Args:
        prefix: IPv4 prefix string
        
    Returns:
        True if valid IPv4 prefix, False otherwise
    """
    # Try binary first
    result = _call_ipaddrcheck("--is-ipv4-cidr", prefix)
    if result or _IPADDRCHECK_BINARY:
        return result
    
    # Fallback to Python ipaddress module
    try:
        ipaddress.IPv4Network(prefix, strict=False)
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError):
        return False


def validate_ipv6_prefix(prefix: str) -> bool:
    """Validate an IPv6 prefix in CIDR notation.
    
    Args:
        prefix: IPv6 prefix string
        
    Returns:
        True if valid IPv6 prefix, False otherwise
    """
    # Try binary first
    result = _call_ipaddrcheck("--is-ipv6-cidr", prefix)
    if result or _IPADDRCHECK_BINARY:
        return result
    
    # Fallback to Python ipaddress module
    try:
        ipaddress.IPv6Network(prefix, strict=False)
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError):
        return False


def validate_ipv4_range(range_str: str) -> bool:
    """Validate an IPv4 address range (e.g., 192.168.1.1-192.168.1.10).
    
    Args:
        range_str: IPv4 range string
        
    Returns:
        True if valid IPv4 range, False otherwise
    """
    # Try binary first
    result = _call_ipaddrcheck("--is-ipv4-range", range_str)
    if result or _IPADDRCHECK_BINARY:
        return result
    
    # Fallback to Python validation
    if '-' not in range_str:
        return False
    
    try:
        start_str, end_str = range_str.split('-', 1)
        start = ipaddress.IPv4Address(start_str.strip())
        end = ipaddress.IPv4Address(end_str.strip())
        return int(start) <= int(end)
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_ipv6_range(range_str: str) -> bool:
    """Validate an IPv6 address range.
    
    Args:
        range_str: IPv6 range string
        
    Returns:
        True if valid IPv6 range, False otherwise
    """
    # Try binary first
    result = _call_ipaddrcheck("--is-ipv6-range", range_str)
    if result or _IPADDRCHECK_BINARY:
        return result
    
    # Fallback to Python validation
    if '-' not in range_str:
        return False
    
    try:
        start_str, end_str = range_str.split('-', 1)
        start = ipaddress.IPv6Address(start_str.strip())
        end = ipaddress.IPv6Address(end_str.strip())
        return int(start) <= int(end)
    except (ipaddress.AddressValueError, ValueError):
        return False


# ============================================================================
# MAC Address Validator
# ============================================================================

def validate_mac_address(mac: str) -> bool:
    """Validate a MAC address (e.g., 00:11:22:33:44:55).
    
    Args:
        mac: MAC address string
        
    Returns:
        True if valid MAC address, False otherwise
    """
    # Try binary first
    regex = r"([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})"
    result = _call_validate_value(regex, mac)
    if result or _VALIDATE_VALUE_BINARY:
        return result
    
    # Fallback to Python regex
    return bool(re.match(r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$', mac))


# ============================================================================
# FQDN Validator
# ============================================================================

def validate_fqdn(fqdn: str) -> bool:
    """Validate a Fully Qualified Domain Name.
    
    Args:
        fqdn: FQDN string
        
    Returns:
        True if valid FQDN, False otherwise
    """
    # Try binary first
    regex = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
    result = _call_validate_value(regex, fqdn)
    if result or _VALIDATE_VALUE_BINARY:
        return result
    
    # Fallback to Python regex (RFC 1123)
    return bool(re.match(
        r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*'
        r'[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$',
        fqdn
    ))


# ============================================================================
# Python-based Validators (imported from vyos-1x)
# ============================================================================

def validate_ip_protocol(protocol: str) -> bool:
    """Validate an IP protocol number or name.
    
    Uses the original VyOS ip-protocol validator logic.
    
    Args:
        protocol: Protocol number (0-255) or name (tcp, udp, icmp, etc.)
        
    Returns:
        True if valid protocol, False otherwise
    """
    # Try numeric protocol
    try:
        if int(protocol) in range(0, 256):
            return True
    except ValueError:
        pass
    
    # Try protocol name (based on vyos-1x/src/validators/ip-protocol)
    pattern = (
        r"!?\b(all|ip|hopopt|icmp|igmp|ggp|ipencap|st|tcp|egp|igp|pup|udp|"
        r"tcp_udp|hmp|xns-idp|rdp|iso-tp4|dccp|xtp|ddp|idpr-cmtp|ipv6|"
        r"ipv6-route|ipv6-frag|idrp|rsvp|gre|esp|ah|skip|ipv6-icmp|icmpv6|"
        r"ipv6-nonxt|ipv6-opts|rspf|vmtp|eigrp|ospf|ax.25|ipip|etherip|"
        r"encap|99|pim|ipcomp|vrrp|l2tp|isis|sctp|fc|mobility-header|"
        r"udplite|mpls-in-ip|manet|hip|shim6|wesp|rohc)\b"
    )
    return bool(re.match(pattern, protocol))


def validate_port_range(port: str) -> bool:
    """Validate a port number, port range, or service name.

    Uses the original VyOS port-range validator logic.

    Args:
        port: Port number (1-65535), range (1-1024), or service name (http, ssh, etc.)

    Returns:
        True if valid port specification, False otherwise
    """
    # Check if it's a port range (e.g., "80-443")
    if re.match(r'^[0-9]{1,5}-[0-9]{1,5}$', port):
        return _validate_port_range_parts(port)

    # Check if it's a single port number
    if port.isnumeric():
        return _validate_single_port(port)

    # Service names - accept common service names
    return _is_common_service(port)


def _validate_port_range_parts(port_range: str) -> bool:
    """Validate a port range like '80-443'."""
    port_1, port_2 = port_range.split('-')
    try:
        p1, p2 = int(port_1), int(port_2)
        return (p1 in range(1, 65536) and
                p2 in range(1, 65536) and
                p1 <= p2)
    except ValueError:
        return False


def _validate_single_port(port: str) -> bool:
    """Validate a single port number."""
    try:
        return int(port) in range(1, 65536)
    except ValueError:
        return False


def _is_common_service(service: str) -> bool:
    """Check if service name is in common services list."""
    common_services = {
        'ftp', 'ssh', 'telnet', 'smtp', 'domain', 'dns', 'http', 'https',
        'pop3', 'imap', 'ldap', 'ldaps', 'mysql', 'postgresql', 'smb',
        'ntp', 'snmp', 'irc', 'rtsp', 'sip', 'git', 'redis', 'mongodb',
    }
    return service.lower() in common_services


# ============================================================================
# Module Initialization
# ============================================================================

# Initialize binaries on module import
_init_binaries()

__all__ = [
    'validate_ipv4_address',
    'validate_ipv6_address',
    'validate_ipv4_prefix',
    'validate_ipv6_prefix',
    'validate_ipv4_range',
    'validate_ipv6_range',
    'validate_mac_address',
    'validate_fqdn',
    'validate_ip_protocol',
    'validate_port_range',
]
