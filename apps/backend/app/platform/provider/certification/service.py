import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from apps.backend.app.core.db import db
from apps.backend.app.platform.provider.certification.models import ProviderCertification
from sqlalchemy import select

logger = logging.getLogger(__name__)


class CertificationStatus(str, Enum):
    MOCK = "mock"
    TESTING = "testing"
    MOCK_LIVE = "mock_live"
    HOMOLOGATION = "homologation"
    CERTIFIED = "certified"
    PRODUCTION = "production"
    SUSPENDED = "suspended"


class CertificationService:
    async def get(self, provider: str) -> Optional[ProviderCertification]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderCertification).where(
                    ProviderCertification.provider == provider
                ).order_by(ProviderCertification.created_at.desc()).limit(1)
            )
            return result.scalar_one_or_none()

    async def get_all(self) -> list[ProviderCertification]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderCertification).order_by(ProviderCertification.provider)
            )
            return list(result.scalars().all())

    async def set_status(
        self,
        provider: str,
        status: CertificationStatus,
        environment: str = "production",
        approved_by: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> ProviderCertification:
        async with db.session_factory() as session:
            cert = ProviderCertification(
                provider=provider,
                environment=environment,
                certification_status=status.value,
                approved_by=approved_by,
                approval_date=datetime.now(timezone.utc) if status in (
                    CertificationStatus.CERTIFIED, CertificationStatus.PRODUCTION
                ) else None,
                notes=notes,
            )
            session.add(cert)
            await session.commit()
            await session.refresh(cert)
            logger.info(f"certification provider={provider} status={status.value}")
            return cert

    async def to_dict(self, provider: str) -> dict:
        cert = await self.get(provider)
        if not cert:
            return {"provider": provider, "status": CertificationStatus.MOCK.value}
        return {
            "provider": cert.provider,
            "environment": cert.environment,
            "status": cert.certification_status,
            "approved_by": cert.approved_by,
            "approval_date": cert.approval_date.isoformat() if cert.approval_date else None,
            "expiration_date": cert.expiration_date.isoformat() if cert.expiration_date else None,
            "notes": cert.notes,
        }
