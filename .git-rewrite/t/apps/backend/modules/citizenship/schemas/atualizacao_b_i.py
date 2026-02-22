from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class StatusEnum(str, Enum):
    pendente = "pendente"
    rascunho = "rascunho"
    em_analise = "em_analise"
    em_validacao = "em_validacao"
    aprovado = "aprovado"
    rejeitado = "rejeitado"
    cancelado = "cancelado"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class DocumentTypeEnum(str, Enum):
    IDENTITY = "identity"  # Matching test data
    RESIDENCE = "residence"
    OTHER = "other"


class DocumentType(BaseModel):
    type: DocumentTypeEnum
    description: str


class AtualizacaoBIBase(BaseModel):
    nome_completo: str
    numero_documento: str
    tipo_documento: DocumentTypeEnum
    data_nascimento: str
    morada: str
    telefone: str
    email: EmailStr
    motivo_atualizacao: str
    status: StatusEnum

    @field_validator("data_nascimento")
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Data de nascimento deve estar no formato YYYY-MM-DD")

    @field_validator("status")
    def validate_status(cls, v: str) -> str:
        if isinstance(v, str):
            if v in StatusEnum._value2member_map_:
                return v  # Keep string, let Pydantic handle enum conversion
            raise ValueError(
                f"Status inválido. Valores permitidos: {[x.value for x in StatusEnum]}"
            )
        return v

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, use_enum_values=True
    )


class AtualizacaoBICreate(AtualizacaoBIBase):
    pass


class AtualizacaoBIUpdate(BaseModel):
    nome_completo: Optional[str] = None
    numero_documento: Optional[str] = None
    tipo_documento: Optional[DocumentTypeEnum] = None
    data_nascimento: Optional[str] = None
    morada: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    motivo_atualizacao: Optional[str] = None
    status: Optional[str] = None  # Allow string input
    motivo_cancelamento: Optional[str] = None
    observacoes: Optional[str] = None

    @field_validator("data_nascimento")
    def validate_date(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Data de nascimento deve estar no formato YYYY-MM-DD")

    @field_validator("status")
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        print(f"DEBUG AtualizacaoBIUpdate.status validator received: {v}")
        if v is None:
            return v
        if isinstance(v, str):
            if v in StatusEnum._value2member_map_:
                return v  # Keep string, let Pydantic handle enum conversion
            print(f"DEBUG Status inválido recebido: {v}")
            raise ValueError(
                f"Status inválido. Valores permitidos: {[x.value for x in StatusEnum]}"
            )
        return v

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, use_enum_values=True
    )


class AtualizacaoBIRead(AtualizacaoBIBase):
    id: int
    created_at: Optional[datetime] = None
    data_criacao: Optional[str] = None
    updated_at: datetime
    documentos: List[str] = []
    motivo_cancelamento: Optional[str] = None
    observacoes: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="allow"
    )

    def __init__(self, **data):
        super().__init__(**data)
        # Compatibilidade com diferentes nomes de campo
        if not self.created_at and self.data_criacao:
            self.created_at = datetime.fromisoformat(self.data_criacao)


class AtualizacaoBIList(BaseModel):
    items: List[AtualizacaoBIRead]
    total: int
    skip: int
    limit: int
