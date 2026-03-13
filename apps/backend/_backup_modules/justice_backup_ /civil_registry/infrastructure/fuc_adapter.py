from typing import Optional
import httpx
from app.core.settings import settings
from apps.backend.app.modules.justice.bounded_contexts.application.ports import CitizenPort

class FUCCitizenAdapter(CitizenPort):
    """Single FUC adapter for citizen read/validation."""

    async def validate(self, citizen_id: str) -> bool:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f'{settings.FUC_BASE_URL}/validate/{citizen_id}')
            return response.status_code == 200

    async def get(self, citizen_id: str) -> Optional[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f'{settings.FUC_BASE_URL}/citizen/{citizen_id}')
            if response.status_code != 200:
                return None
            return response.json()