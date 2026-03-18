from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.tourism.domain.enums import TipoAtracao

@dataclass
class AtracaoTuristica:
    id: UUID
    codigo: str
    nome: str
    tipo: TipoAtracao
    descricao: str
    endereco: str
    municipio: str
    provincia: str
    horario_funcionamento: str
    acessivel: bool
    ativa: bool = True
    gratuita: bool = False
    capacidade_visitantes_dia: int | None = None
    valor_entrada: Decimal | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, tipo: TipoAtracao, descricao: str, endereco: str, municipio: str, provincia: str, horario_funcionamento: str, acessivel: bool, gratuita: bool=False, capacidade_visitantes_dia: int | None=None, valor_entrada: Decimal | None=None, latitude: Decimal | None=None, longitude: Decimal | None=None, observacoes: str | None=None) -> 'AtracaoTuristica':
        if capacidade_visitantes_dia is not None and capacidade_visitantes_dia <= 0:
            raise ValueError('Capacidade de visitantes deve ser maior que zero')
        if valor_entrada is not None and valor_entrada < 0:
            raise ValueError('Valor da entrada nao pode ser negativo')
        return cls(id=uuid4(), codigo='', nome=nome.strip(), tipo=tipo, descricao=descricao.strip(), endereco=endereco.strip(), municipio=municipio.strip(), provincia=provincia.strip(), horario_funcionamento=horario_funcionamento.strip(), acessivel=acessivel, gratuita=gratuita, capacidade_visitantes_dia=capacidade_visitantes_dia, valor_entrada=valor_entrada, latitude=latitude, longitude=longitude, observacoes=observacoes.strip() if observacoes else None, ativa=True)

    def atualizar(self, *, nome: str | None=None, tipo: TipoAtracao | None=None, descricao: str | None=None, endereco: str | None=None, municipio: str | None=None, provincia: str | None=None, horario_funcionamento: str | None=None, acessivel: bool | None=None, gratuita: bool | None=None, capacidade_visitantes_dia: int | None=None, valor_entrada: Decimal | None=None, latitude: Decimal | None=None, longitude: Decimal | None=None, observacoes: str | None=None) -> None:
        if capacidade_visitantes_dia is not None and capacidade_visitantes_dia <= 0:
            raise ValueError('Capacidade de visitantes deve ser maior que zero')
        if valor_entrada is not None and valor_entrada < 0:
            raise ValueError('Valor da entrada nao pode ser negativo')
        if nome is not None:
            self.nome = nome.strip()
        if tipo is not None:
            self.tipo = tipo
        if descricao is not None:
            self.descricao = descricao.strip()
        if endereco is not None:
            self.endereco = endereco.strip()
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if horario_funcionamento is not None:
            self.horario_funcionamento = horario_funcionamento.strip()
        if acessivel is not None:
            self.acessivel = acessivel
        if gratuita is not None:
            self.gratuita = gratuita
        if capacidade_visitantes_dia is not None:
            self.capacidade_visitantes_dia = capacidade_visitantes_dia
        if valor_entrada is not None:
            self.valor_entrada = valor_entrada
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None

    def desativar(self) -> None:
        self.ativa = False

    def ativar(self) -> None:
        self.ativa = True