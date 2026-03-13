"""Router FastAPI para operações com Tabelas de Temporalidade."""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.db import get_db
from apps.backend.app.modules.intelligence.arquivo_nacional.application.services.tabela_temporalidade_service import TabelaTemporalidadeService
from apps.backend.app.modules.intelligence.arquivo_nacional.api.schemas import TabelaTemporalidadeCreateSchema, TabelaTemporalidadeResponseSchema, RegraTemporalidadeCreateSchema, RegraTemporalidadeResponseSchema, EventoTemporalidadeCreateSchema, EventoTemporalidadeResponseSchema, TabelaTemporalidadeUpdateSchema, RegraTemporalidadeUpdateSchema, AplicarTemporalidadeSchema
router = APIRouter()

@router.post('/', response_model=TabelaTemporalidadeResponseSchema, status_code=201)
async def criar_tabela_temporalidade(tabela_data: TabelaTemporalidadeCreateSchema, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Cria uma nova tabela de temporalidade."""
    try:
        tabela = await service.criar_tabela_temporalidade(tabela_data, db)
        return TabelaTemporalidadeResponseSchema.from_domain(tabela)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/{tabela_id}', response_model=TabelaTemporalidadeResponseSchema)
async def obter_tabela_temporalidade(tabela_id: UUID, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Obtém uma tabela de temporalidade por ID."""
    tabela = await service.obter_tabela_temporalidade_por_id(tabela_id, db)
    if not tabela:
        raise HTTPException(status_code=404, detail='Tabela de temporalidade não encontrada')
    return TabelaTemporalidadeResponseSchema.from_domain(tabela)

@router.get('/', response_model=List[TabelaTemporalidadeResponseSchema])
async def listar_tabelas_temporalidade(skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=1000), codigo: Optional[str]=None, titulo: Optional[str]=None, ativo: Optional[bool]=None, orgao_id: Optional[UUID]=None, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Lista tabelas de temporalidade com filtros opcionais."""
    tabelas = await service.listar_tabelas_temporalidade(db, skip=skip, limit=limit, codigo=codigo, titulo=titulo, ativo=ativo, orgao_id=orgao_id)
    return [TabelaTemporalidadeResponseSchema.from_domain(tabela) for tabela in tabelas]

@router.put('/{tabela_id}', response_model=TabelaTemporalidadeResponseSchema)
async def atualizar_tabela_temporalidade(tabela_id: UUID, tabela_data: TabelaTemporalidadeUpdateSchema, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Atualiza uma tabela de temporalidade existente."""
    try:
        tabela = await service.atualizar_tabela_temporalidade(tabela_id, tabela_data, db)
        if not tabela:
            raise HTTPException(status_code=404, detail='Tabela de temporalidade não encontrada')
        return TabelaTemporalidadeResponseSchema.from_domain(tabela)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete('/{tabela_id}', status_code=204)
async def excluir_tabela_temporalidade(tabela_id: UUID, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Exclui uma tabela de temporalidade."""
    sucesso = await service.excluir_tabela_temporalidade(tabela_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail='Tabela de temporalidade não encontrada')

@router.post('/{tabela_id}/regras', response_model=RegraTemporalidadeResponseSchema, status_code=201)
async def criar_regra_temporalidade(tabela_id: UUID, regra_data: RegraTemporalidadeCreateSchema, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Cria uma nova regra de temporalidade em uma tabela."""
    try:
        regra = await service.criar_regra_temporalidade(tabela_id, regra_data, db)
        return RegraTemporalidadeResponseSchema.from_domain(regra)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/{tabela_id}/regras', response_model=List[RegraTemporalidadeResponseSchema])
async def listar_regras_tabela(tabela_id: UUID, skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=1000), ativo: Optional[bool]=None, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Lista regras de uma tabela de temporalidade."""
    regras = await service.listar_regras_tabela(tabela_id, db, skip=skip, limit=limit, ativo=ativo)
    return [RegraTemporalidadeResponseSchema.from_domain(regra) for regra in regras]

@router.get('/regras/{regra_id}', response_model=RegraTemporalidadeResponseSchema)
async def obter_regra_temporalidade(regra_id: UUID, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Obtém uma regra de temporalidade por ID."""
    regra = await service.obter_regra_temporalidade_por_id(regra_id, db)
    if not regra:
        raise HTTPException(status_code=404, detail='Regra de temporalidade não encontrada')
    return RegraTemporalidadeResponseSchema.from_domain(regra)

@router.put('/regras/{regra_id}', response_model=RegraTemporalidadeResponseSchema)
async def atualizar_regra_temporalidade(regra_id: UUID, regra_data: RegraTemporalidadeUpdateSchema, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Atualiza uma regra de temporalidade existente."""
    try:
        regra = await service.atualizar_regra_temporalidade(regra_id, regra_data, db)
        if not regra:
            raise HTTPException(status_code=404, detail='Regra de temporalidade não encontrada')
        return RegraTemporalidadeResponseSchema.from_domain(regra)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete('/regras/{regra_id}', status_code=204)
async def excluir_regra_temporalidade(regra_id: UUID, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Exclui uma regra de temporalidade."""
    sucesso = await service.excluir_regra_temporalidade(regra_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail='Regra de temporalidade não encontrada')

@router.post('/eventos', response_model=EventoTemporalidadeResponseSchema, status_code=201)
async def registrar_evento_temporalidade(evento_data: EventoTemporalidadeCreateSchema, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Registra um novo evento de temporalidade."""
    try:
        evento = await service.registrar_evento_temporalidade(evento_data, db)
        return EventoTemporalidadeResponseSchema.from_domain(evento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/eventos/{documento_id}', response_model=List[EventoTemporalidadeResponseSchema])
async def listar_eventos_documento(documento_id: UUID, skip: int=Query(0, ge=0), limit: int=Query(100, ge=1, le=1000), db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Lista eventos de temporalidade de um documento."""
    eventos = await service.listar_eventos_documento(documento_id, db, skip=skip, limit=limit)
    return [EventoTemporalidadeResponseSchema.from_domain(evento) for evento in eventos]

@router.post('/aplicar', response_model=EventoTemporalidadeResponseSchema, status_code=201)
async def aplicar_temporalidade(aplicacao_data: AplicarTemporalidadeSchema, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Aplica uma regra de temporalidade a um documento."""
    try:
        evento = await service.aplicar_temporalidade(aplicacao_data, db)
        return EventoTemporalidadeResponseSchema.from_domain(evento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/documentos/{documento_id}/status-temporalidade')
async def obter_status_temporalidade_documento(documento_id: UUID, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Obtém o status atual de temporalidade de um documento."""
    status = await service.obter_status_temporalidade_documento(documento_id, db)
    if not status:
        raise HTTPException(status_code=404, detail='Documento não encontrado ou sem temporalidade aplicada')
    return status

@router.get('/regras/aplicaveis/{documento_id}', response_model=List[RegraTemporalidadeResponseSchema])
async def obter_regras_aplicaveis_documento(documento_id: UUID, db: AsyncSession=Depends(get_db), service: TabelaTemporalidadeService=Depends()):
    """Obtém regras de temporalidade aplicáveis a um documento."""
    regras = await service.obter_regras_aplicaveis_documento(documento_id, db)
    return [RegraTemporalidadeResponseSchema.from_domain(regra) for regra in regras]