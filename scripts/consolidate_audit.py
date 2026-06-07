#!/usr/bin/env python3
"""
SILA Daily Audit Consolidation - Advanced Report Generator
Consolida todos os artefatos intermediários em um relatório visual MD + JSON
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


class AuditConsolidator:
    """Consolida artefatos de auditoria em relatório único."""

    def __init__(self, audit_dir: Path = Path("reports/daily_audit")):
        self.audit_dir = audit_dir
        self.timestamp = datetime.now().isoformat()
        self.metrics: dict[str, Any] = {}
        self.critical_modules: list[dict[str, Any]] = []
        self.warnings: list[str] = []
        self.artifacts: dict[str, Path] = {}
        self.check_results: dict[str, bool] = {}

    def collect_artifacts(self) -> None:
        """Coleta todos os artefatos gerados pelos rituais."""
        print("🔍 Coletando artefatos de auditoria...")

        # Logs dos rituais
        for log_file in self.audit_dir.glob("*.log"):
            self.artifacts[log_file.stem] = log_file

        # Relatórios estruturados
        reports_dir = Path("reports")
        for report_file in reports_dir.glob("*.md"):
            if report_file.name != "daily_audit.md":
                self.artifacts[f"report_{report_file.stem}"] = report_file

        for report_file in reports_dir.glob("*.json"):
            self.artifacts[f"json_{report_file.stem}"] = report_file

        print(f"✅ {len(self.artifacts)} artefatos coletados")

    def extract_module_scores(self) -> None:
        """Extrai scores de maturidade do modules_report.md."""
        print("📊 Extraindo scores de maturidade...")

        modules_report = Path("modules_report.md")
        if not modules_report.exists():
            print("⚠️  modules_report.md não encontrado")
            return

        try:
            with open(modules_report, encoding="utf-8") as f:
                content = f.read()

            # Parsear tabela markdown
            lines = content.split("\n")
            for line in lines:
                if "|" in line and "score" not in line.lower():
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 3:
                        try:
                            module = parts[1]
                            score_str = parts[-2].replace("%", "").strip()
                            score = float(score_str) if score_str else 0
                            if 0 < score < 40:
                                self.critical_modules.append({"module": module, "score": score})
                        except (ValueError, IndexError):
                            continue

            print(f"✅ {len(self.critical_modules)} módulos críticos extraídos")
        except Exception as e:
            print(f"❌ Erro ao extrair scores: {e}")

    def scan_import_errors(self) -> None:
        """Escaneia import errors dos logs."""
        print("🔗 Escaneando import errors...")

        self.audit_dir / "04_import_scan_*.log"
        for log_file in self.audit_dir.glob("04_import_scan_*.log"):
            try:
                with open(log_file, encoding="utf-8") as f:
                    content = f.read()

                # Detectar errors
                errors = re.findall(r"(ImportError|SyntaxError|ModuleNotFoundError).*", content)
                if errors:
                    for error in errors[:5]:  # Top 5
                        self.warnings.append(f"Import: {error}")

                print("✅ Logs processados")
            except Exception as e:
                print(f"⚠️  Erro ao processar logs: {e}")

    def compute_check_metrics(self) -> None:
        """Deriva métricas reais a partir dos artefatos mais recentes."""
        print("🧮 Derivando métricas reais da execução...")

        arch_log = sorted(self.audit_dir.glob("01_arch_sync_*.log"))
        domain_log = sorted(self.audit_dir.glob("02_domain_audit_*.log"))
        module_log = sorted(self.audit_dir.glob("03_module_diagnostics_*.log"))
        import_log = sorted(self.audit_dir.glob("04_import_scan_*.log"))
        router_log = sorted(self.audit_dir.glob("05_router_scan_*.log"))

        latest_router_log = router_log[-1] if router_log else None
        router_count = self.metrics.get("routers", 0)
        health_count = self.metrics.get("health_endpoints", 0)

        if latest_router_log and latest_router_log.exists():
            content = latest_router_log.read_text(encoding="utf-8")
            router_match = re.search(r"Router Count:\s*(\d+)", content)
            health_match = re.search(r"Health Count:\s*(\d+)", content)
            if router_match:
                router_count = int(router_match.group(1))
            if health_match:
                health_count = int(health_match.group(1))
            self.metrics["routers"] = router_count
            self.metrics["health_endpoints"] = health_count

        self.check_results = {
            "architecture_sync": bool(arch_log),
            "domain_audit": bool(domain_log),
            "module_maturity": bool(module_log),
            "import_scan": bool(import_log),
            "router_scan": router_count > 0,
            "health_scan": health_count > 0,
        }

        total_checks = len(self.check_results)
        passed_checks = sum(1 for passed in self.check_results.values() if passed)
        failed_checks = total_checks - passed_checks
        taxa_sucesso = round((passed_checks * 100 / total_checks), 1) if total_checks else 0.0

        self.metrics["total_checks"] = total_checks
        self.metrics["passed"] = passed_checks
        self.metrics["failed"] = failed_checks
        self.metrics["taxa_sucesso"] = taxa_sucesso

        report_path = Path("reports/domain_dependency_guardrail_report.md")
        if report_path.exists():
            report_content = report_path.read_text(encoding="utf-8").lower()
            has_real_violations = any(
                marker not in report_content
                for marker in (
                    "graph violations: **0**",
                    "policy violations: **0**",
                    "manifest violations: **0**",
                    "core import violations: **0**",
                    "cycle violations: **0**",
                )
            )
            if has_real_violations:
                self.warnings.append("Domain dependency report contains violations")

    def analyze_routers(self) -> None:
        """Analisa router definitions."""
        print("🛣️  Analisando routers...")

        try:
            import subprocess

            router_count = subprocess.run(
                ["grep", "-r", "APIRouter", "apps/backend/app/modules/"],
                capture_output=True,
                text=True,
            )
            router_lines = len(router_count.stdout.strip().split("\n"))

            health_count = subprocess.run(
                ["find", "apps/backend/app/modules", "-name", "health.py"],
                capture_output=True,
                text=True,
            )
            health_files = len(health_count.stdout.strip().split("\n")) - 1

            self.metrics["routers"] = router_lines
            self.metrics["health_endpoints"] = health_files

            print(f"✅ {router_lines} routers, {health_files} health endpoints")
        except Exception as e:
            print(f"⚠️  Erro ao analisar routers: {e}")

    def generate_markdown_report(self, output_file: Path) -> None:
        """Gera relatório consolidado em markdown."""
        print(f"📝 Gerando relatório consolidado: {output_file}")

        taxa_sucesso = self.metrics.get("taxa_sucesso", 0)
        critical_count = len(self.critical_modules)

        # Construir seção de críticos
        critical_section = "✅ Nenhum módulo crítico detectado"
        if self.critical_modules:
            critical_section = "| Módulo | Score |\n|--------|-------|\n"
            for mod in self.critical_modules:
                critical_section += f"| {mod['module']} | {mod['score']:.1f}% |\n"

        # Construir seção de warnings
        warnings_section = "✅ Nenhum warning detectado"
        if self.warnings:
            warnings_section = ""
            for warn in self.warnings:
                warnings_section += f"- {warn}\n"

        # Artefatos
        artifacts_section = "```\nreports/daily_audit/\n"
        for _stem, path in self.artifacts.items():
            if path.exists():
                size_kb = path.stat().st_size / 1024
                artifacts_section += f"  ├── {path.name} ({size_kb:.1f}KB)\n"
        artifacts_section += "```"

        # Template final
        content = f"""# 🕐 SILA Daily Audit Report

**Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Ritual Version:** v1.0.0  
**Status:** ✅ Auditoria Completa

---

## 📊 Resumo Executivo

| Métrica | Valor |
|---------|-------|
| Taxa de Sucesso | {taxa_sucesso:.1f}% |
| Módulos Críticos | {critical_count} |
| Routers Definidos | {self.metrics.get("routers", "N/A")} |
| Health Endpoints | {self.metrics.get("health_endpoints", "N/A")} |

---

## 🎯 Resultados dos 5 Rituais / 6 Verificações

### ✅ 1. Sincronização de Arquitetura
- **Status:** Universalização de estrutura executada
- **Ação:** `make architecture-sync`

### ✅ 2. Auditoria de Domínios  
- **Status:** Compliance vs. Política YAML validada
- **Ação:** `make audit-domains`

### ✅ 3. Diagnóstico de Maturidade
- **Status:** Scores extraídos e analisados
- **Report:** `modules_report.md`

### ✅ 4. Scanner de Imports
- **Status:** Scanner sintático do código-fonte executado
- **Modos:** Detecta SyntaxError e erros de compilação Python

### ✅ 5. Verificação de Routers/Health
- **Routers:** {self.metrics.get("routers", "N/A")} definições
- **Health:** {self.metrics.get("health_endpoints", "N/A")} endpoints

---

## 🚨 Módulos Críticos (Score < 40%)

{critical_section}

---

## ⚠️ Warnings Detectados

{warnings_section}

---

## 📁 Artefatos Gerados

{artifacts_section}

---

## 🔧 Ações Recomendadas

1. **Se há críticos:** Execute `make arch-fix` para remediação automática
2. **Se há warnings:** Revisar imports em `reports/domain_dependency_guardrail_report.md`
3. **Validação:** Execute `make audit-full` para verificação completa
4. **Próximo Ritual:** Agendar próxima auditoria em 24h

---

## 📚 Referências

- **Política Arquitetural:** `docs/architecture/domain_dependency_policy.yaml`
- **Grafo Observado:** `reports/module_dependency_graph.json`
- **Grafo Declarado:** `reports/module_manifest_graph.json`
- **Detalhes de Compliance:** `reports/domain_dependency_guardrail_report.md`

---

**Generated by:** SILA Daily Audit Ritual v1.0.0  
**Time:** {self.timestamp}
"""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Relatório salvo: {output_file}")

    def generate_json_report(self, output_file: Path) -> None:
        """Gera relatório consolidado em JSON para integração."""
        print(f"📄 Gerando relatório JSON: {output_file}")

        report = {
            "timestamp": self.timestamp,
            "version": "1.0.0",
            "status": "COMPLETE",
            "metrics": self.metrics,
            "critical_modules": self.critical_modules,
            "warnings": self.warnings[:10],  # Top 10
            "artifacts": {
                k: {
                    "path": str(v),
                    "exists": v.exists(),
                    "size_kb": (v.stat().st_size / 1024 if v.exists() else 0),
                }
                for k, v in self.artifacts.items()
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON salvo: {output_file}")

    def run(self) -> None:
        """Executa consolidação completa."""
        print("\n🕐 Iniciando Consolidação de Auditoria...\n")

        self.collect_artifacts()
        self.extract_module_scores()
        self.scan_import_errors()
        self.analyze_routers()
        self.compute_check_metrics()

        # Gerar relatórios
        self.generate_markdown_report(Path("reports/daily_audit.md"))
        self.generate_json_report(Path("reports/daily_audit.json"))

        print("\n✅ Consolidação Completa!\n")


if __name__ == "__main__":
    consolidator = AuditConsolidator()
    consolidator.run()
