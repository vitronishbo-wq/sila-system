from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4
from apps.backend.app.modules.logistics.domain.enums import StatusVeiculoOperacional, TipoVeiculo

@dataclass
class Veiculo:
    id: UUID
    placa: str
    tipo: TipoVeiculo
    marca: str
    modelo: str
    ano_fabricacao: int
    ano_modelo: int
    proprietario_id: UUID
    proprietario_tipo: str
    data_aquisicao: date
    status: StatusVeiculoOperacional
    capacidade_passageiros: int | None = None
    capacidade_carga_kg: Decimal | None = None
    capacidade_carga_m3: Decimal | None = None
    comprimento: Decimal | None = None
    largura: Decimal | None = None
    altura: Decimal | None = None
    peso_bruto_total: Decimal | None = None
    numero_eixos: int | None = None
    combustivel: str | None = None
    consumo_medio: Decimal | None = None
    operadora_id: UUID | None = None
    licenciamento: dict[str, Any] | None = None
    seguro: dict[str, Any] | None = None
    rastreador_id: str | None = None
    data_ultima_manutencao: date | None = None
    data_proxima_manutencao: date | None = None
    quilometragem: int | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None

    @classmethod
    def cadastrar(cls, *, placa: str, tipo: TipoVeiculo, marca: str, modelo: str, ano_fabricacao: int, ano_modelo: int, proprietario_id: UUID, proprietario_tipo: str, data_aquisicao: date, capacidade_passageiros: int | None=None, operadora_id: UUID | None=None, observacoes: str | None=None) -> 'Veiculo':
        normalized = placa.strip().upper()
        if not normalized:
            raise ValueError('Placa do veiculo e obrigatoria')
        if not marca.strip() or not modelo.strip():
            raise ValueError('Marca e modelo do veiculo sao obrigatorios')
        if ano_fabricacao <= 1950 or ano_modelo <= 1950:
            raise ValueError('Ano do veiculo invalido')
        return cls(id=uuid4(), placa=normalized, tipo=tipo, marca=marca.strip(), modelo=modelo.strip(), ano_fabricacao=ano_fabricacao, ano_modelo=ano_modelo, proprietario_id=proprietario_id, proprietario_tipo=proprietario_tipo.strip().lower(), data_aquisicao=data_aquisicao, status=StatusVeiculoOperacional.ATIVO, capacidade_passageiros=capacidade_passageiros, operadora_id=operadora_id, observacoes=observacoes.strip() if observacoes else None)

    def atualizar_quilometragem(self, km: int) -> None:
        if km < 0:
            raise ValueError('Quilometragem do veiculo nao pode ser negativa')
        if self.quilometragem is not None and km < self.quilometragem:
            raise ValueError('Quilometragem nao pode reduzir')
        self.quilometragem = km
        self.data_atualizacao = date.today()

    def registrar_manutencao(self, *, data_manutencao: date, proxima_manutencao: date | None=None) -> None:
        self.data_ultima_manutencao = data_manutencao
        self.data_proxima_manutencao = proxima_manutencao
        self.status = StatusVeiculoOperacional.ATIVO
        self.data_atualizacao = date.today()

    def bloquear(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo do bloqueio do veiculo e obrigatorio')
        self.status = StatusVeiculoOperacional.BLOQUEADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()