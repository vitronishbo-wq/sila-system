from enum import Enum

from pydantic import BaseModel


class DocumentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"


class DocumentCreate(BaseModel):
    title: str
    description: str | None = None
