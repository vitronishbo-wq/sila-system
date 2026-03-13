from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.modules.governance.administracao_local.application.service import AdministracaoLocalService
from app.modules.governance.administracao_local.infrastructure.repositories.sqlalchemy_repository import Repository

def get_administracao_service(db: AsyncSession=Depends(get_db)) -> AdministracaoLocalService:
    repo = Repository(db)
    return AdministracaoLocalService(repo)