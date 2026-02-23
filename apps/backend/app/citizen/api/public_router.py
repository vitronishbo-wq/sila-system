"""
Citizen Public API - Endpoints para cidadãos autenticados
Acesso à sua própria FUC (Ficha Única do Cidadão)
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user, get_current_citizen_user, get_db
from modules.identity.models.user import User
from app.citizen.events.models import CitizenEventModel
from app.citizen.core.models import CitizenFUC
from app.modules.identidade_civil.application.services.citizen_service import CitizenService
from pydantic import BaseModel

router = APIRouter(prefix="/citizen", tags=["Citizen Public API"])


def safe_isoformat(value):
    """Safely convert datetime/date to ISO format string"""
    if value is None:
        return None
    try:
        return value.isoformat()
    except Exception:
        return str(value) if value else None


def safe_get(obj, attr, default=None):
    """Safely get attribute from object"""
    return getattr(obj, attr, default)


def _iso_or_str(obj, attr):
    val = getattr(obj, attr, None)
    if val is None:
        return None
    try:
        return val.isoformat()
    except Exception:
        return str(val)


def _value_or_raw(obj, attr):
    val = getattr(obj, attr, None)
    if val is None:
        return None
    return getattr(val, "value", val)


# ========== Schemas ==========
class ValidateCitizenResponse(BaseModel):
    """Resposta de validação de cidadão"""
    is_valid: bool
    citizen_id: str
    reason: str | None = None
    details: dict | None = None


class GetCitizenDataResponse(BaseModel):
    """Resposta com dados do cidadão"""
    id: str
    full_name: str
    status: str
    document_type: str
    document_number: str | None = None
    birth_date: str | None = None
    nationality: str | None = None


@router.get("/profile")
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's FUC profile - lenient version that works for all authenticated users"""
    
    try:
        # Para cidadãos normais, usar citizen_id
        citizen_id = current_user.citizen_id
        
        # Se tem citizen_id, tentar buscar perfil completo
        if citizen_id:
            try:
                result = await db.execute(
                    select(CitizenFUC).where(CitizenFUC.citizen_id == citizen_id)
                )
                citizen = result.scalars().first()
                
                if citizen:
                    return {
                        "id": str(citizen.citizen_id),
                        "full_name": citizen.full_name,
                        "birth_date": safe_isoformat(citizen.birth_date),
                        "gender": safe_get(citizen, "gender"),
                        "nationality": safe_get(citizen, "nationality"),
                        "vital_status": safe_get(citizen, "vital_status"),
                        "current_address": safe_get(citizen, "current_address"),
                        "id_number": safe_get(citizen, "id_number"),
                        "nif": safe_get(citizen, "nif"),
                        "version": safe_get(citizen, "version"),
                        "email": safe_get(citizen, "email"),
                        "phone": safe_get(citizen, "phone"),
                        "last_updated": safe_isoformat(safe_get(citizen, "last_updated"))
                    }
            except Exception as e:
                # Se erro na busca, continuar para fallback
                pass
        
        # Fallback: retornar perfil do usuário autenticado
        return {
            "id": str(current_user.id),
            "full_name": current_user.full_name or current_user.username or "Utilizador",
            "birth_date": None,
            "gender": None,
            "nationality": None,
            "vital_status": None,
            "current_address": None,
            "id_number": None,
            "nif": None,
            "version": None,
            "email": current_user.email,
            "phone": current_user.phone,
            "last_updated": None
        }
        
    except Exception as e:
        # Último fallback - retornar erro mas de forma legível
        return {
            "id": str(current_user.id),
            "full_name": "Erro ao carregar",
            "birth_date": None,
            "gender": None,
            "nationality": None,
            "vital_status": None,
            "current_address": None,
            "id_number": None,
            "nif": None,
            "version": None,
            "email": current_user.email,
            "phone": current_user.phone,
            "last_updated": None,
            "_error_detail": str(e)
        }


@router.get("/events")
async def get_my_events(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's event timeline"""
    if not current_user.citizen_id:
        # Retornar lista vazia se não tiver citizen_id
        return []
    
    try:
        result = await db.execute(
            select(CitizenEventModel)
            .where(CitizenEventModel.citizen_id == current_user.citizen_id)
            .order_by(CitizenEventModel.created_at.desc())
        )
        events = result.scalars().all()
        
        return [{
            "id": str(event.id),
            "citizen_id": str(event.citizen_id),
            "event_type": event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            "payload": event.payload or {},
            "service_id": event.service_id,
            "performed_by": event.performed_by,
            "legal_basis": event.legal_basis,
            "created_at": event.created_at.isoformat() if event.created_at else None
        } for event in events]
    except Exception as e:
        # Retornar lista vazia se houver erro na query
        print(f"[WARN] Erro ao buscar events do cidadão: {str(e)}")
        return []


@router.get("/{citizen_id}/profile")
async def get_citizen_profile(
    citizen_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get any citizen's profile (if authorized)"""
    try:
        citizen_uuid = uuid.UUID(citizen_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid citizen ID")
    
    result = await db.execute(
        select(CitizenFUC).where(CitizenFUC.citizen_id == citizen_uuid)
    )
    citizen = result.scalars().first()
    
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    
    return {
        "id": str(citizen.citizen_id),
        "full_name": citizen.full_name,
        "birth_date": safe_isoformat(citizen.birth_date),
        "gender": safe_get(citizen, "gender"),
        "vital_status": safe_get(citizen, "vital_status"),
        "id_number": safe_get(citizen, "id_number"),
        "nif": safe_get(citizen, "nif"),
        "version": safe_get(citizen, "version"),
        "last_updated": safe_isoformat(safe_get(citizen, "last_updated"))
    }

# ========== FUC Validation Endpoints ==========
@router.post("/validate/{citizen_id}")
async def validate_citizen_endpoint(citizen_id: str) -> ValidateCitizenResponse:
    """
    Valida se um cidadão existe e está ATIVO no FUC.
    
    **Critérios de validação:**
    - Cidadão deve existir na base FUC
    - Status deve ser ACTIVE
    - Não deve estar suspenso, falecido ou inativo
    
    **Usado por:** InvoiceService, PaymentService, módulos administrativos
    
    **Exemplos:**
    ```bash
    curl -X POST http://localhost:8000/api/citizen/validate/CIT-12345
    
    # Response (sucesso)
    {
      "is_valid": true,
      "citizen_id": "CIT-12345",
      "reason": null,
      "details": null
    }
    
    # Response (falha)
    {
      "is_valid": false,
      "citizen_id": "CIT-INATIVO",
      "reason": "STATUS_INACTIVE",
      "details": {"current_status": "INACTIVE"}
    }
    ```
    """
    citizen_service = CitizenService(db_session=None)
    
    try:
        is_valid = await citizen_service.validate_citizen(citizen_id)
        
        if is_valid:
            return ValidateCitizenResponse(
                is_valid=True,
                citizen_id=citizen_id,
                reason=None,
                details=None
            )
        else:
            # Cidadão existe mas status inválido
            return ValidateCitizenResponse(
                is_valid=False,
                citizen_id=citizen_id,
                reason="STATUS_INACTIVE",
                details=None
            )
    except Exception as e:
        return ValidateCitizenResponse(
            is_valid=False,
            citizen_id=citizen_id,
            reason="VALIDATION_ERROR",
            details={"error": str(e)}
        )


@router.get("/data/{citizen_id}")
async def get_citizen_data_endpoint(citizen_id: str) -> GetCitizenDataResponse:
    """
    Recupera dados consolidados de um cidadão no FUC.
    
    **Dados retornados:**
    - ID, nome completo, status
    - Tipo e número de documento
    - Data de nascimento, nacionalidade
    
    **Usado por:** Módulos que necessitam dados do cidadão sem fazer pedidos à API FUC
    
    **Exemplos:**
    ```bash
    curl http://localhost:8000/api/citizen/data/CIT-12345
    
    # Response
    {
      "id": "CIT-12345",
      "full_name": "João da Silva",
      "status": "ACTIVE",
      "document_type": "BI",
      "document_number": "12345678",
      "birth_date": "1980-01-01",
      "nationality": "Portuguesa"
    }
    ```
    """
    citizen_service = CitizenService(db_session=None)
    
    try:
        data = await citizen_service.get_citizen_data(citizen_id)
        return GetCitizenDataResponse(
            id=data.get("id"),
            full_name=data.get("full_name"),
            status=data.get("status"),
            document_type=data.get("document_type"),
            document_number=data.get("document_number"),
            birth_date=data.get("birth_date"),
            nationality=data.get("nationality")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cidadão '{citizen_id}' não localizado: {str(e)}"
        )


# ========== DOCUMENTOS & CERTIDÕES ==========
@router.get("/certidoes")
async def get_certidoes(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's certificates (birth, marriage, death)"""
    # TODO: Implementar logic
    return {
        "certidoes": [],
        "total": 0,
        "message": "Endpoint em desenvolvimento"
    }


@router.get("/atestados")
async def get_atestados(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's attestations (residence, life)"""
    # TODO: Implementar logic
    return {
        "atestados": [],
        "total": 0,
        "message": "Endpoint em desenvolvimento"
    }


@router.get("/bi")
async def get_bi(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's ID card (BI) information"""
    # TODO: Implementar logic
    return {
        "bi": None,
        "status": "ATIVO",
        "message": "Endpoint em desenvolvimento"
    }


# ========== FINANÇAS ==========
@router.get("/invoices")
async def get_invoices(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's invoices"""
    # TODO: Implementar logic
    return {
        "invoices": [],
        "total": 0,
        "total_value": 0.00,
        "message": "Endpoint em desenvolvimento"
    }


@router.get("/payments")
async def get_payments(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current citizen's payments"""
    # TODO: Implementar logic
    return {
        "payments": [],
        "total": 0,
        "total_value": 0.00,
        "message": "Endpoint em desenvolvimento"
    }


# ========== NOTIFICAÇÕES ==========
@router.get("/notifications/unread-count")
async def get_unread_notifications_count(
    current_user: User = Depends(get_current_citizen_user),
    db: AsyncSession = Depends(get_db)
):
    """Get unread notifications count"""
    # TODO: Implementar logic
    return {"unread_count": 0}