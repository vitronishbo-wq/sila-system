"""Helpers to build search queries and translate request params to filters."""
from __future__ import annotations

from typing import Dict, Any


def build_filters_from_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Map HTTP query params to projection filters.

    Only a small, safe subset is allowed here to avoid complex SQL
    generation at this stage.
    """
    allowed = {
        "city": "city",
        "district": "district",
        "grade": "available_slots",
        "monthly_fee": "monthly_fee",
        "type": "type",
        "turno": "shift",
    }
    filters: Dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        mapped = allowed.get(k)
        if mapped:
            filters[mapped] = v
    return filters

from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import select
from sqlalchemy.sql import Select

from .filters import SearchFilterBuilder
from .indexer import PostgresSearchIndexer
from .ranking import SearchRanking


@dataclass
class SearchQuery:
    text: str | None = None
    filters: dict[Any, Any] = field(default_factory=dict)
    page: int = 1
    page_size: int = 25
    sort_by: str | None = None
    sort_order: str = "desc"
    language: str = "simple"


class SearchQueryBuilder:
    """Build search statements and apply pagination / sorting rules."""

    def __init__(self, indexer: PostgresSearchIndexer, ranking: SearchRanking):
        self._indexer = indexer
        self._ranking = ranking

    def build_search_statement(
        self,
        model: Any,
        query: SearchQuery,
        search_fields: list[Any],
        filters: dict[Any, Any] | None = None,
    ) -> Select:
        statement = select(model)

        if query.text and search_fields:
            vector = self._indexer.build_search_vector(search_fields)
            search_condition = self._indexer.build_search_condition(query.text, vector)
            statement = statement.where(search_condition)
            statement = statement.order_by(self._ranking.rank_expression(query.text, vector).desc())

            if query.sort_by and hasattr(model, query.sort_by):
                sort_attr = getattr(model, query.sort_by)
                order_method = sort_attr.asc if query.sort_order == "asc" else sort_attr.desc
                statement = statement.order_by(order_method())
        elif query.sort_by and hasattr(model, query.sort_by):
            sort_attr = getattr(model, query.sort_by)
            order_method = sort_attr.asc if query.sort_order == "asc" else sort_attr.desc
            statement = statement.order_by(order_method())

        combined_filters = query.filters.copy() if query.filters else {}
        if filters:
            combined_filters.update(filters)

        filter_clause = SearchFilterBuilder.build(combined_filters)
        if filter_clause is not None:
            statement = statement.where(filter_clause)

        offset = max(0, query.page - 1) * max(1, query.page_size)
        statement = statement.offset(offset).limit(max(1, query.page_size))

        return statement
