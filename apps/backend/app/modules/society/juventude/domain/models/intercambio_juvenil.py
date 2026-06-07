from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusIntercambio


@dataclass
class IntercambioJuvenil:
    id: UUID
    codigo_intercambio: str
    jovem_id: UUID
    pais_destino: str
    instituicao_destino: str
    area_interesse: AreaInteresse
    data_inicio: date
    data_cadastro: date
    status: StatusIntercambio = StatusIntercambio.SOLICITADO
    data_fim: date | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def solicitar(
        cls,
        *,
        codigo_intercambio: str,
        jovem_id: UUID,
        pais_destino: str,
        instituicao_destino: str,
        area_interesse: AreaInteresse,
        data_inicio: date,
        data_fim: date | None = None,
        observacoes: str | None = None,
    ) -> IntercambioJuvenil:
        if len(pais_destino.strip()) < 2:
            raise ValueError("Pais destino invalido")
        if len(instituicao_destino.strip()) < 3:
            raise ValueError("Instituicao destino deve ter pelo menos 3 caracteres")
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError("Data fim do intercambio deve ser maior ou igual a data inicio")
        return cls(
            id=uuid4(),
            codigo_intercambio=codigo_intercambio.strip(),
            jovem_id=jovem_id,
            pais_destino=pais_destino.strip(),
            instituicao_destino=instituicao_destino.strip(),
            area_interesse=area_interesse,
            data_inicio=data_inicio,
            data_fim=data_fim,
            data_cadastro=date.today(),
            observacoes=observacoes.strip() if observacoes else None,
            status=StatusIntercambio.SOLICITADO,
            ativo=True,
        )

    def atualizar_status(self, status: StatusIntercambio) -> None:
        self.status = status
        self.ativo = status not in {StatusIntercambio.CANCELADO, StatusIntercambio.CONCLUIDO}
        if status == StatusIntercambio.CONCLUIDO and self.data_fim is None:
            self.data_fim = date.today()
