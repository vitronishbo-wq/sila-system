from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional
import uuid

class BIStatus(Enum):
    """Estados administrativos do documento no módulo de Identidade Civil."""
    DRAFT = 'DRAFT'
    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    SUSPENDED = 'SUSPENDED'
    CANCELLED = 'CANCELLED'
    LOST = 'LOST'

@dataclass(frozen=True)
class BI:
    """
    Entidade Bilhete de Identidade.
    Soberania: Este modelo NÃO armazena dados biográficos (nome, filiação, etc).
    Esses dados devem ser sempre consultados no FUC via citizen_fuc_id.
    """
    citizen_fuc_id: str
    bi_number: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    issue_date: date = field(default_factory=date.today)
    expiry_date: Optional[date] = None
    status: BIStatus = BIStatus.DRAFT
    version: int = 1

    @property
    def is_valid(self) -> bool:
        """Verifica se o documento é válido para identificação oficial."""
        if self.status != BIStatus.ACTIVE:
            return False
        if self.expiry_date and self.expiry_date < date.today():
            return False
        return True

    @property
    def is_expired(self) -> bool:
        """Verifica se o documento já passou da data de validade."""
        return self.expiry_date is not None and self.expiry_date < date.today()

    def with_status(self, new_status: BIStatus) -> 'BI':
        """Cria uma nova instância com estado atualizado (Imutabilidade)."""
        return dataclass.replace(self, status=new_status, version=self.version + 1)