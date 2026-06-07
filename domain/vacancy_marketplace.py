from typing import Any

from foundation.persistence import EducacaoRepository, InfrastructureUnavailableError


class VacancyMarketplace:
    """Vacancy marketplace backed by institutional capacity."""

    def __init__(self, repository: EducacaoRepository | None = None):
        self.repository = repository or EducacaoRepository()

    def list_vacancies(self, filters: dict[str, Any] = None) -> list[dict[str, Any]]:
        try:
            return self.repository.list_vacancies_sync(
                institution_id=filters.get("institution_id") if filters else None,
                class_name=filters.get("class_name") if filters else None,
                academic_year=filters.get("academic_year") if filters else None,
            )
        except InfrastructureUnavailableError:
            return []
        except Exception:
            return []

    def get_available_for(self, institution_id: str, class_name: str, academic_year: str = "2026") -> int:
        try:
            return self.repository.get_available_capacity_sync(institution_id, class_name, academic_year)
        except InfrastructureUnavailableError:
            return 0
        except Exception:
            return 0
