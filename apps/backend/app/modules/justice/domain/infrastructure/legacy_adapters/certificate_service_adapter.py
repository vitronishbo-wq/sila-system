import asyncio
from typing import Any


class CertificateServiceAdapter:
    """Compatibility adapter for certificate issuance lookups."""

    def __init__(self, certificate_service: Any = None):
        self.certificate_service = certificate_service

    def issue_certificate(self, payload: dict) -> dict:
        if self.certificate_service and hasattr(self.certificate_service, "issue_certificate"):
            result = self.certificate_service.issue_certificate(payload)
            return result or {}
        return {}

    def verify_certificate(self, certificate_id: str) -> dict:
        if self.certificate_service and hasattr(self.certificate_service, "verify_certificate"):
            result = self.certificate_service.verify_certificate(certificate_id)
            return result or {}
        return {}

    def get_certificates(self, citizen_id: str) -> list:
        if self.certificate_service and hasattr(self.certificate_service, "get_certificates"):
            result = self.certificate_service.get_certificates(citizen_id)
            return result or []
        return []

    async def get_certificates_by_citizen(self, citizen_id) -> list:
        if self.certificate_service and hasattr(self.certificate_service, "get_certificates_by_citizen"):
            result = self.certificate_service.get_certificates_by_citizen(citizen_id)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, list) else []
        return []

    async def request_certificate(self, payload: dict) -> dict:
        if self.certificate_service and hasattr(self.certificate_service, "request_certificate"):
            result = self.certificate_service.request_certificate(payload)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, dict) else {}
        return {}
