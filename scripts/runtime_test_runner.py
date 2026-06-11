#!/usr/bin/env python3
"""
Simple runtime test runner for SILA access enforcement.

Usage:
  BASE_URL=http://localhost:8000 python3 scripts/runtime_test_runner.py reports/ENDPOINTS_TO_TEST.json

The script:
 - Generates tokens for a set of test profiles using `JWTHandler` from the repo
 - Executes each endpoint with each profile
 - Saves results to `reports/RUNTIME_TEST_RESULTS.json`

Note: install `requests` if missing: `pip install requests`
"""
import json
import os
import sys
from datetime import timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APPS_BACKEND = os.path.join(ROOT, "apps", "backend")
if APPS_BACKEND not in sys.path:
    sys.path.insert(0, APPS_BACKEND)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

print("DEBUG: before importing requests", flush=True)
try:
    import requests
    print("DEBUG: requests imported", flush=True)
except Exception:
    print("Missing dependency 'requests'. Install with: pip install requests", flush=True)
    raise

print("DEBUG: before importing project JWTHandler/settings", flush=True)
try:
    from apps.backend.core.auth.jwt_handler import JWTHandler
    from apps.backend.app.core.settings import settings
    print("DEBUG: imported JWTHandler and settings", flush=True)
except Exception as e:
    print("Failed to import project JWT/Settings. Ensure script is run from repo root and PYTHONPATH includes project root.", flush=True)
    raise

BASE_URL = os.environ.get("BASE_URL") or settings.API_BASE_URL

RESULTS_PATH = os.path.join(ROOT, "reports", "RUNTIME_TEST_RESULTS.json")

# Request timeout (seconds) - can be overridden via env REQUEST_TIMEOUT
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "3"))

# Default trust headers (high score to avoid TrustEvaluationMiddleware blocking)
TRUST_HEADERS = {
    "X-Device-Score": os.environ.get("X_DEVICE_SCORE", "0.98"),
    "X-Biometric-Score": os.environ.get("X_BIOMETRIC_SCORE", "0.98"),
    "X-Behavior-Score": os.environ.get("X_BEHAVIOR_SCORE", "0.98"),
    "X-MFA-Token": os.environ.get("X_MFA_TOKEN", "mfa-test"),
}

# Test profiles (customize as needed)
PROFILES = {
    "citizen": {"email": "citizen@example.com", "realm_access": {"roles": ["CITIZEN"]}, "territory_id": "mun-001"},
    "municipal_admin": {"email": "mun001-admin@example.com", "realm_access": {"roles": ["MANAGER"]}, "territory_id": "mun-001"},
    "provincial_admin": {"email": "prov001-admin@example.com", "realm_access": {"roles": ["MANAGER"]}, "territory_id": "prov-001"},
    "central_admin": {"email": "admin-central@example.com", "realm_access": {"roles": ["ADMIN"]}},
    "super_admin": {"email": "root@example.com", "realm_access": {"roles": ["SUPERADMIN"]}},
}


def load_endpoints(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_token(claims: dict[str, any]) -> str:
    handler = JWTHandler(secret_key=settings.SECRET_KEY)
    subject = claims.get("email") or claims.get("sub") or "test-user"
    # copy claims to avoid mutation
    data = dict(claims)
    return handler.create_access_token(subject=subject, data=data)


def perform_request(method: str, url: str, token: str, headers: dict, params=None, json_body=None):
    hdrs = dict(headers or {})
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.request(method=method.upper(), url=url, headers=hdrs, params=params, json=json_body, timeout=REQUEST_TIMEOUT)
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        return {"status_code": resp.status_code, "headers": dict(resp.headers), "body": body}
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/runtime_test_runner.py <endpoints.json>")
        sys.exit(1)

    endpoints_file = sys.argv[1]
    if not os.path.exists(endpoints_file):
        print(f"Endpoints file not found: {endpoints_file}")
        sys.exit(2)

    endpoints = load_endpoints(endpoints_file)

    results = {"base_url": BASE_URL, "tests": []}

    # pre-generate tokens for profiles
    tokens = {}
    for name, claims in PROFILES.items():
        tokens[name] = make_token(claims)

    for ep in endpoints:
        method = ep.get("method", "GET")
        raw_path = ep.get("path")
        path_params = ep.get("path_params", {}) or {}
        query_params = ep.get("query_params", {}) or {}
        body = ep.get("body")
        description = ep.get("description")

        # format path with path_params if present
        try:
            path = raw_path.format(**path_params) if path_params else raw_path
        except Exception:
            path = raw_path

        url = BASE_URL.rstrip("/") + path

        ep_result = {"path": path, "method": method, "description": description, "by_profile": {}}

        # anonymous (no token) check
        print(f"DEBUG: requesting ANON {method} {url}", flush=True)
        anon = perform_request(method, url, token=None, headers=TRUST_HEADERS, params=query_params, json_body=body)
        print(f"DEBUG: ANON result {method} {url} -> {anon.get('status_code') if anon else 'ERR'}", flush=True)
        ep_result["anonymous"] = anon

        for profile_name, token in tokens.items():
            print(f"DEBUG: requesting {profile_name.upper()} {method} {url}", flush=True)
            res = perform_request(method, url, token=token, headers=TRUST_HEADERS, params=query_params, json_body=body)
            print(f"DEBUG: {profile_name.upper()} result {method} {url} -> {res.get('status_code') if res else 'ERR'}", flush=True)
            ep_result["by_profile"][profile_name] = res

        results["tests"].append(ep_result)

    # save
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Results written to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
