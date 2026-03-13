from __future__ import annotations
from decimal import Decimal
from app.modules.infrastructure.infrastructure.adapters.tcu_adapter import TCUAdapter

async def handle_aditivo(payload: dict, tenant_id: str, correlation_id: str) -> None:
    adapter = TCUAdapter(tenant_id=tenant_id)
    await adapter.registrar_aditivo(obra_id=str(payload['obra_id']), valor_adicional=Decimal(str(payload.get('valor_adicional', '0.00'))), idempotency_key=str(payload['event_id']), correlation_id=correlation_id)
