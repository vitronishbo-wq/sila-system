"""Schemas Pydantic para Processo - Validação e serialização de API."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ProcessoCreateSchema(BaseModel):
    """Schema para criação de processo."""

    numero: str = Field(..., min_length=3, max_length=100, description="Número único do processo")
    orgao_origem_id: UUID = Field(..., description="ID do órgão de origem")
    assunto: str = Field(..., min_length=5, max_length=255, description="Assunto do processo")
    interessado_cpf: str | None = Field(None, description="CPF do interessado")
    sigiloso: bool = Field(False, description="Se o processo é sigiloso")
    descricao_detalhada: str | None = Field(
        None, max_length=2000, description="Descrição detalhada"
    )


class ProcessoResponseSchema(BaseModel):
    """Schema para resposta de processo."""

    id: UUID
    numero: str
    orgao_origem_id: UUID
    assunto: str
    interessado_cpf: str | None = None
    data_autuacao: datetime
    status: str
    localizacao_atual: dict[str, Any]
    documentos_count: int = Field(default=0, description="Número de documentos anexados")

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, processo) -> "ProcessoResponseSchema":
        """Converte entidade de domínio para schema de resposta."""
        return cls(
            id=processo.id,
            numero=processo.numero,
            orgao_origem_id=processo.orgao_origem_id,
            assunto=processo.assunto,
            interessado_cpf=processo.interessado_cpf,
            data_autuacao=processo.data_autuacao,
            status=processo.status,
            localizacao_atual=processo.localizacao_atual,
            documentos_count=len(processo.documentos) if processo.documentos else 0,
        )


class ProcessoTramitacaoSchema(BaseModel):
    """Schema para tramitar processo."""

    unidade_destino_id: UUID = Field(..., description="ID da unidade de destino")
    motivo_tramitacao: str = Field(..., min_length=5, description="Motivo da tramitação")


class ProcessoRecebimentoSchema(BaseModel):
    """Schema para registrar recebimento."""

    responsavel_id: str = Field(..., description="ID do responsável pelo recebimento")
    observacoes: str | None = Field(None, description="Observações do recebimento")


class ProcessoEncerramentoSchema(BaseModel):
    """Schema para encerrar processo."""

    motivo_encerramento: str = Field(..., min_length=5, description="Motivo do encerramento")
    resultado: str = Field(..., min_length=5, description="Resultado do processo")


class ProcessoArquivamentoSchema(BaseModel):
    """Schema para arquivar processo."""

    motivo_arquivo: str = Field(..., min_length=5, description="Motivo do arquivamento")


class ProcessoAutuarDocumentoSchema(BaseModel):
    """Schema para autuar documento em processo."""

    documento_id: UUID = Field(..., description="ID do documento a autuar")
    ordem_documento: int = Field(..., gt=0, description="Ordem do documento no processo")


class HistoricoTramitacaoSchema(BaseModel):
    """Schema para histórico de tramitações."""

    unidade_origem_id: UUID | None = None
    unidade_destino_id: UUID | None = None
    data_tramitacao: datetime | None = None
    prazo_resposta: datetime | None = None
    motivo: str | None = None
    responsavel: str | None = None
