"""Indexing utilities for the marketplace projection.

This provides a minimal upsert-based indexer that writes into the
`institution_marketplace_projection` read-model. In the future it can be
extended to support batch updates and full-text tsvector maintenance.
"""
from __future__ import annotations

from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from apps.backend.app.modules.educacao.infrastructure.models.marketplace_projection_model import (
        InstitutionMarketplaceProjection,
    )
except Exception:
    InstitutionMarketplaceProjection = None


class Indexer:
    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    async def index_institution(self, payload: Dict[str, Any]):
        """Upsert a single institution projection row."""
        if self.db is None or InstitutionMarketplaceProjection is None:
            return None
        # Basic upsert: try to find by institution_id, otherwise insert
        stmt = await self.db.execute(
            InstitutionMarketplaceProjection.__table__.select().where(
                InstitutionMarketplaceProjection.institution_id == payload.get("institution_id")
            )
        )
        row = stmt.first()
        if row:
            # update
            await self.db.execute(
                InstitutionMarketplaceProjection.__table__.update()
                .where(InstitutionMarketplaceProjection.institution_id == payload.get("institution_id"))
                .values(**payload)
            )
        else:
            await self.db.execute(InstitutionMarketplaceProjection.__table__.insert().values(**payload))
        await self.db.commit()
        return True

from typing import Any

from sqlalchemy import String, cast, func
from sqlalchemy.sql.elements import ColumnElement


class PostgresSearchIndexer:
    """PostgreSQL-specific search index helpers using tsvector and tsquery."""

    def __init__(self, language: str = "simple"):
        self.language = language

    def build_search_vector(self, columns: list[ColumnElement]) -> ColumnElement:
        normalized_columns = [func.coalesce(cast(column, String), "") for column in columns]
        return func.to_tsvector(self.language, func.concat_ws(" ", *normalized_columns))

    def build_search_condition(self, query_text: str, vector: ColumnElement) -> ColumnElement:
        return vector.match(func.plainto_tsquery(self.language, query_text))

    def build_rank_expression(self, query_text: str, vector: ColumnElement) -> ColumnElement:
        return func.ts_rank_cd(vector, func.plainto_tsquery(self.language, query_text), 32)

    def build_refresh_statement(self, model: Any, columns: list[ColumnElement], target_column: ColumnElement) -> Any:
        return model.__table__.update().values({target_column: self.build_search_vector(columns)})
