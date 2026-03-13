from __future__ import annotations
from fastapi import APIRouter
from app.modules.economy.trade.services.api.schemas.catalogo_schema import CatalogoItemSchema
from app.modules.economy.trade.services.domain.shared import list_portes, list_ramos
router = APIRouter(tags=['Comercio Servicos - Catalogos'])

@router.get('/ramos', response_model=list[CatalogoItemSchema])
async def listar_ramos() -> list[CatalogoItemSchema]:
    return [CatalogoItemSchema(codigo=item.codigo.value, descricao=item.descricao) for item in list_ramos()]

@router.get('/portes', response_model=list[CatalogoItemSchema])
async def listar_portes() -> list[CatalogoItemSchema]:
    return [CatalogoItemSchema(codigo=item.codigo.value, descricao=item.descricao) for item in list_portes()]