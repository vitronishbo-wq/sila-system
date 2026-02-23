from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4


@dataclass
class WorkflowDefinition:
    """Definição do workflow (template)"""
    # Required fields (must come first in dataclass)
    code: str
    name: str
    entity_type: str  # SERVICE_REQUEST, CITIZEN, etc

    # Optional / defaults
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    version: int = 1
    
    # Configurações
    is_active: bool = True
    is_public: bool = False
    timeout_hours: Optional[int] = None  # SLA global
    
    # Metadados
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    
    def __post_init__(self):
        if not self.code or len(self.code.strip()) < 2:
            raise ValueError("Código deve ter pelo menos 2 caracteres")
        self.code = self.code.upper().strip()
    
    def activate(self):
        """Ativa o workflow"""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def deactivate(self):
        """Desativa o workflow"""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def new_version(self) -> 'WorkflowDefinition':
        """Cria nova versão do workflow"""
        return WorkflowDefinition(
            code=self.code,
            name=self.name,
            description=self.description,
            version=self.version + 1,
            entity_type=self.entity_type,
            is_active=True,
            metadata=self.metadata.copy(),
            tags=self.tags.copy()
        )
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "entity_type": self.entity_type,
            "is_active": self.is_active,
            "is_public": self.is_public,
            "timeout_hours": self.timeout_hours,
            "metadata": self.metadata,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": str(self.created_by) if self.created_by else None
        }
