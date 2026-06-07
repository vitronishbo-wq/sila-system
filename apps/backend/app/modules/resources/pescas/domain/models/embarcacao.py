from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.pescas.domain.enums import ModalidadePesca, TipoEmbarcacao


@dataclass
class Embarcacao:
    id: UUID
    nome: str
    numero_inscricao: str
    tipo: TipoEmbarcacao
    modalidades: list[ModalidadePesca]
    comprimento: Decimal
    arqueacao_bruta: Decimal
    tripulacao_minima: int
    porto_registro: str
    ano_construcao: int
    material_casco: str
    proprietario_id: UUID
    potencia_motor: Decimal | None = None
    capacidade_porao: Decimal | None = None
    armador_id: UUID | None = None
    licenca_id: UUID | None = None
    equipamentos_seguranca: list[str] = field(default_factory=list)
    sistema_rastreio: str | None = None
    data_inspecao: date | None = None
    data_validade_doc: date | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        nome: str,
        numero_inscricao: str,
        tipo: TipoEmbarcacao,
        comprimento: Decimal,
        arqueacao_bruta: Decimal,
        porto_registro: str,
        proprietario_id: UUID,
        modalidades: list[ModalidadePesca] | None = None,
    ) -> Embarcacao:
        return cls(
            id=uuid4(),
            nome=nome,
            numero_inscricao=numero_inscricao,
            tipo=tipo,
            modalidades=modalidades or [],
            comprimento=comprimento,
            arqueacao_bruta=arqueacao_bruta,
            tripulacao_minima=1,
            porto_registro=porto_registro,
            ano_construcao=date.today().year,
            material_casco="nao informado",
            proprietario_id=proprietario_id,
        )
