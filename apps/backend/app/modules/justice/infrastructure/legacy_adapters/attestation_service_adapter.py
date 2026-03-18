import asyncio
from typing import Any

class AttestationServiceAdapter:
    """Compatibility adapter for attestation workflows."""

    def __init__(self, attestation_service: Any=None):
        self.attestation_service = attestation_service

    def create_attestation(self, payload: dict) -> dict:
        if self.attestation_service and hasattr(self.attestation_service, 'create_attestation'):
            result = self.attestation_service.create_attestation(payload)
            return result or {}
        return {}

    def verify_attestation(self, attestation_id: str) -> dict:
        if self.attestation_service and hasattr(self.attestation_service, 'verify_attestation'):
            result = self.attestation_service.verify_attestation(attestation_id)
            return result or {}
        return {}

    def list_attestations(self, citizen_id: str) -> list:
        if self.attestation_service and hasattr(self.attestation_service, 'list_attestations'):
            result = self.attestation_service.list_attestations(citizen_id)
            return result or []
        return []

    async def get_attestations_by_citizen(self, citizen_id) -> list:
        if self.attestation_service and hasattr(self.attestation_service, 'get_attestations_by_citizen'):
            result = self.attestation_service.get_attestations_by_citizen(citizen_id)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, list) else []
        return []

    async def request_attestation(self, payload: dict) -> dict:
        if self.attestation_service and hasattr(self.attestation_service, 'request_attestation'):
            result = self.attestation_service.request_attestation(payload)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, dict) else {}
        return {}