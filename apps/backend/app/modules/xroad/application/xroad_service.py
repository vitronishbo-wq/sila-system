from apps.backend.app.modules.xroad.domain.envelope import SILAEnvelope
from apps.backend.app.modules.xroad.domain.audit_log import AuditEntry
from apps.backend.app.modules.xroad.infrastructure.audit_repository import ImmutableAuditRepository
import hashlib

class XRoadInterconnect:

    def __init__(self):
        self.audit_repo = ImmutableAuditRepository()

    async def exchange(self, envelope: SILAEnvelope) -> dict:
        p_hash = hashlib.sha256(str(envelope.payload).encode()).hexdigest()
        entry = AuditEntry(message_id=envelope.message_id, origin=envelope.sender_service, destination=envelope.receiver_service, payload_hash=p_hash, previous_hash=self.audit_repo.get_last_hash())
        self.audit_repo.append(entry)
        return {'status': 'delivered', 'audit_trail_hash': entry.compute_hash(), 'chain_link': entry.previous_hash}