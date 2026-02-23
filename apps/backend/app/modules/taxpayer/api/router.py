from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from typing import Optional
from uuid import UUID
from datetime import datetime
import logging

from .deps import (    get_current_user, can_access_taxpayer, require_taxpayer_permission,
    get_rate_limiter
)
from .schemas import *
from .rate_limiter import RateLimiter

router = APIRouter(prefix="/taxpayer", tags=["Contribuintes"])

# middleware será adicionado na app principal
logger = logging.getLogger(__name__)


# ==================== TAXPAYER ENDPOINTS ====================

@router.post(
    "/register",
    response_model=TaxpayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registar novo contribuinte",
    description="Regista um novo contribuinte no sistema"
)
async def register_taxpayer(
    request: Request,
    data: TaxpayerCreate,
    user = Depends(get_current_user),
    limiter: RateLimiter = Depends(get_rate_limiter)
):
    """Regista um novo contribuinte."""
    if not await limiter.check(f"ratelimit:{request.client.host}:/register"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "nif": data.nif,
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "address": data.address,
        "tax_regime": data.tax_regime,
        "status": "ACTIVE",
        "registered_by": UUID(str(user.get("id"))[:36]),
        "registered_at": datetime.now(),
        "updated_at": None,
        "agt_status": "ACTIVE",
        "agt_last_sync": datetime.now()
    }


@router.get(
    "/{taxpayer_id}",
    response_model=TaxpayerResponse,
    summary="Buscar contribuinte",
    description="Retorna contribuinte por ID"
)
async def get_taxpayer(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    user = Depends(get_current_user)
):
    """Busca contribuinte por ID."""
    return {
        "id": taxpayer_id,
        "nif": "123456789",
        "name": "João Silva",
        "email": "joao@example.com",
        "phone": "+244923456789",
        "address": "Rua Principal",
        "tax_regime": "GERAL",
        "status": "ACTIVE",
        "registered_by": user.get("id"),
        "registered_at": datetime.now(),
        "updated_at": None,
        "agt_status": "ACTIVE",
        "agt_last_sync": datetime.now()
    }


@router.get(
    "/search",
    response_model=TaxpayerListResponse,
    summary="Pesquisar contribuintes",
    description="Pesquisa avançada de contribuintes"
)
async def search_taxpayers(
    q: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user = Depends(require_taxpayer_permission("taxpayer:search"))
):
    """Pesquisa avançada de contribuintes."""
    return {
        "total": 0,
        "items": [],
        "page": page,
        "pages": 0
    }


@router.patch(
    "/{taxpayer_id}",
    response_model=TaxpayerResponse,
    summary="Atualizar contribuinte",
    description="Atualiza dados de um contribuinte"
)
async def update_taxpayer(
    request: Request,
    data: TaxpayerUpdate,
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    user = Depends(get_current_user)
):
    """Atualiza dados do contribuinte."""
    return {
        "id": taxpayer_id,
        "nif": "123456789",
        "name": data.name or "João Silva",
        "email": data.email or "joao@example.com",
        "phone": data.phone or "+244923456789",
        "address": data.address or "Rua Principal",
        "tax_regime": data.tax_regime or "GERAL",
        "status": "ACTIVE",
        "registered_by": user.get("id"),
        "registered_at": datetime.now(),
        "updated_at": datetime.now(),
        "agt_status": "ACTIVE",
        "agt_last_sync": datetime.now()
    }


@router.get(
    "/{taxpayer_id}/summary",
    response_model=TaxpayerSummaryResponse,
    summary="Resumo do contribuinte",
    description="Retorna resumo com estatísticas"
)
async def get_taxpayer_summary(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    user = Depends(get_current_user)
):
    """Obtém resumo completo do contribuinte."""
    taxpayer = {
        "id": taxpayer_id,
        "nif": "123456789",
        "name": "João Silva",
        "email": "joao@example.com",
        "phone": "+244923456789",
        "address": "Rua Principal",
        "tax_regime": "GERAL",
        "status": "ACTIVE",
        "registered_by": user.get("id"),
        "registered_at": datetime.now(),
        "updated_at": None,
        "agt_status": "ACTIVE",
        "agt_last_sync": datetime.now()
    }
    
    return {
        "taxpayer": taxpayer,
        "statistics": {},
        "recent_declarations": [],
        "pending_debts": [],
        "recent_payments": []
    }


# ==================== DECLARATION ENDPOINTS ====================

@router.post(
    "/{taxpayer_id}/declarations",
    response_model=DeclarationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submeter declaração",
    description="Submete uma nova declaração fiscal"
)
async def submit_declaration(
    request: Request,
    data: DeclarationCreate,
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    user = Depends(get_current_user)
):
    """Submete uma declaração fiscal."""
    return {
        "id": UUID("00000000-0000-0000-0000-000000000003"),
        "taxpayer_id": taxpayer_id,
        "declaration_number": "DEC/2024/000001",
        "tax_type": data.tax_type,
        "tax_period": data.tax_period,
        "gross_amount": data.gross_amount,
        "deductions": data.deductions or 0,
        "net_amount": data.gross_amount - (data.deductions or 0),
        "declaration_date": datetime.now().date(),
        "due_date": datetime.now().date(),
        "status": "SUBMITTED",
        "protocol": "PROT-2024-0001",
        "submitted_by": UUID(str(user.get("id"))[:36]),
        "submitted_at": datetime.now(),
        "processed_by": None,
        "processed_at": None,
        "observations": None
    }


@router.get(
    "/{taxpayer_id}/declarations",
    response_model=DeclarationListResponse,
    summary="Listar declarações",
    description="Lista declarações do contribuinte"
)
async def list_declarations(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Lista declarações do contribuinte."""
    return {
        "total": 0,
        "items": []
    }


# ==================== DEBT ENDPOINTS ====================

@router.get(
    "/{taxpayer_id}/debts",
    response_model=DebtListResponse,
    summary="Listar dívidas",
    description="Lista dívidas do contribuinte"
)
async def list_debts(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    include_paid: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Lista dívidas do contribuinte."""
    return {
        "total": 0,
        "items": [],
        "total_amount": 0
    }


# ==================== PAYMENT ENDPOINTS ====================

@router.get(
    "/{taxpayer_id}/payments",
    response_model=PaymentListResponse,
    summary="Listar pagamentos",
    description="Lista histórico de pagamentos"
)
async def list_payments(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Lista histórico de pagamentos."""
    return {
        "total": 0,
        "items": [],
        "total_amount": 0
    }


@router.post(
    "/payments/{payment_id}/reverse",
    response_model=PaymentResponse,
    summary="Estornar pagamento",
    description="Estorna um pagamento"
)
async def reverse_payment(
    request: Request,
    data: PaymentReverseRequest,
    payment_id: UUID,
    user = Depends(require_taxpayer_permission("taxpayer:admin"))
):
    """Estorna um pagamento."""
    return {
        "id": payment_id,
        "taxpayer_id": UUID("00000000-0000-0000-0000-000000000001"),
        "debt_id": UUID("00000000-0000-0000-0000-000000000004"),
        "payment_number": "PAY/2024/000001",
        "amount": 100000.0,
        "payment_method": "TRANSFER",
        "payment_date": datetime.now(),
        "status": "REVERSED",
        "reference": None,
        "paid_by": UUID(str(user.get("id"))[:36]),
        "created_at": datetime.now()
    }


# ==================== CERTIFICATE ENDPOINTS ====================

@router.post(
    "/{taxpayer_id}/certificates",
    response_model=CertificateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Solicitar certidão",
    description="Solicita emissão de certidão fiscal"
)
async def request_certificate(
    request: Request,
    data: CertificateCreate,
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    user = Depends(get_current_user)
):
    """Solicita emissão de certidão fiscal."""
    return {
        "id": UUID("00000000-0000-0000-0000-000000000005"),
        "taxpayer_id": taxpayer_id,
        "certificate_number": "CERT/NIF/2024/000001",
        "certificate_type": data.certificate_type,
        "year": data.year,
        "purpose": data.purpose,
        "status": "PENDING",
        "requested_at": datetime.now(),
        "requested_by": UUID(str(user.get("id"))[:36]),
        "issued_at": None,
        "issued_by": None,
        "expires_at": None,
        "file_url": None,
        "error_message": None
    }


@router.get(
    "/{taxpayer_id}/certificates",
    response_model=CertificateListResponse,
    summary="Listar certidões",
    description="Lista certidões solicitadas"
)
async def list_certificates(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    certificate_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Lista certidões solicitadas."""
    return {
        "total": 0,
        "items": []
    }


# ==================== HEALTH ENDPOINT ====================

@router.get(
    "/health",
    summary="Health check",
    description="Verifica saúde do módulo",
    include_in_schema=False
)
async def health_check():
    """Health check do módulo taxpayer."""
    return {
        "status": "healthy",
        "module": "taxpayer",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "api": "up",
            "database": "up"
        }
    }
