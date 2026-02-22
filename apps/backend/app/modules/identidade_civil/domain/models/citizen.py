from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Any, Dict, Optional


@dataclass
class Citizen:
    citizen_id: Any
    full_name: str
    document_number: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    vital_status: str = "alive"
    fuc_sync_timestamp: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # --- Additional convenience properties ----------------------------------
    @property
    def document_number_safe(self) -> Optional[str]:
        """Backward-compatible accessor for document number.

        Some code paths expect a property accessor; keep this alias to avoid
        breaking call sites while keeping the dataclass field as source of truth.
        """
        return self.document_number

    @property
    def age(self) -> Optional[int]:
        """Return age in years calculated from `birth_date`, or None if unknown."""
        if not self.birth_date:
            return None
        today = date.today()
        try:
            years = today.year - self.birth_date.year
            # subtract one if birthday hasn't occurred yet this year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                years -= 1
            return years
        except Exception:
            return None

    # --- Representation & equality -------------------------------------------------
    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Citizen(id={self.citizen_id}, name={self.full_name})"

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<Citizen(id={self.citizen_id}, full_name={self.full_name})>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Citizen):
            return False
        return str(self.citizen_id) == str(other.citizen_id)

    # --- Domain helpers ------------------------------------------------------------
    @property
    def document_number_prop(self) -> Optional[str]:
        return self.document_number

    @property
    def is_alive(self) -> bool:  # convenience property
        return self.vital_status == "alive"

    def is_active(self) -> bool:
        return self.vital_status == "alive"

    def activate(self) -> None:
        self.vital_status = "alive"
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.vital_status = "inactive"
        self.updated_at = datetime.utcnow()

    def mark_deceased(self) -> None:
        self.vital_status = "deceased"
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "citizen_id": str(self.citizen_id),
            "full_name": self.full_name,
            "document_number": self.document_number,
            "birth_date": self.birth_date.isoformat() if isinstance(self.birth_date, date) else None,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "vital_status": self.vital_status,
            "fuc_sync_timestamp": self.fuc_sync_timestamp.isoformat() if isinstance(self.fuc_sync_timestamp, datetime) else None,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else None,
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else None,
        }

    # --- Factories / converters ---------------------------------------------------
    @classmethod
    def from_fuc_projection(cls, data: Dict[str, Any]) -> "Citizen":
        # Required fields: id and full_name
        citizen_id = data.get("id")
        full_name = data.get("full_name")
        if citizen_id is None or full_name is None:
            raise TypeError("`id` and `full_name` are required in FUC projection")

        # Optional conversions
        doc = data.get("document_number")
        birth = data.get("birth_date")
        if isinstance(birth, str):
            try:
                birth = date.fromisoformat(birth)
            except Exception:
                birth = None

        gender = data.get("gender")
        phone = data.get("phone")
        email = data.get("email")
        vital = data.get("vital_status") or "alive"

        citizen = cls(
            citizen_id=citizen_id,
            full_name=full_name,
            document_number=doc,
            birth_date=birth,
            gender=gender,
            phone=phone,
            email=email,
            vital_status=vital,
            fuc_sync_timestamp=datetime.utcnow(),
        )
        return citizen
