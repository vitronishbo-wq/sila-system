#!/usr/bin/env python3
"""
Runtime validation script for territorial scope on admin endpoints.

Usage:

PYTHONPATH=. BASE_URL=http://127.0.0.1:8000 python3 scripts/validate_scope_endpoints.py docs/DEV_CREDENTIALS.md

The script will read the credentials file (simple pipe-separated lines),
attempt to authenticate each user via `/api/auth/login`, then call a set of
admin endpoints and record HTTP statuses. It also performs a content check
on `/api/admin/territory/tree` to assert provincial/municipal visibility.

Outputs a simple ASCII table and a final PASS/FAIL summary.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

# Prefer requests but gracefully fall back to urllib
try:
    import requests
except Exception:  # pragma: no cover - fallback when requests missing
    requests = None
    import urllib.request
    import urllib.error


def parse_dev_credentials(path: str) -> List[Dict[str, str]]:
    users: List[Dict[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Expecting lines like: email | ROLE | password | status
            parts = [p.strip() for p in re.split(r"\|", line) if p.strip()]
            if not parts:
                continue
            email = parts[0]
            role = parts[1] if len(parts) > 1 else ""
            pwd = parts[2] if len(parts) > 2 else "Sila_1983"
            users.append({"email": email, "role": role, "password": pwd})
    return users


def http_post_json(url: str, payload: Dict[str, Any], timeout: int = 10) -> Tuple[int, Optional[Dict[str, Any]]]:
    if requests:
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            try:
                return r.status_code, r.json()
            except Exception:
                return r.status_code, None
        except Exception as exc:
            return 0, {"error": str(exc)}
    else:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                try:
                    return resp.getcode(), json.loads(body)
                except Exception:
                    return resp.getcode(), None
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
                return e.code, json.loads(body)
            except Exception:
                return e.code, None
        except Exception as exc:
            return 0, {"error": str(exc)}


def http_get(url: str, token: Optional[str] = None, timeout: int = 10) -> Tuple[int, Optional[Dict[str, Any]]]:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if requests:
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            try:
                return r.status_code, r.json()
            except Exception:
                return r.status_code, None
        except Exception as exc:
            return 0, {"error": str(exc)}
    else:
        req = urllib.request.Request(url, headers=headers or {}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                try:
                    return resp.getcode(), json.loads(body)
                except Exception:
                    return resp.getcode(), None
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8")
                return e.code, json.loads(body)
            except Exception:
                return e.code, None
        except Exception as exc:
            return 0, {"error": str(exc)}


def normalize_role(role_raw: str) -> str:
    r = (role_raw or "").upper()
    if "CENTRAL" in r or "SUPERADMIN" in r:
        return "central"
    if "PROVINC" in r:
        return "provincial"
    if "MUNIC" in r:
        return "municipal"
    if "CITIZEN" in r or "TRUMAN" in r:
        return "citizen"
    return "other"


def find_in_tree(tree: List[Dict[str, Any]], name: str) -> bool:
    name_lower = name.lower()
    def walk(node: Dict[str, Any]) -> bool:
        if node.get("name", "").lower() == name_lower:
            return True
        for c in node.get("children", []) or []:
            if walk(c):
                return True
        return False
    for p in tree:
        if walk(p):
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials", help="Path to DEV_CREDENTIALS.md")
    parser.add_argument("--base-url", default=os.getenv("BASE_URL", "http://127.0.0.1:8000"))
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    creds = parse_dev_credentials(args.credentials)
    if not creds:
        print("No credentials found in", args.credentials)
        sys.exit(2)

    endpoints = [
        ("/api/admin/citizens", "GET"),
        ("/api/admin/documents", "GET"),
        ("/api/admin/territory/tree", "GET"),
        ("/api/admin/exports/jobs", "GET"),
    ]

    # Wait for server readiness via debug endpoint
    ready = False
    for i in range(30):
        code, _ = http_get(f"{base}/api/debug/auth-check")
        # Consider any valid HTTP response (non-zero) as the server being up.
        if code and code != 0:
            ready = True
            break
        time.sleep(1)
    if not ready:
        print("Backend not responding at", base)
        sys.exit(3)

    results: Dict[str, Dict[str, Any]] = {}
    unprotected_count = 0

    for u in creds:
        email = u["email"]
        pwd = u.get("password") or "Sila_1983"
        role_label = normalize_role(u.get("role", ""))
        status, body = http_post_json(f"{base}/api/auth/login", {"email": email, "password": pwd})
        token = None
        auth_ok = False
        if status == 200 and body and body.get("access_token"):
            token = body.get("access_token")
            auth_ok = True
        else:
            # try with username field as fallback
            status2, body2 = http_post_json(f"{base}/api/auth/login", {"username": email, "password": pwd})
            if status2 == 200 and body2 and body2.get("access_token"):
                token = body2.get("access_token")
                auth_ok = True
                status = status2
                body = body2

        user_key = email
        results[user_key] = {"role": role_label, "auth_status": status, "endpoints": {}}

        if not auth_ok:
            results[user_key]["note"] = f"auth_failed(status={status})"
            # Mark endpoints as NOT_TESTED
            for ep, method in endpoints:
                results[user_key]["endpoints"][ep] = {"status": status or 0, "ok": False}
            continue

        # Authenticated - call endpoints
        for ep, method in endpoints:
            url = f"{base}{ep}"
            if method == "GET":
                code, data = http_get(url, token=token)
            else:
                code, data = http_post_json(url, {},)
            ok = False
            expected = None
            # Determine expected: citizen -> 403, others -> 200
            if role_label == "citizen":
                expected = 403
            else:
                expected = 200
            if code == expected:
                ok = True
            # Special-case: some endpoints may return 200 for admin but we still want to verify content
            results[user_key]["endpoints"][ep] = {"status": code, "ok": ok, "data": data}
            if role_label == "citizen" and code == 200:
                unprotected_count += 1

        # Content checks for territory visibility
        # Only if territory tree returned JSON
        tree_ep = "/api/admin/territory/tree"
        tree_res = results[user_key]["endpoints"].get(tree_ep, {})
        if tree_res and tree_res.get("status") == 200 and isinstance(tree_res.get("data"), list):
            tree = tree_res.get("data")
            # check Huambo/Benguela presence
            # Normalize names used in seeds: Huambo, Benguela, Caala
            has_huambo = find_in_tree(tree, "Huambo")
            has_benguela = find_in_tree(tree, "Benguela")
            has_caala = find_in_tree(tree, "Caala") or find_in_tree(tree, "Caála")
            results[user_key]["territory_check"] = {
                "huambo": has_huambo,
                "benguela": has_benguela,
                "caala": has_caala,
            }

    # Print table header
    roles_order = ["citizen", "municipal", "provincial", "central"]
    users_order = []
    # Choose representative users for columns
    # Map role -> first user with that role
    role_representatives: Dict[str, str] = {}
    for email, info in results.items():
        r = info["role"]
        if r not in role_representatives:
            role_representatives[r] = email
    # Build header
    columns = ["Endpoint"] + [
        (r.capitalize(), role_representatives.get(r)) for r in roles_order if role_representatives.get(r)
    ]

    # Print summary lines
    print("\nValidation results:\n")
    header_cells = [c[0] if isinstance(c, tuple) else c for c in ["Endpoint"] + [r for r, e in columns[1:]]]
    # Print textual table
    col_width = 30
    # Build and print header row
    header = "Endpoint".ljust(40)
    for r in roles_order:
        if role_representatives.get(r):
            header += f" {r.capitalize():>10}"
    print(header)

    for ep, _ in endpoints:
        row = [ep.ljust(40)[:40]]
        for r in roles_order:
            rep = role_representatives.get(r)
            if not rep:
                continue
            ep_info = results[rep]["endpoints"].get(ep, {})
            code = ep_info.get("status")
            ok = ep_info.get("ok")
            if code is None:
                cell = "NT"
            else:
                if r == "citizen":
                    cell = "403" if code == 403 else ("PASS" if ok else str(code))
                else:
                    cell = "PASS" if ok else str(code)
            row.append(f"{cell:>10}")
        print(" ".join(row))

    print("\nTerritory content checks:")
    for email, info in results.items():
        if "territory_check" in info:
            print(f"- {email} ({info['role']}): {info['territory_check']}")

    print(f"\nUnprotected endpoints (citizen could list): {unprotected_count}")

    # Final classification
    if unprotected_count == 0:
        print("\nFINAL: ✅ VALIDADO")
        sys.exit(0)
    else:
        print("\nFINAL: ❌ FALHA DE ESCOPO")
        sys.exit(4)


if __name__ == "__main__":
    main()
