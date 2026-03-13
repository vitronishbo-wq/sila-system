"""
Eventos de domínio do módulo Citizen.
Publisher/subscriber pattern para integração cross-module.
"""
import uuid
from typing import Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    """Contrato base para todos os eventos de domínio emitidos pelo módulo Citizen."""
    event_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = '1.0'
    source: str = 'citizen_module'

class CitizenValidated(BaseEvent):
    """Emitido quando um cidadão passa na validação FUC com sucesso."""
    citizen_id: str
    status: str

class CitizenValidationFailed(BaseEvent):
    """Emitido quando a validação FUC é rejeitada (cidadão inválido, inactivo ou não encontrado)."""
    citizen_id: str
    reason: str
    details: Dict[str, Any] = Field(default_factory=dict)