from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.pescas.industrial.domain.enums import (
    ClassificacaoIndustrial,
    TipoProcessamento,
)


@dataclass
class UnidadeProcessamento:
    id: UUID
    cnpj: str
    razao_social: str
    tipo_processamento: list[TipoProcessamento]
    classificacao: ClassificacaoIndustrial
    capacidade_kg_dia: Decimal
    area_total_m2: Decimal
    area_producao_m2: Decimal
    area_armazenagem_m2: Decimal
    numero_funcionarios: int
    endereco: str
    municipio: str
    provincia: str
    data_inauguracao: date
    nome_fantasia: str | None = None
    inscricao_estadual: str | None = None
    inscricao_municipal: str | None = None
    capacidade_frigorifica_m3: Decimal | None = None
    temperatura_media: Decimal | None = None
    responsavel_tecnico_id: UUID | None = None
    responsavel_tecnico_registro: str | None = None
    coordenadas_lat: Decimal | None = None
    coordenadas_long: Decimal | None = None
    armador_id: UUID | None = None
    licenca_operacao_id: UUID | None = None
    alvara_sanitario_id: UUID | None = None
    certificacoes: list[UUID] | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        cnpj: str,
        razao_social: str,
        tipo_processamento: list[TipoProcessamento],
        classificacao: ClassificacaoIndustrial,
        capacidade_kg_dia: Decimal,
        area_total_m2: Decimal,
        area_producao_m2: Decimal,
        area_armazenagem_m2: Decimal,
        numero_funcionarios: int,
        endereco: str,
        municipio: str,
        provincia: str,
    ) -> UnidadeProcessamento:
        if not tipo_processamento:
            raise ValueError("Tipo de processamento e obrigatorio")
        if capacidade_kg_dia <= 0:
            raise ValueError("Capacidade diaria deve ser maior que zero")
        if area_total_m2 <= 0 or area_producao_m2 <= 0 or area_armazenagem_m2 <= 0:
            raise ValueError("Areas devem ser maiores que zero")
        if numero_funcionarios < 1:
            raise ValueError("Numero de funcionarios deve ser no minimo 1")
        return cls(
            id=uuid4(),
            cnpj=cnpj.strip(),
            razao_social=razao_social.strip(),
            tipo_processamento=list(tipo_processamento),
            classificacao=classificacao,
            capacidade_kg_dia=capacidade_kg_dia,
            area_total_m2=area_total_m2,
            area_producao_m2=area_producao_m2,
            area_armazenagem_m2=area_armazenagem_m2,
            numero_funcionarios=numero_funcionarios,
            endereco=endereco.strip(),
            municipio=municipio.strip(),
            provincia=provincia.strip(),
            data_inauguracao=date.today(),
        )

    def atualizar_capacidade(self, capacidade_kg_dia: Decimal) -> None:
        if capacidade_kg_dia <= 0:
            raise ValueError("Capacidade diaria deve ser maior que zero")
        self.capacidade_kg_dia = capacidade_kg_dia

    def atualizar_responsavel_tecnico(
        self, *, responsavel_tecnico_id: UUID | None, responsavel_tecnico_registro: str | None
    ) -> None:
        self.responsavel_tecnico_id = responsavel_tecnico_id
        self.responsavel_tecnico_registro = (
            responsavel_tecnico_registro.strip() if responsavel_tecnico_registro else None
        )
