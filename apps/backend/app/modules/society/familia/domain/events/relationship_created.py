from dataclasses import dataclass


@dataclass(frozen=True)
class RelationshipCreatedEvent:
    payload: dict
    event_name: str = "RelationshipCreated"

    def to_payload(self) -> dict:
        return self.payload
