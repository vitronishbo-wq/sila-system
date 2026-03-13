from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusAssinante, TipoPlano, TipoServico

@dataclass
class Assinante:
    id: UUID
    codigo_assinante: str
    operadora_id: UUID
    tipo_plano: TipoPlano
    servico_principal: TipoServico
    data_adesao: date
    status: StatusAssinante
    municipio: str
    provincia: str
    nome: str | None = None
    citizen_id: UUID | None = None
    telefone_contato: str | None = None
    email_contato: str | None = None
    contrato_numero: str | None = None
    valor_mensal: float | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, codigo_assinante: str, operadora_id: UUID, tipo_plano: TipoPlano, servico_principal: TipoServico, municipio: str, provincia: str, nome: str | None=None, citizen_id: UUID | None=None, telefone_contato: str | None=None, email_contato: str | None=None, contrato_numero: str | None=None, valor_mensal: float | None=None, observacoes: str | None=None) -> 'Assinante':
        if valor_mensal is not None and valor_mensal < 0:
            raise ValueError('Valor mensal nao pode ser negativo')
        return cls(id=uuid4(), codigo_assinante=codigo_assinante.strip(), operadora_id=operadora_id, tipo_plano=tipo_plano, servico_principal=servico_principal, data_adesao=date.today(), status=StatusAssinante.ATIVO, municipio=municipio.strip(), provincia=provincia.strip(), nome=nome.strip() if nome else None, citizen_id=citizen_id, telefone_contato=telefone_contato.strip() if telefone_contato else None, email_contato=email_contato.strip().lower() if email_contato else None, contrato_numero=contrato_numero.strip() if contrato_numero else None, valor_mensal=valor_mensal, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def atualizar_status(self, status: StatusAssinante) -> None:
        self.status = status
        self.ativo = status == StatusAssinante.ATIVO