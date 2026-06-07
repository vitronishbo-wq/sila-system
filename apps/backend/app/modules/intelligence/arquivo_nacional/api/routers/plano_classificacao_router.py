"""Router FastAPI para operações com Planos de Classificação."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import get_db
from apps.backend.app.modules.intelligence.arquivo_nacional.api.schemas import (
    ClasseCreateSchema,
    ClasseResponseSchema,
    ClasseUpdateSchema,
    PlanoClassificacaoCreateSchema,
    PlanoClassificacaoResponseSchema,
    PlanoClassificacaoUpdateSchema,
    SubclasseCreateSchema,
    SubclasseResponseSchema,
    SubclasseUpdateSchema,
)
from apps.backend.app.modules.intelligence.arquivo_nacional.application.services.plano_classificacao_service import (
    PlanoClassificacaoService,
)

router = APIRouter()


@router.post("/", response_model=PlanoClassificacaoResponseSchema, status_code=201)
async def criar_plano_classificacao(
    plano_data: PlanoClassificacaoCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Cria um novo plano de classificação."""
    try:
        plano = await service.criar_plano_classificacao(plano_data, db)
        return PlanoClassificacaoResponseSchema.from_domain(plano)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{plano_id}", response_model=PlanoClassificacaoResponseSchema)
async def obter_plano_classificacao(
    plano_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Obtém um plano de classificação por ID."""
    plano = await service.obter_plano_classificacao_por_id(plano_id, db)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano de classificação não encontrado")
    return PlanoClassificacaoResponseSchema.from_domain(plano)


@router.get("/", response_model=list[PlanoClassificacaoResponseSchema])
async def listar_planos_classificacao(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    codigo: str | None = None,
    titulo: str | None = None,
    ativo: bool | None = None,
    orgao_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Lista planos de classificação com filtros opcionais."""
    planos = await service.listar_planos_classificacao(
        db, skip=skip, limit=limit, codigo=codigo, titulo=titulo, ativo=ativo, orgao_id=orgao_id
    )
    return [PlanoClassificacaoResponseSchema.from_domain(plano) for plano in planos]


@router.put("/{plano_id}", response_model=PlanoClassificacaoResponseSchema)
async def atualizar_plano_classificacao(
    plano_id: UUID,
    plano_data: PlanoClassificacaoUpdateSchema,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Atualiza um plano de classificação existente."""
    try:
        plano = await service.atualizar_plano_classificacao(plano_id, plano_data, db)
        if not plano:
            raise HTTPException(status_code=404, detail="Plano de classificação não encontrado")
        return PlanoClassificacaoResponseSchema.from_domain(plano)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{plano_id}", status_code=204)
async def excluir_plano_classificacao(
    plano_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Exclui um plano de classificação."""
    sucesso = await service.excluir_plano_classificacao(plano_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Plano de classificação não encontrado")


@router.post("/{plano_id}/classes", response_model=ClasseResponseSchema, status_code=201)
async def criar_classe(
    plano_id: UUID,
    classe_data: ClasseCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Cria uma nova classe em um plano de classificação."""
    try:
        classe = await service.criar_classe(plano_id, classe_data, db)
        return ClasseResponseSchema.from_domain(classe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{plano_id}/classes", response_model=list[ClasseResponseSchema])
async def listar_classes_plano(
    plano_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: bool | None = None,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Lista classes de um plano de classificação."""
    classes = await service.listar_classes_plano(plano_id, db, skip=skip, limit=limit, ativo=ativo)
    return [ClasseResponseSchema.from_domain(classe) for classe in classes]


@router.get("/classes/{classe_id}", response_model=ClasseResponseSchema)
async def obter_classe(
    classe_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Obtém uma classe por ID."""
    classe = await service.obter_classe_por_id(classe_id, db)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe não encontrada")
    return ClasseResponseSchema.from_domain(classe)


@router.put("/classes/{classe_id}", response_model=ClasseResponseSchema)
async def atualizar_classe(
    classe_id: UUID,
    classe_data: ClasseUpdateSchema,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Atualiza uma classe existente."""
    try:
        classe = await service.atualizar_classe(classe_id, classe_data, db)
        if not classe:
            raise HTTPException(status_code=404, detail="Classe não encontrada")
        return ClasseResponseSchema.from_domain(classe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/classes/{classe_id}", status_code=204)
async def excluir_classe(
    classe_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Exclui uma classe."""
    sucesso = await service.excluir_classe(classe_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Classe não encontrada")


@router.post(
    "/classes/{classe_id}/subclasses", response_model=SubclasseResponseSchema, status_code=201
)
async def criar_subclasse(
    classe_id: UUID,
    subclasse_data: SubclasseCreateSchema,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Cria uma nova subclasse em uma classe."""
    try:
        subclasse = await service.criar_subclasse(classe_id, subclasse_data, db)
        return SubclasseResponseSchema.from_domain(subclasse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/classes/{classe_id}/subclasses", response_model=list[SubclasseResponseSchema])
async def listar_subclasses_classe(
    classe_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ativo: bool | None = None,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Lista subclasses de uma classe."""
    subclasses = await service.listar_subclasses_classe(
        classe_id, db, skip=skip, limit=limit, ativo=ativo
    )
    return [SubclasseResponseSchema.from_domain(sub) for sub in subclasses]


@router.get("/subclasses/{subclasse_id}", response_model=SubclasseResponseSchema)
async def obter_subclasse(
    subclasse_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Obtém uma subclasse por ID."""
    subclasse = await service.obter_subclasse_por_id(subclasse_id, db)
    if not subclasse:
        raise HTTPException(status_code=404, detail="Subclasse não encontrada")
    return SubclasseResponseSchema.from_domain(subclasse)


@router.put("/subclasses/{subclasse_id}", response_model=SubclasseResponseSchema)
async def atualizar_subclasse(
    subclasse_id: UUID,
    subclasse_data: SubclasseUpdateSchema,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Atualiza uma subclasse existente."""
    try:
        subclasse = await service.atualizar_subclasse(subclasse_id, subclasse_data, db)
        if not subclasse:
            raise HTTPException(status_code=404, detail="Subclasse não encontrada")
        return SubclasseResponseSchema.from_domain(subclasse)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/subclasses/{subclasse_id}", status_code=204)
async def excluir_subclasse(
    subclasse_id: UUID,
    db: AsyncSession = Depends(get_db),
    service: PlanoClassificacaoService = Depends(),
):
    """Exclui uma subclasse."""
    sucesso = await service.excluir_subclasse(subclasse_id, db)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Subclasse não encontrada")
