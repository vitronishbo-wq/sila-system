from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta

import click
from apps.backend.app.core.db import AsyncSessionLocal
from sqlalchemy import func, select

from .calculator import SLACalculator
from .models import CitizenType, Province, SLABaseDB, SLAContext, SLAPolicyDB, SLAViolationDB


@click.group()
def sla() -> None:
    """Comandos de gestão de SLA"""


@sla.command()
@click.option("--file", "-f", "file_path", required=True, help="Arquivo JSON com SLAs")
def import_slas(file_path: str) -> None:
    async def _run() -> None:
        with open(file_path, encoding="utf-8") as handle:
            data = json.load(handle)
        async with AsyncSessionLocal() as db:  # type: AsyncSession
            try:
                for sla_data in data.get("slas", []):
                    record = SLABaseDB(
                        service_id=sla_data["service_id"],
                        service_name=sla_data["service_name"],
                        module=sla_data["module"],
                        base_hours=sla_data["base_hours"],
                        priority=sla_data["priority"],
                        tier=sla_data["tier"],
                        version=sla_data.get("version", "1.0"),
                        legal_basis=sla_data.get("legal_basis"),
                    )
                    db.add(record)
                await db.commit()
                click.echo(f"OK: {len(data.get('slas', []))} SLAs importados")
            except Exception as exc:
                await db.rollback()
                click.echo(f"Erro: {exc}")

    asyncio.run(_run())


@sla.command()
@click.option("--service", "-s", "service_id", required=True, help="ID do serviço")
@click.option("--province", "-p", default="luanda", help="Província")
@click.option("--citizen", "-c", default="normal", help="Tipo de cidadão")
def calculate(service_id: str, province: str, citizen: str) -> None:
    async def _run() -> None:
        async with AsyncSessionLocal() as db:  # type: AsyncSession
            try:
                context = SLAContext(
                    province=Province(province),
                    citizen_type=CitizenType(citizen),
                )
                calculator = SLACalculator(db)
                result = await calculator.calculate(service_id, context)
                click.echo(f"\nSLA para {result.service_name}")
                click.echo(f"Base: {result.base_hours}h")
                click.echo(f"Calculado: {result.calculated_hours}h")
                click.echo("\nBreakdown:")
                for key, value in result.breakdown.items():
                    click.echo(f"  {key}: {value}")
            except Exception as exc:
                click.echo(f"Erro: {exc}")

    asyncio.run(_run())


@sla.command()
@click.option("--service", "-s", "service_id", help="Filtrar por serviço")
@click.option("--days", "-d", default=7, help="Dias para buscar")
def violations(service_id: str | None, days: int) -> None:
    async def _run() -> None:
        async with AsyncSessionLocal() as db:  # type: AsyncSession
            stmt = select(SLAViolationDB)
            if service_id:
                stmt = stmt.where(SLAViolationDB.service_id == service_id)
            since = datetime.utcnow() - timedelta(days=days)
            stmt = stmt.where(SLAViolationDB.created_at >= since)
            stmt = stmt.order_by(SLAViolationDB.created_at.desc()).limit(50)
            result = await db.execute(stmt)
            violations = result.scalars().all()
            click.echo(f"\nViolacoes nos ultimos {days} dias: {len(violations)}")
            for v in violations[:10]:
                click.echo(f"{v.created_at}: {v.service_id} - {v.delta_hours}h acima")

    asyncio.run(_run())


@sla.command()
def stats() -> None:
    async def _run() -> None:
        async with AsyncSessionLocal() as db:  # type: AsyncSession
            total_result = await db.execute(select(func.count()).select_from(SLABaseDB))
            total = total_result.scalar() or 0
            by_module = await db.execute(
                select(SLABaseDB.module, func.count().label("count")).group_by(SLABaseDB.module)
            )
            policies_result = await db.execute(select(func.count()).select_from(SLAPolicyDB))
            policies = policies_result.scalar() or 0
            violations_result = await db.execute(select(func.count()).select_from(SLAViolationDB))
            violations = violations_result.scalar() or 0

            click.echo("\nESTATISTICAS DE SLA")
            click.echo("=" * 40)
            click.echo(f"Total de servicos: {total}")
            click.echo(f"Politicas ativas: {policies}")
            click.echo(f"Total de violacoes: {violations}")
            click.echo("\nPor modulo:")
            for module, count in by_module.all():
                click.echo(f"  {module}: {count}")

    asyncio.run(_run())


if __name__ == "__main__":
    sla()
