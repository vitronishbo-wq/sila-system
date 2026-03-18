"""Identity command handlers."""
import uuid
from apps.backend.app.modules.identity.application.commands.identity_commands import CreateIdentityCommand, UpdateTrustScoreCommand, PublishIdentityEventCommand
from apps.backend.app.modules.identity.domain.models.identity import Identity
from apps.backend.app.modules.identity.domain.models.trust_score import TrustScore
from apps.backend.app.modules.identity.domain.models.enums import IdentityStatus
from apps.backend.app.modules.identity.domain.ports.aggregate_repository_port import AggregateRepositoryPort
from apps.backend.app.modules.identity.domain.ports.event_publisher_port import EventPublisherPort

class CreateIdentityHandler:

    def __init__(self, repo: AggregateRepositoryPort, publisher: EventPublisherPort):
        self.repo = repo
        self.publisher = publisher

    async def handle(self, command: CreateIdentityCommand) -> Identity:
        identity = Identity(id=str(uuid.uuid4()), citizen_id=command.citizen_id, document_id=command.document_id, full_name=command.full_name, status=IdentityStatus.PENDING, metadata=command.metadata or {})
        saved = await self.repo.save(identity)
        await self.publisher.publish('identity.created', {'identity_id': saved.id, 'citizen_id': saved.citizen_id})
        return saved

class UpdateTrustScoreHandler:

    def __init__(self, repo: AggregateRepositoryPort, publisher: EventPublisherPort):
        self.repo = repo
        self.publisher = publisher

    async def handle(self, command: UpdateTrustScoreCommand) -> TrustScore:
        trust_score = await self.repo.get_by_citizen(command.citizen_id) or TrustScore(id=str(uuid.uuid4()), citizen_id=command.citizen_id, score=0.0)
        audit_data = trust_score.update_score(command.new_score, command.metadata.get('reason', '') if command.metadata else '')
        saved = await self.repo.save(trust_score)
        await self.publisher.publish('trust_score.updated', audit_data)
        return saved

class PublishIdentityEventHandler:

    def __init__(self, publisher: EventPublisherPort):
        self.publisher = publisher

    async def handle(self, command: PublishIdentityEventCommand) -> dict:
        event_data = command.metadata or {}
        await self.publisher.publish(command.event_type, event_data)
        return {'event_published': True, 'event_type': command.event_type}