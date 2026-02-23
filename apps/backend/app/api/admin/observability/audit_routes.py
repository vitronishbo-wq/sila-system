"""
Observability API - Extensão para AuditAnalytics + SLA/SLO.
Expõe métricas, anomalias e timeline via REST interno.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.api.deps import get_current_admin_user, get_db
from modules.identity.models.user import User
from app.core.audit.analytics import AuditAnalytics
from app.core.audit.sla_definitions import (
    SLA_DEFINITIONS,
    SLO_TARGETS,
    ANOMALY_THRESHOLDS,
    evaluate_sla_status,
)

router = APIRouter(prefix="/audit", tags=["Audit & Observability"])


@router.get("/sla/metrics")
async def get_sla_metrics(
    days: int = Query(default=7, ge=1, le=90, description="Lookback in days"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    SLA Metrics: tempo médio/min/max entre REQUEST_CREATED e DOCUMENT_ISSUED.
    """
    end = datetime.utcnow()
    start = end - timedelta(days=days)

    analytics = AuditAnalytics(db)
    metrics = await analytics.get_sla_metrics(start, end)

    # Enriquecer com avaliação SLA
    avg = metrics.get("avg_issuance_time_seconds", 0)
    sla_eval = evaluate_sla_status(avg, "DEFAULT")

    return {
        **metrics,
        "period_days": days,
        "sla_status": sla_eval,
        "sla_target_seconds": SLA_DEFINITIONS["DEFAULT"]["target_sla_seconds"],
    }


@router.get("/sla/definitions")
async def get_sla_definitions(
    current_user: User = Depends(get_current_admin_user),
):
    """
    Lista todos os SLA/SLO definidos no sistema (read-only).
    """
    return {
        "sla": SLA_DEFINITIONS,
        "slo": SLO_TARGETS,
        "anomaly_thresholds": ANOMALY_THRESHOLDS,
    }


@router.get("/anomalies")
async def detect_anomalies(
    window_minutes: int = Query(default=60, ge=5, le=1440),
    threshold: int = Query(default=10, ge=1, le=1000),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Detecta picos anormais de eventos na janela de tempo especificada.
    """
    analytics = AuditAnalytics(db)
    anomalies = await analytics.detect_anomalies(window_minutes, threshold)
    return {
        "anomalies": anomalies,
        "window_minutes": window_minutes,
        "threshold": threshold,
        "checked_at": datetime.utcnow().isoformat(),
    }


@router.get("/timeline/{resource_id}")
async def get_resource_timeline(
    resource_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Reconstrói a linha do tempo completa de auditoria de um recurso.
    """
    analytics = AuditAnalytics(db)
    timeline = await analytics.get_event_timeline(resource_id)

    if not timeline:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado para este recurso.")

    return {
        "resource_id": resource_id,
        "events": timeline,
        "total": len(timeline),
    }
