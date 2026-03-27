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
- Releases
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

### Binary Dependencies (Optional but Recommended)

VyFwMatch uses VyOS's original validators for configuration validation. For full validation capabilities, you need to build two binaries:

1. **ipaddrcheck** - IP address validation (C-based)
2. **validate-value** - Regex validation (OCaml-based)

**Note:** Python fallback validators are available when binaries aren't built, providing basic validation without external dependencies.

#### Building Dependencies on Debian/Ubuntu

```bash
# Install build tools
sudo apt-get install autoconf automake libtool gcc make \
  libcidr-dev libpcre2-dev opam ocaml dune

# Build both binaries using Make
make build-deps
```

#### Building Dependencies on macOS

```bash
# Install build tools via Homebrew
brew install autoconf automake libtool pcre2 opam dune

# Note: libcidr needs to be built from source on macOS
# The binaries are primarily for Linux/Docker deployment

# For local development, Python fallbacks work without building
```

#### Using Docker

The Docker build automatically compiles both binaries:

```bash
docker build -t vyfwmatch:latest .
```

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
# or using Make
make test
```

Run with coverage:

```bash
pytest --cov=vyfwmatch --cov-report=html
# or using Make
make test-cov
```

Run pylint for code quality:

```bash
pylint vyfwmatch/
# or using Make
make lint
```

Run all checks:

```bash
make check
```

Releases
--------

This repository uses [semantic-release](https://github.com/semantic-release/semantic-release)
in CI for automated versioning, tags, changelog updates, and GitHub releases.

- Releases run automatically on pushes to `main` after lint/test/security jobs pass.
- Version bumps are inferred from commit messages using Conventional Commits.

Commit types used for release bumping:

- `fix:` -> patch release (e.g. `1.2.3` -> `1.2.4`)
- `feat:` -> minor release (e.g. `1.2.3` -> `1.3.0`)
- `feat!:` or `BREAKING CHANGE:` -> major release (e.g. `1.2.3` -> `2.0.0`)

Examples:

```text
fix(validators): trim whitespace in address and port validation
feat(ci): add release notes publication
feat!: remove legacy rule loader fallback
```

Troubleshooting
---------------

### Configuration Validation Errors

- **"Configuration validation failed: Invalid network prefix"**
  - Ensure all IP addresses and networks use valid CIDR notation
  - Build the ipaddrcheck binary for comprehensive IP validation
  - Python fallbacks provide basic validation without the binary

- **"Configuration validation failed: Invalid port"**
  - Check port ranges are valid (1-65535)
  - Ensure port ranges have start <= end (e.g., "80-443" not "443-80")

- **"Configuration validation failed: Jump target not found"**
  - Ensure all `jump-target` values reference existing chains
  - Chain names are case-sensitive

### Runtime Errors

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
  - `raw_config_validator.py` - Validates config before parsing (NEW)
  - `vyos_validators.py` - VyOS validator wrappers (NEW)
  - `rule_loader.py` - Loads firewall config from VyOS config
  - `decision_engine.py` - Evaluates rules against traffic tuples
  - `helpers.py` - IP/port/interface matching utilities and service resolution
- **Domain layer**: `vyfwmatch/domain/` - Core models
  - `models.py` - Domain models (Rule, Chain, FirewallConfig, etc.)
- **Adapter layer**: `vyfwmatch/adapters/` - External integrations
  - `vyos_config.py` - VyOS configuration adapter
  - `config_parser.py` - VyOS boot config tokenizer and parser

All functionality is self-contained within the `vyfwmatch/` package.

### Code quality

The project maintains high code quality standards:

- **Pylint score**: 9.96/10
- **Python version**: 3.10+ minimum
- **Test coverage**: 177 tests, all passing
- **Type hints**: Used throughout all modules

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
