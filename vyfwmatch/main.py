#!/usr/bin/env python3
"""VyFwMatch — VyOS Firewall Policy Matcher.

Parses a VyOS boot configuration file and matches user-provided traffic
tuples against firewall rules, returning the first matching policy.

Usage:
    vyfwmatch --config config.boot \\
        --inbound-interface eth0 --outbound-interface eth1 \\
        --source 10.0.0.1 --destination 192.168.0.10 \\
        --service 443 --protocol tcp
"""

import sys

from vyfwmatch.adapters.vyos_config import VyOSConfigAdapter
from vyfwmatch.cli.argument_parser import parse_args
from vyfwmatch.cli.output_formatter import format_result
from vyfwmatch.domain.models import TrafficTuple
from vyfwmatch.services.decision_engine import DecisionEngine
from vyfwmatch.services.raw_config_validator import (
    ConfigValidationError,
    RawConfigValidator,
)
from vyfwmatch.services.rule_loader import RuleLoaderService


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    # Load VyOS configuration
    try:
        adapter = VyOSConfigAdapter(args.config)
    except FileNotFoundError:
        print(f"Error: Config file not found: {args.config}", file=sys.stderr)
        return 1
    except SystemError as e:
        print(f"Error: Failed to load config file: {e}", file=sys.stderr)
        return 1

    # Validate raw configuration before parsing
    try:
        raw_config = adapter.get_firewall_config()
        validator = RawConfigValidator()
        validator.validate(raw_config)
    except ConfigValidationError as e:
        print("Configuration validation failed:", file=sys.stderr)
        for error in e.errors:
            path = getattr(error, "path", None)
            if path:
                print(f"  - {path}: {error.message}", file=sys.stderr)
            else:
                print(f"  - {error.message}", file=sys.stderr)
        return 1

    # Load firewall rules (configuration already validated)
    loader = RuleLoaderService(adapter)
    fw_config = loader.load_firewall_config()

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

    # Run the decision engine
    engine = DecisionEngine(fw_config)
    result = engine.match(traffic)

    # Format and print the result
    output = format_result(result, args.output_format)
    print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
