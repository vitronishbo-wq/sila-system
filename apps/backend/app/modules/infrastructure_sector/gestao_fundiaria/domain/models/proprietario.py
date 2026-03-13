from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import TipoPessoa, TipoTitularidade

@dataclass
class Proprietario:
    id: UUID
    numero_cadastro: str
    nome: str
    documento: str
    tipo_pessoa: TipoPessoa
    tipo_titularidade: TipoTitularidade
    data_cadastro: date
    ativo: bool = True
    percentual_titularidade: Decimal | None = None
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, documento: str, tipo_pessoa: TipoPessoa, tipo_titularidade: TipoTitularidade, numero_cadastro: str='', percentual_titularidade: Decimal | None=None, email: str | None=None, telefone: str | None=None, endereco: str | None=None) -> 'Proprietario':
        if not nome.strip():
            raise ValueError('Nome do proprietario e obrigatorio')
        if not documento.strip():
            raise ValueError('Documento do proprietario e obrigatorio')
        if percentual_titularidade is not None and (percentual_titularidade <= Decimal('0') or percentual_titularidade > Decimal('100')):
            raise ValueError('Percentual de titularidade deve estar entre 0 e 100')
        if tipo_titularidade == TipoTitularidade.COTITULAR and percentual_titularidade is None:
            raise ValueError('Cotitular deve informar percentual de titularidade')
        return cls(id=uuid4(), numero_cadastro=numero_cadastro, nome=nome.strip(), documento=documento.strip(), tipo_pessoa=tipo_pessoa, tipo_titularidade=tipo_titularidade, data_cadastro=date.today(), percentual_titularidade=percentual_titularidade.quantize(Decimal('0.01')) if percentual_titularidade is not None else None, email=email.strip() if email else None, telefone=telefone.strip() if telefone else None, endereco=endereco.strip() if endereco else None, ativo=True)

    def atualizar_contato(self, *, email: str | None=None, telefone: str | None=None, endereco: str | None=None) -> None:
        if email is not None:
            self.email = email.strip() or None
        if telefone is not None:
            self.telefone = telefone.strip() or None
        if endereco is not None:
            self.endereco = endereco.strip() or None
        self.data_atualizacao = date.today()

    def atualizar_titularidade(self, *, tipo_titularidade: TipoTitularidade, percentual_titularidade: Decimal | None=None) -> None:
        if percentual_titularidade is not None and (percentual_titularidade <= Decimal('0') or percentual_titularidade > Decimal('100')):
            raise ValueError('Percentual de titularidade deve estar entre 0 e 100')
        if tipo_titularidade == TipoTitularidade.COTITULAR and percentual_titularidade is None:
            raise ValueError('Cotitular deve informar percentual de titularidade')
        self.tipo_titularidade = tipo_titularidade
        self.percentual_titularidade = percentual_titularidade.quantize(Decimal('0.01')) if percentual_titularidade is not None else None
        self.data_atualizacao = date.today()

    def desativar(self, motivo: str) -> None:
        if not motivo.strip():
            raise ValueError('Motivo da desativacao e obrigatorio')
        self.ativo = False
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()