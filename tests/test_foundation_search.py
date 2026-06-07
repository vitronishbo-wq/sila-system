from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.dialects import postgresql

from foundation.search import (
    PostgresSearchIndexer,
    SearchEngine,
    SearchFilterBuilder,
    SearchQuery,
    SearchQueryBuilder,
    SearchRanking,
)

metadata = MetaData()
document = Table(
    "documents",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("body", String),
    Column("status", String),
)


def test_postgres_search_indexer_builds_search_vector():
    indexer = PostgresSearchIndexer(language="simple")
    vector = indexer.build_search_vector([document.c.title, document.c.body])
    compiled = str(vector.compile(dialect=postgresql.dialect()))

    assert "to_tsvector(" in compiled
    assert "concat_ws(" in compiled


def test_search_filter_builder_builds_exact_and_range_clauses():
    clause = SearchFilterBuilder.build(
        {
            document.c.status: "ACTIVE",
            document.c.id: {"gte": 10, "lte": 100},
            document.c.title: {"in": ["A", "B"]},
        }
    )
    compiled = str(clause.compile(dialect=postgresql.dialect()))

    assert "documents.status" in compiled
    assert ">=" in compiled
    assert "<=" in compiled
    assert "IN" in compiled


def test_search_query_builder_constructs_full_text_search_statement():
    indexer = PostgresSearchIndexer()
    ranking = SearchRanking(language=indexer.language)
    builder = SearchQueryBuilder(indexer, ranking)
    query = SearchQuery(text="student transfer", filters={document.c.status: "ACTIVE"}, page=2, page_size=10)

    statement = builder.build_search_statement(document, query, [document.c.title, document.c.body])
    compiled = str(statement.compile(dialect=postgresql.dialect()))

    compiled = compiled.replace(' ', '')
    assert "@@" in compiled
    assert "plainto_tsquery(" in compiled
    assert "ts_rank_cd" in compiled
    assert "LIMIT" in compiled.upper()
    assert "OFFSET" in compiled.upper()
    assert "documents.status" in compiled


@pytest.mark.asyncio
async def test_search_engine_executes_search_statement():
    session = AsyncMock()
    fake_result = Mock()
    fake_result.scalars.return_value.all.return_value = ["result-item"]
    session.execute = AsyncMock(return_value=fake_result)

    engine = SearchEngine()
    query = SearchQuery(text="search phrase", page=1, page_size=5)
    result = await engine.search(session, document, query, [document.c.title, document.c.body])

    session.execute.assert_awaited_once()
    assert result.items == ["result-item"]
    assert result.page == 1
    assert result.page_size == 5
