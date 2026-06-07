from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import (
    StatusEquipamento,
    TipoEquipamento,
)


@dataclass
class Equipamento:
    id: UUID
    codigo_equipamento: str
    nome: str
    tipo: TipoEquipamento
    fabricante: str | None
    modelo: str | None
    ano_fabricacao: int | None
    data_aquisicao: date | None
    status: StatusEquipamento
    horas_uso: float
    ultima_manutencao: date | None = None

    @classmethod
    def cadastrar(
        cls,
        *,
        nome: str,
        tipo: TipoEquipamento,
        fabricante: str | None = None,
        modelo: str | None = None,
        ano_fabricacao: int | None = None,
        data_aquisicao: date | None = None,
    ) -> Equipamento:
        if ano_fabricacao is not None:
            ano_atual = date.today().year
            if ano_fabricacao < 1950 or ano_fabricacao > ano_atual + 1:
                raise ValueError("Ano de fabricacao invalido")
        return cls(
            id=uuid4(),
            codigo_equipamento="",
            nome=nome,
            tipo=tipo,
            fabricante=fabricante,
            modelo=modelo,
            ano_fabricacao=ano_fabricacao,
            data_aquisicao=data_aquisicao,
            status=StatusEquipamento.DISPONIVEL,
            horas_uso=0.0,
        )

    def iniciar_uso(self) -> None:
        if self.status != StatusEquipamento.DISPONIVEL:
            raise ValueError("Equipamento nao esta disponivel para uso")
        self.status = StatusEquipamento.EM_USO

    def registrar_uso(self, horas: float) -> None:
        if self.status != StatusEquipamento.EM_USO:
            raise ValueError("Equipamento deve estar em uso para registrar horas")
        if horas <= 0:
            raise ValueError("Horas de uso devem ser maiores que zero")
        self.horas_uso = round(self.horas_uso + horas, 2)

    def finalizar_uso(self) -> None:
        if self.status != StatusEquipamento.EM_USO:
            raise ValueError("Equipamento nao esta em uso")
        self.status = StatusEquipamento.DISPONIVEL

    def enviar_manutencao(self) -> None:
        if self.status == StatusEquipamento.INATIVO:
            raise ValueError("Equipamento inativo nao pode ir para manutencao")
        self.status = StatusEquipamento.EM_MANUTENCAO

    def concluir_manutencao(self) -> None:
        if self.status != StatusEquipamento.EM_MANUTENCAO:
            raise ValueError("Equipamento nao esta em manutencao")
        self.status = StatusEquipamento.DISPONIVEL
        self.ultima_manutencao = date.today()

    def inativar(self) -> None:
        if self.status == StatusEquipamento.EM_USO:
            raise ValueError("Nao e possivel inativar equipamento em uso")
        self.status = StatusEquipamento.INATIVO
