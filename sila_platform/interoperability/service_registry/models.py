from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ServiceStatus(str, Enum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    DOWN = "down"


class ServiceVisibility(str, Enum):
    PUBLIC = "public"
    INTER_MODULE = "inter_module"
    INTERNAL = "internal"


@dataclass
class ServiceEntry:
    """Serviço publicado por um módulo, consumível por outros módulos ou pelo cidadão."""
    id: str
    module: str
    name: str
    description: str
    version: str = "1.0.0"
    visibility: ServiceVisibility = ServiceVisibility.INTER_MODULE
    status: ServiceStatus = ServiceStatus.ACTIVE
    endpoint: str = ""
    required_roles: list[str] = field(default_factory=list)
    required_consent: list[str] = field(default_factory=list)
    input_schema: Optional[dict] = None
    output_schema: Optional[dict] = None
    tags: list[str] = field(default_factory=list)


class ServiceRegistry:
    """Registo de serviços expostos por cada módulo para interoperabilidade."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceEntry] = {}

    def register(self, service: ServiceEntry) -> ServiceEntry:
        self._services[service.id] = service
        return service

    def get(self, service_id: str) -> Optional[ServiceEntry]:
        return self._services.get(service_id)

    def list_by_module(self, module: str) -> list[ServiceEntry]:
        return [s for s in self._services.values() if s.module == module]

    def list_public(self) -> list[ServiceEntry]:
        return [s for s in self._services.values() if s.visibility == ServiceVisibility.PUBLIC]

    def list_by_tag(self, tag: str) -> list[ServiceEntry]:
        return [s for s in self._services.values() if tag in s.tags]

    def list_all(self) -> list[ServiceEntry]:
        return list(self._services.values())

    def check_access(self, service_id: str, role: str) -> bool:
        service = self._services.get(service_id)
        if not service or service.status != ServiceStatus.ACTIVE:
            return False
        if not service.required_roles:
            return True
        return role in service.required_roles
