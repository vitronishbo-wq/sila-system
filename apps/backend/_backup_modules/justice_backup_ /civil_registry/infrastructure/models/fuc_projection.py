from dataclasses import dataclass, field
from typing import Final, Optional, Dict, Any
from datetime import datetime, date

@dataclass(frozen=True)
class FucAddress:
    """Projeção de Morada Soberana vinda do FUC."""
    province: Final[str]
    municipality: Final[str]
    district: Final[str]
    neighborhood: Final[str]
    street: Final[Optional[str]] = None
    house_number: Final[Optional[str]] = None

@dataclass(frozen=True)
class FucParents:
    """Projeção de Filiação Soberana vinda do FUC."""
    father_full_name: Final[str]
    mother_full_name: Final[str]

@dataclass(frozen=True)
class FucSovereigntyProjection:
    """
    CONTRATO OFICIAL DE SOBERANIA (FUC)
    Este DTO é a única representação válida do cidadão no módulo Identidade Civil.
    Qualquer dado aqui contido é considerado 'Verdade Soberana'.
    """
    fuc_id: Final[str]
    full_name: Final[str]
    birth_date: Final[date]
    gender: Final[str]
    nationality: Final[str]
    place_of_birth: Final[str]
    civil_status: Final[str]
    parents: Final[FucParents]
    address: Final[FucAddress]
    is_alive: Final[bool] = True
    sync_timestamp: Final[datetime] = field(default_factory=datetime.utcnow)
    metadata: Final[Dict[str, Any]] = field(default_factory=dict)

    def to_summary(self) -> Dict[str, str]:
        """Gera um resumo biográfico para logs e interfaces rápidas."""
        return {'id': self.fuc_id, 'nome': self.full_name, 'status': 'VIVO' if self.is_alive else 'ÓBITO', 'sync': self.sync_timestamp.strftime('%Y-%m-%d %H:%M:%S')}