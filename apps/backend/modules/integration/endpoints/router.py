# modules/integration/endpoints/router.py
from datetime import datetime
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from core.security import get_current_user
from modules.auth.schemas.user import UserResponse
from modules.integration.schemas import (
    CitizenLegacyBatch,
    CitizenLegacyResponse,
    MigrationStatusResponse,
    SyncProvinceRequest,
    SyncProvinceResponse,
)

router = APIRouter(prefix="/integration", tags=["integration"])


@router.get("/ping")
async def ping() -> dict:
    """Health check do módulo integration."""
    return {"status": "ok", "module": "integration", "timestamp": datetime.utcnow().isoformat()}


@router.get("/migration/status", response_model=MigrationStatusResponse)
async def get_migration_status(current_user: UserResponse = Depends(get_current_user)):
    """Status geral da migração de dados legacy (acesso central/superuser)."""
    if not (current_user.is_superuser or current_user.level == "central"):
        raise HTTPException(status_code=403, detail="Acesso restrito a nível central ou superuser")

    return MigrationStatusResponse(
        total_legacy_records=0,
        total_migrated=0,
        total_duplicates=0,
        total_errors=0,
        percentage_complete=0.0,
        last_migration_at=None,
        provinces_status={},
    )


@router.post("/migrate/citizens", response_model=List[CitizenLegacyResponse])
async def migrate_citizens_batch(
    payload: CitizenLegacyBatch,
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user),
):
    """Migração em lote de cidadãos legacy (central/provincial/superuser)."""
    if not (current_user.is_superuser or current_user.level in ["central", "provincial"]):
        raise HTTPException(status_code=403, detail="Permissão insuficiente para migração")

    # background_tasks.add_task(migrate_citizens_batch_service, payload, current_user)
    return []


@router.get("/legacy/{province_code}/citizens")
async def get_legacy_citizens(
    province_code: str,
    limit: int = 1000,
    offset: int = 0,
    current_user: UserResponse = Depends(get_current_user),
):
    """Pull de cidadãos legacy por província (acesso central)."""
    if not (current_user.is_superuser or current_user.level == "central"):
        raise HTTPException(status_code=403, detail="Acesso restrito ao nível central")

    return []


@router.post("/sync/province/{province_id}", response_model=SyncProvinceResponse)
async def sync_province_data(
    province_id: str,
    request: SyncProvinceRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """Sincronização completa de dados de uma província (acesso central)."""
    if not (current_user.is_superuser or current_user.level == "central"):
        raise HTTPException(status_code=403, detail="Sincronização apenas por nível central")

    return SyncProvinceResponse(
        province_id=province_id,
        records_processed=0,
        records_added=0,
        records_updated=0,
        errors=0,
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
        status="completed",
    )


@router.get("/audit/log")
async def get_integration_audit_log(
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_user),
):
    """Log de auditoria de operações de integração (apenas superuser)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Acesso restrito a superuser")

    return {"entries": [], "total": 0}