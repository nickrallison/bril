#!/usr/bin/env python3
"""Load and lightly validate Bril JSON (e.g. add.json).

Usage:
  python3 scripts/parse_add.py add.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_bril_json(path: Path) -> dict[str, Any]:
    """Open and parse a Bril JSON file.

    Returns the parsed JSON object (expected to be a dict).
    Raises ValueError with a readable message on schema issues.
    """

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Could not read {path}: {exc}") from exc

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path} at line {exc.lineno}, col {exc.colno}: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Expected top-level JSON object in {path}, got {type(data).__name__}")

    functions = data.get("functions")
    if not isinstance(functions, list):
        raise ValueError(f"Expected 'functions' to be a list in {path}")

    for i, fn in enumerate(functions):
        if not isinstance(fn, dict):
            raise ValueError(f"Expected functions[{i}] to be an object, got {type(fn).__name__}")
        if not isinstance(fn.get("name"), str):
            raise ValueError(f"Expected functions[{i}]['name'] to be a string")
        instrs = fn.get("instrs")
        if not isinstance(instrs, list):
            raise ValueError(f"Expected functions[{i}]['instrs'] to be a list")

    return data


def main(argv: list[str]) -> int:
    json_path = Path(argv[1]) if len(argv) > 1 else Path("add.json")

    try:
        program = load_bril_json(json_path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    functions = program["functions"]
    print(f"Loaded {json_path}: {len(functions)} function(s)")
    for fn in functions:
        name = fn["name"]
        instrs = fn["instrs"]
        print(f"- {name}: {len(instrs)} instruction(s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
