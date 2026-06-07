from __future__ import annotations

from typing import Optional

from sila_platform.governance.organization.models import Organization, OrganizationTree, OrganizationType
from .seed import seed_mined_organization


class MINEDOrganizationService:
    """Service for querying the MINED organizational hierarchy."""

    def __init__(self) -> None:
        self._tree: OrganizationTree = seed_mined_organization()

    def get_tree(self) -> OrganizationTree:
        return self._tree

    def get_ministry(self) -> Optional[Organization]:
        roots = self._tree.get_roots()
        return roots[0] if roots else None

    def get_provincial_directorates(self) -> list[Organization]:
        return self._tree.get_by_type(OrganizationType.PROVINCIAL_DIRECTORATE)

    def get_municipal_directorates(self) -> list[Organization]:
        return self._tree.get_by_type(OrganizationType.MUNICIPAL_DIRECTORATE)

    def get_schools(self) -> list[Organization]:
        return self._tree.get_by_type(OrganizationType.UNIT)

    def get_by_province(self, province_id: str) -> list[Organization]:
        """Return all orgs (DMEs + schools) in a given province."""
        return [o for o in self._tree._orgs.values()
                if o.province_id == province_id]

    def get_by_municipality(self, municipality_id: str) -> list[Organization]:
        """Return all orgs (schools) in a given municipality."""
        return [o for o in self._tree._orgs.values()
                if o.municipality_id == municipality_id]

    def get_schools_by_municipality(self, municipality_id: str) -> list[Organization]:
        return [o for o in self._tree._orgs.values()
                if o.municipality_id == municipality_id
                and o.org_type == OrganizationType.UNIT]

    def get_children(self, org_id: str) -> list[Organization]:
        org = self._tree.get(org_id)
        return org.children if org else []

    def get_ancestors(self, org_id: str) -> list[Organization]:
        return self._tree.get_ancestors(org_id)

    def get_descendants(self, org_id: str) -> list[Organization]:
        return self._tree.get_descendants(org_id)

    def get_school(self, school_id: str) -> Optional[Organization]:
        return self._tree.get(school_id)

    def get_dme(self, dme_id: str) -> Optional[Organization]:
        return self._tree.get(dme_id)

    def get_dpe(self, dpe_id: str) -> Optional[Organization]:
        return self._tree.get(dpe_id)

    def to_tree_dict(self, org_id: Optional[str] = None) -> list[dict]:
        return self._tree.to_tree_dict(org_id)

    def count(self) -> int:
        return self._tree.count()

    def list_all(self) -> list[Organization]:
        return list(self._tree._orgs.values())
