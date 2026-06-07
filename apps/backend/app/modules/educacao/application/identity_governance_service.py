from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.events.outbox.outbox_repository import OutboxRepository


class IdentityGovernanceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.outbox = OutboxRepository(session)

    async def emit_audit_event(
        self,
        event_type: str,
        entity_id: str,
        actor_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        payload = {
            "event_type": event_type,
            "entity_type": "academic_identity",
            "entity_id": entity_id,
            "actor_id": actor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        await self.outbox.save(
            event_name=f"audit.{event_type}",
            event_id=str(uuid.uuid4()),
            payload=payload,
        )

    async def emit_service_request_event(
        self,
        event_type: str,
        identity_id: str,
        description: str,
        metadata: dict[str, Any] | None = None,
    ):
        payload = {
            "event_type": event_type,
            "identity_id": identity_id,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        await self.outbox.save(
            event_name=f"service_request.{event_type}",
            event_id=str(uuid.uuid4()),
            payload=payload,
        )

    async def emit_timeline_event(
        self,
        event_type: str,
        identity_id: str,
        description: str,
        metadata: dict[str, Any] | None = None,
    ):
        payload = {
            "event_type": event_type,
            "identity_id": identity_id,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        await self.outbox.save(
            event_name=f"timeline.{event_type}",
            event_id=str(uuid.uuid4()),
            payload=payload,
        )

    async def emit_identity_event(
        self,
        domain_event: str,
        identity_id: str,
        payload_data: dict[str, Any],
    ):
        payload = {
            "domain_event": domain_event,
            "identity_id": identity_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload_data,
        }
        await self.outbox.save(
            event_name=domain_event,
            event_id=str(uuid.uuid4()),
            payload=payload,
        )

    async def governance_on_identity_created(
        self,
        identity_id: str,
        full_name: str,
        national_student_number: str,
        actor_id: str | None = None,
    ):
        meta = {"full_name": full_name, "national_student_number": national_student_number}
        await self.emit_audit_event("identity_created", identity_id, actor_id, meta)
        await self.emit_service_request_event(
            "identity_created", identity_id,
            f"Academic identity created for {full_name} (ENS: {national_student_number})",
            meta,
        )
        await self.emit_timeline_event(
            "identity_created", identity_id,
            f"Identity created: {full_name}",
            meta,
        )
        await self.emit_identity_event(
            "identity_created", identity_id, meta,
        )

    async def governance_on_identity_resolved(
        self,
        identity_id: str,
        match_type: str,
        confidence: str,
        search_criteria: dict[str, Any],
        actor_id: str | None = None,
    ):
        meta = {"match_type": match_type, "confidence": confidence, "search_criteria": search_criteria}
        await self.emit_audit_event("identity_resolved", identity_id, actor_id, meta)
        await self.emit_timeline_event(
            "identity_resolved", identity_id,
            f"Identity resolved via {match_type} ({confidence})",
            meta,
        )

    async def governance_on_duplicate_detected(
        self,
        identity_id: str,
        duplicate_of: str,
        match_type: str,
        confidence: str,
        fields: list[str],
    ):
        meta = {"duplicate_of": duplicate_of, "match_type": match_type, "confidence": confidence, "fields": fields}
        await self.emit_audit_event("duplicate_detected", identity_id, None, meta)
        await self.emit_timeline_event(
            "duplicate_detected", identity_id,
            f"Duplicate detected: {match_type} ({confidence})",
            meta,
        )
        await self.emit_identity_event(
            "identity_duplicate_detected", identity_id, meta,
        )

    async def governance_on_merge_requested(
        self,
        merge_id: str,
        primary_id: str,
        duplicate_id: str,
        confidence: str,
        reason: str,
        requested_by: str | None = None,
    ):
        meta = {"merge_id": merge_id, "primary_id": primary_id, "duplicate_id": duplicate_id,
                "confidence": confidence, "reason": reason}
        await self.emit_audit_event("merge_requested", primary_id, requested_by, meta)
        await self.emit_service_request_event(
            "merge_requested", primary_id,
            f"Merge requested: {duplicate_id} into {primary_id}",
            meta,
        )
        await self.emit_timeline_event(
            "merge_requested", primary_id,
            f"Merge requested ({confidence} confidence)",
            meta,
        )
        await self.emit_identity_event(
            "identity_merge_requested", primary_id, meta,
        )

    async def governance_on_merge_executed(
        self,
        merge_id: str,
        primary_id: str,
        duplicate_id: str,
        merged_fields: list[str],
        resolved_by: str | None = None,
    ):
        meta = {"merge_id": merge_id, "primary_id": primary_id, "duplicate_id": duplicate_id,
                "merged_fields": merged_fields}
        await self.emit_audit_event("merge_executed", primary_id, resolved_by, meta)
        await self.emit_service_request_event(
            "merge_executed", primary_id,
            f"Merge executed: {duplicate_id} merged into {primary_id}",
            meta,
        )
        await self.emit_timeline_event(
            "merge_executed", primary_id,
            f"Merge completed: {len(merged_fields)} fields merged",
            meta,
        )
        await self.emit_identity_event(
            "identity_merged", primary_id, meta,
        )
