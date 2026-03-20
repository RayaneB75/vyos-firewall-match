Architecture
============

This document describes how the program parses a VyOS boot configuration and
evaluates firewall rules for a traffic tuple.

Directory layout
----------------
- `policy_matcher.py` entry point
- `parser/` config parsing and extraction
- `matcher/` matching engine and helpers
- `ui/` CLI argument handling and output formatting
- `tests/` pytest suite

Execution flow
--------------
1. `policy_matcher.py` parses CLI args and reads the config file
2. `parser/config_parser.py` tokenizes and builds a config tree
3. `parser/firewall_extractor.py` converts the tree to typed models
4. `matcher/engine.py` evaluates rules against the traffic tuple
5. `ui/output.py` formats the result (table or JSON)

Config parsing
--------------
The parser consumes the hierarchical boot format and preserves valueless
leaves. For example:

```
state {
  established
  related
}
```

is stored as keys under `state`, and repeated leaves (e.g. `state "foo"` lines)
are supported.

Models
------
- `FirewallConfig` contains groups, chains, and state-policy
- `FirewallChain` holds rules and default-action
- `FirewallRule` stores criteria and action
- `SourceDestMatch` and `InterfaceMatch` represent criteria blocks

Matching engine
---------------
- Determines hook: `forward` by default, or explicit `--hook`
- Determines address family from source/destination IPs
- Evaluates the corresponding base chain (`<hook>-filter`)
- Supports `jump`, `continue`, `return`, and default-actions
- Rules use AND semantics across criteria
- Rules without destination criteria match any destination

Group resolution
----------------
Group references are resolved via `FirewallConfig.get_group`. For IPv6 rules
that reference non-IPv6 group names, the matcher will attempt the IPv6 group
types (`ipv6-network`, `ipv6-address`) when the primary lookup fails.

Address mask matching
---------------------
If a rule includes `address-mask`, the matcher uses bitmask matching:

```
(ip & mask) == (address & mask)
```

This is equivalent to netfilter `--src-mask` / `--dst-mask` behavior.

Output formatting
-----------------
- Table output includes a trace of rule evaluation
- JSON output provides a structured result object
