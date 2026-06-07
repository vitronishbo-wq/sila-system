TEMPLATE = """from fastapi import APIRouter, HTTPException, Depends
from apps.backend.app.modules.{{ module_name }}.presentation.schemas import EntityRead
from apps.backend.app.modules.{{ module_name }}.presentation.dependencies import get_{{ module_name }}_service
from apps.backend.app.modules.{{ module_name }}.application.service import {{ module_name_camel }}Service

router = APIRouter(prefix="/{{ module_url }}", tags=["{{ module_name_pretty }}"])

@router.get("/{entity_id}", response_model=EntityRead)
async def get_entity(
    entity_id: str,
    service: {{ module_name_camel }}Service = Depends(get_{{ module_name }}_service)
):
    entity = await service.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Not found")
    return entity
"""

__all__ = ["TEMPLATE"]
