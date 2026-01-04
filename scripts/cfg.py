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

from parse_bril import load_bril_json


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


program = load_bril_json(Path("add.json"))
functions = program["functions"]
print([fn["name"] for fn in functions])