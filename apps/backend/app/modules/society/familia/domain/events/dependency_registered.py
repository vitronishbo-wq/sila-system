from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyRegisteredEvent:
    payload: dict
    event_name: str = "DependencyRegistered"

    def to_payload(self) -> dict:
        return self.payload
