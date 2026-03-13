from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from uuid import UUID
from app.api.deps import get_db_async
from app.api.dependencies import extract_citizen_id
from app.core.bridges.finance_bridge import InvoiceRepository
from app.core.utils.dates import safe_isoformat
from app.core.utils.parsing import safe_enum_value, safe_get
from apps.backend.app.modules.justice.bounded_contexts.application.services.services.document_service import CitizenDocumentService
from apps.backend.app.modules.justice.bounded_contexts.application.services.services.request_service import RequestService
router = APIRouter(prefix='/api/citizen', tags=['citizen-documents'])

@router.get('/certidoes')
async def get_meus_certidoes(tipo: Optional[str]=None, citizen_id: UUID=Depends(extract_citizen_id), db: AsyncSession=Depends(get_db_async)) -> Dict[str, Any]:
    """
    Listar certificados do cidadão (Via DocumentService)
    """
    doc_service = CitizenDocumentService(db)
    category_filter = f'CERTIDAO_{tipo.upper()}' if tipo else None
    try:
        docs = await doc_service.get_citizen_documents(citizen_id, category=category_filter)
    except Exception:
        docs = []
    return {'citizen_id': str(citizen_id), 'tipo': tipo, 'certificados': [{'id': str(safe_get(d, 'id')), 'file_name': safe_get(d, 'file_name'), 'created_at': safe_isoformat(safe_get(d, 'created_at')), 'category': safe_get(d, 'category')} for d in docs], 'total': len(docs)}

@router.post('/certidoes/solicitar')
async def request_certificate(certificate_type: str, quantity: int=1, citizen_id: UUID=Depends(extract_citizen_id), db: AsyncSession=Depends(get_db_async)) -> Dict[str, Any]:
    """
    Solicitar um certificado (Gera um Request)
    """
    req_service = RequestService(db)
    service_code = f'CERTIDAO_{certificate_type.upper()}'
    try:
        request = await req_service.create_request(citizen_id=citizen_id, service_id=None, service_code=service_code, data={'quantity': quantity, 'type': certificate_type})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'request_id': str(request.id), 'status': request.status, 'message': 'Solicitação criada com sucesso. Aguarde processamento.'}

@router.get('/atestados')
async def get_meus_atestados(tipo: Optional[str]=None, citizen_id: UUID=Depends(extract_citizen_id), db: AsyncSession=Depends(get_db_async)) -> Dict[str, Any]:
    """
    Listar atestados do cidadão
    """
    doc_service = CitizenDocumentService(db)
    category = f'ATESTADO_{tipo.upper()}' if tipo else 'ATESTADO'
    docs = await doc_service.get_citizen_documents(citizen_id)
    atestados = [d for d in docs if 'ATESTADO' in (d.category or '')]
    if tipo:
        atestados = [d for d in atestados if tipo.upper() in (d.category or '')]
    return {'citizen_id': str(citizen_id), 'tipo': tipo, 'atestados': [{'id': str(safe_get(d, 'id')), 'file_name': safe_get(d, 'file_name'), 'created_at': safe_isoformat(safe_get(d, 'created_at'))} for d in atestados], 'total': len(atestados)}

@router.post('/atestados/solicitar')
async def request_attestation(attestation_type: str, purpose: Optional[str]=None, citizen_id: UUID=Depends(extract_citizen_id), db: AsyncSession=Depends(get_db_async)) -> Dict[str, Any]:
    """
    Solicitar atestado
    """
    req_service = RequestService(db)
    service_code = f'ATESTADO_{attestation_type.upper()}'
    try:
        request = await req_service.create_request(citizen_id=citizen_id, service_id=None, service_code=service_code, data={'purpose': purpose, 'type': attestation_type})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'request_id': str(request.id), 'status': request.status, 'message': 'Solicitação de atestado criada.'}

@router.get('/faturas')
async def get_minas_faturas(status: Optional[str]=None, citizen_id: UUID=Depends(extract_citizen_id), db: AsyncSession=Depends(get_db_async)) -> Dict[str, Any]:
    inv_repo = InvoiceRepository(db)
    invoices = await inv_repo.get_by_citizen(citizen_id)
    if status:
        invoices = [i for i in invoices if i.status.value == status or i.status == status]
    return {'citizen_id': str(citizen_id), 'faturas': [{'id': str(safe_get(i, 'id')), 'amount': str(safe_get(i, 'amount')), 'status': safe_enum_value(safe_get(i, 'status')), 'reference': safe_get(i, 'reference'), 'created_at': safe_isoformat(safe_get(i, 'created_at')), 'due_date': safe_isoformat(safe_get(i, 'due_date'))} for i in invoices], 'total': len(invoices)}