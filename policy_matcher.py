#!/usr/bin/env python3
"""VyOS Firewall Policy Matcher — Entry Point.

Parses a VyOS boot configuration file and matches user-provided traffic
tuples against firewall rules, returning the first matching policy.

Usage:
    python policy_matcher.py --config config.boot \\
        --inbound-interface eth0 --outbound-interface eth1 \\
        --source 10.0.0.1 --destination 192.168.0.10 \\
        --service 443 --protocol tcp
"""

from __future__ import annotations

import sys

from matcher.engine import MatchingEngine, TrafficTuple
from parser.config_parser import parse_config_file
from parser.firewall_extractor import extract_firewall
from ui.cli import parse_args
from ui.output import format_result


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    # Parse the config file
    try:
        config_tree = parse_config_file(args.config)
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Failed to parse config file: {e}", file=sys.stderr)
        return 1

    # Extract firewall configuration
    fw_config = extract_firewall(config_tree)

    # Build the traffic tuple
    traffic = TrafficTuple(
        inbound_interface=args.inbound_interface,
        outbound_interface=args.outbound_interface,
        source_ip=args.source,
        destination_ip=args.destination,
        protocol=args.resolved_protocol,
        port=args.resolved_port,
        state=args.state,
        hook=args.hook,
    )

    # Run the matching engine
    engine = MatchingEngine(fw_config)
    result = engine.match(traffic)

    # Format and print the result
    output = format_result(result, args.output_format)
    print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
