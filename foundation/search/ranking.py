"""Basic ranking utilities for search results.

This is intentionally simple for phase 3.2: it provides a composable
scoring function that can be extended with ML models or OpenSearch scores.
"""
from __future__ import annotations

from typing import Dict, Any, List


def score_results(results: List[Dict[str, Any]], preferences: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    prefs = preferences or {}
    # Very small example: boost by available_slots and low monthly_fee
    def score(item: Dict[str, Any]) -> float:
        slots = item.get("available_slots") or 0
        fee = item.get("monthly_fee") or 0
        return float(slots) * 2.0 - float(fee) / 1000.0

    for r in results:
        r["match_score"] = score(r)
    return sorted(results, key=lambda x: x["match_score"], reverse=True)

from sqlalchemy import func
from sqlalchemy.sql.elements import ColumnElement


class SearchRanking:
    """Ranking helper for PostgreSQL full-text search results."""

    def __init__(self, language: str = "simple", normalization: int = 32):
        self.language = language
        self.normalization = normalization

    def rank_expression(self, query_text: str, vector: ColumnElement) -> ColumnElement:
        return func.ts_rank_cd(vector, func.plainto_tsquery(self.language, query_text), self.normalization)
