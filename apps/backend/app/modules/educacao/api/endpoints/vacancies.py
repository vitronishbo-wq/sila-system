from __future__ import annotations

from fastapi import APIRouter, Query

from apps.backend.app.modules.educacao.api.schemas.vacancy_schema import VacancyResponse
from domain.vacancy_marketplace import VacancyMarketplace

router = APIRouter(prefix="/vacancies", tags=["Educacao - Vacancies"])


@router.get("/", response_model=list[VacancyResponse])
def listar_vacancies(
    institution_id: str | None = Query(None, alias="institution_id"),
    class_name: str | None = Query(None, alias="class_name"),
    academic_year: str | None = Query(None, alias="academic_year"),
):
    """List vacancies from the real Vacancy Marketplace backed by institution capacity."""
    marketplace = VacancyMarketplace()
    return marketplace.list_vacancies(
        {
            "institution_id": institution_id,
            "class_name": class_name,
            "academic_year": academic_year,
        }
    )
