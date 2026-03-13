from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube

@dataclass
class Clube:
    id: UUID
    codigo_clube: str
    nome: str
    sigla: str
    tipo: TipoClube
    modalidade_principal: ModalidadeDesportiva
    municipio: str
    provincia: str
    data_cadastro: date
    data_fundacao: date | None = None
    codigo_obra_instalacao: str | None = None
    instituicao_educacional_id: UUID | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, codigo_clube: str, nome: str, sigla: str, tipo: TipoClube, modalidade_principal: ModalidadeDesportiva, municipio: str, provincia: str, data_fundacao: date | None=None, codigo_obra_instalacao: str | None=None, instituicao_educacional_id: UUID | None=None, observacoes: str | None=None) -> 'Clube':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do clube deve ter pelo menos 3 caracteres')
        sigla_normalizada = sigla.strip().upper()
        if len(sigla_normalizada) < 2 or len(sigla_normalizada) > 10:
            raise ValueError('Sigla do clube deve ter entre 2 e 10 caracteres')
        if data_fundacao is not None and data_fundacao > date.today():
            raise ValueError('Data de fundacao nao pode estar no futuro')
        return cls(id=uuid4(), codigo_clube=codigo_clube.strip(), nome=nome_normalizado, sigla=sigla_normalizada, tipo=tipo, modalidade_principal=modalidade_principal, municipio=municipio.strip(), provincia=provincia.strip(), data_cadastro=date.today(), data_fundacao=data_fundacao, codigo_obra_instalacao=codigo_obra_instalacao.strip() if codigo_obra_instalacao else None, instituicao_educacional_id=instituicao_educacional_id, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome: str | None=None, sigla: str | None=None, tipo: TipoClube | None=None, modalidade_principal: ModalidadeDesportiva | None=None, municipio: str | None=None, provincia: str | None=None, data_fundacao: date | None=None, codigo_obra_instalacao: str | None=None, instituicao_educacional_id: UUID | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError('Nome do clube deve ter pelo menos 3 caracteres')
            self.nome = nome_normalizado
        if sigla is not None:
            sigla_normalizada = sigla.strip().upper()
            if len(sigla_normalizada) < 2 or len(sigla_normalizada) > 10:
                raise ValueError('Sigla do clube deve ter entre 2 e 10 caracteres')
            self.sigla = sigla_normalizada
        if tipo is not None:
            self.tipo = tipo
        if modalidade_principal is not None:
            self.modalidade_principal = modalidade_principal
        if municipio is not None:
            self.municipio = municipio.strip()
        if provincia is not None:
            self.provincia = provincia.strip()
        if data_fundacao is not None:
            if data_fundacao > date.today():
                raise ValueError('Data de fundacao nao pode estar no futuro')
            self.data_fundacao = data_fundacao
        if codigo_obra_instalacao is not None:
            self.codigo_obra_instalacao = codigo_obra_instalacao.strip() if codigo_obra_instalacao else None
        if instituicao_educacional_id is not None:
            self.instituicao_educacional_id = instituicao_educacional_id
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None