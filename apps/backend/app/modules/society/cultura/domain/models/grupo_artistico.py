from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from apps.backend.app.modules.society.cultura.domain.enums import TipoGrupoArtistico

@dataclass
class GrupoArtistico:
    id: UUID
    codigo_grupo: str
    nome: str
    tipo: TipoGrupoArtistico
    lider_artista_id: UUID
    data_cadastro: date
    descricao: str | None = None
    data_fundacao: date | None = None
    municipio: str | None = None
    provincia: str | None = None
    instituicao_educacional_id: UUID | None = None
    membros_ids: list[UUID] | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, codigo_grupo: str, nome: str, tipo: TipoGrupoArtistico, lider_artista_id: UUID, descricao: str | None=None, data_fundacao: date | None=None, municipio: str | None=None, provincia: str | None=None, instituicao_educacional_id: UUID | None=None, membros_ids: list[UUID] | None=None, observacoes: str | None=None) -> 'GrupoArtistico':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do grupo deve ter pelo menos 3 caracteres')
        if data_fundacao is not None and data_fundacao > date.today():
            raise ValueError('Data de fundacao nao pode estar no futuro')
        return cls(id=uuid4(), codigo_grupo=codigo_grupo.strip(), nome=nome_normalizado, tipo=tipo, lider_artista_id=lider_artista_id, data_cadastro=date.today(), descricao=descricao.strip() if descricao else None, data_fundacao=data_fundacao, municipio=municipio.strip() if municipio else None, provincia=provincia.strip() if provincia else None, instituicao_educacional_id=instituicao_educacional_id, membros_ids=list(dict.fromkeys(membros_ids)) if membros_ids else None, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome: str | None=None, tipo: TipoGrupoArtistico | None=None, lider_artista_id: UUID | None=None, descricao: str | None=None, data_fundacao: date | None=None, municipio: str | None=None, provincia: str | None=None, instituicao_educacional_id: UUID | None=None, membros_ids: list[UUID] | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError('Nome do grupo deve ter pelo menos 3 caracteres')
            self.nome = nome_normalizado
        if tipo is not None:
            self.tipo = tipo
        if lider_artista_id is not None:
            self.lider_artista_id = lider_artista_id
        if descricao is not None:
            self.descricao = descricao.strip() if descricao else None
        if data_fundacao is not None:
            if data_fundacao > date.today():
                raise ValueError('Data de fundacao nao pode estar no futuro')
            self.data_fundacao = data_fundacao
        if municipio is not None:
            self.municipio = municipio.strip() if municipio else None
        if provincia is not None:
            self.provincia = provincia.strip() if provincia else None
        if instituicao_educacional_id is not None:
            self.instituicao_educacional_id = instituicao_educacional_id
        if membros_ids is not None:
            self.membros_ids = list(dict.fromkeys(membros_ids)) if membros_ids else None
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None