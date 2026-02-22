#!/usr/bin/env python3
"""
SILA Pre-commit Report Generator
Consolida resultados de todos os hooks em relatório unificado
"""

import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports" / "pre-commit"


def load_hook_results():
    """Carrega resultados de todos os hooks."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "hooks": {},
        "summary": {"total": 0, "passed": 0, "failed": 0},
    }

    # Dependency validation report
    deps_report = REPORTS_DIR / "deps_validation.json"
    if deps_report.exists():
        with deps_report.open() as f:
            deps_data = json.load(f)
            has_issues = bool(
                deps_data.get("invalid")
                or deps_data.get("missing")
                or deps_data.get("blocked")
            )
            results["hooks"]["validate-deps"] = {
                "status": "FAIL" if has_issues else "PASS",
                "data": deps_data,
            }
    else:
        results["hooks"]["validate-deps"] = {
            "status": "SKIP",
            "reason": "No report found",
        }

    # Structure validation (assume success if no error file)
    structure_error = REPORTS_DIR / "structure_error.log"
    results["hooks"]["validate-structure"] = {
        "status": "FAIL" if structure_error.exists() else "PASS"
    }

    # Docker validation (assume success if no error file)
    docker_error = REPORTS_DIR / "docker_error.log"
    results["hooks"]["validate-docker"] = {
        "status": "FAIL" if docker_error.exists() else "PASS"
    }

    # Calculate summary
    for hook_name, hook_data in results["hooks"].items():
        results["summary"]["total"] += 1
        if hook_data["status"] == "PASS":
            results["summary"]["passed"] += 1
        elif hook_data["status"] == "FAIL":
            results["summary"]["failed"] += 1

    return results


def generate_html_report(data):
    """Gera relatório HTML."""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SILA Pre-commit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; }}
        .hook {{ margin: 10px 0; padding: 15px; border-left: 4px solid #ccc; }}
        .hook.pass {{ border-color: #28a745; background: #d4edda; }}
        .hook.fail {{ border-color: #dc3545; background: #f8d7da; }}
        .hook.skip {{ border-color: #ffc107; background: #fff3cd; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔧 SILA Pre-commit Report</h1>
        <p>Generated: {data['timestamp']}</p>
    </div>

    <div class="summary">
        <div class="metric">
            <h3>{data['summary']['total']}</h3>
            <p>Total Hooks</p>
        </div>
        <div class="metric">
            <h3>{data['summary']['passed']}</h3>
            <p>Passed</p>
        </div>
        <div class="metric">
            <h3>{data['summary']['failed']}</h3>
            <p>Failed</p>
        </div>
    </div>

    <h2>Hook Results</h2>
"""

    for hook_name, hook_data in data["hooks"].items():
        status_class = hook_data["status"].lower()
        status_icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️"}.get(
            hook_data["status"], "❓"
        )

        html += f"""
    <div class="hook {status_class}">
        <h3>{status_icon} {hook_name}</h3>
        <p>Status: <strong>{hook_data["status"]}</strong></p>
"""

        if "data" in hook_data:
            html += f"<pre>{json.dumps(hook_data['data'], indent=2)}</pre>"

        html += "</div>"

    html += """
</body>
</html>
"""
    return html


def main():
    """Gera relatório consolidado."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load results
    results = load_hook_results()

    # Save JSON report
    json_report = REPORTS_DIR / "precommit_summary.json"
    with json_report.open("w") as f:
        json.dump(results, f, indent=2)

    # Generate HTML report
    html_content = generate_html_report(results)
    html_report = REPORTS_DIR / "precommit_summary.html"
    with html_report.open("w") as f:
        f.write(html_content)

    print(f"📊 Pre-commit reports generated:")
    print(f"   JSON: {json_report}")
    print(f"   HTML: {html_report}")

    # Summary
    total = results["summary"]["total"]
    passed = results["summary"]["passed"]
    failed = results["summary"]["failed"]

    print(f"\n📈 Summary: {passed}/{total} hooks passed")

    if failed > 0:
        print("⚠️ Some hooks failed - check the reports for details")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
