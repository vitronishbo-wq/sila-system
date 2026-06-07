import os
from unittest.mock import Mock

os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379")

from domain.vacancy_marketplace import VacancyMarketplace
from foundation.persistence import InfrastructureUnavailableError


def test_get_available_for_uses_real_capacity_and_falls_back_to_zero_on_failure() -> None:
    repo = Mock()
    repo.get_available_capacity_sync.return_value = 7
    marketplace = VacancyMarketplace(repository=repo)

    available = marketplace.get_available_for("school-123", "9", "2026")

    repo.get_available_capacity_sync.assert_called_once_with("school-123", "9", "2026")
    assert available == 7

    repo.get_available_capacity_sync.reset_mock()
    repo.get_available_capacity_sync.side_effect = InfrastructureUnavailableError()

    assert marketplace.get_available_for("school-123", "9", "2026") == 0
    repo.get_available_capacity_sync.assert_called_once()


def test_list_vacancies_queries_real_capacity_repository() -> None:
    repo = Mock()
    repo.list_vacancies_sync.return_value = [
        {"institution": "school-123", "grade": "9", "available_slots": 5}
    ]
    marketplace = VacancyMarketplace(repository=repo)

    vacancies = marketplace.list_vacancies({"institution_id": "school-123", "class_name": "9"})

    repo.list_vacancies_sync.assert_called_once_with(
        institution_id="school-123",
        class_name="9",
        academic_year=None,
    )
    assert vacancies == [{"institution": "school-123", "grade": "9", "available_slots": 5}]
