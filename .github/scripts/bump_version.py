#!/usr/bin/env python3
"""Bump project version in setup.py and package __init__.py."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETUP_PY = ROOT / "setup.py"
INIT_PY = ROOT / "vyfwmatch" / "__init__.py"


def _replace_version(path: Path, pattern: str, replacement: str) -> None:
    content = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, content, count=1)
    if count != 1:
        raise RuntimeError(f"Failed to update version in {path}")
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <version>", file=sys.stderr)
        return 1

    version = sys.argv[1].strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        print(f"Invalid semantic version: {version}", file=sys.stderr)
        return 1

    _replace_version(SETUP_PY, r'version="[^"]+"', f'version="{version}"')
    _replace_version(INIT_PY, r'__version__ = "[^"]+"', f'__version__ = "{version}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
