"""Router FastAPI para operações com Processos."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import get_db
from apps.backend.app.modules.intelligence.arquivo_nacional.api.schemas import (
    HistoricoTramitacaoSchema,
    ProcessoArquivamentoSchema,
    ProcessoAutuarDocumentoSchema,
    ProcessoCreateSchema,
    ProcessoEncerramentoSchema,
    ProcessoRecebimentoSchema,
    ProcessoResponseSchema,
    ProcessoTramitacaoSchema,
)
from apps.backend.app.modules.intelligence.arquivo_nacional.application.services.processo_service import (
    ProcessoService,
)

router = APIRouter()


@router.post("/", response_model=ProcessoResponseSchema, status_code=201)
async def criar_processo(
    processo_data: ProcessoCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Cria um novo processo."""
    try:
        processo = await service.criar_processo(processo_data, db)
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{processo_id}", response_model=ProcessoResponseSchema)
async def obter_processo(
    processo_id: UUID, db: AsyncSession = Depends(get_db), service: ProcessoService = Depends()
):
    """Obtém um processo por ID."""
    processo = await service.obter_processo_por_id(processo_id, db)
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    return ProcessoResponseSchema.from_domain(processo)


@router.get("/", response_model=list[ProcessoResponseSchema])
async def listar_processos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    numero: str | None = None,
    assunto: str | None = None,
    status: str | None = None,
    orgao_origem_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Lista processos com filtros opcionais."""
    processos = await service.listar_processos(
        db,
        skip=skip,
        limit=limit,
        numero=numero,
        assunto=assunto,
        status=status,
        orgao_origem_id=orgao_origem_id,
    )
    return [ProcessoResponseSchema.from_domain(proc) for proc in processos]


@router.put("/{processo_id}", response_model=ProcessoResponseSchema)
async def atualizar_processo(
    processo_id: UUID,
    processo_data: ProcessoCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Atualiza um processo existente."""
    try:
        processo = await service.atualizar_processo(processo_id, processo_data, db)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado")
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{processo_id}", status_code=204)
async def excluir_processo(
    processo_id: UUID, db: AsyncSession = Depends(get_db), service: ProcessoService = Depends()
):
    """Exclui um processo."""
    sucesso = await service.excluir_processo(processo_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Processo não encontrado")


@router.post("/{processo_id}/tramitar", response_model=ProcessoResponseSchema)
async def tramitar_processo(
    processo_id: UUID,
    tramitacao_data: ProcessoTramitacaoSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Tramita um processo para outra unidade."""
    try:
        processo = await service.tramitar_processo(processo_id, tramitacao_data, db)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado")
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{processo_id}/receber", response_model=ProcessoResponseSchema)
async def receber_processo(
    processo_id: UUID,
    recebimento_data: ProcessoRecebimentoSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Registra recebimento de um processo tramitado."""
    try:
        processo = await service.receber_processo(processo_id, recebimento_data, db)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado")
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{processo_id}/encerrar", response_model=ProcessoResponseSchema)
async def encerrar_processo(
    processo_id: UUID,
    encerramento_data: ProcessoEncerramentoSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Encerra um processo."""
    try:
        processo = await service.encerrar_processo(processo_id, encerramento_data, db)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado")
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{processo_id}/arquivar", response_model=ProcessoResponseSchema)
async def arquivar_processo(
    processo_id: UUID,
    arquivamento_data: ProcessoArquivamentoSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Arquiva um processo."""
    try:
        processo = await service.arquivar_processo(processo_id, arquivamento_data, db)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado")
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{processo_id}/autuar-documento", response_model=ProcessoResponseSchema)
async def autuar_documento_processo(
    processo_id: UUID,
    autuacao_data: ProcessoAutuarDocumentoSchema,
    db: AsyncSession = Depends(get_db),
    service: ProcessoService = Depends(),
):
    """Autua um documento em um processo."""
    try:
        processo = await service.autuar_documento_processo(processo_id, autuacao_data, db)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado")
        return ProcessoResponseSchema.from_domain(processo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{processo_id}/historico", response_model=list[HistoricoTramitacaoSchema])
async def obter_historico_tramitacao(
    processo_id: UUID, db: AsyncSession = Depends(get_db), service: ProcessoService = Depends()
):
    """Obtém histórico de tramitações de um processo."""
    historico = await service.obter_historico_tramitacao(processo_id, db)
    return historico
