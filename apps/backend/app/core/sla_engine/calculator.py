from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .cache import SLACache
from .metrics import SLAMetrics
from .models import (
    CHANNEL_FACTORS,
    CITIZEN_TYPE_FACTORS,
    LOAD_FACTORS,
    PROVINCE_FACTORS,
    LoadLevel,
    SLAContext,
    SLARequest,
    SLAResponse,
    SLABaseDB,
)
from .policies import load_overrides, load_policies

logger = logging.getLogger(__name__)


def apply_context_factors(
    base_hours: float, context: SLAContext
) -> tuple[float, Dict[str, float], List[str]]:
    breakdown: Dict[str, float] = {"base": base_hours}
    warnings: List[str] = []

    breakdown["province"] = PROVINCE_FACTORS.get(context.province, 1.0)
    breakdown["citizen_type"] = CITIZEN_TYPE_FACTORS.get(context.citizen_type, 1.0)
    breakdown["channel"] = CHANNEL_FACTORS.get(context.channel, 1.0)
    breakdown["load"] = LOAD_FACTORS.get(context.load_level, 1.0)

    total_factor = (
        breakdown["province"]
        * breakdown["citizen_type"]
        * breakdown["channel"]
        * breakdown["load"]
    )

    if context.is_holiday:
        breakdown["holiday"] = 1.2
        total_factor *= 1.2
    if not context.business_hours:
        breakdown["after_hours"] = 1.1
        total_factor *= 1.1

    for key, factor in context.custom_factors.items():
        if factor <= 0:
            warnings.append(f"Fator customizado inválido: {key}={factor}")
        breakdown[f"custom_{key}"] = factor
        total_factor *= factor

    breakdown["total_factor"] = total_factor
    calculated = max(base_hours * total_factor, 0.1)
    return calculated, breakdown, warnings


class SLACalculator:
    """
    Engine principal de cálculo de SLA
    Aplica hierarquia: Base > Políticas > Overrides > Contexto
    """

    def __init__(self, db: AsyncSession, cache: Optional[SLACache] = None, metrics: Optional[SLAMetrics] = None):
        self.db = db
        self.cache = cache
        self.metrics = metrics or SLAMetrics()

    async def calculate(
        self,
        service_id: str,
        context: Optional[SLAContext] = None,
        skip_cache: bool = False,
    ) -> SLAResponse:
        start_time = datetime.utcnow()
        if self.cache and not skip_cache:
            cached = await self.cache.get(service_id, context.model_dump() if context else None)
            if cached:
                logger.debug("Cache hit para %s", service_id)
                self.metrics.record_calculation(service_id, cached.get("calculated_hours", 0.0))
                return SLAResponse(**cached)

        sla_base = await self._get_sla_base(service_id)
        if not sla_base:
            self.metrics.record_calculation(service_id, 0.0, error=True)
            raise ValueError(f"Serviço {service_id} não encontrado")

        context = context or SLAContext()

        hours = sla_base.base_hours
        applied_policies: List[Dict[str, Any]] = []
        policies = await self._get_applicable_policies(service_id, context)
        for policy in policies:
            if policy["multiplier"] != 1.0:
                old_hours = hours
                hours *= policy["multiplier"]
                applied_policies.append(
                    {
                        "id": policy.get("id"),
                        "scope": policy["scope"],
                        "scope_id": policy["scope_id"],
                        "multiplier": policy["multiplier"],
                        "old_hours": old_hours,
                        "new_hours": hours,
                    }
                )
            if policy.get("max_hours") and hours > policy["max_hours"]:
                hours = policy["max_hours"]
                applied_policies.append({"type": "max_hours", "value": policy["max_hours"]})
            if policy.get("min_hours") and hours < policy["min_hours"]:
                hours = policy["min_hours"]
                applied_policies.append({"type": "min_hours", "value": policy["min_hours"]})

        breakdown = {"base": sla_base.base_hours}
        applied_overrides: List[Dict[str, Any]] = []
        overrides = await self._get_applicable_overrides(service_id, context)
        for override in overrides:
            if override["multiplier"] != 1.0:
                old_hours = hours
                hours *= override["multiplier"]
                applied_overrides.append(
                    {
                        "id": override.get("id"),
                        "name": override.get("name"),
                        "multiplier": override["multiplier"],
                        "old_hours": old_hours,
                        "new_hours": hours,
                    }
                )

        adjusted_hours, context_breakdown, warnings = apply_context_factors(hours, context)
        context_breakdown.pop("base", None)
        breakdown.update(context_breakdown)

        calculated_hours = round(adjusted_hours, 2)
        response = SLAResponse(
            service_id=service_id,
            service_name=sla_base.service_name,
            base_hours=sla_base.base_hours,
            calculated_hours=calculated_hours,
            applied_policies=applied_policies,
            applied_overrides=applied_overrides,
            breakdown=breakdown,
            warnings=self._generate_warnings(calculated_hours, sla_base.base_hours) + warnings,
            expires_at=datetime.utcnow() + timedelta(minutes=5),
        )

        if self.cache:
            await self.cache.set(service_id, context.model_dump(), response.model_dump())

        self.metrics.record_calculation(service_id, calculated_hours)
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        self.metrics.record_calculation_time(elapsed)
        self.metrics.update_current_sla(
            service_id,
            calculated_hours,
            context.province.value,
            context.citizen_type.value,
        )
        return response

    async def calculate_batch(
        self,
        requests: List[Tuple[str, Optional[SLAContext]]],
        batch_size: int = 100,
    ) -> List[Optional[SLAResponse]]:
        results: List[Optional[SLAResponse]] = []
        for i in range(0, len(requests), batch_size):
            batch = requests[i : i + batch_size]
            for service_id, context in batch:
                try:
                    result = await self.calculate(service_id, context, skip_cache=True)
                    results.append(result)
                except Exception as exc:
                    logger.error("Erro ao calcular SLA para %s: %s", service_id, exc)
                    results.append(None)
        return results

    async def predict_breach(
        self,
        service_id: str,
        elapsed_hours: float,
        context: Optional[SLAContext] = None,
    ) -> Dict[str, Any]:
        sla = await self.calculate(service_id, context)
        target = sla.calculated_hours
        progress = elapsed_hours / target if target else 0

        if progress < 0.5:
            probability = 0.1
        elif progress < 0.7:
            probability = 0.3
        elif progress < 0.85:
            probability = 0.6
        elif progress < 0.95:
            probability = 0.8
        else:
            probability = 0.95

        risk_factors = []
        if context and context.load_level == LoadLevel.CRITICAL:
            probability += 0.2
            risk_factors.append("carga_critica")
        if elapsed_hours > sla.base_hours * 0.8:
            risk_factors.append("proximo_base")

        self.metrics.update_breach_probability(service_id, round(min(probability, 1.0), 2))
        return {
            "service_id": service_id,
            "elapsed_hours": elapsed_hours,
            "target_hours": target,
            "progress_percentage": round(progress * 100, 2),
            "breach_probability": round(min(probability, 1.0), 2),
            "risk_factors": risk_factors,
            "estimated_remaining": round(target - elapsed_hours, 2),
            "status": "breached" if elapsed_hours > target else "active",
        }

    async def _get_sla_base(self, service_id: str) -> Optional[SLABaseDB]:
        result = await self.db.execute(
            select(SLABaseDB).where(SLABaseDB.service_id == service_id)
        )
        return result.scalar_one_or_none()

    async def _get_applicable_policies(self, service_id: str, context: SLAContext) -> List[Dict[str, Any]]:
        return await load_policies(self.db, service_id, context)

    async def _get_applicable_overrides(
        self, service_id: str, context: SLAContext
    ) -> List[Dict[str, Any]]:
        return await load_overrides(self.db, service_id, context)

    def _generate_warnings(self, calculated: float, base: float) -> List[str]:
        warnings = []
        if calculated > base * 1.5:
            warnings.append("SLA muito superior à base (50%+)")
        elif calculated < base * 0.5:
            warnings.append("SLA muito inferior à base (50%-)")
        if calculated > 720:
            warnings.append("SLA superior a 30 dias")
        return warnings


class SLAEngine:
    async def calculate(self, db: AsyncSession, request: SLARequest) -> SLAResponse:
        cache = SLACache()
        calculator = SLACalculator(db, cache=cache)
        return await calculator.calculate(request.service_id, request.context)
