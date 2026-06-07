from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ModuleStatus(str, Enum):
    ACTIVE = "active"
    DEVELOPMENT = "development"
    DEPRECATED = "deprecated"
    DISABLED = "disabled"


class TerritorialModel(str, Enum):
    NACIONAL_PROVINCIAL_MUNICIPAL_UNIDADE = "nacional_provincial_municipal_unidade"
    NACIONAL_PROVINCIAL_UNIDADE = "nacional_provincial_unidade"
    NACIONAL_UNIDADE = "nacional_unidade"
    NACIONAL_ONLY = "nacional_only"


@dataclass
class ModuleRegistry:
    """Catálogo oficial de um módulo governamental na plataforma.
    
    Exemplos:
        - educacao: MINED, territorial_model = nacional_provincial_municipal_unidade
        - saude: MINSA, territorial_model = nacional_provincial_unidade
        - justica: MINJUSDH, territorial_model = nacional_provincial_municipal
    """
    module: str
    name: str
    description: str
    version: str = "1.0.0"
    owner_ministry: str = ""
    owner_ministry_code: str = ""
    responsible_entity: str = ""
    territorial_model: TerritorialModel = TerritorialModel.NACIONAL_PROVINCIAL_MUNICIPAL_UNIDADE
    status: ModuleStatus = ModuleStatus.DEVELOPMENT
    approval_chain: list[str] = field(default_factory=list)
    enabled_services: list[str] = field(default_factory=list)
    required_roles: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)
    api_prefix: str = ""
    exposed_events: list[str] = field(default_factory=list)
    consumed_events: list[str] = field(default_factory=list)


class RegistryCatalog:
    """Catálogo oficial de todos os módulos governamentais da plataforma."""

    def __init__(self) -> None:
        self._modules: dict[str, ModuleRegistry] = {}

    def register(self, entry: ModuleRegistry) -> ModuleRegistry:
        self._modules[entry.module] = entry
        return entry

    def get(self, module: str) -> Optional[ModuleRegistry]:
        return self._modules.get(module)

    def list_active(self) -> list[ModuleRegistry]:
        return [m for m in self._modules.values() if m.status == ModuleStatus.ACTIVE]

    def list_by_ministry(self, ministry_code: str) -> list[ModuleRegistry]:
        return [m for m in self._modules.values() if m.owner_ministry_code == ministry_code]

    def list_all(self) -> list[ModuleRegistry]:
        return list(self._modules.values())

    def get_services(self, module: str) -> list[str]:
        entry = self._modules.get(module)
        return list(entry.enabled_services) if entry else []

    def has_module(self, module: str) -> bool:
        return module in self._modules

    def get_exposed_events(self, module: str) -> list[str]:
        entry = self._modules.get(module)
        return list(entry.exposed_events) if entry else []

    def get_consumed_events(self, module: str) -> list[str]:
        entry = self._modules.get(module)
        return list(entry.consumed_events) if entry else []

    def get_subscribers_for_event(self, event: str) -> list[ModuleRegistry]:
        return [m for m in self._modules.values() if event in m.consumed_events]

    def get_publishers_for_event(self, event: str) -> list[ModuleRegistry]:
        return [m for m in self._modules.values() if event in m.exposed_events]

    def count(self) -> int:
        return len(self._modules)

    def count_by_status(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for m in self._modules.values():
            counts[m.status.value] = counts.get(m.status.value, 0) + 1
        return counts
