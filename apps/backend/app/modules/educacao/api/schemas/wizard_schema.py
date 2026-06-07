from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apps.backend.app.modules.educacao.domain.wizard_session import (
    PassoStatus,
    WizardStatus,
)


# ─── Passo 1: Dados do Estudante ───────────────────────────────────


class Passo1EstudanteCreate(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=200)
    data_nascimento: date
    sexo: str = Field(..., pattern=r"^(M|F)$")
    bi: str = Field(..., min_length=10, max_length=20)
    nif: str | None = Field(None, max_length=20)
    nacionalidade: str = Field(default="Angolana", max_length=50)
    naturalidade: str | None = Field(None, max_length=100)
    filiacao_pai: str | None = Field(None, max_length=200)
    filiacao_mae: str = Field(..., max_length=200)
    deficiencia: str = Field(
        default="nenhuma",
        pattern=r"^(nenhuma|motora|visual|auditiva|intelectual|multipla)$",
    )
    necessidades_especiais: str | None = None
    email: str | None = None
    telefone: str | None = Field(None, max_length=20)

    @field_validator("data_nascimento")
    @classmethod
    def validar_idade(cls, v: date) -> date:
        today = date.today()
        idade = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if idade < 4:
            raise ValueError("Idade minima para matricula e 4 anos")
        if idade > 25:
            raise ValueError("Idade maxima para matricula no ensino basico e 25 anos")
        return v


class Passo1EstudanteResponse(BaseModel):
    wizard_id: UUID
    passo: int = Field(default=1)
    status: PassoStatus
    dados: Passo1EstudanteCreate


# ─── Passo 2: Dados do Encarregado ─────────────────────────────────


class Passo2EncarregadoCreate(BaseModel):
    nome_completo: str = Field(..., min_length=3, max_length=200)
    parentesco: str = Field(
        ..., pattern=r"^(pai|mae|tutor_legal|avo|outro)$"
    )
    bi: str = Field(..., min_length=10, max_length=20)
    telefone: str = Field(..., max_length=20)
    email: str = Field(..., max_length=100)
    morada: str = Field(..., min_length=5)
    provincia: str = Field(..., max_length=50)
    municipio: str = Field(..., max_length=50)
    comuna: str | None = Field(None, max_length=50)
    profissao: str | None = Field(None, max_length=100)
    local_trabalho: str | None = Field(None, max_length=200)


class Passo2EncarregadoResponse(BaseModel):
    wizard_id: UUID
    passo: int = Field(default=2)
    status: PassoStatus
    dados: Passo2EncarregadoCreate


# ─── Passo 3: Escola / Turma ────────────────────────────────────────


class EscolaFilterParams(BaseModel):
    nome: str | None = Field(None, max_length=200)
    provincia: str | None = Field(None, max_length=50)
    tipo: str | None = Field(
        None, pattern=r"^(publica|privada|comunitaria)$"
    )


class TurmaDisponivel(BaseModel):
    turma_id: UUID
    classe: str
    turno: str
    capacidade: int
    vagas_disponiveis: int
    propina_mensal: float | None = None


class EscolaComVagas(BaseModel):
    escola_id: UUID
    nome: str
    tipo: str
    provincia: str
    municipio: str
    turmas: list[TurmaDisponivel]


class Passo3SelecaoCreate(BaseModel):
    escola_id: UUID
    turma_id: UUID
    turno: str = Field(..., pattern=r"^(manha|tarde|noite|integral)$")
    classe: str = Field(..., max_length=20)
    ano_letivo_id: UUID
    tipo_ensino: str = Field(
        ...,
        pattern=r"^(pre_escolar|primario|secundario_1|secundario_2)$",
    )
    reservation_id: Optional[UUID] = Field(None, description="ID da reserva feita via marketplace (se aplicavel)")


class Passo3SelecaoResponse(BaseModel):
    wizard_id: UUID
    passo: int = Field(default=3)
    status: PassoStatus
    dados: Passo3SelecaoCreate


# ─── Passo 4: Documentos ────────────────────────────────────────────


class DocumentoUpload(BaseModel):
    wizard_id: UUID
    tipo: str = Field(
        ...,
        pattern=r"^(bi_estudante|bi_encarregado|fotografia|certificado_anterior|boletim_anterior|comprovativo_morada)$",
    )
    nome_original: str = Field(..., max_length=255)
    tamanho_bytes: int = Field(..., gt=0)
    content_type: str = Field(..., max_length=100)


class DocumentoResponse(BaseModel):
    document_id: UUID
    tipo: str
    nome_original: str
    tamanho_bytes: int
    content_type: str
    url: str


class Passo4DocumentosResponse(BaseModel):
    wizard_id: UUID
    passo: int = Field(default=4)
    status: PassoStatus
    documentos: list[DocumentoResponse]
    obrigatorios_pendentes: list[str]


# ─── Passo 5: Elegibilidade ─────────────────────────────────────────


class ValidacaoItem(BaseModel):
    nome: str
    status: str = Field(..., pattern=r"^(APROVADO|REPROVADO|WARNING)$")
    detalhe: str


class Passo5ElegibilidadeResponse(BaseModel):
    wizard_id: UUID
    elegivel: bool
    validacoes: list[ValidacaoItem]
    bloqueantes: int
    warnings: int


# ─── Passo 6: Pagamento ─────────────────────────────────────────────


class PagamentoGerarReferencia(BaseModel):
    modalidade: str = Field(
        ..., pattern=r"^(multicaixa|referencia|wallet)$"
    )


class PagamentoReferenciaResponse(BaseModel):
    wizard_id: UUID
    modalidade: str
    entidade: str | None = None
    referencia: str | None = None
    valor: str
    moeda: str = "AOA"
    status: str = "PENDENTE"
    comprovativo_url: str | None = None


class PagamentoComprovativoUpload(BaseModel):
    wizard_id: UUID
    comprovativo_base64: str


class Passo6PagamentoResponse(BaseModel):
    wizard_id: UUID
    passo: int = Field(default=6)
    status: PassoStatus
    pagamento: PagamentoReferenciaResponse


# ─── Passo 7: Confirmacao ───────────────────────────────────────────


class TimelineEvent(BaseModel):
    etapa: str
    data_hora: datetime | None = None
    concluido: bool = False

class Passo7ConfirmacaoResponse(BaseModel):
    wizard_id: UUID
    matricula_id: UUID
    numero_processo: str
    numero_pedido: str
    status: str
    sla_previsto: str = "3 dias uteis"
    proxima_acao: str = "Acompanhar o estado no portal do cidadao"
    timeline: list[TimelineEvent] = Field(
        default_factory=lambda: [
            TimelineEvent(etapa="Pedido criado", concluido=True),
            TimelineEvent(etapa="Documentos recebidos", concluido=True),
            TimelineEvent(etapa="Validacao concluida", concluido=True),
            TimelineEvent(etapa="Pagamento confirmado"),
            TimelineEvent(etapa="Matricula emitida"),
            TimelineEvent(etapa="Concluido"),
        ]
    )
    estudante: str
    escola: str
    classe: str
    turno: str
    ano_letivo: str
    data_matricula: date
    qr_code_url: str
    comprovativo_url: str


# ─── Resumo do Wizard ───────────────────────────────────────────────


class WizardResumoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wizard_id: UUID
    citizen_id: UUID
    numero_pedido: str | None = None
    status: WizardStatus
    passo_atual: int
    sla_previsto: str = "3 dias uteis"
    proxima_acao: str = "Iniciar o wizard de matricula"
    timeline: list[TimelineEvent] = Field(
        default_factory=lambda: [
            TimelineEvent(etapa="Pedido criado"),
            TimelineEvent(etapa="Documentos recebidos"),
            TimelineEvent(etapa="Validacao concluida"),
            TimelineEvent(etapa="Pagamento confirmado"),
            TimelineEvent(etapa="Matricula emitida"),
            TimelineEvent(etapa="Concluido"),
        ]
    )
    passos: dict[str, PassoStatus] = Field(
        default_factory=lambda: {
            "passo1": PassoStatus.RASCUNHO,
            "passo2": PassoStatus.RASCUNHO,
            "passo3": PassoStatus.RASCUNHO,
            "passo4": PassoStatus.RASCUNHO,
            "passo5": PassoStatus.RASCUNHO,
            "passo6": PassoStatus.RASCUNHO,
            "passo7": PassoStatus.RASCUNHO,
        }
    )
    created_at: datetime | None = None
    updated_at: datetime | None = None
    expires_at: datetime | None = None
