"""CLI argument parsing for VyFwMatch."""

import argparse
import ipaddress
from typing import Optional

from matcher.helpers import resolve_service


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="vyfwmatch",
        description="VyOS Firewall Policy Matcher — match traffic tuples against firewall rules.",
        epilog=(
            "Examples:\n"
            "  vyfwmatch --config config.boot --inbound-interface eth0 "
            "--outbound-interface eth1 --source 10.0.0.1 --destination 192.168.0.10 "
            "--service 443 --protocol tcp\n\n"
            "  vyfwmatch --config config.boot --inbound-interface eth0 "
            "--source 1.2.3.4 --destination 192.168.0.1 --protocol icmp\n\n"
            "  vyfwmatch --config config.boot --inbound-interface eth1 "
            "--source 192.168.0.50 --destination 192.168.0.1 --service ssh"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to VyOS boot configuration file.",
    )
    parser.add_argument(
        "--inbound-interface",
        required=True,
        help="Inbound interface name (e.g. eth0, bond0).",
    )
    parser.add_argument(
        "--outbound-interface",
        default=None,
        help="Outbound interface name (optional).",
    )
    parser.add_argument(
        "--hook",
        default=None,
        choices=["forward", "input", "output"],
        help=(
            "Firewall hook to evaluate (forward, input, output). "
            "Defaults to 'forward'. Use 'input' for traffic destined to the router itself."
        ),
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source IP address (e.g. 10.0.0.1, 2001:db8::1).",
    )
    parser.add_argument(
        "--destination",
        required=True,
        help="Destination IP address (e.g. 192.168.0.10, 2001:db8::1).",
    )
    parser.add_argument(
        "--service",
        default=None,
        help="Service port number or name (e.g. 443, http, ssh, dns).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Destination port number (e.g. 443). Use with --protocol.",
    )
    parser.add_argument(
        "--protocol",
        default=None,
        help="Protocol (e.g. tcp, udp, icmp, icmpv6). Auto-resolved from service if not given.",
    )
    parser.add_argument(
        "--state",
        default=None,
        choices=["new", "established", "related", "invalid"],
        help="Connection state (e.g. new, established). Defaults to 'new' for new connections.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        dest="output_format",
        help="Output format: table (default) or json.",
    )

    return parser


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse and validate command-line arguments.

    Returns the parsed namespace, or exits with an error message.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # Validate: at least one of --service or --protocol must be set
    if args.service is None and args.protocol is None:
        parser.error("At least one of --service or --protocol must be specified.")

    # Validate source IP
    try:
        ipaddress.ip_address(args.source)
    except ValueError:
        parser.error("--source must be an IP address (FQDNs are not supported).")

    # Validate destination IP
    try:
        ipaddress.ip_address(args.destination)
    except ValueError:
        parser.error(
            "--destination must be an IP address (FQDNs are not supported)."
        )

    # Validate port usage
    if args.service is not None and args.port is not None:
        parser.error("--service and --port are mutually exclusive.")
    if args.port is not None and args.port <= 0:
        parser.error("--port must be a positive integer.")
    if args.port is not None and args.protocol is None:
        parser.error("--port requires --protocol to be specified.")

    # Resolve service to port + protocol
    resolved_port: Optional[int] = None
    resolved_protocol: Optional[str] = args.protocol

    if args.port is not None:
        if args.port > 65535:
            parser.error("--port must be in the range 1-65535.")
        resolved_port = args.port

    if args.service is not None:
        port, svc_proto = resolve_service(args.service)
        if port is None:
            parser.error(f"Unknown service: '{args.service}'")
        resolved_port = port
        # Auto-resolve protocol from service if not explicitly given
        if resolved_protocol is None and svc_proto is not None:
            resolved_protocol = svc_proto

    # Store resolved values
    args.resolved_port = resolved_port
    args.resolved_protocol = resolved_protocol

    return args
