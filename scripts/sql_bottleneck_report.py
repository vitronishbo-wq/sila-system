#!/usr/bin/env python3
"""
Generates a simple SQL bottleneck report for energy_invoices and toll_passages.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parents[1]
LIB_DIR = ROOT_DIR / "scripts" / "lib"
for path in (ROOT_DIR, LIB_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from db_connector import DatabaseConnector


async def run() -> dict:
    connector = DatabaseConnector()
    await connector.connect()
    session_factory = connector.get_session_factory()

    payload: dict = {
        "timestamp": datetime.now(UTC).isoformat(),
        "tables": {},
        "indexes": [],
        "notes": [],
    }

    async with session_factory() as session:
        table_stats = await session.execute(
            text(
                """
                SELECT relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch
                FROM pg_stat_user_tables
                WHERE relname IN ('energy_invoices', 'toll_passages')
                """
            )
        )
        for row in table_stats.mappings().all():
            payload["tables"][row["relname"]] = {
                "seq_scan": row["seq_scan"],
                "seq_tup_read": row["seq_tup_read"],
                "idx_scan": row["idx_scan"],
                "idx_tup_fetch": row["idx_tup_fetch"],
            }

        index_stats = await session.execute(
            text(
                """
                SELECT relname AS table_name, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
                FROM pg_stat_user_indexes
                WHERE relname IN ('energy_invoices', 'toll_passages')
                ORDER BY idx_scan ASC, indexrelname
                """
            )
        )
        payload["indexes"] = [dict(row) for row in index_stats.mappings().all()]

        size_stats = await session.execute(
            text(
                """
                SELECT relname, pg_total_relation_size(relid) AS total_bytes
                FROM pg_catalog.pg_statio_user_tables
                WHERE relname IN ('energy_invoices', 'toll_passages')
                """
            )
        )
        for row in size_stats.mappings().all():
            payload.setdefault("sizes", {})[row["relname"]] = row["total_bytes"]

    payload["notes"].append(
        "Indices com idx_scan muito baixo apos carga indicam possivel ausencia de consultas usando esses campos."
    )

    await connector.disconnect()
    return payload


def render_md(payload: dict) -> str:
    tables = payload.get("tables", {})
    sizes = payload.get("sizes", {})
    indexes = payload.get("indexes", [])
    lines = [
        "# SQL Bottleneck Report",
        "",
        f"**Timestamp:** {payload.get('timestamp')}",
        "",
        "## Tabelas",
        "",
        "| Tabela | Seq Scan | Seq Tup Read | Idx Scan | Idx Tup Fetch | Size (bytes) |",
        "|---|---|---|---|---|---|",
    ]
    for table, stats in tables.items():
        lines.append(
            f"| {table} | {stats.get('seq_scan')} | {stats.get('seq_tup_read')} | "
            f"{stats.get('idx_scan')} | {stats.get('idx_tup_fetch')} | {sizes.get(table, 0)} |"
        )

    lines += [
        "",
        "## Indices",
        "",
        "| Tabela | Index | Idx Scan | Idx Tup Read | Idx Tup Fetch |",
        "|---|---|---|---|---|",
    ]
    for row in indexes:
        lines.append(
            f"| {row['table_name']} | {row['indexrelname']} | {row['idx_scan']} | "
            f"{row['idx_tup_read']} | {row['idx_tup_fetch']} |"
        )

    lines += ["", "## Notas"]
    for note in payload.get("notes", []):
        lines.append(f"- {note}")
    return "\n".join(lines)


async def main() -> int:
    if not os.getenv("DATABASE_URL"):
        print("DATABASE_URL not set.", file=sys.stderr)
        return 2
    payload = await run()
    Path("reports").mkdir(parents=True, exist_ok=True)
    json_path = Path("reports/sql_bottleneck_report.json")
    md_path = Path("reports/sql_bottleneck_report.md")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(render_md(payload), encoding="utf-8")
    print(md_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(__import__("asyncio").run(main()))
