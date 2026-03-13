from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.api.deps import get_db
from apps.backend.app.modules.governance.administracao_local.application.service import AdministracaoLocalService
from apps.backend.app.modules.governance.administracao_local.infrastructure.repositories.sqlalchemy_repository import Repository

def get_administracao_service(db: AsyncSession=Depends(get_db)) -> AdministracaoLocalService:
    repo = Repository(db)
    return AdministracaoLocalService(repo)