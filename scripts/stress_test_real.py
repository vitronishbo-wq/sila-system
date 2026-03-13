#!/usr/bin/env python3
"""
Async stress test for PostgreSQL tables: energy_invoices and toll_passages.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import random
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


def _normalize_async_url(url: str) -> str:
    if "+asyncpg" in url:
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


@dataclass
class Stats:
    total_rows: int = 0
    total_elapsed: float = 0.0
    batches: int = 0


async def _insert_batch(engine, sql: str, rows: list[dict], sem: asyncio.Semaphore, stats: Stats, lock: asyncio.Lock):
    async with sem:
        start = time.perf_counter()
        async with engine.begin() as conn:
            await conn.execute(text(sql), rows)
        elapsed = time.perf_counter() - start
        async with lock:
            stats.total_rows += len(rows)
            stats.total_elapsed += elapsed
            stats.batches += 1


def _invoice_rows(count: int, start_index: int) -> list[dict]:
    rows = []
    today = date.today()
    for i in range(count):
        idx = start_index + i
        consumo_kwh = Decimal(random.randint(50, 5000)) / Decimal(10)
        tarifa_kwh = Decimal("0.45")
        valor_consumo = consumo_kwh * tarifa_kwh
        valor_bandeira = Decimal("25.00")
        valor_iluminacao = Decimal("10.00")
        valor_total = valor_consumo + valor_bandeira + valor_iluminacao
        rows.append(
            {
                "id": uuid4(),
                "numero_fatura": f"FT-{idx:06d}-{uuid4().hex[:8]}",
                "consumo_id": uuid4(),
                "unidade_consumidora_id": uuid4(),
                "cpf_titular": f"{random.randint(10000000000, 99999999999)}",
                "mes_referencia": f"{today.year}-{today.month:02d}",
                "consumo_kwh": float(consumo_kwh),
                "tarifa_kwh": float(tarifa_kwh),
                "bandeira_tarifaria": "VERDE",
                "valor_consumo": float(valor_consumo),
                "valor_bandeira": float(valor_bandeira),
                "valor_iluminacao_publica": float(valor_iluminacao),
                "valor_total": float(valor_total),
                "data_emissao": today,
                "data_vencimento": today,
                "status": "EMITIDA",
                "data_pagamento": None,
                "valor_pago": None,
                "metodo_pagamento": None,
                "created_at": datetime.now(timezone.utc),
            }
        )
    return rows


def _toll_rows(count: int, start_index: int) -> list[dict]:
    rows = []
    now = datetime.now(timezone.utc)
    for i in range(count):
        idx = start_index + i
        rows.append(
            {
                "id": uuid4(),
                "vehicle_did": f"did:sila:vehicle:{uuid4().hex[:12]}",
                "gantry_id": f"GANTRY-{random.randint(1, 250):03d}",
                "amount": float(Decimal("1500.00")),
                "currency": "Kz",
                "category": "TRANSPORT_TOLL",
                "occurred_at": now,
                "created_at": now,
            }
        )
    return rows


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5000)
    parser.add_argument("--concurrency", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    url = os.getenv("DATABASE_URL")
    if not url:
        print("DATABASE_URL not set.", file=sys.stderr)
        return 2
    url = _normalize_async_url(url)

    engine = create_async_engine(url, pool_pre_ping=True, pool_size=args.concurrency, max_overflow=10)
    sem = asyncio.Semaphore(args.concurrency)
    lock = asyncio.Lock()
    stats = Stats()

    invoices = args.count // 2
    tolls = args.count - invoices

    invoice_sql = """
        INSERT INTO energy_invoices (
            id, numero_fatura, consumo_id, unidade_consumidora_id, cpf_titular,
            mes_referencia, consumo_kwh, tarifa_kwh, bandeira_tarifaria,
            valor_consumo, valor_bandeira, valor_iluminacao_publica, valor_total,
            data_emissao, data_vencimento, status, data_pagamento, valor_pago,
            metodo_pagamento, created_at
        ) VALUES (
            :id, :numero_fatura, :consumo_id, :unidade_consumidora_id, :cpf_titular,
            :mes_referencia, :consumo_kwh, :tarifa_kwh, :bandeira_tarifaria,
            :valor_consumo, :valor_bandeira, :valor_iluminacao_publica, :valor_total,
            :data_emissao, :data_vencimento, :status, :data_pagamento, :valor_pago,
            :metodo_pagamento, :created_at
        )
    """

    toll_sql = """
        INSERT INTO toll_passages (
            id, vehicle_did, gantry_id, amount, currency, category, occurred_at, created_at
        ) VALUES (
            :id, :vehicle_did, :gantry_id, :amount, :currency, :category, :occurred_at, :created_at
        )
    """

    start_all = time.perf_counter()
    tasks = []

    for batch_start in range(0, invoices, args.batch_size):
        batch = _invoice_rows(min(args.batch_size, invoices - batch_start), batch_start)
        tasks.append(_insert_batch(engine, invoice_sql, batch, sem, stats, lock))

    for batch_start in range(0, tolls, args.batch_size):
        batch = _toll_rows(min(args.batch_size, tolls - batch_start), batch_start)
        tasks.append(_insert_batch(engine, toll_sql, batch, sem, stats, lock))

    await asyncio.gather(*tasks)
    total_elapsed = time.perf_counter() - start_all

    tps = stats.total_rows / total_elapsed if total_elapsed else 0.0
    avg_latency_ms = (stats.total_elapsed / stats.total_rows) * 1000 if stats.total_rows else 0.0

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "count": args.count,
        "concurrency": args.concurrency,
        "batch_size": args.batch_size,
        "rows_inserted": stats.total_rows,
        "total_elapsed_s": round(total_elapsed, 4),
        "tps": round(tps, 2),
        "avg_latency_ms_per_row": round(avg_latency_ms, 4),
    }

    Path("reports").mkdir(parents=True, exist_ok=True)
    report_path = Path("reports/stress_test_real.json")
    report_path.write_text(
        __import__("json").dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(report_path.as_posix())

    await engine.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
