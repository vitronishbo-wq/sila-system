"""Adapters package: Mock and real adapters for external systems.

This package provides simple MockAdapter scaffolding that can be replaced
by HttpAdapter/SoapAdapter/QueueAdapter implementations later.
"""

from .mock_adapter import MockAdapter

__all__ = ["MockAdapter"]
