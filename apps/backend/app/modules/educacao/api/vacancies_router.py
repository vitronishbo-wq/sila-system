from __future__ import annotations

from fastapi import APIRouter, Query

from apps.backend.app.modules.educacao.api.schemas.vacancy_schema import VacancyResponse
from domain.vacancy_marketplace import VacancyMarketplace

router = APIRouter(prefix="/vacancies", tags=["Educacao - Vacancies"])


@router.get(
    "/",
    response_model=list[VacancyResponse],
    summary="List School Vacancies",
    description="""
    Retrieve available vacancies across institutions, grades, and academic years.
    
    This endpoint queries the real Vacancy Marketplace which is backed by 
    the InstitutionCapacityModel and provides accurate, database-driven 
    availability information.
    
    **Response Fields:**
    - `institution`: Institution identifier (UUID as string)
    - `grade`: Grade/class name (e.g., "9", "5A")
    - `available_slots`: Number of open positions for enrollment
    
    **Examples:**
    - `GET /api/v1/educacao/vacancies/` → All vacancies
    - `GET /api/v1/educacao/vacancies/?institution_id=school-123` → For specific institution
    - `GET /api/v1/educacao/vacancies/?class_name=9` → For specific grade
    - `GET /api/v1/educacao/vacancies/?institution_id=school-123&class_name=9` → Combined filter
    """,
)
def listar_vacancies(
    institution_id: str | None = Query(
        None,
        alias="institution_id",
        description="Filter by institution ID (UUID)",
        examples=["school-123"],
    ),
    class_name: str | None = Query(
        None,
        alias="class_name",
        description="Filter by grade/class name (e.g., '9', '5A')",
        examples=["9", "5A"],
    ),
    academic_year: str | None = Query(
        None,
        alias="academic_year",
        description="Filter by academic year (e.g., '2026')",
        examples=["2026"],
    ),
):
    """
    Get available school vacancies from the marketplace.
    
    Returns real capacity data from the database, not hardcoded samples.
    """
    marketplace = VacancyMarketplace()
    return marketplace.list_vacancies(
        {
            "institution_id": institution_id,
            "class_name": class_name,
            "academic_year": academic_year,
        }
    )
