from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from apps.backend.app.modules.resources.aguas_saneamento.api.deps import (
    get_faturamento_service,
    get_outbox_worker,
)
from apps.backend.app.modules.resources.aguas_saneamento.api.schemas.fatura_schema import (
    FaturaEmitirInput,
    FaturaMotivoInput,
    FaturaPagamentoInput,
    FaturaResponse,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.faturamento_service import (
    FaturamentoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusFatura
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import (
    FaturaAlreadyExistsError,
    FaturaNotFoundError,
)
from apps.backend.app.modules.resources.aguas_saneamento.workers.outbox_worker import OutboxWorker

router = APIRouter(prefix="/faturas", tags=["Aguas Saneamento - Faturamento"])
faturamento_service_dep = Depends(get_faturamento_service)
outbox_worker_dep = Depends(get_outbox_worker)


@router.post("/", response_model=FaturaResponse, status_code=status.HTTP_201_CREATED)
async def emitir_fatura(
    data: FaturaEmitirInput,
    background_tasks: BackgroundTasks,
    service: FaturamentoService = faturamento_service_dep,
    outbox_worker: OutboxWorker = outbox_worker_dep,
):
    try:
        item = await service.emitir(
            consumo_id=data.consumo_id,
            titular_id=data.titular_id,
            referencia=data.referencia,
            volume_m3=data.volume_m3,
            tarifa_m3=data.tarifa_m3,
            data_vencimento=data.data_vencimento,
        )
        background_tasks.add_task(outbox_worker.process_once)
        return item
    except FaturaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_fatura:path}/pagar", response_model=FaturaResponse)
async def registrar_pagamento_fatura(
    numero_fatura: str,
    data: FaturaPagamentoInput,
    background_tasks: BackgroundTasks,
    service: FaturamentoService = faturamento_service_dep,
    outbox_worker: OutboxWorker = outbox_worker_dep,
):
    try:
        item = await service.registrar_pagamento(
            numero_fatura,
            data_pagamento=data.data_pagamento,
            valor_pago=data.valor_pago,
            metodo_pagamento=data.metodo_pagamento,
        )
        background_tasks.add_task(outbox_worker.process_once)
        return item
    except FaturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{numero_fatura:path}/cancelar", response_model=FaturaResponse)
async def cancelar_fatura(
    numero_fatura: str,
    data: FaturaMotivoInput,
    service: FaturamentoService = faturamento_service_dep,
):
    try:
        return await service.cancelar(numero_fatura, motivo=data.motivo)
    except FaturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{numero_fatura:path}", response_model=FaturaResponse)
async def obter_fatura(
    numero_fatura: str, service: FaturamentoService = faturamento_service_dep
):
    try:
        return await service.obter_por_numero(numero_fatura)
    except FaturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[FaturaResponse])
async def listar_faturas(
    consumo_id: UUID | None = None,
    titular_id: UUID | None = None,
    referencia: str | None = None,
    status_fatura: StatusFatura | None = None,
    service: FaturamentoService = faturamento_service_dep,
):
    return await service.listar(
        consumo_id=consumo_id, titular_id=titular_id, referencia=referencia, status=status_fatura
    )
