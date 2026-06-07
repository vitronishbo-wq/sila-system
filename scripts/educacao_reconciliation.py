#!/usr/bin/env python3
"""
Education data reconciliation report for matriculas and ano_letivo integrity.
Generates JSON + MD summary in reports/.
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT_DIR / "scripts" / "lib"
for path in (ROOT_DIR, LIB_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from db_connector import DatabaseConnector


async def _scalar(session, sql: str) -> int:
    result = await session.execute(text(sql))
    return int(result.scalar() or 0)


async def _rows(session, sql: str, limit: int = 25) -> list[dict]:
    result = await session.execute(text(sql))
    rows = result.mappings().all()
    return rows[:limit]


async def run() -> dict:
    report: dict = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "UNKNOWN",
        "metrics": {},
        "samples": {},
        "notes": [],
    }

    connector = DatabaseConnector()
    try:
        await connector.connect()
        session_factory = connector.get_session_factory()
        async with session_factory() as session:
            report["metrics"]["total_matriculas"] = await _scalar(
                session, "SELECT COUNT(*) FROM educacao_matriculas"
            )
            report["metrics"]["total_anos_letivos"] = await _scalar(
                session, "SELECT COUNT(*) FROM educacao_anos_letivos"
            )
            report["metrics"]["total_turmas"] = await _scalar(
                session, "SELECT COUNT(*) FROM educacao_turmas"
            )

            report["metrics"]["orphan_matriculas"] = await _scalar(
                session,
                """
                SELECT COUNT(*)
                FROM educacao_matriculas m
                LEFT JOIN educacao_anos_letivos a ON a.id = m.ano_letivo_id
                WHERE a.id IS NULL
                """,
            )
            report["samples"]["orphan_matriculas"] = await _rows(
                session,
                """
                SELECT m.id, m.ano_letivo_id, m.turma_id, m.escola_id, m.citizen_id
                FROM educacao_matriculas m
                LEFT JOIN educacao_anos_letivos a ON a.id = m.ano_letivo_id
                WHERE a.id IS NULL
                ORDER BY m.data_matricula DESC
                """,
            )

            report["metrics"]["matriculas_turma_ano_mismatch"] = await _scalar(
                session,
                """
                SELECT COUNT(*)
                FROM educacao_matriculas m
                JOIN educacao_turmas t ON t.id = m.turma_id
                WHERE m.ano_letivo_id <> t.ano_letivo_id
                """,
            )
            report["samples"]["matriculas_turma_ano_mismatch"] = await _rows(
                session,
                """
                SELECT m.id, m.ano_letivo_id AS matricula_ano_letivo_id,
                       t.ano_letivo_id AS turma_ano_letivo_id,
                       m.turma_id, m.escola_id
                FROM educacao_matriculas m
                JOIN educacao_turmas t ON t.id = m.turma_id
                WHERE m.ano_letivo_id <> t.ano_letivo_id
                ORDER BY m.data_matricula DESC
                """,
            )

            report["metrics"]["matriculas_sem_turma"] = await _scalar(
                session,
                """
                SELECT COUNT(*)
                FROM educacao_matriculas m
                LEFT JOIN educacao_turmas t ON t.id = m.turma_id
                WHERE t.id IS NULL
                """,
            )
            report["samples"]["matriculas_sem_turma"] = await _rows(
                session,
                """
                SELECT m.id, m.turma_id, m.escola_id, m.ano_letivo_id
                FROM educacao_matriculas m
                LEFT JOIN educacao_turmas t ON t.id = m.turma_id
                WHERE t.id IS NULL
                ORDER BY m.data_matricula DESC
                """,
            )

            report["notes"].append(
                "Propinas: tabela educacao_propinas armazena valores em metadata_json; "
                "validacao de Kz deve ser feita na camada de aplicacao."
            )

        report["status"] = "OK"
        return report
    finally:
        await connector.disconnect()


def _render_markdown(report: dict) -> str:
    metrics = report.get("metrics", {})
    samples = report.get("samples", {})
    notes = report.get("notes", [])
    return f"""# Educacao - Relatorio de Reconciliacao

**Timestamp:** {report.get("timestamp", "N/A")}
**Status:** {report.get("status", "UNKNOWN")}

## Resumo

| Metrica | Valor |
|---|---|
| Total Matriculas | {metrics.get("total_matriculas", "N/A")} |
| Total Anos Letivos | {metrics.get("total_anos_letivos", "N/A")} |
| Total Turmas | {metrics.get("total_turmas", "N/A")} |
| Matriculas Orfas (ano_letivo) | {metrics.get("orphan_matriculas", "N/A")} |
| Matriculas Turma/Ano mismatch | {metrics.get("matriculas_turma_ano_mismatch", "N/A")} |
| Matriculas sem Turma | {metrics.get("matriculas_sem_turma", "N/A")} |

## Amostras (max 25)

### Orfas (ano_letivo)
```
{json.dumps(samples.get("orphan_matriculas", []), indent=2, ensure_ascii=False)}
```

### Mismatch Turma/Ano
```
{json.dumps(samples.get("matriculas_turma_ano_mismatch", []), indent=2, ensure_ascii=False)}
```

### Sem Turma
```
{json.dumps(samples.get("matriculas_sem_turma", []), indent=2, ensure_ascii=False)}
```

## Notas
{chr(10).join(f"- {note}" for note in notes) if notes else "- Nenhuma"}
"""


def main() -> None:
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    try:
        report = asyncio.run(run())
    except Exception as exc:  # pragma: no cover - runtime diagnostics
        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "FAILED",
            "error": str(exc),
        }

    json_path = reports_dir / "educacao_reconciliation.json"
    md_path = reports_dir / "educacao_reconciliation.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(_render_markdown(report), encoding="utf-8")


if __name__ == "__main__":
    main()
