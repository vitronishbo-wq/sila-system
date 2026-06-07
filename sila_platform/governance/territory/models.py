from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from sila_platform.governance.territory.constants import NivelTerritorial, nivel_index


@dataclass
class TerritorialScope:
    """Âmbito territorial genérico para qualquer módulo governamental."""
    nivel: NivelTerritorial = NivelTerritorial.NACIONAL
    province_id: Optional[str] = None
    province_name: Optional[str] = None
    municipality_id: Optional[str] = None
    municipality_name: Optional[str] = None
    unit_id: Optional[str] = None
    unit_name: Optional[str] = None
    institution_id: Optional[str] = None
    institution_type: Optional[str] = None

    def covers(self, other: TerritorialScope) -> bool:
        self_idx = nivel_index(self.nivel.value)
        other_idx = nivel_index(other.nivel.value)

        if self_idx == 0:
            return True
        if self_idx > other_idx:
            return False
        if self_idx == 1 and self.province_id and other.province_id:
            return self.province_id == other.province_id
        if self_idx == 2 and self.municipality_id and other.municipality_id:
            if self.province_id and other.province_id and self.province_id != other.province_id:
                return False
            return self.municipality_id == other.municipality_id
        if self_idx >= 3 and self.unit_id and other.unit_id:
            return self.unit_id == other.unit_id
        return False

    def to_dict(self) -> dict:
        return {
            "nivel": self.nivel.value,
            "province_id": self.province_id,
            "province_name": self.province_name,
            "municipality_id": self.municipality_id,
            "municipality_name": self.municipality_name,
            "unit_id": self.unit_id,
            "unit_name": self.unit_name,
            "institution_id": self.institution_id,
            "institution_type": self.institution_type,
        }
