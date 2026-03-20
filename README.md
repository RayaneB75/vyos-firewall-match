VyFwMatch — VyOS Firewall Policy Matcher
=========================================

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

VyFwMatch is a modular VyOS firewall policy testing tool that parses VyOS boot 
configuration files and evaluates firewall rules for a given traffic tuple. It 
follows VyOS first-match-wins behavior, supports IPv4 and IPv6 chains, and 
resolves group references (address, network, port, interface).

The tool is designed as a wrapper around the official VyOS codebase (`vyos-1x` 
submodule), using VyOS's own configuration parsing when available, and provides 
a minimal decision engine for offline firewall rule simulation.

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

- Python 3.10+ (tested with 3.13)
- pytest for running tests
- pylint for code quality checks

Installation
------------

### Development installation

Clone the repository and install in editable mode:

```bash
git clone <repository-url>
cd vyos-fw-match
python -m venv venv
source venv/bin/activate
pip install -e .
```

This will install the `vyfwmatch` command-line tool.

### Running from source

If you prefer not to install the package:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python vyfwmatch/main.py --help
```

Quick start
-----------

Using the installed command:

```bash
vyfwmatch \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
  --service https
```

Or running from source:

```bash
python vyfwmatch/main.py \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
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
vyfwmatch \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
  --service https
```

Input traffic to the router itself:

```bash
vyfwmatch \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 1.2.3.4 \
  --destination 192.168.0.1 \
  --protocol icmp \
  --hook input
```

Protocol + port without service name:

```bash
vyfwmatch \
  --config example/sample_config.boot \
  --inbound-interface eth0 \
  --source 10.0.0.1 \
  --destination 192.168.0.10 \
  --protocol tcp \
  --port 443
```

Testing
-------

Run the full test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=vyfwmatch --cov-report=html
```

Run pylint for code quality:

```bash
pylint vyfwmatch/
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

### Architecture

The project follows a modular, layered architecture:

- **Entry point**: `vyfwmatch/main.py` - Main CLI entry point
- **CLI layer**: `vyfwmatch/cli/` - Argument parsing and output formatting
  - `argument_parser.py` - CLI argument validation
  - `output_formatter.py` - Result formatting (table/JSON)
- **Service layer**: `vyfwmatch/services/` - Business logic
  - `rule_loader.py` - Loads firewall config from VyOS config
  - `decision_engine.py` - Evaluates rules against traffic tuples
- **Domain layer**: `vyfwmatch/domain/` - Core models
  - `models.py` - Domain models (Rule, Chain, FirewallConfig, etc.)
- **Adapter layer**: `vyfwmatch/adapters/` - External integrations
  - `vyos_config.py` - VyOS configuration adapter (bridge to vyos-1x)

### Legacy modules (still used internally)

The following modules are maintained for backward compatibility and internal use:

- `parser/` - Configuration parsing (used by adapter)
  - `config_parser.py` - VyOS config tokenizer and tree builder
  - `firewall_extractor.py` - Legacy extractor (functionality moved to rule_loader)
  - `models.py` - Legacy models (replaced by domain models)
- `matcher/` - Matching helpers
  - `helpers.py` - IP/port matching, service resolution (used by decision engine)
  - `engine.py` - Legacy engine (replaced by decision_engine)
- `ui/` - Legacy CLI (replaced by vyfwmatch/cli)
  - `cli.py` - Legacy argument parser
  - `output.py` - Legacy output formatter

### Code quality

The project maintains high code quality standards:

- **Pylint score**: 9.91/10
- **Python version**: 3.10+ minimum
- **Test coverage**: 177 tests, all passing
- **Type hints**: Used throughout new modules

API reference
-------------

The primary interface is the CLI. Internal APIs are documented in:

- `docs/api.md`

Config schema appendix
----------------------

See `docs/config-schema.md` for supported config elements and examples.

License
-------

MIT License. See `LICENSE`.

Docs
----

- `docs/index.md`
- `docs/architecture.md`
- `docs/tests/README.md`
- `docs/api.md`
- `docs/config-schema.md`
