from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.api.schemas.transfer_wizard_schema import (
    ElegibilidadeResponse,
    IniciarResponse,
    Passo1OrigemRequest,
    Passo2DestinoRequest,
    Passo4ReservarRequest,
    Passo5ConfirmarRequest,
    TransferWizardResponse,
)
from apps.backend.app.modules.educacao.application.marketplace.transfer_wizard_service import (
    TransferWizardService,
)

router = APIRouter(
    prefix="/transferencias/wizard",
    tags=["Educacao - Transferencia Wizard"],
)


async def _get_service(db: AsyncSession = Depends(get_db)) -> TransferWizardService:
    return TransferWizardService(db)


@router.post("/iniciar", response_model=IniciarResponse, status_code=status.HTTP_201_CREATED)
async def iniciar(
    _: dict = Depends(get_current_user),
    service: TransferWizardService = Depends(_get_service),
):
    citizen_id = _.get("citizen_id", _.get("sub"))
    if not citizen_id:
        raise HTTPException(status_code=400, detail="citizen_id nao encontrado no token")
    session = await service.iniciar(uuid.UUID(citizen_id))
    return IniciarResponse(
        wizard_id=session.id,
        status=session.status.value,
        passo_atual=session.passo_atual,
        expires_at=session.expires_at,
    )


@router.get("/{wizard_id}", response_model=TransferWizardResponse)
async def obter(
    wizard_id: uuid.UUID,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
):
    session = await service.obter(wizard_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada")
    return TransferWizardResponse(
        id=session.id,
        citizen_id=session.citizen_id,
        status=session.status.value,
        passo_atual=session.passo_atual,
        origem_escola_id=session.origem_escola_id,
        origem_classe=session.origem_classe,
        destino_escola_id=session.destino_escola_id,
        destino_classe=session.destino_classe,
        destino_turno=session.destino_turno,
        motivo=session.motivo,
        elegibilidade=session.elegibilidade,
        reserva_id=session.reserva_id,
        transferencia_id=session.transferencia_id,
        created_at=session.created_at,
        expires_at=session.expires_at,
    )


@router.get("/", response_model=list[TransferWizardResponse])
async def listar(
    _: dict = Depends(get_current_user),
    service: TransferWizardService = Depends(_get_service),
):
    citizen_id = _.get("citizen_id", _.get("sub"))
    if not citizen_id:
        raise HTTPException(status_code=400, detail="citizen_id nao encontrado no token")
    sessions = await service.listar(uuid.UUID(citizen_id))
    return [
        TransferWizardResponse(
            id=s.id,
            citizen_id=s.citizen_id,
            status=s.status.value,
            passo_atual=s.passo_atual,
            origem_escola_id=s.origem_escola_id,
            origem_classe=s.origem_classe,
            destino_escola_id=s.destino_escola_id,
            destino_classe=s.destino_classe,
            destino_turno=s.destino_turno,
            motivo=s.motivo,
            elegibilidade=s.elegibilidade,
            reserva_id=s.reserva_id,
            transferencia_id=s.transferencia_id,
            created_at=s.created_at,
            expires_at=s.expires_at,
        )
        for s in sessions
    ]


@router.post("/{wizard_id}/passo1/origem", response_model=TransferWizardResponse)
async def salvar_origem(
    wizard_id: uuid.UUID,
    dados: Passo1OrigemRequest,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
):
    try:
        session = await service.passo1_origem(wizard_id, dados.origem_escola_id, dados.origem_classe)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return TransferWizardResponse(
        id=session.id,
        citizen_id=session.citizen_id,
        status=session.status.value,
        passo_atual=session.passo_atual,
        origem_escola_id=session.origem_escola_id,
        origem_classe=session.origem_classe,
        destino_escola_id=session.destino_escola_id,
        destino_classe=session.destino_classe,
        destino_turno=session.destino_turno,
        motivo=session.motivo,
        elegibilidade=session.elegibilidade,
        reserva_id=session.reserva_id,
        transferencia_id=session.transferencia_id,
        created_at=session.created_at,
        expires_at=session.expires_at,
    )


@router.post("/{wizard_id}/passo2/destino", response_model=TransferWizardResponse)
async def salvar_destino(
    wizard_id: uuid.UUID,
    dados: Passo2DestinoRequest,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
):
    try:
        session = await service.passo2_destino(
            wizard_id, dados.destino_escola_id, dados.destino_classe, dados.destino_turno, dados.motivo
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return TransferWizardResponse(
        id=session.id,
        citizen_id=session.citizen_id,
        status=session.status.value,
        passo_atual=session.passo_atual,
        origem_escola_id=session.origem_escola_id,
        origem_classe=session.origem_classe,
        destino_escola_id=session.destino_escola_id,
        destino_classe=session.destino_classe,
        destino_turno=session.destino_turno,
        motivo=session.motivo,
        elegibilidade=session.elegibilidade,
        reserva_id=session.reserva_id,
        transferencia_id=session.transferencia_id,
        created_at=session.created_at,
        expires_at=session.expires_at,
    )


@router.post("/{wizard_id}/passo3/elegibilidade", response_model=ElegibilidadeResponse)
async def verificar_elegibilidade(
    wizard_id: uuid.UUID,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
    ano_letivo: str = Query("2026"),
):
    try:
        session, eligibility = await service.passo3_elegibilidade(wizard_id, ano_letivo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return ElegibilidadeResponse(
        elegivel=eligibility["elegivel"],
        score=eligibility["score"],
        motivos=eligibility["motivos"],
        tem_vaga=eligibility["tem_vaga"],
        mesma_rede=eligibility["mesma_rede"],
        classes_compativeis=eligibility["classes_compativeis"],
        ano_letivo=eligibility["ano_letivo"],
    )


@router.post("/{wizard_id}/passo4/reservar", response_model=dict)
async def reservar_vaga(
    wizard_id: uuid.UUID,
    dados: Passo4ReservarRequest,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
):
    try:
        _, reserva = await service.passo4_reservar(wizard_id, dados.student_id, dados.ano_letivo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return reserva


@router.post("/{wizard_id}/passo5/confirmar", response_model=TransferWizardResponse)
async def confirmar_transferencia(
    wizard_id: uuid.UUID,
    dados: Passo5ConfirmarRequest,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
):
    try:
        session = await service.passo5_confirmar(wizard_id, dados.transferencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return TransferWizardResponse(
        id=session.id,
        citizen_id=session.citizen_id,
        status=session.status.value,
        passo_atual=session.passo_atual,
        origem_escola_id=session.origem_escola_id,
        origem_classe=session.origem_classe,
        destino_escola_id=session.destino_escola_id,
        destino_classe=session.destino_classe,
        destino_turno=session.destino_turno,
        motivo=session.motivo,
        elegibilidade=session.elegibilidade,
        reserva_id=session.reserva_id,
        transferencia_id=session.transferencia_id,
        created_at=session.created_at,
        expires_at=session.expires_at,
    )


@router.post("/{wizard_id}/cancelar", response_model=TransferWizardResponse)
async def cancelar(
    wizard_id: uuid.UUID,
    service: TransferWizardService = Depends(_get_service),
    _: dict = Depends(get_current_user),
):
    try:
        session = await service.cancelar(wizard_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return TransferWizardResponse(
        id=session.id,
        citizen_id=session.citizen_id,
        status=session.status.value,
        passo_atual=session.passo_atual,
        origem_escola_id=session.origem_escola_id,
        origem_classe=session.origem_classe,
        destino_escola_id=session.destino_escola_id,
        destino_classe=session.destino_classe,
        destino_turno=session.destino_turno,
        motivo=session.motivo,
        elegibilidade=session.elegibilidade,
        reserva_id=session.reserva_id,
        transferencia_id=session.transferencia_id,
        created_at=session.created_at,
        expires_at=session.expires_at,
    )
