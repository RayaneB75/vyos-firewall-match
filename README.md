VyOS Policy Matcher
===================

Table of contents
-----------------

- Overview
- Key features
- Requirements
- Installation
- Quick start
- CLI reference
- Configuration format
- Matching behavior
- Output formats
- Examples
- Testing
- Troubleshooting
- Development
- API reference
- Config schema appendix
- License
- Docs

Overview
--------

This tool parses a VyOS boot configuration (hierarchical curly-brace format)
and evaluates firewall rules for a given traffic tuple. It follows VyOS
first-match-wins behavior, supports IPv4 and IPv6 chains, and resolves group
references (address, network, port, interface).

Key features
------------

- Parses VyOS boot config files (not `set` command format)
- Supports `forward`, `input`, and `output` hooks (default is `forward`)
- Evaluates chains with jump/continue/return semantics
- Resolves group references for matching
- Accepts service names or raw ports
- Outputs results in table (default) or JSON

Requirements
------------

- Python 3.11+ (tested with 3.13)
- pytest for running tests

Installation
------------

Use the repo directly:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Quick start
-----------

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

- `--config` Path to VyOS boot config file
- `--inbound-interface` Inbound interface name
- `--source` Source IP address (must be an IP)
- `--destination` Destination IP address (must be an IP)
- At least one of `--service` or `--protocol`

Optional arguments:

- `--outbound-interface` Outbound interface name
- `--hook` Hook to evaluate (`forward`, `input`, `output`), default is `forward`
- `--service` Service name or port (e.g. `http`, `443`)
- `--protocol` Protocol (e.g. `tcp`, `udp`, `icmp`)
- `--port` Destination port number (use with `--protocol`)
- `--state` Connection state (`new`, `established`, `related`, `invalid`)
- `--format` Output format (`table` or `json`)

Configuration format
--------------------

Only the VyOS boot configuration format is supported (curly-brace hierarchy).
The tool does not accept `set` commands.

Supported elements include:

- `firewall { ipv4 { ... } ipv6 { ... } }`
- Base chains: `forward`, `input`, `output`
- Named chains: `name <CHAIN>`
- Group definitions under `firewall { group { ... } }`

Matching behavior
-----------------

- First-match-wins evaluation (top-down within a chain)
- `jump` evaluates a target chain; `return` resumes the caller
- `continue` skips to the next rule
- If no rule matches, the chain `default-action` is applied
- Global `state-policy` is evaluated only if no chain rule matched

Output formats
--------------

- `table` shows the selected chain, rule, action, criteria, and trace
- `json` returns structured output suitable for scripting

Examples
--------

Forwarded HTTPS traffic:

```bash
python policy_matcher.py \
  --config sample_config.boot \
  --inbound-interface eth4 \
  --source 10.38.1.2 \
  --destination 10.4.9.1 \
  --service https
```

Input traffic to the router itself:

```bash
python policy_matcher.py \
  --config sample_config.boot \
  --inbound-interface eth0 \
  --source 1.2.3.4 \
  --destination 192.168.0.1 \
  --protocol icmp \
  --hook input
```

Protocol + port without service name:

```bash
python policy_matcher.py \
  --config sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
  --protocol tcp \
  --port 443
```

Testing
-------

```bash
python -m pytest
```

Troubleshooting
---------------

- Error: `--destination must be an IP address`
  - Provide an IP address instead of an FQDN
- Error: `--source must be an IP address`
  - Provide an IP address instead of an FQDN
- Error: `Unknown service`
  - Use a numeric port or a supported service name
- No matching chain
  - Ensure the config includes the selected hook (`forward`, `input`, `output`)

Development
-----------

- Entry point: `policy_matcher.py`
- Parsing: `parser/config_parser.py` and `parser/firewall_extractor.py`
- Matching: `matcher/engine.py` and `matcher/helpers.py`
- CLI: `ui/cli.py`
- Output: `ui/output.py`

API reference
-------------

The primary interface is the CLI. Internal APIs are documented in:

- `docs/api.md`

Config schema appendix
----------------------

See `docs/config-schema.md` for supported config elements and examples.

License
-------

No license specified.

Docs
----

- `docs/index.md`
- `docs/architecture.md`
- `docs/tests/README.md`
- `docs/api.md`
- `docs/config-schema.md`
