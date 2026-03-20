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

The VyOS Policy Matcher parses a VyOS boot configuration file and evaluates
firewall rules for a traffic tuple. It supports IPv4 and IPv6 chains, jump/
continue/return semantics, and group-based matching.

Getting started
---------------

```bash
python policy_matcher.py \
  --config sample_config.boot \
  --inbound-interface eth4 \
  --source 10.38.1.2 \
  --destination 10.4.9.1 \
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

- Entry point: `policy_matcher.py`
- Parser: `parser/config_parser.py`
- Extractor: `parser/firewall_extractor.py`
- Matcher: `matcher/engine.py`
- CLI: `ui/cli.py`
- Output: `ui/output.py`

Testing
-------

See `docs/tests/README.md` for test coverage and how to run subsets.

API reference
-------------

See `docs/api.md`.

Config schema appendix
----------------------

See `docs/config-schema.md`.
