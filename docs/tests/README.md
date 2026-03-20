Tests
=====

This project uses pytest to validate parsing, extraction, matching, and CLI
behavior. The tests use real VyOS documentation examples and a production-like
sample config to ensure end-to-end correctness.

Test layout
-----------

- `tests/test_config_parser.py`
  - Tokenization and parsing of hierarchical boot configs
  - Newline-aware parsing for valueless leaves and repeated keys

- `tests/test_firewall_extractor.py`
  - Group extraction (address/network/port/interface)
  - Chain and rule extraction
  - State-policy extraction
  - Repeated leaf handling (`state` list)

- `tests/test_helpers.py`
  - IP, range, CIDR, negation matching
  - Port matching (ranges, lists, service names)
  - Interface wildcards and negation
  - Protocol matching
  - Address-mask matching

- `tests/test_matching_engine.py`
  - End-to-end matching for forward/input/output chains
  - Jump/continue/return behavior
  - IPv4/IPv6 family selection
  - Default-action behavior
  - Group reference resolution and negation
  - Match-any destination behavior when destination criteria are absent

- `tests/test_cli.py`
  - Required and optional CLI args
  - Service resolution and protocol inference
  - `--hook` behavior
  - `--port` validation
  - IP-only validation for `--source` and `--destination`

Fixtures
--------

Common configs are defined in `tests/conftest.py`:

- `QUICKSTART_CONFIG` from the VyOS quick-start guide
- `GROUPS_CONFIG` from the firewall groups documentation
- `ZONE_CONFIG` from the zone-based firewall documentation
- `DETAILED_CONFIG` from IPv4 rule examples

How to run
----------

Run everything:

```bash
python -m pytest
```

Run a single file:

```bash
python -m pytest tests/test_matching_engine.py
```

Run a specific test:

```bash
python -m pytest tests/test_matching_engine.py -k "icmp"
```
