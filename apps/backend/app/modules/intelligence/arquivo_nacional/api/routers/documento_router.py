"""Router FastAPI para operações com Documentos."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import get_db
from apps.backend.app.modules.intelligence.arquivo_nacional.api.schemas import (
    DocumentoConservacaoSchema,
    DocumentoCreateSchema,
    DocumentoDigitalizacaoSchema,
    DocumentoEliminacaoSchema,
    DocumentoFaseSchema,
    DocumentoResponseSchema,
    DocumentoRestricaoSchema,
)
from apps.backend.app.modules.intelligence.arquivo_nacional.application.services.documento_service import (
    DocumentoService,
)

router = APIRouter()


@router.post("/", response_model=DocumentoResponseSchema, status_code=201)
async def criar_documento(
    documento_data: DocumentoCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Cria um novo documento."""
    try:
        documento = await service.criar_documento(documento_data, db)
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{documento_id}", response_model=DocumentoResponseSchema)
async def obter_documento(
    documento_id: UUID, db: AsyncSession = Depends(get_db), service: DocumentoService = Depends()
):
    """Obtém um documento por ID."""
    documento = await service.obter_documento_por_id(documento_id, db)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return DocumentoResponseSchema.from_domain(documento)


@router.get("/", response_model=list[DocumentoResponseSchema])
async def listar_documentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    numero: str | None = None,
    titulo: str | None = None,
    tipo: str | None = None,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Lista documentos com filtros opcionais."""
    documentos = await service.listar_documentos(
        db, skip=skip, limit=limit, numero=numero, titulo=titulo, tipo=tipo
    )
    return [DocumentoResponseSchema.from_domain(doc) for doc in documentos]


@router.put("/{documento_id}", response_model=DocumentoResponseSchema)
async def atualizar_documento(
    documento_id: UUID,
    documento_data: DocumentoCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Atualiza um documento existente."""
    try:
        documento = await service.atualizar_documento(documento_id, documento_data, db)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{documento_id}", status_code=204)
async def excluir_documento(
    documento_id: UUID, db: AsyncSession = Depends(get_db), service: DocumentoService = Depends()
):
    """Exclui um documento."""
    sucesso = await service.excluir_documento(documento_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Documento não encontrado")


@router.post("/{documento_id}/digitalizar", response_model=DocumentoResponseSchema)
async def digitalizar_documento(
    documento_id: UUID,
    digitalizacao_data: DocumentoDigitalizacaoSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Digitaliza um documento."""
    try:
        documento = await service.digitalizar_documento(documento_id, digitalizacao_data, db)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{documento_id}/restringir", response_model=DocumentoResponseSchema)
async def restringir_documento(
    documento_id: UUID,
    restricao_data: DocumentoRestricaoSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Aplica restrição a um documento."""
    try:
        documento = await service.restringir_documento(documento_id, restricao_data, db)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{documento_id}/conservar", response_model=DocumentoResponseSchema)
async def conservar_documento(
    documento_id: UUID,
    conservacao_data: DocumentoConservacaoSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Inicia processo de conservação de um documento."""
    try:
        documento = await service.conservar_documento(documento_id, conservacao_data, db)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{documento_id}/fase", response_model=DocumentoResponseSchema)
async def alterar_fase_documento(
    documento_id: UUID,
    fase_data: DocumentoFaseSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Altera a fase de um documento."""
    try:
        documento = await service.alterar_fase_documento(documento_id, fase_data, db)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{documento_id}/eliminar", response_model=DocumentoResponseSchema)
async def eliminar_documento(
    documento_id: UUID,
    eliminacao_data: DocumentoEliminacaoSchema,
    db: AsyncSession = Depends(get_db),
    service: DocumentoService = Depends(),
):
    """Elimina um documento permanentemente."""
    try:
        documento = await service.eliminar_documento(documento_id, eliminacao_data, db)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return DocumentoResponseSchema.from_domain(documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
