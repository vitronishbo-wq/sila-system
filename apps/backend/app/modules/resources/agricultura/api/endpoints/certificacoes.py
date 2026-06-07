from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.resources.agricultura.api.deps import get_certificacao_service
from apps.backend.app.modules.resources.agricultura.api.schemas.certificacao_schema import (
    CertificacaoAprovacaoInput,
    CertificacaoCreate,
    CertificacaoReprovacaoInput,
    CertificacaoResponse,
)
from apps.backend.app.modules.resources.agricultura.application.services.certificacao_service import (
    CertificacaoService,
)
from apps.backend.app.modules.resources.agricultura.exceptions import (
    CertificacaoNotFoundError,
    PropriedadeNotFoundError,
)

router = APIRouter(prefix="/certificacoes", tags=["Agricultura - certificacoes"])
certificacao_service_dep = Depends(get_certificacao_service)


@router.post("/", response_model=CertificacaoResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_certificacao(
    data: CertificacaoCreate, service: CertificacaoService = certificacao_service_dep
):
    try:
        return await service.solicitar(
            codigo_propriedade=data.codigo_propriedade,
            tipo=data.tipo,
            orgao_emissor=data.orgao_emissor,
        )
    except PropriedadeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_certificacao:path}/aprovar", response_model=CertificacaoResponse)
async def aprovar_certificacao(
    codigo_certificacao: str,
    data: CertificacaoAprovacaoInput,
    service: CertificacaoService = certificacao_service_dep,
):
    try:
        return await service.aprovar(codigo_certificacao, data_validade=data.data_validade)
    except CertificacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_certificacao:path}/reprovar", response_model=CertificacaoResponse)
async def reprovar_certificacao(
    codigo_certificacao: str,
    data: CertificacaoReprovacaoInput,
    service: CertificacaoService = certificacao_service_dep,
):
    try:
        return await service.reprovar(codigo_certificacao, motivo=data.motivo)
    except CertificacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_certificacao:path}", response_model=CertificacaoResponse)
async def obter_certificacao(
    codigo_certificacao: str, service: CertificacaoService = certificacao_service_dep
):
    try:
        return await service.obter(codigo_certificacao)
    except CertificacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[CertificacaoResponse])
async def listar_certificacoes(
    codigo_propriedade: str | None = None,
    service: CertificacaoService = certificacao_service_dep,
):
    return await service.listar(codigo_propriedade=codigo_propriedade)
