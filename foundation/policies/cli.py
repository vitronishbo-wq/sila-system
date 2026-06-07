"""Simple CLI to inspect and update in-memory/persisted policies.

Usage:
  python -m foundation.policies.cli list
  python -m foundation.policies.cli get MAX_PENDING_DEBT
  python -m foundation.policies.cli set MAX_PENDING_DEBT 10
  python -m foundation.policies.cli export ./policies.json
  python -m foundation.policies.cli import ./policies.json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .engine import policy_engine


def parse_value(raw: str) -> Any:
    # Try to interpret as JSON first, fallback to string or int/float
    try:
        return json.loads(raw)
    except Exception:
        # try int/float
        try:
            if "." in raw:
                return float(raw)
            return int(raw)
        except Exception:
            return raw


def cmd_list(args: argparse.Namespace) -> int:
    data = policy_engine.list_policies()
    print(json.dumps(data, indent=2, default=str))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    v = policy_engine.get_policy(args.name, args.default)
    print(json.dumps(v, indent=2, default=str))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    val = parse_value(args.value)
    policy_engine.update_policy(args.name, val)
    print(f"OK: {args.name} -> {val}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    data = policy_engine.list_policies()
    with open(args.path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Exported to {args.path}")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    with open(args.path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        print("Expected a JSON object mapping policy names to values", file=sys.stderr)
        return 2
    for name, val in raw.items():
        policy_engine.update_policy(name, val)
    print(f"Imported {len(raw)} policies")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="policy-cli")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list")

    g = sub.add_parser("get")
    g.add_argument("name")
    g.add_argument("--default", default=None)

    s = sub.add_parser("set")
    s.add_argument("name")
    s.add_argument("value")

    e = sub.add_parser("export")
    e.add_argument("path")

    i = sub.add_parser("import")
    i.add_argument("path")

    args = p.parse_args(argv)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "get":
        return cmd_get(args)
    if args.cmd == "set":
        return cmd_set(args)
    if args.cmd == "export":
        return cmd_export(args)
    if args.cmd == "import":
        return cmd_import(args)
    p.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
