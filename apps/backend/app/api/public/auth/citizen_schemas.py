"""Schemas for citizen authentication"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any


class CitizenLoginRequest(BaseModel):
    """Request para login de cidadão"""
    identifier: str = Field(
        ..., 
        description="BI, NIF, Email, Username ou ID do cidadão",
        min_length=3
    )
    password: str = Field(..., description="Senha", min_length=6)
    mfa_code: Optional[str] = Field(None, description="Código MFA (se habilitado)")


class CitizenLoginResponse(BaseModel):
    """Response de login de cidadão"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int
    user: Dict[str, Any]
    citizen: Optional[Dict[str, Any]] = None


class MFAResponse(BaseModel):
    """Response quando MFA é required"""
    requires_mfa: bool = True
    user_id: str
    mfa_type: str


class CitizenRegisterRequest(BaseModel):
    """Request para criar conta de cidadão"""
    citizen_id: str = Field(..., description="ID do cidadão (UUID)")
    email: EmailStr = Field(..., description="Email para login")
    password: str = Field(..., description="Senha", min_length=8)
    confirm_password: str = Field(..., description="Confirmação de senha")
    full_name: str = Field(..., description="Nome completo", min_length=3)
    phone: Optional[str] = Field(None, description="Telefone")
    accept_terms: bool = Field(..., description="Aceita os termos de uso")
    
    @validator('password')
    def validate_password(cls, v):
        """Valida requisitos de senha"""
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter pelo menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve ter pelo menos uma letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve ter pelo menos um número')
        return v


class CitizenLinkRequest(BaseModel):
    """Request para vincular conta existente a cidadão"""
    citizen_id: str = Field(..., description="ID do cidadão no FUC (UUID)")


class CitizenLinkResponse(BaseModel):
    """Response de vínculo bem-sucedido"""
    message: str
    user_id: str
    citizen_id: str


class CitizenProfileResponse(BaseModel):
    """Response do perfil completo do cidadão"""
    user_id: str
    username: str
    email: str
    citizen_id: Optional[str]
    full_name: Optional[str]
    phone: Optional[str]
    status: str
    is_active: bool
    mfa_enabled: bool
    created_at: Optional[str]


class CitizenCheckRequest(BaseModel):
    """Request para Check profissional"""
    identifier: str = Field(..., description="BI, NIF ou ID do cidadão")


class CitizenCheckResponse(BaseModel):
    """Response de verificação de cidadão"""
    found: bool
    id: Optional[str] = None
    name: Optional[str] = None
    birth_date: Optional[str] = None
    bi_number: Optional[str] = None
    nif: Optional[str] = None
    has_account: bool = False


class ErrorResponse(BaseModel):
    """Response de erro"""
    detail: str
    code: Optional[str] = None


class MessageResponse(BaseModel):
    """Response simples com mensagem"""
    message: str
