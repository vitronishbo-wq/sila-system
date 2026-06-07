from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusZoneamento,
    TipoZona,
    UsoPermitido,
)


@dataclass
class Zoneamento:
    id: UUID
    codigo_zoneamento: str
    nome: str
    tipo_zona: TipoZona
    status: StatusZoneamento
    plano_diretor_id: UUID
    provincia: str
    usos_permitidos: list[UsoPermitido]
    municipio: str | None = None
    coeficiente_aproveitamento_max: Decimal | None = None
    taxa_ocupacao_max: Decimal | None = None
    gabarito_maximo: int | None = None
    recuo_frontal_minimo: Decimal | None = None
    permeabilidade_minima: Decimal | None = None
    area_lote_minima: Decimal | None = None
    data_inicio_vigencia: date | None = None
    data_cadastro: date = field(default_factory=date.today)
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        codigo_zoneamento: str,
        nome: str,
        tipo_zona: TipoZona,
        plano_diretor_id: UUID,
        provincia: str,
        usos_permitidos: list[UsoPermitido],
        municipio: str | None = None,
    ) -> Zoneamento:
        if not codigo_zoneamento.strip():
            raise ValueError("Codigo do zoneamento e obrigatorio")
        if not nome.strip():
            raise ValueError("Nome do zoneamento e obrigatorio")
        if not provincia.strip():
            raise ValueError("Provincia e obrigatoria")
        if not usos_permitidos:
            raise ValueError("Pelo menos um uso permitido deve ser informado")
        return cls(
            id=uuid4(),
            codigo_zoneamento=codigo_zoneamento.strip(),
            nome=nome.strip(),
            tipo_zona=tipo_zona,
            status=StatusZoneamento.ELABORACAO,
            plano_diretor_id=plano_diretor_id,
            provincia=provincia.strip(),
            municipio=municipio.strip() if municipio else None,
            usos_permitidos=usos_permitidos,
        )

    def iniciar_consulta_publica(self) -> None:
        if self.status != StatusZoneamento.ELABORACAO:
            raise ValueError("Zoneamento precisa estar em elaboracao")
        self.status = StatusZoneamento.EM_CONSULTA
        self.data_atualizacao = date.today()

    def aprovar(self) -> None:
        if self.status not in {StatusZoneamento.ELABORACAO, StatusZoneamento.EM_CONSULTA}:
            raise ValueError("Zoneamento nao pode ser aprovado neste status")
        self.status = StatusZoneamento.APROVADO
        self.data_atualizacao = date.today()

    def vigorar(self, *, data_inicio_vigencia: date) -> None:
        if self.status != StatusZoneamento.APROVADO:
            raise ValueError("Zoneamento precisa estar aprovado")
        self.status = StatusZoneamento.VIGENTE
        self.data_inicio_vigencia = data_inicio_vigencia
        self.data_atualizacao = date.today()

    def suspender(self, *, motivo: str) -> None:
        if self.status != StatusZoneamento.VIGENTE:
            raise ValueError("Apenas zoneamento vigente pode ser suspenso")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao e obrigatorio")
        self.status = StatusZoneamento.SUSPENSO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def revogar(self, *, motivo: str) -> None:
        if self.status == StatusZoneamento.REVOGADO:
            raise ValueError("Zoneamento ja esta revogado")
        if not motivo.strip():
            raise ValueError("Motivo da revogacao e obrigatorio")
        self.status = StatusZoneamento.REVOGADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def atualizar_parametros(
        self,
        *,
        usos_permitidos: list[UsoPermitido] | None = None,
        coeficiente_aproveitamento_max: Decimal | None = None,
        taxa_ocupacao_max: Decimal | None = None,
        gabarito_maximo: int | None = None,
        recuo_frontal_minimo: Decimal | None = None,
        permeabilidade_minima: Decimal | None = None,
        area_lote_minima: Decimal | None = None,
    ) -> None:
        if usos_permitidos is not None:
            if not usos_permitidos:
                raise ValueError("Usos permitidos nao pode ser vazio")
            self.usos_permitidos = usos_permitidos
        if coeficiente_aproveitamento_max is not None:
            self.coeficiente_aproveitamento_max = coeficiente_aproveitamento_max
        if taxa_ocupacao_max is not None:
            self.taxa_ocupacao_max = taxa_ocupacao_max
        if gabarito_maximo is not None:
            self.gabarito_maximo = gabarito_maximo
        if recuo_frontal_minimo is not None:
            self.recuo_frontal_minimo = recuo_frontal_minimo
        if permeabilidade_minima is not None:
            self.permeabilidade_minima = permeabilidade_minima
        if area_lote_minima is not None:
            self.area_lote_minima = area_lote_minima
        self.data_atualizacao = date.today()
