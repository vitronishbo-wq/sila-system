from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging

from .deps import (
    get_taxpayer_service, get_declaration_service, get_debt_service,
    get_payment_service, get_certificate_service, get_agt_sync_service,
    get_audit_logger, require_taxpayer_permission, can_access_taxpayer,
    get_current_user, get_current_user_optional
)
from .schemas import *
from .exceptions import NotFoundError, ValidationError, AGTIntegrationError
from ..infrastructure.integrations.agt_webhook_handler import AGTWebhookHandler


router = APIRouter(prefix="/taxpayer", tags=["Contribuintes"])
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
    service: TaxpayerService = Depends(get_taxpayer_service),
    user = Depends(get_current_user)
):
    """Regista um novo contribuinte"""
    try:
        taxpayer = await service.register_taxpayer(
            nif=data.nif,
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address,
            tax_regime=data.tax_regime,
            registered_by=str(user.get("id", "system")),
            ip_address=request.client.host if request.client else "unknown"
        )
        return taxpayer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{taxpayer_id}",
    response_model=TaxpayerResponse,
    summary="Buscar contribuinte por ID"
)
async def get_taxpayer(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    service: TaxpayerService = Depends(get_taxpayer_service)
):
    """Busca contribuinte por ID"""
    taxpayer = await service.get_taxpayer(taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Contribuinte não encontrado")
    return taxpayer


@router.get(
    "/nif/{nif}",
    response_model=TaxpayerResponse,
    summary="Buscar contribuinte por NIF"
)
async def get_taxpayer_by_nif(
    nif: str,
    service: TaxpayerService = Depends(get_taxpayer_service),
    user = Depends(get_current_user)
):
    """Busca contribuinte por NIF"""
    taxpayer = await service.get_taxpayer_by_nif(nif)
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Contribuinte não encontrado")
    return taxpayer


@router.patch(
    "/{taxpayer_id}",
    response_model=TaxpayerResponse,
    summary="Atualizar contribuinte"
)
async def update_taxpayer(
    request: Request,
    taxpayer_id: UUID,
    data: TaxpayerUpdate,
    service: TaxpayerService = Depends(get_taxpayer_service),
    user = Depends(get_current_user)
):
    """Atualiza dados do contribuinte"""
    try:
        taxpayer = await service.update_taxpayer(
            taxpayer_id=taxpayer_id,
            updates=data.model_dump(exclude_unset=True),
            updated_by=str(user.get("id", "system")),
            ip_address=request.client.host if request.client else "unknown"
        )
        return taxpayer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{taxpayer_id}/summary",
    response_model=TaxpayerSummaryResponse,
    summary="Resumo do contribuinte"
)
async def get_taxpayer_summary(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    service: TaxpayerService = Depends(get_taxpayer_service)
):
    """Obtém resumo completo do contribuinte"""
    try:
        summary = await service.get_taxpayer_summary(taxpayer_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ==================== DECLARATION ENDPOINTS ====================

@router.post(
    "/{taxpayer_id}/declarations",
    response_model=DeclarationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submeter declaração"
)
async def submit_declaration(
    request: Request,
    taxpayer_id: UUID,
    data: DeclarationCreate,
    service: TaxDeclarationService = Depends(get_declaration_service),
    user = Depends(get_current_user)
):
    """Submete uma declaração fiscal"""
    try:
        declaration = await service.submit_declaration(
            taxpayer_id=taxpayer_id,
            tax_type=data.tax_type,
            tax_period=data.tax_period,
            gross_amount=data.gross_amount,
            deductions=data.deductions,
            submitted_by=str(user.get("id", "system")),
            ip_address=request.client.host if request.client else "unknown"
        )
        return declaration
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{taxpayer_id}/declarations",
    response_model=DeclarationListResponse,
    summary="Listar declarações"
)
async def list_declarations(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    year: Optional[int] = Query(None, description="Filtrar por ano"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: TaxDeclarationService = Depends(get_declaration_service)
):
    """Lista declarações do contribuinte"""
    declarations, total = await service.get_taxpayer_declarations(
        taxpayer_id, year, skip, limit
    )
    return {
        "total": total,
        "items": declarations
    }


@router.get(
    "/declarations/{declaration_id}",
    response_model=DeclarationResponse,
    summary="Buscar declaração"
)
async def get_declaration(
    declaration_id: UUID,
    service: TaxDeclarationService = Depends(get_declaration_service)
):
    """Busca declaração por ID"""
    declaration = await service.get_declaration(declaration_id)
    if not declaration:
        raise HTTPException(status_code=404, detail="Declaração não encontrada")
    return declaration


# ==================== DEBT ENDPOINTS ====================

@router.get(
    "/{taxpayer_id}/debts",
    response_model=DebtListResponse,
    summary="Listar dívidas"
)
async def list_debts(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    include_paid: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: TaxDebtService = Depends(get_debt_service)
):
    """Lista dívidas do contribuinte"""
    debts, total = await service.get_taxpayer_debts(
        taxpayer_id, include_paid, skip, limit
    )
    total_amount = sum(d.get("current_amount", 0) for d in debts)
    
    return {
        "total": total,
        "items": debts,
        "total_amount": total_amount
    }


@router.post(
    "/debts/{debt_id}/pay",
    response_model=List[PaymentResponse],
    summary="Pagar dívida"
)
async def pay_debt(
    request: Request,
    debt_id: UUID,
    data: DebtPaymentRequest,
    service: TaxPaymentService = Depends(get_payment_service),
    user = Depends(get_current_user)
):
    """Regista pagamento de dívida"""
    try:
        payments = await service.process_payment(
            taxpayer_id=None,
            amount=data.amount,
            payment_method=data.payment_method,
            paid_by=str(user.get("id", "system")),
            debt_ids=[debt_id],
            reference=data.reference,
            ip_address=request.client.host if request.client else "unknown"
        )
        return payments
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== PAYMENT ENDPOINTS ====================

@router.get(
    "/{taxpayer_id}/payments",
    response_model=PaymentListResponse,
    summary="Listar pagamentos"
)
async def list_payments(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: TaxPaymentService = Depends(get_payment_service)
):
    """Lista histórico de pagamentos"""
    payments = await service.get_taxpayer_payments(taxpayer_id, skip, limit)
    total_amount = sum(p.get("amount", 0) for p in payments)
    
    return {
        "total": len(payments),
        "items": payments,
        "total_amount": total_amount
    }


@router.post(
    "/payments/{payment_id}/reverse",
    response_model=PaymentResponse,
    summary="Estornar pagamento"
)
async def reverse_payment(
    request: Request,
    payment_id: UUID,
    data: PaymentReverseRequest,
    service: TaxPaymentService = Depends(get_payment_service),
    user = Depends(require_taxpayer_permission("taxpayer:admin"))
):
    """Estorna um pagamento (admin)"""
    try:
        payment = await service.reverse_payment(
            payment_id=payment_id,
            reason=data.reason,
            reversed_by=str(user.get("id", "system")),
            ip_address=request.client.host if request.client else "unknown"
        )
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== CERTIFICATE ENDPOINTS ====================

@router.post(
    "/{taxpayer_id}/certificates",
    response_model=CertificateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Solicitar certidão"
)
async def request_certificate(
    request: Request,
    taxpayer_id: UUID,
    data: CertificateCreate,
    service: TaxCertificateService = Depends(get_certificate_service),
    user = Depends(get_current_user)
):
    """Solicita emissão de certidão fiscal"""
    try:
        certificate = await service.request_certificate(
            taxpayer_id=taxpayer_id,
            certificate_type=data.certificate_type,
            year=data.year,
            requested_by=str(user.get("id", "system")),
            purpose=data.purpose,
            ip_address=request.client.host if request.client else "unknown"
        )
        return certificate
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{taxpayer_id}/certificates",
    response_model=CertificateListResponse,
    summary="Listar certidões"
)
async def list_certificates(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    certificate_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: TaxCertificateService = Depends(get_certificate_service)
):
    """Lista certidões solicitadas"""
    certificates, total = await service.get_taxpayer_certificates(
        taxpayer_id, certificate_type, skip, limit
    )
    return {
        "total": total,
        "items": certificates
    }


@router.get(
    "/certificates/{certificate_id}/download",
    response_model=CertificateDownloadResponse,
    summary="Download de certidão"
)
async def download_certificate(
    certificate_id: UUID,
    service: TaxCertificateService = Depends(get_certificate_service)
):
    """Download da certidão em PDF"""
    try:
        content = await service.download_certificate(certificate_id)
        from fastapi.responses import Response
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=certificate_{certificate_id}.pdf"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ==================== SYNC ENDPOINTS ====================

@router.post(
    "/{taxpayer_id}/sync",
    response_model=dict,
    summary="Sincronizar com AGT"
)
async def sync_with_agt(
    taxpayer_id: UUID = Depends(can_access_taxpayer),
    service: AGTSyncService = Depends(get_agt_sync_service),
    user = Depends(require_taxpayer_permission("taxpayer:sync"))
):
    """Força sincronização com a AGT"""
    try:
        result = await service.sync_taxpayer(taxpayer_id)
        return {
            "message": "Sincronização concluída",
            "updates": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/sync/all",
    response_model=dict,
    summary="Sincronizar todos"
)
async def sync_all(
    service: AGTSyncService = Depends(get_agt_sync_service),
    user = Depends(require_taxpayer_permission("taxpayer:admin"))
):
    """Sincronização em massa de todos os contribuintes"""
    try:
        result = await service.sync_all_taxpayers()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== WEBHOOK ENDPOINTS ====================

@router.post(
    "/webhook/agt",
    status_code=status.HTTP_200_OK,
    summary="Webhook da AGT",
    include_in_schema=False
)
async def agt_webhook(request: Request):
    """Endpoint para receber notificações da AGT"""
    try:
        handler = AGTWebhookHandler()
        
        # Verificar assinatura
        signature = request.headers.get("X-AGT-Signature")
        body = await request.body()
        
        if not handler.verify_signature(body, signature):
            logger.warning("Assinatura inválida no webhook AGT")
            raise HTTPException(status_code=401, detail="Assinatura inválida")
        
        # Processar webhook
        data = await request.json()
        event_type = data.get("event_type")
        
        result = await handler.process_webhook(event_type, data)
        
        return result
    except Exception as e:
        logger.error(f"Erro ao processar webhook AGT: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar webhook")


# ==================== SEARCH ENDPOINTS ====================

@router.get(
    "/search",
    response_model=TaxpayerListResponse,
    summary="Pesquisar contribuintes"
)
async def search_taxpayers(
    q: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    tax_regime: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: TaxpayerService = Depends(get_taxpayer_service),
    user = Depends(require_taxpayer_permission("taxpayer:search"))
):
    """Pesquisa avançada de contribuintes"""
    skip = (page - 1) * limit
    
    filters = {}
    if status_filter:
        filters["status"] = status_filter
    if tax_regime:
        filters["tax_regime"] = tax_regime
    if q:
        filters["search"] = q
    
    taxpayers, total = await service.list_taxpayers(skip, limit, filters)
    
    pages = (total + limit - 1) // limit
    
    return {
        "total": total,
        "items": taxpayers,
        "page": page,
        "pages": pages
    }


# ==================== STATS ENDPOINTS ====================

@router.get(
    "/stats/overdue",
    response_model=List[DebtResponse],
    summary="Dívidas vencidas"
)
async def get_overdue_debts(
    service: TaxDebtService = Depends(get_debt_service),
    user = Depends(require_taxpayer_permission("taxpayer:admin"))
):
    """Lista todas as dívidas vencidas (admin)"""
    debts = await service.check_overdue_debts()
    return debts


# ==================== HEALTH CHECK ====================

@router.get(
    "/health",
    summary="Health check",
    include_in_schema=False
)
async def health_check(
    agt_service: AGTSyncService = Depends(get_agt_sync_service)
):
    """Health check do módulo taxpayer"""
    health_status = {
        "status": "healthy",
        "module": "taxpayer",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # Verificar AGT
    try:
        agt_health = await agt_service.check_agt_health()
        health_status["checks"]["agt"] = agt_health
    except Exception as e:
        health_status["checks"]["agt"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status
