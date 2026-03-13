from __future__ import annotations
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import logging
import httpx
from pydantic import BaseModel, Field
from app.core.settings import settings
from apps.backend.app.modules.justice.bounded_contexts.application.ports.citizen_fuc_client_port import CitizenFUCClientPort
from app.core.resilience import ResilientClient
logger = logging.getLogger(__name__)

class FucSovereigntyProjection(BaseModel):
    id: str
    full_name: str
    birth_date: Optional[date] = None
    vital_status: Optional[str] = Field(default='alive')
    documents: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    sync_timestamp: Optional[datetime] = None

class CitizenFUCClient(CitizenFUCClientPort):
    """HTTP async client for the Ficha Única do Cidadão (FUC).

    This is a production-capable client (not a test stub). It performs
    async HTTP requests to the configured FUC service. Tests may subclass
    or mock this class to provide deterministic behavior.
    """

    def __init__(self, base_url: Optional[str]=None, timeout: int=10, **kwargs):
        self.base_url = base_url or settings.FUC_BASE_URL
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = ResilientClient(base_url=self.base_url, timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get_citizen_by_id(self, citizen_fuc_id: str) -> Optional[FucSovereigntyProjection]:
        """Retrieve citizen projection by FUC id.

        Returns `None` if not found.
        """
        try:
            client = await self._get_client()
            resp = await client.get(f'/citizens/{citizen_fuc_id}')
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            payload = resp.json()
            return FucSovereigntyProjection(**payload)
        except httpx.HTTPStatusError as e:
            logger.error('FUC HTTP error fetching citizen: %s', e)
            return None
        except Exception as e:
            logger.exception('Unexpected error contacting FUC: %s', e)
            return None

    async def get_sovereignty_projection(self, citizen_fuc_id: str) -> Optional[FucSovereigntyProjection]:
        """Alias / specialized endpoint for sovereignty projection."""
        try:
            client = await self._get_client()
            resp = await client.get(f'/citizens/{citizen_fuc_id}/sovereignty')
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            payload = resp.json()
            return FucSovereigntyProjection(**payload)
        except Exception:
            logger.exception('Error getting sovereignty projection for %s', citizen_fuc_id)
            return None

    async def validate_eligibility(self, citizen_fuc_id: str, service_code: str) -> bool:
        """Check if citizen is eligible for a given service code in FUC."""
        try:
            client = await self._get_client()
            resp = await client.get(f'/citizens/{citizen_fuc_id}/eligibility', params={'service_code': service_code})
            if resp.status_code == 404:
                return False
            resp.raise_for_status()
            data = resp.json()
            return bool(data.get('eligible', False))
        except Exception:
            logger.exception('Error validating eligibility for %s', citizen_fuc_id)
            return False