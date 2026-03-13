"""Schemas Pydantic para Plano de Classificação - Validação e serialização de API."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

class PlanoClassificacaoCreateSchema(BaseModel):
    """Schema para criação de plano de classificação."""
    codigo: str = Field(..., min_length=2, max_length=20, description='Código único do plano')
    titulo: str = Field(..., min_length=5, max_length=255, description='Título do plano')
    descricao: Optional[str] = Field(None, max_length=1000, description='Descrição detalhada')
    orgao_id: UUID = Field(..., description='ID do órgão responsável')
    ativo: bool = Field(True, description='Se o plano está ativo')

class PlanoClassificacaoResponseSchema(BaseModel):
    """Schema para resposta de plano de classificação."""
    id: UUID
    codigo: str
    titulo: str
    descricao: Optional[str] = None
    orgao_id: UUID
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    classes_count: int = Field(default=0, description='Número de classes no plano')

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, plano) -> 'PlanoClassificacaoResponseSchema':
        """Converte entidade de domínio para schema de resposta."""
        return cls(id=plano.id, codigo=plano.codigo, titulo=plano.titulo, descricao=plano.descricao, orgao_id=plano.orgao_id, ativo=plano.ativo, data_criacao=plano.data_criacao, data_atualizacao=plano.data_atualizacao, classes_count=len(plano.classes) if plano.classes else 0)

class ClasseCreateSchema(BaseModel):
    """Schema para criação de classe."""
    plano_id: UUID = Field(..., description='ID do plano de classificação')
    codigo: str = Field(..., min_length=1, max_length=10, description='Código da classe')
    titulo: str = Field(..., min_length=5, max_length=255, description='Título da classe')
    descricao: Optional[str] = Field(None, max_length=500, description='Descrição da classe')
    grau: int = Field(..., ge=1, le=5, description='Grau da classe (1-5)')
    prazo_guarda_corrente: int = Field(..., gt=0, description='Prazo de guarda corrente em anos')
    prazo_guarda_intermediaria: Optional[int] = Field(None, ge=0, description='Prazo de guarda intermediária em anos')
    destino_final: str = Field(..., description='Destino final (eliminação ou guarda permanente)')

class ClasseResponseSchema(BaseModel):
    """Schema para resposta de classe."""
    id: UUID
    plano_id: UUID
    codigo: str
    titulo: str
    descricao: Optional[str] = None
    grau: int
    prazo_guarda_corrente: int
    prazo_guarda_intermediaria: Optional[int] = None
    destino_final: str
    ativo: bool
    data_criacao: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, classe) -> 'ClasseResponseSchema':
        """Converte entidade de domínio para schema de resposta."""
        return cls(id=classe.id, plano_id=classe.plano_id, codigo=classe.codigo, titulo=classe.titulo, descricao=classe.descricao, grau=classe.grau, prazo_guarda_corrente=classe.prazo_guarda_corrente, prazo_guarda_intermediaria=classe.prazo_guarda_intermediaria, destino_final=classe.destino_final, ativo=classe.ativo, data_criacao=classe.data_criacao)

class SubclasseCreateSchema(BaseModel):
    """Schema para criação de subclasse."""
    classe_id: UUID = Field(..., description='ID da classe pai')
    codigo: str = Field(..., min_length=1, max_length=10, description='Código da subclasse')
    titulo: str = Field(..., min_length=5, max_length=255, description='Título da subclasse')
    descricao: Optional[str] = Field(None, max_length=500, description='Descrição da subclasse')
    prazo_guarda_corrente: Optional[int] = Field(None, gt=0, description='Prazo de guarda corrente em anos (herda da classe se não informado)')
    prazo_guarda_intermediaria: Optional[int] = Field(None, ge=0, description='Prazo de guarda intermediária em anos')
    destino_final: Optional[str] = Field(None, description='Destino final (herda da classe se não informado)')

class SubclasseResponseSchema(BaseModel):
    """Schema para resposta de subclasse."""
    id: UUID
    classe_id: UUID
    codigo: str
    titulo: str
    descricao: Optional[str] = None
    prazo_guarda_corrente: int
    prazo_guarda_intermediaria: Optional[int] = None
    destino_final: str
    ativo: bool
    data_criacao: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, subclasse) -> 'SubclasseResponseSchema':
        """Converte entidade de domínio para schema de resposta."""
        return cls(id=subclasse.id, classe_id=subclasse.classe_id, codigo=subclasse.codigo, titulo=subclasse.titulo, descricao=subclasse.descricao, prazo_guarda_corrente=subclasse.prazo_guarda_corrente, prazo_guarda_intermediaria=subclasse.prazo_guarda_intermediaria, destino_final=subclasse.destino_final, ativo=subclasse.ativo, data_criacao=subclasse.data_criacao)

class PlanoClassificacaoUpdateSchema(BaseModel):
    """Schema para atualização de plano de classificação."""
    titulo: Optional[str] = Field(None, min_length=5, max_length=255, description='Novo título')
    descricao: Optional[str] = Field(None, max_length=1000, description='Nova descrição')
    ativo: Optional[bool] = Field(None, description='Novo status ativo')

class ClasseUpdateSchema(BaseModel):
    """Schema para atualização de classe."""
    titulo: Optional[str] = Field(None, min_length=5, max_length=255, description='Novo título')
    descricao: Optional[str] = Field(None, max_length=500, description='Nova descrição')
    prazo_guarda_corrente: Optional[int] = Field(None, gt=0, description='Novo prazo de guarda corrente')
    prazo_guarda_intermediaria: Optional[int] = Field(None, ge=0, description='Novo prazo de guarda intermediária')
    destino_final: Optional[str] = Field(None, description='Novo destino final')
    ativo: Optional[bool] = Field(None, description='Novo status ativo')

class SubclasseUpdateSchema(BaseModel):
    """Schema para atualização de subclasse."""
    titulo: Optional[str] = Field(None, min_length=5, max_length=255, description='Novo título')
    descricao: Optional[str] = Field(None, max_length=500, description='Nova descrição')
    prazo_guarda_corrente: Optional[int] = Field(None, gt=0, description='Novo prazo de guarda corrente')
    prazo_guarda_intermediaria: Optional[int] = Field(None, ge=0, description='Novo prazo de guarda intermediária')
    destino_final: Optional[str] = Field(None, description='Novo destino final')
    ativo: Optional[bool] = Field(None, description='Novo status ativo')