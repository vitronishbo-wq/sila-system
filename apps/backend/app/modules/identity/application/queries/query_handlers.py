"""Identity query handlers."""

from apps.backend.app.modules.identity.application.queries.identity_queries import (
    GetIdentityByCitizenQuery,
    GetTrustScoreQuery,
    ListIdentitiesQuery,
)
from apps.backend.app.modules.identity.domain.ports.aggregate_repository_port import (
    AggregateRepositoryPort,
)


class GetIdentityByCitizenHandler:
    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, query: GetIdentityByCitizenQuery):
        return await self.repo.get_by_citizen(query.citizen_id)


class GetTrustScoreHandler:
    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, query: GetTrustScoreQuery):
        return await self.repo.get_trust_score(query.citizen_id)


class ListIdentitiesHandler:
    def __init__(self, repo: AggregateRepositoryPort):
        self.repo = repo

    async def handle(self, query: ListIdentitiesQuery) -> list:
        return await self.repo.list_all(limit=query.limit, offset=query.offset)
