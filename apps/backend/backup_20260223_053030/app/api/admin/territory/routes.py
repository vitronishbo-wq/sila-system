"""
API Routes para Territory
Endpoints limpos e simples para navegação territorial
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin_user, get_db
from modules.identity.models.user import User
from .schemas import TerritoryNode, TerritoryNodeWithChildren
from .service import TerritoryService

router = APIRouter(prefix="/territory", tags=["Territory"])


@router.get("/provinces", response_model=list[TerritoryNode])
async def list_provinces(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista todas as províncias de Angola
    
    Resposta:
    ```json
    [
      {"id": "...", "name": "Luanda", "code": "LUA", "type": "province", "parent_id": null},
      {"id": "...", "name": "Bengo", "code": "BGO", "type": "province", "parent_id": null}
    ]
    ```
    """
    return await TerritoryService.get_provinces(db)


@router.get("/provinces/{province_id}/municipalities", response_model=list[TerritoryNode])
async def list_municipalities(
    province_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista municípios de uma provência
    
    Parâmetros:
    - province_id: UUID da provência
    
    Resposta:
    ```json
    [
      {"id": "...", "name": "Luanda", "code": "LUA-LUA", "type": "municipality", "parent_id": "..."},
      {"id": "...", "name": "Cacuaco", "code": "LUA-CAC", "type": "municipality", "parent_id": "..."}
    ]
    ```
    """
    # Validar se a provência existe
    province = await TerritoryService.get_territory_by_id(db, province_id)
    if not province or province.type != "province":
        raise HTTPException(status_code=404, detail="Provência não encontrada")

    return await TerritoryService.get_municipalities_by_province(db, province_id)


@router.get("/municipalities/{municipality_id}/communes", response_model=list[TerritoryNode])
async def list_communes(
    municipality_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista comunas de um município
    
    Parâmetros:
    - municipality_id: UUID do município
    
    Resposta:
    ```json
    [
      {"id": "...", "name": "Luanda", "code": "LUA-LUA-LUA", "type": "commune", "parent_id": "..."},
      {"id": "...", "name": "Rangel", "code": "LUA-LUA-RAN", "type": "commune", "parent_id": "..."}
    ]
    ```
    """
    # Validar se o município existe
    municipality = await TerritoryService.get_territory_by_id(db, municipality_id)
    if not municipality or municipality.type != "municipality":
        raise HTTPException(status_code=404, detail="Município não encontrado")

    return await TerritoryService.get_communes_by_municipality(db, municipality_id)


@router.get("/tree", response_model=list[TerritoryNodeWithChildren])
async def get_hierarchy_tree(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna árvore hierárquica completa de territórios
    (Províncias → Municípios → Comunas)
    
    NOTA: Este endpoint é mais pesado; prefira endpoints específicos para filtros em cascata
    
    Resposta (exemplo truncado):
    ```json
    [
      {
        "id": "...",
        "name": "Luanda",
        "code": "LUA",
        "type": "province",
        "parent_id": null,
        "children": [
          {
            "id": "...",
            "name": "Luanda",
            "code": "LUA-LUA",
            "type": "municipality",
            "parent_id": "...",
            "children": [
              {
                "id": "...",
                "name": "Luanda",
                "code": "LUA-LUA-LUA",
                "type": "commune",
                "parent_id": "...",
                "children": []
              }
            ]
          }
        ]
      }
    ]
    ```
    """
    return await TerritoryService.get_hierarchy_tree(db)
