"""Parser for VyOS hierarchical (curly-brace) boot configuration files.

Parses config like:
    firewall {
        ipv4 {
            forward {
                filter {
                    default-action accept
                    rule 10 {
                        action drop
                        source {
                            address 10.0.0.0/8
                        }
                    }
                }
            }
        }
    }

Into a nested dict structure.
"""

from __future__ import annotations

import re
from typing import Union

# Type alias for the parsed config tree
ConfigTree = dict[str, Union[str, list[str], "ConfigTree"]]


def parse_config(text: str) -> ConfigTree:
    """Parse a VyOS hierarchical boot config string into a nested dict.

    Tag nodes (e.g. ``rule 10 { ... }``) produce nested dicts:
        {"rule": {"10": {...}}}

    Repeated leaf keys (e.g. multiple ``address`` lines) produce lists.

    Valueless leaves (e.g. ``established`` inside ``state { }``) are stored
    with an empty-string value.
    """
    tokens = _tokenize(text)
    result, _ = _parse_block(tokens, 0)
    return result


def parse_config_file(path: str) -> ConfigTree:
    """Read and parse a VyOS boot config file."""
    with open(path, "r", encoding="utf-8") as f:
        return parse_config(f.read())


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

# Token types
_TOKEN_OPEN = "{"
_TOKEN_CLOSE = "}"
_TOKEN_WORD = "WORD"
_TOKEN_NEWLINE = "NL"

_TOKEN_RE = re.compile(
    r"""
      (?P<open>\{)
    | (?P<close>\})
    | (?P<comment>/\*.*?\*/)           # block comments
    | (?P<line_comment>//[^\n]*)       # line comments
    | (?P<hash_comment>\#[^\n]*)       # hash comments
    | (?P<newline>\n)                  # newlines (for disambiguating valueless leaves)
    | (?P<quoted>'[^']*'|"[^"]*")      # quoted strings
    | (?P<word>[^\s{}'\"]+)            # bare words
    """,
    re.VERBOSE | re.DOTALL,
)


def _tokenize(text: str) -> list[tuple[str, str]]:
    """Tokenize the config text into a list of (type, value) pairs.

    Newlines are emitted as ``_TOKEN_NEWLINE`` tokens so the parser can
    distinguish ``key value`` (same line) from two consecutive valueless
    leaves on separate lines.  Consecutive newlines are collapsed into one.
    """
    tokens: list[tuple[str, str]] = []
    for m in _TOKEN_RE.finditer(text):
        if m.group("open"):
            tokens.append((_TOKEN_OPEN, "{"))
        elif m.group("close"):
            tokens.append((_TOKEN_CLOSE, "}"))
        elif m.group("comment") or m.group("line_comment") or m.group("hash_comment"):
            continue  # skip comments
        elif m.group("newline"):
            # Collapse consecutive newlines and skip if last token is already NL
            if tokens and tokens[-1][0] == _TOKEN_NEWLINE:
                continue
            tokens.append((_TOKEN_NEWLINE, "\n"))
        elif m.group("quoted"):
            # Strip surrounding quotes
            val = m.group("quoted")[1:-1]
            tokens.append((_TOKEN_WORD, val))
        elif m.group("word"):
            tokens.append((_TOKEN_WORD, m.group("word")))
    return tokens


# ---------------------------------------------------------------------------
# Recursive-descent parser
# ---------------------------------------------------------------------------


def _parse_block(tokens: list[tuple[str, str]], pos: int) -> tuple[ConfigTree, int]:
    """Parse a block of key-value pairs / sub-blocks.

    Returns (parsed_dict, new_position).

    Newline tokens are used to disambiguate ``key value`` (same line) from
    two consecutive valueless leaves on separate lines.
    """
    result: ConfigTree = {}
    while pos < len(tokens):
        tok_type, tok_val = tokens[pos]

        # Skip newlines at the statement boundary
        if tok_type == _TOKEN_NEWLINE:
            pos += 1
            continue

        if tok_type == _TOKEN_CLOSE:
            # End of current block
            return result, pos + 1

        if tok_type != _TOKEN_WORD:
            pos += 1
            continue

        key = tok_val
        pos += 1

        if pos >= len(tokens):
            # Bare key at end of input (valueless leaf)
            _insert(result, key, "")
            break

        next_type, next_val = tokens[pos]

        if next_type == _TOKEN_OPEN:
            # key { ... }  — sub-block with no tag
            pos += 1  # skip '{'
            child, pos = _parse_block(tokens, pos)
            _insert(result, key, child)

        elif next_type == _TOKEN_NEWLINE:
            # Key followed by a newline → valueless leaf
            _insert(result, key, "")
            # Don't consume the newline — the loop will skip it

        elif next_type == _TOKEN_CLOSE:
            # Valueless leaf at end of block (e.g. ``established`` inside state)
            _insert(result, key, "")
            # Don't consume the '}' — let the caller handle it

        elif next_type == _TOKEN_WORD:
            # key followed by another word on the same line.
            # Could be:
            #   key value           (leaf)
            #   key tag { ... }     (tag node)
            value = next_val
            pos += 1

            # Skip any newlines between the value/tag and what follows
            while pos < len(tokens) and tokens[pos][0] == _TOKEN_NEWLINE:
                pos += 1

            if pos < len(tokens) and tokens[pos][0] == _TOKEN_OPEN:
                # key tag { ... }  — tag node
                pos += 1  # skip '{'
                child, pos = _parse_block(tokens, pos)
                # Store as key -> {tag: child}
                if key not in result:
                    result[key] = {}
                container = result[key]
                if isinstance(container, dict):
                    container[value] = child
                else:
                    # Key was previously a leaf; convert to tag node
                    result[key] = {value: child}
            else:
                # key value  — simple leaf
                _insert(result, key, value)

        else:
            _insert(result, key, "")

    return result, pos


def _insert(tree: ConfigTree, key: str, value: Union[str, dict, list]) -> None:
    """Insert a key-value pair into the tree, handling repeated keys.

    If the key already exists:
      - Two string values → convert to list
      - Existing list → append
      - Two dicts → merge
    """
    if key not in tree:
        tree[key] = value
        return

    existing = tree[key]

    # Both dicts: merge
    if isinstance(existing, dict) and isinstance(value, dict):
        for k, v in value.items():
            if k in existing:
                # Recurse for nested merging
                if isinstance(existing[k], dict) and isinstance(v, dict):
                    existing[k].update(v)
                else:
                    _insert(existing, k, v)
            else:
                existing[k] = v
        return

    # Convert to list or append
    if isinstance(existing, list):
        if isinstance(value, list):
            existing.extend(value)
        else:
            existing.append(value)
    else:
        tree[key] = [existing, value]
