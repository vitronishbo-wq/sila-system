#!/usr/bin/env python3
"""
Auditoria de grafia e normalização de locations.

Gera:
  - reports/locations_corrections_full.csv (todos os nomes)
  - reports/locations_corrections_suggested.csv (apenas conflitos)
"""

from __future__ import annotations

import csv
import os
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    import psycopg
    _CONNECT = psycopg.connect
except ImportError:  # pragma: no cover - fallback when psycopg isn't installed
    try:
        import psycopg2
        _CONNECT = psycopg2.connect
    except ImportError as exc:
        raise SystemExit(
            "Missing database driver. Install psycopg or psycopg2 to run this audit."
        ) from exc



def _normalize_key(value: str) -> str:
    base = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    base = base.replace("-", "").replace(" ", "")
    return base.strip().lower()


def _canonical_title(value: str) -> str:
    parts = value.replace("-", " - ").title().replace(" - ", "-")
    for word in [" E ", " De ", " Da ", " Do ", " Dos ", " Das "]:
        parts = parts.replace(word, word.lower())
    return parts


def _connect():
    user = os.getenv("POSTGRES_USER", "sila_user")
    password = os.getenv("POSTGRES_PASSWORD", "Trumanmarcelo_1983")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "sila_db")
    return _CONNECT(
        host=host,
        port=port,
        dbname=db,
        user=user,
        password=password,
    )


def main() -> None:
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    full_path = reports_dir / "locations_corrections_full.csv"
    suggested_path = reports_dir / "locations_corrections_suggested.csv"

    with _connect() as conn:
        if hasattr(conn, "execute"):
            rows = conn.execute(
                "SELECT id, name, type, parent_id FROM locations ORDER BY type, name"
            ).fetchall()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, type, parent_id FROM locations ORDER BY type, name"
                )
                rows = cur.fetchall()

    grouped = defaultdict(list)
    full_rows = []
    for row in rows:
        id_, name, loc_type, parent_id = row
        name = name or ""
        canonical = _canonical_title(name)
        key = _normalize_key(name)
        grouped[key].append((name, loc_type))
        full_rows.append([id_, name, loc_type, parent_id, canonical, key])

    with full_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "type", "parent_id", "canonical", "name_norm"])
        writer.writerows(full_rows)

    with suggested_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name_norm", "variants", "types", "total", "suggested_canonical"])
        for key, items in sorted(grouped.items()):
            variants = sorted({name for name, _ in items})
            if len(variants) <= 1:
                continue
            types = sorted({loc_type for _, loc_type in items})
            suggested = _canonical_title(variants[0]) if variants else ""
            writer.writerow([key, variants, types, len(items), suggested])


if __name__ == "__main__":
    main()
