from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sila_platform.governance.territory.constants import NivelTerritorial
from sila_platform.governance.territory.models import TerritorialScope as GovTerritorialScope


@dataclass
class TerritorialScope:
    """Âmbito territorial da Educação. Reutiliza a governance com alias para school."""
    nivel: NivelTerritorial = NivelTerritorial.NACIONAL
    province_id: Optional[str] = None
    province_name: Optional[str] = None
    municipality_id: Optional[str] = None
    municipality_name: Optional[str] = None
    school_id: Optional[str] = None
    school_name: Optional[str] = None
    institution_id: Optional[str] = None
    institution_type: Optional[str] = None

    def _to_gov(self) -> GovTerritorialScope:
        return GovTerritorialScope(
            nivel=self.nivel,
            province_id=self.province_id,
            province_name=self.province_name,
            municipality_id=self.municipality_id,
            municipality_name=self.municipality_name,
            unit_id=self.school_id,
            unit_name=self.school_name,
            institution_id=self.institution_id,
            institution_type=self.institution_type,
        )

    @classmethod
    def _from_gov(cls, gov: GovTerritorialScope) -> TerritorialScope:
        return cls(
            nivel=gov.nivel,
            province_id=gov.province_id,
            province_name=gov.province_name,
            municipality_id=gov.municipality_id,
            municipality_name=gov.municipality_name,
            school_id=gov.unit_id,
            school_name=gov.unit_name,
            institution_id=gov.institution_id,
            institution_type=gov.institution_type,
        )

    def covers(self, other: TerritorialScope) -> bool:
        return self._to_gov().covers(other._to_gov())

    def to_dict(self) -> dict:
        return self._to_gov().to_dict()
