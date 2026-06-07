"""Search foundation utilities for PostgreSQL full-text search.

This package is designed to provide a PostgreSQL first search engine that can
later be extended with an OpenSearch backend without changing application
search semantics.
"""

from .engine import SearchEngine, SearchQuery, SearchResult
from .filters import SearchFilterBuilder
from .indexer import PostgresSearchIndexer
from .queries import SearchQueryBuilder
from .ranking import SearchRanking

__all__ = [
    "SearchEngine",
    "SearchQuery",
    "SearchResult",
    "SearchQueryBuilder",
    "SearchFilterBuilder",
    "PostgresSearchIndexer",
    "SearchRanking",
]
