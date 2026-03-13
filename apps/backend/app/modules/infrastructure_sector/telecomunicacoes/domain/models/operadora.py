from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOperadora, TipoServico

@dataclass
class Operadora:
    id: UUID
    cnpj: str
    razao_social: str
    tipo: TipoOperadora
    servicos_autorizados: list[TipoServico]
    endereco: str
    municipio: str
    provincia: str
    telefone: str
    email: str
    representante_legal: str
    representante_documento: str
    representante_cargo: str
    nome_fantasia: str | None = None
    outorga_id: UUID | None = None
    data_autorizacao: date | None = None
    data_validade: date | None = None
    status: StatusOutorga = StatusOutorga.REQUERIDA
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def cadastrar(cls, *, cnpj: str, razao_social: str, tipo: TipoOperadora, servicos_autorizados: list[TipoServico], endereco: str, municipio: str, provincia: str, telefone: str, email: str, representante_legal: str, representante_documento: str, representante_cargo: str, nome_fantasia: str | None=None, observacoes: str | None=None) -> 'Operadora':
        cnpj_normalizado = cnpj.strip()
        if len(razao_social.strip()) < 3:
            raise ValueError('Razao social deve ter pelo menos 3 caracteres')
        if not servicos_autorizados:
            raise ValueError('Operadora deve ter ao menos um servico autorizado')
        return cls(id=uuid4(), cnpj=cnpj_normalizado, razao_social=razao_social.strip(), nome_fantasia=nome_fantasia.strip() if nome_fantasia else None, tipo=tipo, servicos_autorizados=servicos_autorizados, endereco=endereco.strip(), municipio=municipio.strip(), provincia=provincia.strip(), telefone=telefone.strip(), email=email.strip().lower(), representante_legal=representante_legal.strip(), representante_documento=representante_documento.strip(), representante_cargo=representante_cargo.strip(), status=StatusOutorga.REQUERIDA, observacoes=observacoes.strip() if observacoes else None, ativo=True)

    def autorizar(self, *, outorga_id: UUID, data_autorizacao: date, data_validade: date) -> None:
        if data_validade < data_autorizacao:
            raise ValueError('Data de validade deve ser posterior a data de autorizacao')
        self.outorga_id = outorga_id
        self.data_autorizacao = data_autorizacao
        self.data_validade = data_validade
        self.status = StatusOutorga.DEFERIDA
        self.ativo = True

    def renovar(self, nova_data_validade: date) -> None:
        if self.data_autorizacao is None:
            raise ValueError('Operadora ainda nao possui data de autorizacao')
        if nova_data_validade < self.data_autorizacao:
            raise ValueError('Nova validade invalida')
        self.data_validade = nova_data_validade
        self.status = StatusOutorga.RENOVADA
        self.ativo = True

    def cancelar_outorga(self, motivo: str | None=None) -> None:
        self.status = StatusOutorga.CANCELADA
        self.ativo = False
        if motivo:
            self.observacoes = motivo.strip()