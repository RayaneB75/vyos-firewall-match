API Reference
=============

This project is primarily a CLI tool. The internal modules are stable enough
to use programmatically, but they are not packaged as a public library.

CLI entry point
---------------
- `policy_matcher.py`
  - Reads CLI args, loads config, runs matching, outputs results.

Python modules
--------------

Parser
------
- `parser/config_parser.py`
  - `parse_config(text: str) -> ConfigTree`
  - Parses VyOS boot config text into a nested dict structure.

- `parser/firewall_extractor.py`
  - `extract_firewall(config: ConfigTree) -> FirewallConfig`
  - Converts a parsed tree into typed models used by the matcher.

Models
------
- `parser/models.py`
  - `FirewallConfig`: container for groups, chains, and state-policy
  - `FirewallChain`: chain definition and default-action
  - `FirewallRule`: rule definition and matching criteria
  - `SourceDestMatch`, `InterfaceMatch`: match blocks
  - `FirewallGroup`: address/network/port/interface group

Matching
--------
- `matcher/engine.py`
  - `MatchingEngine(config: FirewallConfig)`
  - `match(traffic: TrafficTuple) -> MatchResult`
  - `TrafficTuple`: inbound/outbound, src/dst, protocol, port, state, hook
  - `MatchResult`: action, chain, rule, trace, default-action info

Helpers
-------
- `matcher/helpers.py`
  - IP and port matching helpers
  - Service name resolution
  - Interface wildcard matching

Output
------
- `ui/output.py`
  - `format_table(result: MatchResult) -> str`
  - `format_json(result: MatchResult) -> str`

Programmatic usage example
--------------------------
```python
from parser.config_parser import parse_config
from parser.firewall_extractor import extract_firewall
from matcher.engine import MatchingEngine, TrafficTuple

config = extract_firewall(parse_config(open("sample_config.boot").read()))
engine = MatchingEngine(config)

traffic = TrafficTuple(
    inbound_interface="eth0",
    outbound_interface="eth1",
    source_ip="10.0.0.1",
    destination_ip="192.168.0.10",
    protocol="tcp",
    port=443,
)

result = engine.match(traffic)
print(result.action, result.chain_name, result.rule_number)
```
