Documentation
=============

Table of contents
-----------------

- Overview
- Getting started
- CLI reference
- Configuration format
- Matching behavior
- Output formats
- Examples
- Troubleshooting
- Development
- Testing
- API reference
- Config schema appendix

Overview
--------

VyFwMatch (VyOS Firewall Matcher) is a modular tool that parses VyOS boot
configuration files and evaluates firewall rules for traffic tuples. It
supports IPv4 and IPv6 chains, jump/continue/return semantics, and group-based
matching.

The tool is designed as a wrapper around the official VyOS codebase (`vyos-1x`
submodule), providing offline firewall rule simulation without requiring a
live VyOS system.

Getting started
---------------

Install the package:

```bash
pip install -e .
```

Run a test:

```bash
vyfwmatch \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
  --service https
```

Or run from source:

```bash
python -m vyfwmatch.main \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
  --service https
```

CLI reference
-------------

Required arguments:

- `--config`
- `--inbound-interface`
- `--source` (IP only)
- `--destination` (IP only)
- At least one of `--service` or `--protocol`

Optional arguments:

- `--outbound-interface`
- `--hook` (`forward`, `input`, `output`)
- `--service` (name or number)
- `--protocol`
- `--port` (use with `--protocol`)
- `--state`
- `--format` (`table`, `json`)

Configuration format
--------------------

Only VyOS boot configs (curly-brace hierarchy) are supported. `set` commands
are not accepted. The parser expects sections such as:

```
firewall {
  group { ... }
  ipv4 { forward { filter { ... } } }
  ipv6 { input { filter { ... } } }
}
```

Matching behavior
-----------------

- Rules are evaluated top-down within a chain
- First match wins
- `jump` evaluates the target chain and returns to the caller unless a match
  (non-return) is found
- `return` exits the current chain
- If no rule matches, the chain `default-action` applies
- Global `state-policy` is a fallback if no chain rule matched

Output formats
--------------

- `table` includes chain, rule, action, and a trace
- `json` provides structured data

Examples
--------

See `README.md` for examples and usage patterns.

Troubleshooting
---------------

- FQDNs are not supported for `--source` or `--destination`
- `--port` requires `--protocol`
- `--service` and `--port` are mutually exclusive

Development
-----------

VyFwMatch follows a modular, layered architecture:

**Core Package** (`vyfwmatch/`):

- `main.py` - Main entry point
- `cli/` - Command-line interface (argument parsing, output formatting)
- `adapters/` - External integrations (VyOS config adapter, config parser)
- `services/` - Business logic (rule loader, decision engine, matching helpers)
- `domain/` - Core models (Rule, Chain, FirewallConfig)

All functionality is now contained within the `vyfwmatch/` package with no external dependencies on legacy modules.

See `docs/architecture.md` for detailed information.

Testing
-------

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=vyfwmatch --cov-report=html
```

See `docs/tests/README.md` for detailed test coverage information.

API reference
-------------

See `docs/api.md`.

Config schema appendix
----------------------

See `docs/config-schema.md`.
