from apps.backend.app.modules.governance.administracao_local.domain.entities import AdministradorLocal

class AdministracaoLocalService:

    def __init__(self, repository):
        self.repository = repository

    async def get_administrador(self, admin_id: str) -> AdministradorLocal:
        return await self.repository.get_by_id(admin_id)