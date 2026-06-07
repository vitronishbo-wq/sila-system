"""Schemas Pydantic para Documento - Validação e serialização de API."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, validator


class DocumentoCreateSchema(BaseModel):
    """Schema para criação de documento."""

    titulo: str = Field(..., min_length=1, max_length=255, description="Título do documento")
    tipo: str = Field(..., description="Tipo do documento (ex: administrativo, judicial)")
    suporte: str = Field(..., description="Suporte físico/digital (ex: papel, digital)")
    data_producao: datetime = Field(..., description="Data de produção do documento")
    orgao_produtor_id: UUID = Field(..., description="ID do órgão produtor")
    classificacao_id: UUID = Field(..., description="ID da classificação no plano")
    num_paginas: int = Field(..., gt=0, description="Número de páginas")
    descricao: str | None = Field(None, max_length=1000, description="Descrição detalhada")
    localizacao_fisica: dict[str, Any] | None = Field(
        default_factory=dict, description="Localização física"
    )

    @validator("data_producao")
    def data_producao_nao_futura(cls, v):
        if v > datetime.now():
            raise ValueError("Data de produção não pode ser no futuro")
        return v


class DocumentoResponseSchema(BaseModel):
    """Schema para resposta de documento."""

    id: UUID
    codigo_referencia: str
    titulo: str
    tipo: str
    suporte: str
    data_producao: datetime
    data_registro: datetime
    orgao_produtor_id: UUID
    classificacao_id: UUID
    num_paginas: int
    estado_conservacao: str
    grau_restricao: str
    fase_arquivistica: str
    status: str
    digitalizado: bool
    versao: int
    descricao: str | None = None
    localizacao_fisica: dict[str, Any] | None = None

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, documento) -> "DocumentoResponseSchema":
        """Converte entidade de domínio para schema de resposta."""
        return cls(
            id=documento.id,
            codigo_referencia=documento.codigo_referencia,
            titulo=documento.titulo,
            tipo=documento.tipo.value,
            suporte=documento.suporte.value,
            data_producao=documento.data_producao,
            data_registro=documento.data_registro,
            orgao_produtor_id=documento.orgao_produtor_id,
            classificacao_id=documento.classificacao_id,
            num_paginas=documento.num_paginas,
            estado_conservacao=documento.estado_conservacao.value,
            grau_restricao=documento.grau_restricao.value,
            fase_arquivistica=documento.fase_arquivistica.value,
            status=documento.status,
            digitalizado=documento.arquivo_digital_path is not None,
            versao=documento.versao,
            descricao=documento.descricao,
            localizacao_fisica=documento.localizacao_fisica,
        )


class DocumentoDigitalizacaoSchema(BaseModel):
    """Schema para registrar digitalização."""

    formato: str = Field(..., description="Formato do arquivo (PDF, JPG, etc.)")
    resolucao_dpi: int = Field(..., gt=0, description="Resolução em DPI")
    hash_arquivo: str = Field(..., min_length=32, description="Hash SHA-256 do arquivo")
    caminho_arquivo: str = Field(..., description="Caminho do arquivo digital")


class DocumentoRestricaoSchema(BaseModel):
    """Schema para aplicar restrição."""

    grau: str = Field(..., description="Grau de restrição (publico, interno, reservado, secreto)")
    motivo: str = Field(..., min_length=5, description="Motivo da restrição")
    validade_ate: datetime | None = Field(None, description="Data de validade da restrição")


class DocumentoConservacaoSchema(BaseModel):
    """Schema para atualizar conservação."""

    estado: str = Field(..., description="Novo estado de conservação")
    intervencao_descricao: str | None = Field(None, description="Descrição da intervenção")


class DocumentoFaseSchema(BaseModel):
    """Schema para mudar fase arquivística."""

    nova_fase: str = Field(..., description="Nova fase (corrente, intermediaria, permanente)")
    motivo: str = Field(..., min_length=5, description="Motivo da mudança")


class DocumentoEliminacaoSchema(BaseModel):
    """Schema para marcar documento para eliminação."""

    motivo_eliminacao: str = Field(..., min_length=10, description="Motivo detalhado da eliminação")
