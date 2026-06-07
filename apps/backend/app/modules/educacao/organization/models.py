from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from sila_platform.governance.organization.models import Organization, OrganizationType


class SchoolOrganizationType(str):
    SCHOOL = "school"


@dataclass
class MINEDOrganization(Organization):
    pass


@dataclass
class ProvincialDirectorate(MINEDOrganization):
    province_id: str = ""
    province_name: str = ""

    def __post_init__(self) -> None:
        self.org_type = OrganizationType.PROVINCIAL_DIRECTORATE


@dataclass
class MunicipalDirectorate(MINEDOrganization):
    province_id: str = ""
    province_name: str = ""
    municipality_id: str = ""
    municipality_name: str = ""

    def __post_init__(self) -> None:
        self.org_type = OrganizationType.MUNICIPAL_DIRECTORATE


@dataclass
class School(MINEDOrganization):
    province_id: str = ""
    province_name: str = ""
    municipality_id: str = ""
    municipality_name: str = ""
    unit_id: str = ""
    unit_name: str = ""

    def __post_init__(self) -> None:
        self.org_type = OrganizationType.UNIT
