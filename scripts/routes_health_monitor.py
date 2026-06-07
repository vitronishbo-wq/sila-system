#!/usr/bin/env python3
"""
Routes Health Monitor - SILA-System
Ferramenta para monitorar saúde de rotas em tempo real
"""

import json
import re
from collections import defaultdict
from pathlib import Path


class RoutesHealthMonitor:
    def __init__(self, backend_path: str = "apps/backend"):
        self.backend_path = Path(backend_path)
        self.stats = {
            "total_endpoints": 0,
            "by_method": defaultdict(int),
            "documented": 0,
            "with_error_handling": 0,
            "with_response_model": 0,
            "with_type_hints": 0,
            "with_docstring": 0,
        }

    def scan_endpoints(self) -> dict:
        """Scan all endpoints in the codebase"""
        patterns = {
            "get": r"@(?:app|router)\.get\s*\(",
            "post": r"@(?:app|router)\.post\s*\(",
            "put": r"@(?:app|router)\.put\s*\(",
            "delete": r"@(?:app|router)\.delete\s*\(",
            "patch": r"@(?:app|router)\.patch\s*\(",
        }

        py_files = list(self.backend_path.rglob("*.py"))
        py_files = [f for f in py_files if "backup" not in str(f) and "__pycache__" not in str(f)]

        for py_file in py_files:
            try:
                with open(py_file, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                for method, pattern in patterns.items():
                    count = len(re.findall(pattern, content))
                    self.stats["by_method"][method.upper()] += count
                    self.stats["total_endpoints"] += count

                # Check quality indicators
                if "response_model=" in content:
                    self.stats["with_response_model"] += len(
                        re.findall(r"response_model\s*=", content)
                    )

                if "except" in content:
                    self.stats["with_error_handling"] += len(re.findall(r"except\s+", content))

                if '"""' in content or "'''" in content:
                    self.stats["with_docstring"] += 1

                if "->" in content and "def" in content:
                    self.stats["with_type_hints"] += 1

            except Exception:
                pass

        return self.stats

    def check_openapi(self) -> dict:
        """Check OpenAPI specification"""
        openapi_path = Path("openapi.json")

        if not openapi_path.exists():
            return {"status": "not_found", "documented": 0}

        try:
            with open(openapi_path) as f:
                openapi = json.load(f)

            paths = openapi.get("paths", {})
            documented = sum(
                1
                for p, methods in paths.items()
                for m, d in methods.items()
                if isinstance(d, dict) and ("summary" in d or "description" in d)
            )

            return {
                "status": "found",
                "total_paths": len(paths),
                "documented": documented,
                "coverage": f"{documented * 100 // len(paths) if paths else 0}%",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def calculate_health_score(self) -> tuple[float, dict]:
        """Calculate overall health score"""
        total = self.stats["total_endpoints"]
        score = 0
        details = {}

        # Completeness: 30 pts
        if total > 500:
            score += 30
            details["completeness"] = 30
        else:
            score += (total / 500) * 30
            details["completeness"] = (total / 500) * 30

        # Documentation: 25 pts
        openapi = self.check_openapi()
        if openapi["status"] == "found":
            doc_rate = openapi["documented"] / total if total > 0 else 0
            score += doc_rate * 25
            details["documentation"] = doc_rate * 25
        else:
            details["documentation"] = 0

        # Error Handling: 20 pts
        error_rate = self.stats["with_error_handling"] / total if total > 0 else 0
        score += error_rate * 20
        details["error_handling"] = error_rate * 20

        # Response Models: 15 pts
        model_rate = self.stats["with_response_model"] / total if total > 0 else 0
        score += model_rate * 15
        details["response_models"] = model_rate * 15

        # Type Hints: 10 pts
        type_rate = self.stats["with_type_hints"] / total if total > 0 else 0
        score += type_rate * 10
        details["type_hints"] = type_rate * 10

        return score, details

    def generate_report(self):
        """Generate comprehensive health report"""
        print("\n" + "=" * 100)
        print("🔍 SILA-SYSTEM ROUTES HEALTH REPORT")
        print("=" * 100 + "\n")

        # Scan endpoints
        self.scan_endpoints()

        # Basic stats
        print("📊 ENDPOINT STATISTICS:")
        print("-" * 100)
        print(f"  Total Endpoints: {self.stats['total_endpoints']}")
        for method, count in sorted(self.stats["by_method"].items(), key=lambda x: -x[1]):
            pct = (
                (count * 100) // self.stats["total_endpoints"]
                if self.stats["total_endpoints"] > 0
                else 0
            )
            bar = "█" * (count // 5)
            print(f"    {method:10} {count:4d} ({pct:3d}%)  {bar}")

        # OpenAPI status
        print("\n📋 OPENAPI DOCUMENTATION:")
        print("-" * 100)
        openapi = self.check_openapi()
        if openapi["status"] == "found":
            print("  Status: ✅ Found")
            print(f"  Paths: {openapi['total_paths']}")
            print(f"  Documented: {openapi['documented']} ({openapi['coverage']})")
            print(
                f"  Gap: {self.stats['total_endpoints'] - openapi['total_paths']} endpoints not in OpenAPI"
            )
        else:
            print("  Status: ❌ Not found")

        # Quality metrics
        print("\n💊 QUALITY METRICS:")
        print("-" * 100)
        total = self.stats["total_endpoints"] or 1
        print(
            f"  Response Models:  {self.stats['with_response_model']} ({self.stats['with_response_model'] * 100 // total}%)"
        )
        print(
            f"  Error Handling:   {self.stats['with_error_handling']} ({self.stats['with_error_handling'] * 100 // total}%)"
        )
        print(
            f"  Type Hints:       {self.stats['with_type_hints']} ({self.stats['with_type_hints'] * 100 // total}%)"
        )
        print(
            f"  Docstrings:       {self.stats['with_docstring']} ({self.stats['with_docstring'] * 100 // total}%)"
        )

        # Health score
        score, details = self.calculate_health_score()
        print("\n🎯 HEALTH SCORE:")
        print("-" * 100)

        if score >= 85:
            status = "✅ EXCELENTE"
        elif score >= 75:
            status = "🟢 BOM"
        elif score >= 60:
            status = "🟡 ACEITÁVEL"
        else:
            status = "🔴 RUIM"

        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"  Overall: [{bar}] {score:.1f}/100  {status}")

        print("\n  Breakdown:")
        for metric, pts in sorted(details.items(), key=lambda x: -x[1]):
            bar = "█" * int(pts / 2.5) + "░" * (10 - int(pts / 2.5))
            print(f"    {metric:20} [{bar}] {pts:.1f}/25")

        # Recommendations
        print("\n⚠️  RECOMMENDATIONS:")
        print("-" * 100)

        if score < 70:
            print("  🔴 CRITICAL: System needs major improvement")
            print("     1. Document all 561 endpoints in OpenAPI")
            print("     2. Add response_model to all endpoints")
            print("     3. Implement global error handling")
        elif score < 85:
            print("  🟡 ACTION REQUIRED: Address documentation gaps")
            print(
                "     1. Complete OpenAPI documentation (current: {:.1f}%)".format(
                    openapi["documented"] * 100 / total if total else 0
                )
            )
            print("     2. Add type hints to remaining endpoints")
            print("     3. Improve error handling coverage")
        else:
            print("  ✅ GOOD: Continue maintaining current standards")
            print("     1. Monitor documentation completeness")
            print("     2. Increase test coverage")
            print("     3. Regular audits recommended")

        print("\n" + "=" * 100 + "\n")
        return score


if __name__ == "__main__":
    monitor = RoutesHealthMonitor()
    score = monitor.generate_report()

    # Exit code based on score
    if score < 60:
        exit(1)  # Critical
    elif score < 75:
        exit(2)  # Warning
    else:
        exit(0)  # OK
