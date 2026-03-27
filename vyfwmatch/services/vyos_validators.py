"""VyOS validator wrappers.

This module provides wrapper functions for VyOS validators from
``vyos-1x/src/validators/``.
"""

from __future__ import annotations

import ipaddress
import logging
import os
import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

_STATE: dict[str, object] = {
    "ipaddrcheck_binary": None,
    "validate_value_binary": None,
    "binaries_checked": False,
}

PROJECT_ROOT = Path(__file__).parent.parent.parent


def _find_binary(name: str, search_paths: list[Path]) -> str | None:
    """Find a binary in explicit paths, then PATH."""
    for path in search_paths:
        if path.exists() and os.access(path, os.X_OK):
            logger.debug("Found %s at %s", name, path)
            return str(path)

    system_binary = shutil.which(name)
    if system_binary:
        logger.debug("Found %s in system PATH at %s", name, system_binary)
        return system_binary

    logger.warning("Binary %s not found in submodules or system PATH", name)
    return None


def _init_binaries() -> None:
    """Initialize binary paths once."""
    if _STATE["binaries_checked"]:
        return

    _STATE["binaries_checked"] = True
    _STATE["ipaddrcheck_binary"] = _find_binary(
        "ipaddrcheck", [PROJECT_ROOT / "ipaddrcheck" / "src" / "ipaddrcheck"]
    )
    _STATE["validate_value_binary"] = _find_binary(
        "validate-value",
        [PROJECT_ROOT / "vyos-utils" / "_build" / "default" / "src" / "validate_value.exe"],
    )

    if not _state_ipaddrcheck_binary():
        logger.warning(
            "ipaddrcheck binary not found. IP validation will fail. "
            "Build it with: cd ipaddrcheck && autoreconf -i && ./configure && make"
        )

    if not _state_validate_value_binary():
        logger.warning(
            "validate-value binary not found. Regex validation will fail. "
            "Build it with: cd vyos-utils && dune build"
        )


def _state_ipaddrcheck_binary() -> str | None:
    return _STATE["ipaddrcheck_binary"] if isinstance(_STATE["ipaddrcheck_binary"], str) else None


def _state_validate_value_binary() -> str | None:
    value = _STATE["validate_value_binary"]
    return value if isinstance(value, str) else None


def _mark_ipaddrcheck_unusable() -> None:
    logger.warning("ipaddrcheck is not runnable in this environment; using Python fallback")
    _STATE["ipaddrcheck_binary"] = None


def _mark_validate_value_unusable() -> None:
    logger.warning("validate-value is not runnable in this environment; using Python fallback")
    _STATE["validate_value_binary"] = None


def _run_binary(command: list[str]) -> subprocess.CompletedProcess[bytes] | None:
    """Run a validator binary and return process result."""
    try:
        return subprocess.run(
            command,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as exc:
        logger.error("Error running validator binary: %s", exc)
        return None


def _binary_not_runnable(result: subprocess.CompletedProcess[bytes]) -> bool:
    stderr = (result.stderr or b"").decode("utf-8", errors="ignore")
    return result.returncode in (126, 127) or "error while loading shared libraries" in stderr


def _call_ipaddrcheck(flag: str, value: str) -> bool:
    """Call ipaddrcheck with a flag."""
    _init_binaries()
    binary = _state_ipaddrcheck_binary()
    if not binary:
        return False

    result = _run_binary([binary, flag, value.strip()])
    if result is None:
        return False
    if _binary_not_runnable(result):
        _mark_ipaddrcheck_unusable()
        return False
    return result.returncode == 0


def _call_validate_value(regex: str, value: str) -> bool:
    """Call validate-value with regex mode."""
    _init_binaries()
    binary = _state_validate_value_binary()
    if not binary:
        return False

    result = _run_binary(
        [binary, "--regex", regex, "--value", value.strip()]
    )
    if result is None:
        return False
    if _binary_not_runnable(result):
        _mark_validate_value_unusable()
        return False
    return result.returncode == 0


def validate_ipv4_address(addr: str) -> bool:
    """Validate an IPv4 address (no prefix)."""
    result = _call_ipaddrcheck("--is-ipv4-single", addr)
    if result or _state_ipaddrcheck_binary():
        return result
    try:
        ipaddress.IPv4Address(addr)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_ipv6_address(addr: str) -> bool:
    """Validate an IPv6 address (no prefix)."""
    result = _call_ipaddrcheck("--is-ipv6-single", addr)
    if result or _state_ipaddrcheck_binary():
        return result
    try:
        ipaddress.IPv6Address(addr)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_ipv4_prefix(prefix: str) -> bool:
    """Validate an IPv4 prefix (CIDR network)."""
    if "/" not in prefix:
        return False
    result = _call_ipaddrcheck("--is-ipv4-net", prefix)
    if result or _state_ipaddrcheck_binary():
        return result
    try:
        ipaddress.IPv4Network(prefix, strict=True)
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError):
        return False


def validate_ipv6_prefix(prefix: str) -> bool:
    """Validate an IPv6 prefix (CIDR network)."""
    if "/" not in prefix:
        return False
    result = _call_ipaddrcheck("--is-ipv6-net", prefix)
    if result or _state_ipaddrcheck_binary():
        return result
    try:
        ipaddress.IPv6Network(prefix, strict=True)
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError):
        return False


def validate_ipv4_range(range_str: str) -> bool:
    """Validate an IPv4 range."""
    result = _call_ipaddrcheck("--is-ipv4-range", range_str)
    if result or _state_ipaddrcheck_binary():
        return result
    if "-" not in range_str:
        return False
    try:
        start_str, end_str = range_str.split("-", 1)
        start = ipaddress.IPv4Address(start_str.strip())
        end = ipaddress.IPv4Address(end_str.strip())
        return int(start) <= int(end)
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_ipv6_range(range_str: str) -> bool:
    """Validate an IPv6 range."""
    result = _call_ipaddrcheck("--is-ipv6-range", range_str)
    if result or _state_ipaddrcheck_binary():
        return result
    if "-" not in range_str:
        return False
    try:
        start_str, end_str = range_str.split("-", 1)
        start = ipaddress.IPv6Address(start_str.strip())
        end = ipaddress.IPv6Address(end_str.strip())
        return int(start) <= int(end)
    except (ipaddress.AddressValueError, ValueError):
        return False


def validate_mac_address(mac: str) -> bool:
    """Validate a MAC address."""
    regex = r"([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})"
    result = _call_validate_value(regex, mac)
    if result or _state_validate_value_binary():
        return result
    return bool(re.match(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$", mac))


def validate_fqdn(fqdn: str) -> bool:
    """Validate an FQDN."""
    regex = (
        r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
    )
    result = _call_validate_value(regex, fqdn)
    if result or _state_validate_value_binary():
        return result
    return bool(re.match(regex, fqdn))


def validate_ip_protocol(protocol: str) -> bool:
    """Validate IP protocol number or name."""
    try:
        if int(protocol) in range(0, 256):
            return True
    except ValueError:
        pass

    pattern = (
        r"!?\b(all|ip|hopopt|icmp|igmp|ggp|ipencap|st|tcp|egp|igp|pup|udp|"
        r"tcp_udp|hmp|xns-idp|rdp|iso-tp4|dccp|xtp|ddp|idpr-cmtp|ipv6|"
        r"ipv6-route|ipv6-frag|idrp|rsvp|gre|esp|ah|skip|ipv6-icmp|icmpv6|"
        r"ipv6-nonxt|ipv6-opts|rspf|vmtp|eigrp|ospf|ax.25|ipip|etherip|"
        r"encap|99|pim|ipcomp|vrrp|l2tp|isis|sctp|fc|mobility-header|"
        r"udplite|mpls-in-ip|manet|hip|shim6|wesp|rohc)\b"
    )
    return bool(re.fullmatch(pattern, protocol))


def validate_port_range(port: str) -> bool:
    """Validate one port token: number, range, or service name."""
    if re.match(r"^[0-9]{1,5}-[0-9]{1,5}$", port):
        return _validate_port_range_parts(port)
    if port.isnumeric():
        return _validate_single_port(port)
    return _is_common_service(port)


def validate_port_multi(ports: str) -> bool:
    """Validate comma-separated port tokens (VyOS port-multi style)."""
    tokens = [token.strip() for token in ports.split(",")]
    if not tokens:
        return False

    for token in tokens:
        if not token:
            return False
        if token.startswith("!"):
            token = token[1:]
        if not validate_port_range(token):
            return False
    return True


def _validate_port_range_parts(port_range: str) -> bool:
    port_1, port_2 = port_range.split("-")
    try:
        p1, p2 = int(port_1), int(port_2)
        return p1 in range(1, 65536) and p2 in range(1, 65536) and p1 <= p2
    except ValueError:
        return False


def _validate_single_port(port: str) -> bool:
    try:
        return int(port) in range(1, 65536)
    except ValueError:
        return False


def _is_common_service(service: str) -> bool:
    return service.lower() in _get_known_services()


@lru_cache(maxsize=1)
def _get_known_services() -> set[str]:
    fallback_services = {
        "ftp",
        "ssh",
        "telnet",
        "smtp",
        "smtps",
        "submission",
        "domain",
        "dns",
        "http",
        "https",
        "pop3",
        "pop3s",
        "imap",
        "imaps",
        "ldap",
        "ldaps",
        "mysql",
        "postgresql",
        "smb",
        "ntp",
        "snmp",
        "irc",
        "rtsp",
        "sip",
        "git",
        "redis",
        "mongodb",
    }

    services = _load_services_from_file(Path("/etc/services"))
    if services:
        return services | fallback_services
    return fallback_services


def _load_services_from_file(path: Path) -> set[str]:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return set()
    return _parse_services_text(content)


def _parse_services_text(content: str) -> set[str]:
    names: set[str] = set()
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        line = line.split("#", 1)[0].strip()
        if not line:
            continue

        fields = line.split()
        if len(fields) < 2:
            continue

        names.add(fields[0].lower())
        for alias in fields[2:]:
            names.add(alias.lower())

    return names


_init_binaries()

__all__ = [
    "validate_ipv4_address",
    "validate_ipv6_address",
    "validate_ipv4_prefix",
    "validate_ipv6_prefix",
    "validate_ipv4_range",
    "validate_ipv6_range",
    "validate_mac_address",
    "validate_fqdn",
    "validate_ip_protocol",
    "validate_port_range",
    "validate_port_multi",
]
