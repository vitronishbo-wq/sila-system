"""
Shared database connection utilities for SILA system seeders and tests.
Consolidates common database connection logic across multiple scripts.
"""

import logging
import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration manager - consolidates env var handling."""

    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
        driver: str = "asyncpg",
    ):
        """
        Initialize database config with fallback to environment variables.

        Args:
            user: PostgreSQL user (fallback: POSTGRES_USER env var)
            password: PostgreSQL password (fallback: POSTGRES_PASSWORD env var)
            host: PostgreSQL host (fallback: POSTGRES_HOST env var)
            port: PostgreSQL port (fallback: POSTGRES_PORT env var)
            database: PostgreSQL database (fallback: POSTGRES_DB env var)
            driver: Async driver for SQLAlchemy (default: asyncpg)
        """
        self.user = user or os.getenv("POSTGRES_USER", "sila_user")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "Trumanmarcelo_1983")
        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = port or int(os.getenv("POSTGRES_PORT", "5432"))
        self.database = database or os.getenv("POSTGRES_DB", "sila_db")
        self.driver = driver

    @property
    def url(self) -> str:
        """Generate SQLAlchemy async database URL."""
        return f"postgresql+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def __repr__(self) -> str:
        return f"DatabaseConfig(user={self.user}, host={self.host}:{self.port}, db={self.database})"


class DatabaseConnector:
    """Unified database connector for SILA seeders and tests."""

    def __init__(self, config: DatabaseConfig | None = None, echo: bool = False):
        """
        Initialize database connector.

        Args:
            config: DatabaseConfig instance (if None, creates default)
            echo: Enable SQLAlchemy echo mode for debugging
        """
        self.config = config or DatabaseConfig()
        self.echo = echo
        self.engine: AsyncEngine | None = None
        self._session_factory = None
        logger.info(f"DatabaseConnector initialized: {self.config}")

    async def connect(self) -> AsyncEngine:
        """Create and store async engine."""
        if self.engine is None:
            self.engine = create_async_engine(
                self.config.url, echo=self.echo, pool_pre_ping=True, pool_size=10
            )
            self._session_factory = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            logger.info(
                f"Database connection established: {self.config.host}:{self.config.port}/{self.config.database}"
            )
        return self.engine

    async def disconnect(self):
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self._session_factory = None
            logger.info("Database connection closed")

    def get_session_factory(self):
        """Get SQLAlchemy session factory."""
        if self._session_factory is None:
            raise RuntimeError("ConnectionPool not initialized. Call connect() first.")
        return self._session_factory

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


# Singleton instance for convenience
_default_connector: DatabaseConnector | None = None


def get_default_connector(reset: bool = False) -> DatabaseConnector:
    """
    Get or create default database connector (singleton pattern).

    Args:
        reset: If True, creates a new connector instance

    Returns:
        DatabaseConnector instance
    """
    global _default_connector
    if _default_connector is None or reset:
        _default_connector = DatabaseConnector()
    return _default_connector
