"""
Citizen Documents API - Wrapper endpoints para documentos, certificados, atestados, faturas
Integra com módulos de Registo Civil, Identidade Civil e Finanças via Services Reais.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from uuid import UUID

from app.api.deps import get_db_async
from app.api.dependencies import extract_citizen_id
from app.core.helpers import safe_get, safe_isoformat, safe_enum_value
from app.citizen.core.services.document_service import CitizenDocumentService
from app.citizen.core.services.request_service import RequestService
from app.modules.financas.infrastructure.repositories.invoice_repository import InvoiceRepository

# Adapters antigos removidos em favor de injeção direta de serviços core
# from app.citizen.adapters.service_adapters import ...

router = APIRouter(
    prefix="/api/citizen",
    tags=["citizen-documents"]
)


# ============================================================================
# CERTIFICADOS (Registo Civil)
# ============================================================================

@router.get("/certidoes")
async def get_meus_certidoes(
    tipo: Optional[str] = None,
    citizen_id: UUID = Depends(extract_citizen_id),
    db: AsyncSession = Depends(get_db_async)
) -> Dict[str, Any]:
    """
    Listar certificados do cidadão (Via DocumentService)
    """
    
    doc_service = CitizenDocumentService(db)
    
    # Filtrar por categoria (se tipo for fornecido, ou padrão)
    # Assumindo que certificados são salvos com category='CERTIDAO_{TIPO}' ou genérico
    category_filter = f"CERTIDAO_{tipo.upper()}" if tipo else None
    
    try:
        docs = await doc_service.get_citizen_documents(
            citizen_id,
            category=category_filter
        )
    except Exception as e:
        # Se category_filter for muito específico, pode retornar vazio. 
        # Tentar listar todos e filtrar em memória se necessário, ou assumir vazio.
        docs = []

    return {
        "citizen_id": str(citizen_id),
        "tipo": tipo,
        "certificados": [
            {
                "id": str(safe_get(d, "id")),
                "file_name": safe_get(d, "file_name"),
                "created_at": safe_isoformat(safe_get(d, "created_at")),
                "category": safe_get(d, "category")
            } for d in docs
        ],
        "total": len(docs)
    }


@router.post("/certidoes/solicitar")
async def request_certificate(
    certificate_type: str,
    quantity: int = 1,
    citizen_id: UUID = Depends(extract_citizen_id),
    db: AsyncSession = Depends(get_db_async)
) -> Dict[str, Any]:
    """
    Solicitar um certificado (Gera um Request)
    """
    
    req_service = RequestService(db)
    
    # Mapear tipo para service_code
    service_code = f"CERTIDAO_{certificate_type.upper()}"
    
    # TODO: Buscar service_id real no catálogo
    # Por enquanto passamos None e confiamos no service_code
    
    try:
        request = await req_service.create_request(
            citizen_id=citizen_id,
            service_id=None, # TBD: Lookup service
            service_code=service_code,
            data={"quantity": quantity, "type": certificate_type}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "request_id": str(request.id),
        "status": request.status,
        "message": "Solicitação criada com sucesso. Aguarde processamento."
    }


# ============================================================================
# ATESTADOS (Identidade Civil)
# ============================================================================

@router.get("/atestados")
async def get_meus_atestados(
    tipo: Optional[str] = None,
    citizen_id: UUID = Depends(extract_citizen_id),
    db: AsyncSession = Depends(get_db_async)
) -> Dict[str, Any]:
    """
    Listar atestados do cidadão
    """
    
    doc_service = CitizenDocumentService(db)
    category = f"ATESTADO_{tipo.upper()}" if tipo else "ATESTADO" # Filtro mais lato se tipo=None?
    
    # Se tipo for None, listar todos docs que começam com ATESTADO?
    # get_citizen_documents usa igualdade estrita.
    # Vamos listar tudo e filtrar ou usar categoria exata.
    
    docs = await doc_service.get_citizen_documents(citizen_id)
    
    # Filtro em memória simples
    atestados = [d for d in docs if "ATESTADO" in (d.category or "")]
    if tipo:
        atestados = [d for d in atestados if tipo.upper() in (d.category or "")]

    return {
        "citizen_id": str(citizen_id),
        "tipo": tipo,
        "atestados": [
            {"id": str(safe_get(d, "id")), "file_name": safe_get(d, "file_name"), "created_at": safe_isoformat(safe_get(d, "created_at"))}
            for d in atestados
        ],
        "total": len(atestados)
    }


@router.post("/atestados/solicitar")
async def request_attestation(
    attestation_type: str,
    purpose: Optional[str] = None,
    citizen_id: UUID = Depends(extract_citizen_id),
    db: AsyncSession = Depends(get_db_async)
) -> Dict[str, Any]:
    """
    Solicitar atestado
    """
    
    req_service = RequestService(db)
    service_code = f"ATESTADO_{attestation_type.upper()}"
    
    try:
        request = await req_service.create_request(
            citizen_id=citizen_id,
            service_id=None,
            service_code=service_code,
            data={"purpose": purpose, "type": attestation_type}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {
        "request_id": str(request.id),
        "status": request.status,
        "message": "Solicitação de atestado criada."
    }

# ============================================================================
# FATURAS (Finanças)
# ============================================================================
# Mantendo compatibilidade com InvoiceService existente

@router.get("/faturas")
async def get_minas_faturas(
    status: Optional[str] = None,
    citizen_id: UUID = Depends(extract_citizen_id),
    db: AsyncSession = Depends(get_db_async)
) -> Dict[str, Any]:
    
    inv_repo = InvoiceRepository(db)
    # Assumindo InvoiceService assíncrono ou repository direto
    # O InvoiceService atual (visto anteriormente) usava repository port.
    # Vamos usar o repository direto para leitura simples
    
    invoices = await inv_repo.get_by_citizen(citizen_id)
    
    # Filtro status
    if status:
        invoices = [i for i in invoices if i.status.value == status or i.status == status]
        
    return {
        "citizen_id": str(citizen_id),
        "faturas": [
            {
                "id": str(safe_get(i, "id")),
                "amount": str(safe_get(i, "amount")),
                "status": safe_enum_value(safe_get(i, "status")),
                "reference": safe_get(i, "reference"),
                "created_at": safe_isoformat(safe_get(i, "created_at")),
                "due_date": safe_isoformat(safe_get(i, "due_date"))
            }
            for i in invoices
        ],
        "total": len(invoices)
    }
