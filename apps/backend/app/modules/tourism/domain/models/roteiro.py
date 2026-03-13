from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

@dataclass
class Roteiro:
    id: UUID
    codigo: str
    titulo: str
    descricao: str
    municipio_origem: str
    provincia_origem: str
    duracao_horas: int
    pontos_parada: list[str]
    acessivel: bool
    ativo: bool = True
    valor_estimado: Decimal | None = None
    meios_transporte_sugeridos: list[str] | None = None
    parceiros_comerciais: list[str] | None = None
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, titulo: str, descricao: str, municipio_origem: str, provincia_origem: str, duracao_horas: int, pontos_parada: list[str] | None=None, acessivel: bool=True, valor_estimado: Decimal | None=None, observacoes: str | None=None) -> 'Roteiro':
        if duracao_horas <= 0:
            raise ValueError('Duracao deve ser maior que zero')
        if valor_estimado is not None and valor_estimado < 0:
            raise ValueError('Valor estimado nao pode ser negativo')
        return cls(id=uuid4(), codigo='', titulo=titulo.strip(), descricao=descricao.strip(), municipio_origem=municipio_origem.strip(), provincia_origem=provincia_origem.strip(), duracao_horas=duracao_horas, pontos_parada=list(pontos_parada or []), acessivel=acessivel, ativo=True, valor_estimado=valor_estimado, meios_transporte_sugeridos=[], parceiros_comerciais=[], observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, titulo: str | None=None, descricao: str | None=None, municipio_origem: str | None=None, provincia_origem: str | None=None, duracao_horas: int | None=None, pontos_parada: list[str] | None=None, acessivel: bool | None=None, valor_estimado: Decimal | None=None, observacoes: str | None=None) -> None:
        if duracao_horas is not None and duracao_horas <= 0:
            raise ValueError('Duracao deve ser maior que zero')
        if valor_estimado is not None and valor_estimado < 0:
            raise ValueError('Valor estimado nao pode ser negativo')
        if titulo is not None:
            self.titulo = titulo.strip()
        if descricao is not None:
            self.descricao = descricao.strip()
        if municipio_origem is not None:
            self.municipio_origem = municipio_origem.strip()
        if provincia_origem is not None:
            self.provincia_origem = provincia_origem.strip()
        if duracao_horas is not None:
            self.duracao_horas = duracao_horas
        if pontos_parada is not None:
            self.pontos_parada = list(pontos_parada)
        if acessivel is not None:
            self.acessivel = acessivel
        if valor_estimado is not None:
            self.valor_estimado = valor_estimado
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def atualizar_integracoes(self, *, meios_transporte_sugeridos: list[str] | None=None, parceiros_comerciais: list[str] | None=None) -> None:
        if meios_transporte_sugeridos is not None:
            self.meios_transporte_sugeridos = list(meios_transporte_sugeridos)
        if parceiros_comerciais is not None:
            self.parceiros_comerciais = list(parceiros_comerciais)

    def ativar(self) -> None:
        self.ativo = True

    def desativar(self) -> None:
        self.ativo = False