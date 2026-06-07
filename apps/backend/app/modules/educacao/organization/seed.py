from __future__ import annotations

import os
from pathlib import Path

import yaml

from sila_platform.governance.organization.models import Organization, OrganizationTree, OrganizationType

_SEEDED_TREE: OrganizationTree | None = None


def _load_yaml() -> dict:
    path = Path(__file__).resolve().parent / "organizations.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_org(key: str, data: dict) -> Organization:
    org_type = data.get("type", "unit")
    type_map = {
        "ministry": OrganizationType.MINISTRY,
        "national_directorate": OrganizationType.PROVINCIAL_DIRECTORATE,
        "provincial_directorate": OrganizationType.PROVINCIAL_DIRECTORATE,
        "municipal_directorate": OrganizationType.MUNICIPAL_DIRECTORATE,
        "school": OrganizationType.UNIT,
        "unit": OrganizationType.UNIT,
    }
    return Organization(
        id=data["id"],
        name=data["name"],
        org_type=type_map.get(org_type, OrganizationType.UNIT),
        module=data.get("module", "educacao"),
        parent_id=data.get("parent_id"),
        province_id=data.get("province_id"),
        province_name=data.get("province_name"),
        municipality_id=data.get("municipality_id"),
        municipality_name=data.get("municipality_name"),
        unit_id=data.get("unit_id"),
        unit_name=data.get("unit_name"),
        code=data.get("code"),
    )


def seed_mined_organization() -> OrganizationTree:
    """Load MINED hierarchy from YAML and register in OrganizationTree."""
    global _SEEDED_TREE

    raw = _load_yaml()
    tree = OrganizationTree()

    for key, data in raw.items():
        org = _build_org(key, data)
        tree.register(org)

    _SEEDED_TREE = tree
    return tree


def get_mined_tree() -> OrganizationTree | None:
    """Return the seeded tree, or None if not seeded."""
    return _SEEDED_TREE
