"""
EMIS HTTP Client — communicates with external Education Management Information System.

In production, point EMIS_BASE_URL to the ministry's EMIS API endpoint.
Uses HMAC-SHA256 signing for request authentication.

Retry policy:
  - Retryable: 429 (rate limit), 500, 502, 503, 504, timeout
  - Non-retryable: 400, 401, 403, 404, 422
  - Exponential backoff: 2^retry * 30s base, max 300s
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

import httpx

from apps.backend.app.core.settings import settings
from apps.backend.app.modules.educacao.emis.domain.exceptions import (
    EmisAuthenticationError,
    EmisClientError,
    EmisNotFoundError,
    EmisSyncError,
)
from apps.backend.app.modules.educacao.emis.domain.models import (
    EmisEnrollment,
    EmisInstitution,
    EmisStudent,
)

logger = logging.getLogger(__name__)

RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
MAX_RETRIES = 3
BASE_BACKOFF = 30
MAX_BACKOFF = 300


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, EmisAuthenticationError):
        return False
    if isinstance(exc, EmisNotFoundError):
        return False
    if isinstance(exc, EmisSyncError):
        for code in RETRYABLE_STATUSES:
            if str(code) in str(exc):
                return True
        return False
    if isinstance(exc, EmisClientError):
        return True
    return False


def _backoff_seconds(retry: int) -> float:
    delay = min(BASE_BACKOFF * (2 ** retry), MAX_BACKOFF)
    jitter = delay * 0.1
    return delay + jitter


def _default_emis_base_url() -> str:
    return getattr(settings, "EMIS_BASE_URL", "https://emis.min-ed.ao/api/v1")


def _default_emis_api_key() -> str:
    return getattr(settings, "EMIS_API_KEY", "emis-dev-key")


def _default_emis_api_secret() -> str:
    return getattr(settings, "EMIS_API_SECRET", "emis-dev-secret")


class EmisClient:
    """HTTP client for EMIS REST API with HMAC-SHA256 signing and retry."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.base_url = (base_url or _default_emis_base_url()).rstrip("/")
        self.api_key = api_key or _default_emis_api_key()
        self.api_secret = api_secret or _default_emis_api_secret()
        self._client = httpx.AsyncClient(timeout=timeout)

    def _sign_request(self, method: str, path: str, body: str = "") -> str:
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))
        message = f"{method}:{path}:{timestamp}:{body}"
        signature = hmac.new(
            self.api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return signature

    def _headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        timestamp = str(int(datetime.now(timezone.utc).timestamp()))
        signature = self._sign_request(method, path, body)
        return {
            "X-EMIS-API-Key": self.api_key,
            "X-EMIS-Timestamp": timestamp,
            "X-EMIS-Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def _request(
        self, method: str, path: str, json_data: Optional[dict] = None,
        _retry: int = 0,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        body = json.dumps(json_data or {})
        headers = self._headers(method, path, body)
        try:
            response = await self._client.request(
                method, url, headers=headers, json=json_data
            )
        except httpx.RequestError as exc:
            if _retry < MAX_RETRIES:
                delay = _backoff_seconds(_retry)
                logger.warning("emis_retry attempt=%d delay=%.1f error=%s", _retry + 1, delay, exc)
                await asyncio.sleep(delay)
                return await self._request(method, path, json_data, _retry=_retry + 1)
            raise EmisClientError(f"EMIS request failed after retries: {exc}")

        if response.status_code == 401:
            raise EmisAuthenticationError("EMIS authentication failed")
        if response.status_code == 404:
            raise EmisNotFoundError(f"EMIS resource not found: {path}")
        if response.status_code in RETRYABLE_STATUSES and _retry < MAX_RETRIES:
            delay = _backoff_seconds(_retry)
            logger.warning("emis_retry status=%d attempt=%d delay=%.1f", response.status_code, _retry + 1, delay)
            await asyncio.sleep(delay)
            return await self._request(method, path, json_data, _retry=_retry + 1)
        if response.status_code >= 400:
            raise EmisSyncError(
                f"EMIS error {response.status_code}: {response.text}"
            )

        return response.json()

    async def health_check(self) -> dict[str, Any]:
        return await self._request("GET", "/health")

    async def create_student(self, student: EmisStudent) -> dict[str, Any]:
        return await self._request("POST", "/students", {
            "student_id": str(student.student_id),
            "full_name": student.full_name,
            "document_id": student.document_id,
            "birth_date": student.birth_date.isoformat(),
            "gender": student.gender,
            "province": student.province,
            "municipio": student.municipio,
            "parent_name": student.parent_name,
            "parent_contact": student.parent_contact,
            "address": student.address,
            "nacionalidade": student.nacionalidade,
        })

    async def update_student(self, student_id: str, data: dict) -> dict[str, Any]:
        return await self._request("PUT", f"/students/{student_id}", data)

    async def get_student(self, student_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/students/{student_id}")

    async def create_enrollment(self, enrollment: EmisEnrollment) -> dict[str, Any]:
        return await self._request("POST", "/enrollments", {
            "enrollment_id": str(enrollment.enrollment_id),
            "student_id": str(enrollment.student_id),
            "institution_id": str(enrollment.institution_id),
            "institution_name": enrollment.institution_name,
            "academic_year": enrollment.academic_year,
            "grade": enrollment.grade,
            "shift": enrollment.shift,
            "status": enrollment.status,
            "started_at": enrollment.started_at.isoformat(),
            "ended_at": enrollment.ended_at.isoformat() if enrollment.ended_at else None,
        })

    async def update_enrollment(self, enrollment_id: str, data: dict) -> dict[str, Any]:
        return await self._request("PUT", f"/enrollments/{enrollment_id}", data)

    async def get_enrollment(self, enrollment_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/enrollments/{enrollment_id}")

    async def get_institution(self, institution_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/institutions/{institution_id}")

    async def sync_institution(self, institution: EmisInstitution) -> dict[str, Any]:
        return await self._request("POST", "/institutions", {
            "institution_id": str(institution.institution_id),
            "name": institution.name,
            "institution_type": institution.institution_type,
            "nivel_ensino": institution.nivel_ensino,
            "province": institution.province,
            "municipio": institution.municipio,
            "bairro": institution.bairro,
            "contactos": institution.contactos,
            "turnos": institution.turnos,
        })

    async def close(self):
        await self._client.aclose()
