"""Health check for Matching Engine"""

from __future__ import annotations


class MatchingEngineHealth:
    """Health check for matching engine"""

    @staticmethod
    async def check() -> dict[str, str]:
        """
        Check health of matching engine.

        Returns:
            Health status dictionary
        """
        return {
            "component": "matching-engine",
            "status": "healthy",
            "version": "0.1.0",
            "subcomponents": [
                "scorer",
                "compatibility",
                "ranking",
                "recommendation",
            ],
        }


async def matching_health() -> dict[str, str]:
    """Health check endpoint for matching engine"""
    return await MatchingEngineHealth.check()
