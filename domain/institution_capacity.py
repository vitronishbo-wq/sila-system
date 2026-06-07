from dataclasses import dataclass


@dataclass
class InstitutionCapacity:
    institution_id: str
    total_vacancies: int
    occupied: int = 0

    @property
    def available(self) -> int:
        return max(0, self.total_vacancies - self.occupied)
