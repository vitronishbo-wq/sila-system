"""Search engine orchestration for PostgreSQL full-text search."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from .indexer import PostgresSearchIndexer
from .queries import SearchQuery, SearchQueryBuilder
from .ranking import SearchRanking


@dataclass
class SearchResult:
    items: list[Any]
    page: int
    page_size: int
    total: int | None = None


class SearchEngine:
    """Search engine orchestration for PostgreSQL full-text search."""

    def __init__(
        self,
        indexer: PostgresSearchIndexer | None = None,
        ranking: SearchRanking | None = None,
    ):
        self.indexer = indexer or PostgresSearchIndexer()
        self.ranking = ranking or SearchRanking(language=self.indexer.language)
        self.builder = SearchQueryBuilder(self.indexer, self.ranking)

    async def search(
        self,
        session: AsyncSession,
        model: Any,
        query: SearchQuery,
        search_fields: list[Any],
        filters: dict[Any, Any] | None = None,
    ) -> SearchResult:
        statement = self.builder.build_search_statement(
            model=model,
            query=query,
            search_fields=search_fields,
            filters=filters,
        )
        result = await session.execute(statement)
        items = result.scalars().all()
        return SearchResult(
            items=items,
            page=query.page,
            page_size=query.page_size,
            total=None,
        )
