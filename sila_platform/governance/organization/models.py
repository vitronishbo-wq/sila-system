from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class OrganizationType(str, Enum):
    MINISTRY = "ministry"
    PROVINCIAL_DIRECTORATE = "provincial_directorate"
    MUNICIPAL_DIRECTORATE = "municipal_directorate"
    UNIT = "unit"


@dataclass
class Organization:
    """Órgão ou entidade do Estado."""
    id: str
    name: str
    org_type: OrganizationType
    module: str
    parent_id: Optional[str] = None
    province_id: Optional[str] = None
    province_name: Optional[str] = None
    municipality_id: Optional[str] = None
    municipality_name: Optional[str] = None
    unit_id: Optional[str] = None
    unit_name: Optional[str] = None
    code: Optional[str] = None
    active: bool = True
    children: list[Organization] = field(default_factory=list)


class OrganizationTree:
    """Árvore hierárquica de órgãos do Estado.
    
    Exemplo:
        MINED
        ├── DPE Huambo
        │   ├── DME Caála
        │   │   └── Escola 4 de Fevereiro
        │   └── DME Bailundo
        └── DPE Benguela
    """

    def __init__(self) -> None:
        self._orgs: dict[str, Organization] = {}
        self._roots: list[Organization] = []

    def register(self, org: Organization) -> Organization:
        self._orgs[org.id] = org
        if org.parent_id and org.parent_id in self._orgs:
            parent = self._orgs[org.parent_id]
            parent.children.append(org)
        else:
            self._roots.append(org)
        return org

    def get(self, org_id: str) -> Optional[Organization]:
        return self._orgs.get(org_id)

    def get_by_module(self, module: str) -> list[Organization]:
        return [o for o in self._orgs.values() if o.module == module]

    def get_by_type(self, org_type: OrganizationType) -> list[Organization]:
        return [o for o in self._orgs.values() if o.org_type == org_type]

    def get_roots(self) -> list[Organization]:
        return list(self._roots)

    def get_ancestors(self, org_id: str) -> list[Organization]:
        result: list[Organization] = []
        org = self._orgs.get(org_id)
        while org and org.parent_id:
            parent = self._orgs.get(org.parent_id)
            if parent:
                result.append(parent)
                org = parent
            else:
                break
        return result

    def get_descendants(self, org_id: str) -> list[Organization]:
        result: list[Organization] = []
        org = self._orgs.get(org_id)
        if org:
            self._collect_descendants(org, result)
        return result

    def _collect_descendants(self, org: Organization, acc: list[Organization]) -> None:
        for child in org.children:
            acc.append(child)
            self._collect_descendants(child, acc)

    def count(self) -> int:
        return len(self._orgs)

    def to_tree_dict(self, org_id: Optional[str] = None) -> list[dict]:
        if org_id:
            org = self._orgs.get(org_id)
            roots = [org] if org else []
        else:
            roots = self._roots
        return [self._node_to_dict(r) for r in roots]

    @staticmethod
    def _node_to_dict(org: Organization) -> dict:
        return {
            "id": org.id,
            "name": org.name,
            "type": org.org_type.value,
            "module": org.module,
            "code": org.code,
            "children": [OrganizationTree._node_to_dict(c) for c in org.children],
        }
