from typing import Dict, Optional
import uuid
from dataclasses import dataclass
from enum import Enum
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class DataSegment(str, Enum):
    """Enum de segmentos de dados para uso em assinaturas FastAPI.

    Usar `DataSegment.IDENTITY`, `DataSegment.HEALTH`, etc., como valores
    string compatíveis com Pydantic/FastAPI para parâmetros de rota.
    """
    IDENTITY = 'IDENTITY'
    HEALTH = 'HEALTH'
    ADDRESS = 'ADDRESS'
    MEDICAL = 'MEDICAL'

    def allows(self, action: str) -> bool:
        return True

class BasePolicy:
    """BasePolicy: sobrescrever `check` com regras reais.

    A implementação padrão permite o acesso (retorna True). Isto evita
    bloqueios durante desenvolvimento mas fornece um único ponto para
    aplicar validações reais posteriormente.
    """

    def check(self, user_id: str, action: str, resource: Optional[Dict]=None) -> bool:
        """Verifica se o `user_id` pode executar `action` sobre `resource`.

        Parâmetros:
        - user_id: identificador do utilizador (string)
        - action: nome da ação (ex: 'read', 'create', 'update', 'delete')
        - resource: dados/contexto opcionais sobre o recurso alvo

        Retorna True se permitido, False caso contrário.
        """
        return True

class PolicyRegistry:
    """Regista políticas por nome (ex: 'citizen', 'document')."""
    _registry: Dict[str, BasePolicy] = {}

    @classmethod
    def register(cls, name: str, policy: BasePolicy) -> None:
        cls._registry[name] = policy

    @classmethod
    def get(cls, name: str) -> BasePolicy:
        return cls._registry.get(name, BasePolicy())

def authorize(user_id: str, action: str, scope: str, resource: Optional[Dict]=None) -> bool:
    """Convenience helper para verificar autorização usando o registry.

    - `scope` é o nome lógico da política (ex: 'citizen').
    """
    policy = PolicyRegistry.get(scope)
    return policy.check(user_id, action, resource)
__all__ = ['DataSegment', 'BasePolicy', 'PolicyRegistry', 'authorize']

class PermissionPolicyModel(Base):
    __tablename__ = 'permission_policies'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id: Mapped[str] = mapped_column(String(length=100), index=True, nullable=False)
    data_segment: Mapped[str] = mapped_column(String(length=100), index=True, nullable=False)
    can_read: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    can_write: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

@dataclass
class PermissionPolicyCreate:
    service_id: str
    data_segment: str
    can_read: bool = True
    can_write: bool = False

@dataclass
class PermissionPolicyUpdate:
    can_read: Optional[bool] = None
    can_write: Optional[bool] = None
__all__.extend(['PermissionPolicyModel', 'PermissionPolicyCreate', 'PermissionPolicyUpdate'])