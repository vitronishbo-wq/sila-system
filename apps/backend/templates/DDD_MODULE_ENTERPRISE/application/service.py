from app.modules.{{ module_name }}.domain.entities import {{ entity_name }}

class {{ module_name_camel }}Service:
    def __init__(self, repository):
        self.repository = repository

    async def get_entity(self, entity_id: str) -> {{ entity_name }}:
        return await self.repository.get_by_id(entity_id)
