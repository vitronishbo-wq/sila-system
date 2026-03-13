from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from apps.backend.app.modules.{{ module_name }}.infrastructure.models import {{ entity_name }}Model
from apps.backend.app.modules.{{ module_name }}.infrastructure.mappers import {{ entity_name }}Mapper
from apps.backend.app.modules.{{ module_name }}.domain.entities import {{ entity_name }}

class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, entity_id: str) -> {{ entity_name }}:
        result = await self.db.execute(select({{ entity_name }}Model).where({{ entity_name }}Model.id == entity_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return {{ entity_name }}Mapper.to_domain(model)
