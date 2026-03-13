from dataclasses import dataclass

@dataclass(frozen=True)
class AgeRange:
    min_age: int
    max_age: int | None = None

    def contains(self, age: int) -> bool:
        if age < self.min_age:
            return False
        if self.max_age is not None and age > self.max_age:
            return False
        return True