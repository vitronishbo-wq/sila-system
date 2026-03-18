import asyncio
from typing import Any

class RequestTrackingServiceAdapter:
    """Compatibility adapter for request tracking service."""

    def __init__(self, tracking_service: Any=None):
        self.tracking_service = tracking_service

    def open_request(self, payload: dict) -> dict:
        if self.tracking_service and hasattr(self.tracking_service, 'open_request'):
            result = self.tracking_service.open_request(payload)
            return result or {}
        return {}

    def get_status(self, request_id: str) -> dict:
        if self.tracking_service and hasattr(self.tracking_service, 'get_status'):
            result = self.tracking_service.get_status(request_id)
            return result or {}
        return {}

    def list_requests(self, citizen_id: str) -> list:
        if self.tracking_service and hasattr(self.tracking_service, 'list_requests'):
            result = self.tracking_service.list_requests(citizen_id)
            return result or []
        return []

    async def get_citizen_requests(self, citizen_id) -> list:
        if self.tracking_service and hasattr(self.tracking_service, 'get_citizen_requests'):
            result = self.tracking_service.get_citizen_requests(citizen_id)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, list) else []
        return []

    async def get_request_detail(self, request_id) -> dict:
        if self.tracking_service and hasattr(self.tracking_service, 'get_request_detail'):
            result = self.tracking_service.get_request_detail(request_id)
            if asyncio.iscoroutine(result):
                result = await result
            return result if isinstance(result, dict) else {}
        return {'request_id': str(request_id)}