#!/usr/bin/env python3
"""
validate_frontend_backend_integration.py
---------------------------------------
Enterprise-grade integration & diagnostic runner between frontend and backend.

Features:
- Health and connectivity checks (health, status endpoints)
- API calls simulation (GET/POST/OPTIONS) including auth token injection
- Retries with exponential backoff and jitter
- Parallel execution of endpoint tests
- CORS preflight validation (OPTIONS)
- Latency measurement, 95/99 percentiles, and basic SLA checks
- Circuit-breaker-like suppression for flaky endpoints
- Output: JSON, Markdown, HTML (with optional graph if matplotlib available)
- Optional context file (--context-file) in JSON/YAML to augment tests
- CI/CD friendly: exit code != 0 if critical failures
- Dry-run mode and verbose logging
"""

import argparse
import json
import logging
import math
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from statistics import median, quantiles
from typing import Any

import requests

# Optional extras
try:
    import yaml

    HAS_YAML = True
except Exception:
    yaml = None
    HAS_YAML = False

try:
    import matplotlib.pyplot as plt

    HAS_PLOT = True
except Exception:
    HAS_PLOT = False

# ================
# Config / Defaults
# ================
DEFAULT_TIMEOUT = 8.0  # seconds
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.5  # base for exponential backoff
MAX_WORKERS = 8
CIRCUIT_BREAKER_THRESHOLD = 3  # failures before temporary suppress
CIRCUIT_BREAKER_TIMEOUT = 30  # seconds to wait after tripping

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("sila-integration")

# Default endpoints to test (will be extended if context file provided)
DEFAULT_ENDPOINTS = [
    {
        "name": "Backend Health",
        "method": "GET",
        "url": "http://localhost:8000/health",
        "critical": True,
    },
    {
        "name": "OpenAPI Schema",
        "method": "GET",
        "url": "http://localhost:8000/openapi.json",
        "critical": False,
    },
    {
        "name": "Auth Login",
        "method": "POST",
        "url": "http://localhost:8000/api/auth/login",
        "critical": True,
        "payload": {"username": "test", "password": "test"},
        "expect_status": [200, 401, 422],
    },
    {
        "name": "User Profile",
        "method": "GET",
        "url": "http://localhost:8000/api/user/me",
        "auth": True,
        "critical": True,
        "expect_status": [200, 401, 403],
    },
    {
        "name": "List Items",
        "method": "GET",
        "url": "http://localhost:8000/api/items",
        "auth": False,
        "critical": False,
    },
    {
        "name": "CORS Preflight",
        "method": "OPTIONS",
        "url": "http://localhost:8000/api/items",
        "critical": False,
        "headers": {
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    },
    {
        "name": "Frontend Root",
        "method": "GET",
        "url": "http://localhost:5173/",
        "critical": False,
    },
]


# ============
# Helpers
# ============
def now_ts():
    return datetime.utcnow().isoformat() + "Z"


def safe_json(obj):
    try:
        return json.dumps(obj, indent=2, default=str)
    except Exception:
        return str(obj)


def load_context_file(path: str) -> dict[str, Any]:
    """Load JSON or YAML file as context, return dict."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="ignore")
    # try json
    try:
        return json.loads(text)
    except Exception:
        pass
    # try yaml
    if HAS_YAML and yaml:
        try:
            return yaml.safe_load(text)
        except Exception:
            pass
    # nothing recognized
    raise ValueError("Context file not JSON/YAML or unparseable")


def run_cmd(cmd: list[str], capture: bool = False) -> tuple[bool, str | None]:
    """Execute command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stdout
        else:
            result = subprocess.run(cmd, timeout=10)
            return result.returncode == 0, None
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        return False, None


# ============
# HTTP Session with Retries
# ============
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session(timeout: float, max_retries: int = MAX_RETRIES):
    s = requests.Session()
    retries = Retry(
        total=max_retries,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"]),
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.request_timeout = timeout
    return s


# ============
# Circuit breaker manager
# ============
class CircuitManager:
    def __init__(self, threshold=CIRCUIT_BREAKER_THRESHOLD, timeout=CIRCUIT_BREAKER_TIMEOUT):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = {}  # endpoint_name -> count
        self.tripped_at = {}  # endpoint_name -> timestamp

    def record_failure(self, name: str):
        self.failures[name] = self.failures.get(name, 0) + 1
        if self.failures[name] >= self.threshold:
            self.tripped_at[name] = time.time()
            logger.warning(f"CIRCUIT TRIPPED for {name} (failures={self.failures[name]})")

    def record_success(self, name: str):
        self.failures[name] = 0
        self.tripped_at.pop(name, None)

    def is_tripped(self, name: str) -> bool:
        t = self.tripped_at.get(name)
        if not t:
            return False
        if time.time() - t > self.timeout:
            # reset
            logger.info(f"Circuit for {name} reset after timeout")
            self.failures[name] = 0
            self.tripped_at.pop(name, None)
            return False
        return True


# ============
# Core test logic
# ============
def do_request(
    session: requests.Session,
    ep: dict[str, Any],
    auth_token: str | None,
    timeout: float,
):
    """Perform one request attempt (single try without high-level retry)"""
    method = ep.get("method", "GET").upper()
    url = ep["url"]
    headers = dict(ep.get("headers", {}))
    if ep.get("auth") and auth_token:
        headers.setdefault("Authorization", f"Bearer {auth_token}")
    body = ep.get("payload")
    start = time.time()
    try:
        if method == "GET":
            r = session.get(url, headers=headers, timeout=timeout)
        elif method == "POST":
            r = session.post(url, json=body, headers=headers, timeout=timeout)
        elif method == "OPTIONS":
            r = session.options(url, headers=headers, timeout=timeout)
        else:
            r = session.request(method, url, json=body, headers=headers, timeout=timeout)
        duration = (time.time() - start) * 1000.0
        return {
            "ok": True,
            "status_code": r.status_code,
            "text": r.text[:2048],
            "duration_ms": round(duration, 2),
            "headers": dict(r.headers),
        }
    except requests.RequestException as e:
        duration = (time.time() - start) * 1000.0
        return {"ok": False, "error": str(e), "duration_ms": round(duration, 2)}


def test_endpoint_with_retries(
    session: requests.Session,
    ep: dict[str, Any],
    auth_token: str | None,
    timeout: float,
    max_retries: int,
    circuit: CircuitManager,
):
    """High-level test with backoff retries and circuit-breaker awareness."""
    name = ep.get("name", ep.get("url"))
    attempt = 0
    results = []
    if circuit.is_tripped(name):
        msg = f"SKIPPED (circuit tripped) - {name}"
        logger.warning(msg)
        return {
            "name": name,
            "skipped": True,
            "reason": "circuit_tripped",
            "results": [],
        }
    while attempt <= max_retries:
        attempt += 1
        backoff = (BACKOFF_FACTOR * (2 ** (attempt - 1))) + (
            0.1 * math.sin(attempt)
        )  # add tiny jitter
        res = do_request(session, ep, auth_token, timeout)
        results.append(res)
        # success heuristics: ok True and acceptable status
        if res.get("ok") and (
            str(res.get("status_code", "")).startswith("2")
            or (ep.get("expect_status") and res.get("status_code") in ep.get("expect_status"))
        ):
            circuit.record_success(name)
            return {
                "name": name,
                "skipped": False,
                "attempts": attempt,
                "results": results,
            }
        else:
            logger.debug(
                f"Attempt {attempt} for {name} failed: {res.get('error') or res.get('status_code')}"
            )
            circuit.record_failure(name)
            if attempt > max_retries:
                break
            time.sleep(min(backoff, 10))
    # final failure
    return {"name": name, "skipped": False, "attempts": attempt, "results": results}


# ============
# Aggregation & Metrics
# ============
def analyze_results(run_results: list[dict[str, Any]]):
    """Compute summary metrics and identify slow endpoints, error rates, etc."""
    summary = {"generated_at": now_ts(), "endpoints": []}
    total_calls = 0
    total_failures = 0
    latencies = []
    for r in run_results:
        name = r["name"]
        if r.get("skipped"):
            summary["endpoints"].append({"name": name, "status": "skipped", "details": r})
            continue
        attempts = r.get("attempts", 0)
        res_items = r.get("results", [])
        # take last attempt as representative
        last = res_items[-1] if res_items else {}
        ok = last.get("ok", False)
        status_code = last.get("status_code") if ok else None
        duration = last.get("duration_ms", None)
        total_calls += 1
        if not ok or not (status_code and str(status_code).startswith("2")):
            total_failures += 1
        if duration is not None:
            latencies.append(duration)
        summary["endpoints"].append(
            {
                "name": name,
                "ok": ok,
                "status_code": status_code,
                "attempts": attempts,
                "duration_ms": duration,
                "raw": last,
            }
        )
    if latencies:
        latencies_sorted = sorted(latencies)
        p95 = (
            quantiles(latencies_sorted, n=100)[94]
            if len(latencies_sorted) >= 100
            else (
                latencies_sorted[int(len(latencies_sorted) * 0.95) - 1]
                if latencies_sorted
                else None
            )
        )
        p99 = (
            quantiles(latencies_sorted, n=100)[98]
            if len(latencies_sorted) >= 100
            else (
                latencies_sorted[int(len(latencies_sorted) * 0.99) - 1]
                if latencies_sorted
                else None
            )
        )
        summary["latency_ms"] = {
            "median": median(latencies_sorted),
            "p95": p95,
            "p99": p99,
            "samples": len(latencies_sorted),
        }
    summary["totals"] = {"calls": total_calls, "failures": total_failures}
    return summary


# ============
# Reporters
# ============
def write_json_report(path: str, raw_results: list[dict[str, Any]], summary: dict[str, Any]):
    payload = {"raw_results": raw_results, "summary": summary, "ts": now_ts()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    logger.info(f"JSON report written to {path}")


def write_md_report(path: str, raw_results: list[dict[str, Any]], summary: dict[str, Any]):
    lines = []
    lines.append(f"# Integration Report\n\nGenerated: {now_ts()}\n")
    lines.append("## Summary\n")
    lines.append(f"- **Total calls:** {summary['totals']['calls']}\n")
    lines.append(f"- **Failures:** {summary['totals']['failures']}\n")
    if "latency_ms" in summary:
        lines.append("\n## Latency\n")
        lines.append(f"- **Median:** {summary['latency_ms']['median']} ms\n")
        lines.append(f"- **P95:** {summary['latency_ms'].get('p95')} ms\n")
        lines.append(f"- **P99:** {summary['latency_ms'].get('p99')} ms\n")
        lines.append(f"- **Samples:** {summary['latency_ms'].get('samples')} \n")
    lines.append("\n## Endpoints\n\n")
    for e in summary["endpoints"]:
        status = "✅" if e.get("ok") else "❌"
        lines.append(f"### {status} {e['name']}\n")
        lines.append(f"- **Status Code:** {e.get('status_code')}\n")
        lines.append(f"- **Attempts:** {e.get('attempts')}\n")
        lines.append(f"- **Duration:** {e.get('duration_ms')} ms\n\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    logger.info(f"Markdown report written to {path}")


def write_html_report(
    path: str,
    raw_results: list[dict[str, Any]],
    summary: dict[str, Any],
    graph_png: str | None = None,
):
    html = ["<html><head><meta charset='utf-8'><title>Integration Report</title>"]
    html.append(
        "<style>body{font-family:sans-serif}table{border-collapse:collapse}th,td{border:1px solid #ccc;padding:8px;text-align:left}th{background:#f0f0f0}tr.fail{background:#ffe0e0}</style>"
    )
    html.append("</head><body>")
    html.append(f"<h1>Integration Report</h1><p><small>Generated: {now_ts()}</small></p>")
    html.append("<h2>Summary</h2>")
    html.append("<ul>")
    html.append(f"<li><strong>Total calls:</strong> {summary['totals']['calls']}</li>")
    html.append(f"<li><strong>Failures:</strong> {summary['totals']['failures']}</li>")
    if "latency_ms" in summary:
        html.append("<li><strong>Latency:</strong> ")
        html.append(f"median {summary['latency_ms']['median']} ms")
        if summary["latency_ms"].get("p95"):
            html.append(f", p95 {summary['latency_ms']['p95']} ms")
        html.append("</li>")
    html.append("</ul>")
    html.append("<h2>Endpoints</h2><table border='1' cellpadding='6'>")
    html.append(
        "<tr><th>Endpoint</th><th>OK</th><th>Status</th><th>Attempts</th><th>Duration (ms)</th></tr>"
    )
    for e in summary["endpoints"]:
        rowclass = " class='fail'" if not e.get("ok") else ""
        html.append(
            f"<tr{rowclass}><td>{e['name']}</td><td>{e.get('ok')}</td><td>{e.get('status_code')}</td><td>{e.get('attempts')}</td><td>{e.get('duration_ms')}</td></tr>"
        )
    html.append("</table>")
    if graph_png and os.path.exists(graph_png):
        html.append(
            f"<h2>Latency Graph</h2><img src='{os.path.basename(graph_png)}' alt='latency graph' style='max-width:100%'>"
        )
    html.append("</body></html>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    logger.info(f"HTML report written to {path}")


def plot_latency(raw_results: list[dict[str, Any]], out_png: str):
    if not HAS_PLOT:
        logger.warning("matplotlib not available; skipping latency plot")
        return None
    # collect durations per endpoint (last attempt)
    names = []
    durations = []
    for r in raw_results:
        if r.get("skipped"):
            continue
        last = r.get("results")[-1] if r.get("results") else {}
        d = last.get("duration_ms")
        names.append(r.get("name"))
        durations.append(d if d is not None else 0)
    if not names:
        logger.warning("No latency data to plot")
        return None
    plt.figure(figsize=(10, 6))
    plt.barh(
        names,
        durations,
        color=["green" if d < 100 else "orange" if d < 500 else "red" for d in durations],
    )
    plt.xlabel("Duration (ms)")
    plt.title("Endpoint Latency (last attempt)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=100)
    plt.close()
    logger.info(f"Latency graph saved to {out_png}")
    return out_png


# ============
# CLI / Orchestration
# ============
def parse_args():
    p = argparse.ArgumentParser(description="Validate frontend-backend integration (SILA System)")
    p.add_argument(
        "--endpoints-file",
        "-e",
        help="JSON/YAML file with endpoints list (overrides defaults)",
        default=None,
    )
    p.add_argument(
        "--context-file",
        "-c",
        help="Optional project file to augment tests (JSON/YAML)",
        default=None,
    )
    p.add_argument(
        "--auth-token",
        help="Auth token to use for endpoints that require auth",
        default=None,
    )
    p.add_argument(
        "--auth-cmd",
        help="Command to run to retrieve auth token (e.g. ./scripts/get_dev_token.sh)",
        default=None,
    )
    p.add_argument("--timeout", type=float, help="Per-request timeout (s)", default=DEFAULT_TIMEOUT)
    p.add_argument("--retries", type=int, help="Max retries per endpoint", default=MAX_RETRIES)
    p.add_argument(
        "--parallel",
        type=int,
        help="Parallel worker count",
        default=min(MAX_WORKERS, os.cpu_count() or 4),
    )
    p.add_argument(
        "--output-dir",
        "-o",
        help="Directory to write reports",
        default="integration_reports",
    )
    p.add_argument(
        "--plot",
        action="store_true",
        help="Generate latency plot (requires matplotlib)",
        default=False,
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run (no real requests)",
        default=False,
    )
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging", default=False)
    return p.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("=== SILA Frontend-Backend Integration Validator ===")
    logger.info(f"Start time: {now_ts()}")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    # load endpoints
    endpoints = DEFAULT_ENDPOINTS.copy()
    if args.endpoints_file:
        try:
            data = load_context_file(args.endpoints_file)
            if isinstance(data, dict) and "endpoints" in data:
                endpoints = data["endpoints"]
            elif isinstance(data, list):
                endpoints = data
            else:
                logger.warning("endpoints-file didn't contain 'endpoints' key; using defaults")
        except Exception as e:
            logger.error(f"Failed to load endpoints-file: {e}")
            sys.exit(1)

    logger.info(f"Loaded {len(endpoints)} endpoints to test")

    # load project context (optional)
    if args.context_file:
        try:
            context = load_context_file(args.context_file)
            # If context contains base_url, patch endpoints
            base = context.get("base_url") if isinstance(context, dict) else None
            if base:
                for ep in endpoints:
                    if ep.get("url", "").startswith("http://localhost"):
                        # attempt to replace host part only
                        parsed = ep["url"].split("/", 3)
                        # keep path
                        if len(parsed) >= 4:
                            path = "/" + parsed[3]
                        else:
                            path = ""
                        ep["url"] = base.rstrip("/") + path
                logger.info(f"Context file applied: base_url={base}")
        except Exception as e:
            logger.warning(f"Ignoring context-file: {e}")

    # auth token retrieval
    auth_token = args.auth_token
    if not auth_token and args.auth_cmd:
        try:
            ok, out = run_cmd(args.auth_cmd.split(), capture=True)
            if ok and out:
                auth_token = out.strip()
                logger.info("Auth token retrieved from command")
        except Exception as e:
            logger.warning(f"Failed to run auth-cmd: {e}")

    if args.dry_run:
        logger.info("DRY-RUN MODE: No actual requests will be made")
        logger.info("Endpoint validation complete (dry-run)")
        sys.exit(0)

    # session
    session = make_session(args.timeout, max_retries=args.retries)
    circuit = CircuitManager()

    logger.info(
        f"Starting parallel tests ({args.parallel} workers, {args.timeout}s timeout, {args.retries} retries)"
    )

    # parallel execution
    results = []
    with ThreadPoolExecutor(max_workers=args.parallel) as exe:
        futures = {
            exe.submit(
                test_endpoint_with_retries,
                session,
                ep,
                auth_token,
                args.timeout,
                args.retries,
                circuit,
            ): ep
            for ep in endpoints
        }
        for fut in as_completed(futures):
            try:
                res = fut.result()
                results.append(res)
                logger.info(
                    f"✓ Completed: {res.get('name')} (skipped={res.get('skipped', False)}, attempts={res.get('attempts')})"
                )
            except Exception as e:
                ep = futures[fut]
                logger.error(f"✗ Exception testing {ep.get('name')}: {e}")
                results.append(
                    {
                        "name": ep.get("name"),
                        "skipped": False,
                        "attempts": 0,
                        "results": [{"ok": False, "error": str(e)}],
                    }
                )

    # analyze
    summary = analyze_results(results)

    # reporting
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    json_path = outdir / f"integration_report_{ts}.json"
    md_path = outdir / f"integration_report_{ts}.md"
    html_path = outdir / f"integration_report_{ts}.html"

    write_json_report(str(json_path), results, summary)
    write_md_report(str(md_path), results, summary)

    graph_png = None
    if args.plot and HAS_PLOT:
        graph_png = outdir / f"latency_{ts}.png"
        plot_latency(results, str(graph_png))

    write_html_report(str(html_path), results, summary, str(graph_png) if graph_png else None)

    logger.info(f"Reports written to {outdir}/")
    logger.info(f"- JSON: {json_path.name}")
    logger.info(f"- Markdown: {md_path.name}")
    logger.info(f"- HTML: {html_path.name}")
    if graph_png:
        logger.info(f"- Graph: {graph_png.name}")

    # exit code: non-zero if any critical endpoint failed
    critical_failures = 0
    for idx, r in enumerate(results):
        # find endpoint defn to see if critical
        if idx >= len(endpoints):
            break
        ep = endpoints[idx]
        if ep.get("critical", False):
            if r.get("skipped"):
                critical_failures += 1
            else:
                last = r.get("results")[-1] if r.get("results") else {}
                if not last.get("ok") or not str(last.get("status_code", "")).startswith("2"):
                    critical_failures += 1

    logger.info(
        f"Summary: {summary['totals']['calls']} calls, {summary['totals']['failures']} failures, {critical_failures} critical failures"
    )

    if critical_failures:
        logger.error(f"✗ {critical_failures} critical endpoint(s) failed or skipped")
        sys.exit(2)

    logger.info("✓ All critical endpoints OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
