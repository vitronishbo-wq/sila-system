
from fastapi import Header, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_notification_service
from app.core.notifications.services.notification_service import NotificationService
from app.modules.saude_primaria.application.services.healthcare_service import HealthcareService

async def get_current_citizen_id(x_citizen_id: UUID = Header(...)) -> UUID:
    """Extrai o UUID do cidadão do cabeçalho X-Citizen-Id."""
    return x_citizen_id

async def get_current_professional_id(x_professional_id: UUID = Header(...)) -> UUID:
    """Extrai o UUID do profissional do cabeçalho X-Professional-Id."""
    return x_professional_id

async def get_healthcare_service(
    db: AsyncSession = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
) -> HealthcareService:
    """Injeta a instância do serviço de saúde primária com a sessão de base de dados ativa."""
    return HealthcareService(db, notification_service=notification_service)
