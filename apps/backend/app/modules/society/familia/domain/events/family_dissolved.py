from dataclasses import dataclass


@dataclass(frozen=True)
class FamilyDissolvedEvent:
    payload: dict
    event_name: str = "FamilyDissolved"

    def to_payload(self) -> dict:
        return self.payload
