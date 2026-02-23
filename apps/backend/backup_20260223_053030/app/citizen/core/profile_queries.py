"""
Re-export module — canonical import path for ProfileQueries.
Actual implementation lives in queries.py.
"""
from app.citizen.core.queries import ProfileQueries

__all__ = ["ProfileQueries"]
