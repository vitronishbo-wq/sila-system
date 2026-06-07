from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusPoliticaJuventude,
)


@dataclass
class PoliticaJuventude:
    id: UUID
    codigo_politica: str
    nome: str
    descricao: str
    area_interesse: AreaInteresse
    data_inicio: date
    data_cadastro: date
    status: StatusPoliticaJuventude = StatusPoliticaJuventude.RASCUNHO
    metas: dict[str, float] | None = None
    indicadores: list[str] | None = None
    data_fim: date | None = None
    observacoes: str | None = None
    ativa: bool = True

    @classmethod
    def criar(
        cls,
        *,
        codigo_politica: str,
        nome: str,
        descricao: str,
        area_interesse: AreaInteresse,
        data_inicio: date,
        metas: dict[str, float] | None = None,
        indicadores: list[str] | None = None,
        data_fim: date | None = None,
        observacoes: str | None = None,
    ) -> PoliticaJuventude:
        if len(nome.strip()) < 3:
            raise ValueError("Nome da politica deve ter pelo menos 3 caracteres")
        if len(descricao.strip()) < 10:
            raise ValueError("Descricao da politica deve ter pelo menos 10 caracteres")
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError("Data fim da politica deve ser maior ou igual a data inicio")
        return cls(
            id=uuid4(),
            codigo_politica=codigo_politica.strip(),
            nome=nome.strip(),
            descricao=descricao.strip(),
            area_interesse=area_interesse,
            data_inicio=data_inicio,
            data_fim=data_fim,
            data_cadastro=date.today(),
            metas=metas,
            indicadores=indicadores,
            observacoes=observacoes.strip() if observacoes else None,
            status=StatusPoliticaJuventude.RASCUNHO,
            ativa=True,
        )

    def atualizar_status(self, status: StatusPoliticaJuventude) -> None:
        self.status = status
        self.ativa = status not in {
            StatusPoliticaJuventude.CONCLUIDA,
            StatusPoliticaJuventude.SUSPENSA,
        }
