"""Routes for citizen authentication"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.api.public.auth.citizen_schemas import (
    CitizenLoginRequest, CitizenLoginResponse, CitizenRegisterRequest,
    CitizenLinkRequest, CitizenLinkResponse, CitizenProfileResponse,
    CitizenCheckResponse, MFAResponse, ErrorResponse, CitizenCheckRequest
)
from app.core.iam.models.user import User
from app.core.iam.application.services.citizen_auth_service import CitizenAuthService
from app.core.iam.application.services.base_service import (
    AuthenticationError, ValidationError, NotFoundError
)

router = APIRouter(prefix="/citizen", tags=["Citizen Auth"])


def get_client_ip(request: Request) -> str:
    """Extrai IP do cliente da requisição"""
    forwarded = request.headers.get("X-Forwarded-For")
    return forwarded.split(",")[0] if forwarded else request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Extrai user-agent da requisição"""
    return request.headers.get("user-agent", "unknown")[:200]


@router.post(
    "/login",
    response_model=CitizenLoginResponse,
    responses={
        200: {"model": CitizenLoginResponse},
        202: {"model": MFAResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def citizen_login(
    request: Request,
    login_data: CitizenLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login específico para cidadãos
    Suporta identificação por: Email, Username, BI, NIF ou ID do cidadão
    """
    service = CitizenAuthService(db)
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        result = service.citizen_login(
            identifier=login_data.identifier,
            password=login_data.password,
            ip_address=ip_address,
            user_agent=user_agent,
            mfa_code=login_data.mfa_code
        )
        
        # Se requer MFA
        if isinstance(result, dict) and result.get("requires_mfa"):
            return MFAResponse(**result)
        
        return CitizenLoginResponse(**result)
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro durante a autenticação"
        )


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse}
    }
)
async def register_citizen_account(
    register_data: CitizenRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Cria conta IAM para um cidadão
    """
    if register_data.password != register_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="As senhas não conferem"
        )
    
    if not register_data.accept_terms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="É necessário aceitar os termos de uso"
        )
    
    service = CitizenAuthService(db)
    
    try:
        result = service.register_citizen_account(
            citizen_id=register_data.citizen_id,
            email=register_data.email,
            password=register_data.password,
            full_name=register_data.full_name,
            phone=register_data.phone
        )
        
        return {
            "message": "Conta criada com sucesso",
            "user_id": result["user_id"],
            "username": result["username"],
            "email": result["email"],
            "citizen_id": result["citizen_id"]
        }
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar conta: {str(e)}"
        )


@router.post(
    "/link",
    response_model=CitizenLinkResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def link_citizen_to_user(
    link_data: CitizenLinkRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Vincula a conta atual a um cidadão do FUC
    Útil para funcionários que também são cidadãos
    """
    service = CitizenAuthService(db)
    
    try:
        result = service.link_citizen_to_user(
            user_id=str(current_user.id),
            citizen_id=link_data.citizen_id,
            linked_by=str(current_user.id)
        )
        
        return CitizenLinkResponse(
            message="Conta vinculada com sucesso",
            user_id=result["user_id"],
            citizen_id=result["citizen_id"]
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/profile",
    response_model=CitizenProfileResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    }
)
async def get_citizen_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtém perfil do cidadão autenticado
    """
    service = CitizenAuthService(db)
    
    try:
        profile = service.get_citizen_profile(str(current_user.id))
        return CitizenProfileResponse(**profile)
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/check/{identifier}",
    response_model=CitizenCheckResponse,
    responses={
        404: {"model": ErrorResponse}
    }
)
async def check_citizen_exists(
    identifier: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Verifica se um cidadão existe e informa se tem conta
    Útil para formulários de registro
    """
    # Placeholder para a lógica de check
    # Em produção, seria consultado o FUC
    
    return CitizenCheckResponse(
        found=False,
        has_account=False
    )
