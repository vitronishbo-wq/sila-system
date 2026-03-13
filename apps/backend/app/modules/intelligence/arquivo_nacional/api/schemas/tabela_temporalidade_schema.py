"""Schemas Pydantic para Tabela de Temporalidade - Validação e serialização de API."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class TabelaTemporalidadeCreateSchema(BaseModel):
    """Schema para criação de tabela de temporalidade."""
    codigo: str = Field(..., min_length=2, max_length=20, description='Código único da tabela')
    titulo: str = Field(..., min_length=5, max_length=255, description='Título da tabela')
    descricao: Optional[str] = Field(None, max_length=1000, description='Descrição detalhada')
    orgao_id: UUID = Field(..., description='ID do órgão responsável')
    base_legal: str = Field(..., min_length=5, description='Base legal da tabela')
    ativo: bool = Field(True, description='Se a tabela está ativa')

class TabelaTemporalidadeResponseSchema(BaseModel):
    """Schema para resposta de tabela de temporalidade."""
    id: UUID
    codigo: str
    titulo: str
    descricao: Optional[str] = None
    orgao_id: UUID
    base_legal: str
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    regras_count: int = Field(default=0, description='Número de regras na tabela')

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, tabela) -> 'TabelaTemporalidadeResponseSchema':
        """Converte entidade de domínio para schema de resposta."""
        return cls(id=tabela.id, codigo=tabela.codigo, titulo=tabela.titulo, descricao=tabela.descricao, orgao_id=tabela.orgao_id, base_legal=tabela.base_legal, ativo=tabela.ativo, data_criacao=tabela.data_criacao, data_atualizacao=tabela.data_atualizacao, regras_count=len(tabela.regras) if tabela.regras else 0)

class RegraTemporalidadeCreateSchema(BaseModel):
    """Schema para criação de regra de temporalidade."""
    tabela_id: UUID = Field(..., description='ID da tabela de temporalidade')
    classe_id: Optional[UUID] = Field(None, description='ID da classe (opcional se subclasse informada)')
    subclasse_id: Optional[UUID] = Field(None, description='ID da subclasse (opcional se classe informada)')
    prazo_guarda_corrente: int = Field(..., gt=0, description='Prazo de guarda corrente em anos')
    prazo_guarda_intermediaria: Optional[int] = Field(None, ge=0, description='Prazo de guarda intermediária em anos')
    destino_final: str = Field(..., description='Destino final (eliminação ou guarda permanente)')
    observacoes: Optional[str] = Field(None, max_length=500, description='Observações sobre a regra')

class RegraTemporalidadeResponseSchema(BaseModel):
    """Schema para resposta de regra de temporalidade."""
    id: UUID
    tabela_id: UUID
    classe_id: Optional[UUID] = None
    subclasse_id: Optional[UUID] = None
    prazo_guarda_corrente: int
    prazo_guarda_intermediaria: Optional[int] = None
    destino_final: str
    observacoes: Optional[str] = None
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, regra) -> 'RegraTemporalidadeResponseSchema':
        """Converte entidade de domínio para schema de resposta."""
        return cls(id=regra.id, tabela_id=regra.tabela_id, classe_id=regra.classe_id, subclasse_id=regra.subclasse_id, prazo_guarda_corrente=regra.prazo_guarda_corrente, prazo_guarda_intermediaria=regra.prazo_guarda_intermediaria, destino_final=regra.destino_final, observacoes=regra.observacoes, ativo=regra.ativo, data_criacao=regra.data_criacao, data_atualizacao=regra.data_atualizacao)

class EventoTemporalidadeCreateSchema(BaseModel):
    """Schema para criação de evento de temporalidade."""
    documento_id: UUID = Field(..., description='ID do documento')
    regra_id: UUID = Field(..., description='ID da regra de temporalidade aplicada')
    tipo_evento: str = Field(..., description='Tipo do evento (início_guarda, transferência, eliminação)')
    data_evento: datetime = Field(..., description='Data do evento')
    responsavel_id: str = Field(..., description='ID do responsável pelo evento')
    observacoes: Optional[str] = Field(None, max_length=500, description='Observações do evento')

class EventoTemporalidadeResponseSchema(BaseModel):
    """Schema para resposta de evento de temporalidade."""
    id: UUID
    documento_id: UUID
    regra_id: UUID
    tipo_evento: str
    data_evento: datetime
    responsavel_id: str
    observacoes: Optional[str] = None
    data_registro: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, evento) -> 'EventoTemporalidadeResponseSchema':
        """Converte entidade de domínio para schema de resposta."""
        return cls(id=evento.id, documento_id=evento.documento_id, regra_id=evento.regra_id, tipo_evento=evento.tipo_evento, data_evento=evento.data_evento, responsavel_id=evento.responsavel_id, observacoes=evento.observacoes, data_registro=evento.data_registro)

class TabelaTemporalidadeUpdateSchema(BaseModel):
    """Schema para atualização de tabela de temporalidade."""
    titulo: Optional[str] = Field(None, min_length=5, max_length=255, description='Novo título')
    descricao: Optional[str] = Field(None, max_length=1000, description='Nova descrição')
    base_legal: Optional[str] = Field(None, min_length=5, description='Nova base legal')
    ativo: Optional[bool] = Field(None, description='Novo status ativo')

class RegraTemporalidadeUpdateSchema(BaseModel):
    """Schema para atualização de regra de temporalidade."""
    prazo_guarda_corrente: Optional[int] = Field(None, gt=0, description='Novo prazo de guarda corrente')
    prazo_guarda_intermediaria: Optional[int] = Field(None, ge=0, description='Novo prazo de guarda intermediária')
    destino_final: Optional[str] = Field(None, description='Novo destino final')
    observacoes: Optional[str] = Field(None, max_length=500, description='Novas observações')
    ativo: Optional[bool] = Field(None, description='Novo status ativo')

class AplicarTemporalidadeSchema(BaseModel):
    """Schema para aplicar temporalidade a documento."""
    documento_id: UUID = Field(..., description='ID do documento')
    regra_id: UUID = Field(..., description='ID da regra a aplicar')
    observacoes: Optional[str] = Field(None, max_length=500, description='Observações da aplicação')