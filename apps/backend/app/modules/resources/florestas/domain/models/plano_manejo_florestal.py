from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.florestas.domain.enums import StatusPlanoManejo


@dataclass
class PlanoManejoFlorestal:
    id: UUID
    numero_pmfs: str
    unidade_manejo_id: UUID
    responsavel_tecnico_id: UUID
    responsavel_tecnico_registro: str
    status: StatusPlanoManejo
    data_submissao: date
    data_aprovacao: date | None = None
    data_validade: date | None = None
    analista_responsavel_id: UUID | None = None
    volume_anual_estimado_m3: Decimal = Decimal("0")
    ciclo_corte_anos: int = 1
    area_anual_ha: Decimal = Decimal("0")
    parecer_tecnico: str | None = None
    observacoes: str | None = None

    @classmethod
    def submeter(
        cls,
        *,
        numero_pmfs: str,
        unidade_manejo_id: UUID,
        responsavel_tecnico_id: UUID,
        responsavel_tecnico_registro: str,
        volume_anual_estimado_m3: Decimal,
        ciclo_corte_anos: int,
        area_anual_ha: Decimal,
    ) -> PlanoManejoFlorestal:
        return cls(
            id=uuid4(),
            numero_pmfs=numero_pmfs,
            unidade_manejo_id=unidade_manejo_id,
            responsavel_tecnico_id=responsavel_tecnico_id,
            responsavel_tecnico_registro=responsavel_tecnico_registro,
            status=StatusPlanoManejo.SUBMETIDO,
            data_submissao=date.today(),
            volume_anual_estimado_m3=volume_anual_estimado_m3,
            ciclo_corte_anos=ciclo_corte_anos,
            area_anual_ha=area_anual_ha,
        )

    def aprovar(self, *, data_aprovacao: date, data_validade: date, analista_id: UUID) -> None:
        self.status = StatusPlanoManejo.APROVADO
        self.data_aprovacao = data_aprovacao
        self.data_validade = data_validade
        self.analista_responsavel_id = analista_id
