from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class DocumentStatus(str, Enum):
    PENDING = "pending"
    EXCHANGED = "exchanged"
    VERIFIED = "verified"
    REJECTED = "rejected"


class DocumentVisibility(str, Enum):
    ORIGIN_ONLY = "origin_only"
    MODULE_ONLY = "module_only"
    CROSS_MODULE = "cross_module"
    PUBLIC = "public"


@dataclass
class DocumentExchange:
    """Documento partilhado entre módulos com controlo de visibilidade."""
    id: str
    document_type: str
    source_module: str
    target_module: str
    citizen_id: str
    reference: str
    visibility: DocumentVisibility = DocumentVisibility.CROSS_MODULE
    status: DocumentStatus = DocumentStatus.PENDING
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    exchanged_at: Optional[datetime] = None


class DocumentExchangeManager:
    """Gestor de troca de documentos entre módulos."""

    def __init__(self) -> None:
        self._documents: dict[str, DocumentExchange] = {}

    def share(self, doc_type: str, source: str, target: str, citizen: str,
              reference: str, visibility: DocumentVisibility = DocumentVisibility.CROSS_MODULE,
              metadata: Optional[dict] = None) -> DocumentExchange:
        doc = DocumentExchange(
            id=f"{source}-{target}-{reference}-{datetime.now(timezone.utc).timestamp()}",
            document_type=doc_type, source_module=source,
            target_module=target, citizen_id=citizen,
            reference=reference, visibility=visibility,
            metadata=metadata or {},
        )
        self._documents[doc.id] = doc
        return doc

    def confirm(self, doc_id: str) -> Optional[DocumentExchange]:
        doc = self._documents.get(doc_id)
        if doc and doc.status == DocumentStatus.PENDING:
            doc.status = DocumentStatus.EXCHANGED
            doc.exchanged_at = datetime.now(timezone.utc)
        return doc

    def verify(self, doc_id: str) -> Optional[DocumentExchange]:
        doc = self._documents.get(doc_id)
        if doc and doc.status == DocumentStatus.EXCHANGED:
            doc.status = DocumentStatus.VERIFIED
        return doc

    def get(self, doc_id: str) -> Optional[DocumentExchange]:
        return self._documents.get(doc_id)

    def list_by_citizen(self, citizen_id: str) -> list[DocumentExchange]:
        return [d for d in self._documents.values() if d.citizen_id == citizen_id]

    def list_by_module(self, module: str) -> list[DocumentExchange]:
        return [d for d in self._documents.values()
                if d.source_module == module or d.target_module == module]
