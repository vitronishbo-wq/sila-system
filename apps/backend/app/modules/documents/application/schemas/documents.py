from enum import StrEnum

from pydantic import BaseModel


class DocumentStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"


class DocumentCreate(BaseModel):
    title: str
    description: str | None = None
