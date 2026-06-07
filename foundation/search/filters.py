"""Filter definitions for marketplace search (simple placeholders)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchFilters:
    city: Optional[str] = None
    district: Optional[str] = None
    min_fee: Optional[int] = None
    max_fee: Optional[int] = None
    shift: Optional[str] = None
    special_needs: Optional[bool] = None

from collections.abc import Iterable
from typing import Any

from sqlalchemy import and_, or_
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement


class SearchFilterBuilder:
    """Build SQLAlchemy filter clauses from field-based filter definitions."""

    @staticmethod
    def build(filters: dict[Any, Any]) -> ColumnElement | None:
        if not filters:
            return None

        clauses: list[BinaryExpression] = []
        for field, value in filters.items():
            if value is None:
                continue

            if isinstance(value, dict):
                if "gte" in value:
                    clauses.append(field >= value["gte"])
                if "lte" in value:
                    clauses.append(field <= value["lte"])
                if "in" in value and isinstance(value["in"], Iterable):
                    clauses.append(field.in_(value["in"]))
                if "not" in value:
                    clauses.append(field != value["not"])
                continue

            if isinstance(value, list) or isinstance(value, tuple):
                clauses.append(field.in_(value))
            else:
                clauses.append(field == value)

        if not clauses:
            return None

        return and_(*clauses)

    @staticmethod
    def any(filters: list[dict[ColumnElement, Any]]) -> ColumnElement | None:
        clauses: list[BinaryExpression] = []
        for item in filters:
            clause = SearchFilterBuilder.build(item)
            if clause is not None:
                clauses.append(clause)
        if not clauses:
            return None
        return or_(*clauses)
