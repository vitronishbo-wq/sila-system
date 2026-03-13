from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, status
from apps.backend.app.modules.society.assistencia_social.api.deps import get_cadastro_unico_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import raise_http_for_value_error
from apps.backend.app.modules.society.assistencia_social.api.schemas.cadastro_unico_schema import CadastroUnicoCreate, CadastroUnicoCreateResponse, CadastroUnicoResponse
from apps.backend.app.modules.society.assistencia_social.application.services.cadastro_unico_service import CadastroUnicoService
router = APIRouter(prefix='/cadastros-unicos', tags=['Assistencia Social - Cadastro Unico'])

@router.post('/', response_model=CadastroUnicoCreateResponse, status_code=status.HTTP_201_CREATED)
async def registrar_cadastro_unico(data: CadastroUnicoCreate, service: CadastroUnicoService=Depends(get_cadastro_unico_service)) -> CadastroUnicoCreateResponse:
    try:
        cadastro, programas, alertas = await service.registrar_cadastro(citizen_id_responsavel=data.citizen_id_responsavel, renda_per_capita=data.renda_per_capita, composicao_familiar=data.composicao_familiar, condicoes_moradia=data.condicoes_moradia, acesso_agua=data.acesso_agua, acesso_energia=data.acesso_energia, observacoes=data.observacoes)
        return CadastroUnicoCreateResponse(cadastro=CadastroUnicoResponse.model_validate(cadastro), programas_elegiveis=programas, alertas=alertas)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/{cadastro_id}', response_model=CadastroUnicoResponse)
async def obter_cadastro_unico(cadastro_id: UUID, service: CadastroUnicoService=Depends(get_cadastro_unico_service)) -> CadastroUnicoResponse:
    try:
        return await service.buscar_cadastro(cadastro_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/', response_model=list[CadastroUnicoResponse])
async def listar_cadastros_unicos(service: CadastroUnicoService=Depends(get_cadastro_unico_service)) -> list[CadastroUnicoResponse]:
    return await service.listar_cadastros()

@router.delete('/{cadastro_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_cadastro_unico(cadastro_id: UUID, service: CadastroUnicoService=Depends(get_cadastro_unico_service)) -> None:
    try:
        await service.remover_cadastro(cadastro_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)