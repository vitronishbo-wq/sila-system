from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TipoDocumento(str, Enum):
    BI = "bi"
    PASSPORT = "passport"
    CERTIFICADO_NASCIMENTO = "certificado_nascimento"
    CERTIFICADO_CONCLUSAO = "certificado_conclusao"
    DIPLOMA = "diploma"
    COMPROVANTE_MORADA = "comprovante_morada"
    FOTOGRAFIA = "fotografia"
    DECLARACAO = "declaracao"
    OUTRO = "outro"


class DocumentoStatus(str, Enum):
    PENDENTE = "pendente"
    VERIFICADO = "verificado"
    REPROVADO = "reprovado"
    INCONCLUSIVO = "inconclusivo"


class MetodoVerificacao(str, Enum):
    OCR = "ocr"
    QR_CODE = "qr_code"
    VALIDACAO_BI = "validacao_bi"
    CONSULTA_XROAD = "consulta_xroad"
    MANUAL = "manual"


@dataclass
class DocumentoVerificavel:
    tipo: TipoDocumento
    base64_content: str
    filename: Optional[str] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class CampoExtraido:
    nome: str
    valor: str
    confianca: float = 1.0


@dataclass
class DocumentVerificationResult:
    documento_tipo: TipoDocumento
    valido: bool
    status: DocumentoStatus
    metodo: MetodoVerificacao
    id: UUID = field(default_factory=uuid4)
    campos_extraidos: list[CampoExtraido] = field(default_factory=list)
    problemas: list[str] = field(default_factory=list)
    confianca_global: float = 0.0
    verificacao_timestamp: datetime = field(default_factory=datetime.utcnow)
