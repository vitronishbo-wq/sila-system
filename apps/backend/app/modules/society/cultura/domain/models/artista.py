from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.cultura.domain.enums import TipoArtista

@dataclass
class Artista:
    id: UUID
    registro_cultural: str
    nome: str
    tipo: list[TipoArtista]
    data_cadastro: date
    nome_artistico: str | None = None
    data_nascimento: date | None = None
    naturalidade: str | None = None
    nacionalidade: str = 'Angolana'
    biografia: str | None = None
    citizen_id: UUID | None = None
    municipio: str | None = None
    provincia: str | None = None
    ativo: bool = True
    observacoes: str | None = None

    @classmethod
    def cadastrar(cls, *, nome: str, tipo: list[TipoArtista], registro: str, citizen_id: UUID | None=None, nome_artistico: str | None=None, data_nascimento: date | None=None, naturalidade: str | None=None, nacionalidade: str='Angolana', biografia: str | None=None, municipio: str | None=None, provincia: str | None=None, observacoes: str | None=None) -> 'Artista':
        nome_normalizado = nome.strip()
        if len(nome_normalizado) < 3:
            raise ValueError('Nome do artista deve ter pelo menos 3 caracteres')
        if not tipo:
            raise ValueError('Tipo de artista e obrigatorio')
        return cls(id=uuid4(), registro_cultural=registro.strip(), nome=nome_normalizado, tipo=tipo, data_cadastro=date.today(), citizen_id=citizen_id, nome_artistico=nome_artistico.strip() if nome_artistico else None, data_nascimento=data_nascimento, naturalidade=naturalidade.strip() if naturalidade else None, nacionalidade=nacionalidade.strip() if nacionalidade else 'Angolana', biografia=biografia.strip() if biografia else None, municipio=municipio.strip() if municipio else None, provincia=provincia.strip() if provincia else None, observacoes=observacoes.strip() if observacoes else None)

    def atualizar(self, *, nome: str | None=None, tipo: list[TipoArtista] | None=None, nome_artistico: str | None=None, data_nascimento: date | None=None, naturalidade: str | None=None, nacionalidade: str | None=None, biografia: str | None=None, municipio: str | None=None, provincia: str | None=None, ativo: bool | None=None, observacoes: str | None=None) -> None:
        if nome is not None:
            nome_normalizado = nome.strip()
            if len(nome_normalizado) < 3:
                raise ValueError('Nome do artista deve ter pelo menos 3 caracteres')
            self.nome = nome_normalizado
        if tipo is not None:
            if not tipo:
                raise ValueError('Tipo de artista e obrigatorio')
            self.tipo = tipo
        if nome_artistico is not None:
            self.nome_artistico = nome_artistico.strip() if nome_artistico else None
        if data_nascimento is not None:
            self.data_nascimento = data_nascimento
        if naturalidade is not None:
            self.naturalidade = naturalidade.strip() if naturalidade else None
        if nacionalidade is not None:
            self.nacionalidade = nacionalidade.strip() if nacionalidade else self.nacionalidade
        if biografia is not None:
            self.biografia = biografia.strip() if biografia else None
        if municipio is not None:
            self.municipio = municipio.strip() if municipio else None
        if provincia is not None:
            self.provincia = provincia.strip() if provincia else None
        if ativo is not None:
            self.ativo = ativo
        if observacoes is not None:
            self.observacoes = observacoes.strip() if observacoes else None