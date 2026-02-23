import os
from config import settings

# Forçar ambiente de teste
settings.ENVIRONMENT = "test"
settings.DATABASE_URL = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_test"
settings.ASYNC_DATABASE_URL = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_test"
settings.PRISMA_DATABASE_URL = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_test"
settings.DATABASE_POOL_SIZE = 5
settings.DATABASE_MAX_OVERFLOW = 10
settings.DATABASE_POOL_TIMEOUT = 30
settings.DATABASE_POOL_RECYCLE = 1800
settings.DATABASE_ECHO = False
settings.TESTING = True


class TestSettings(settings.__class__):
    """Configurações específicas para execução de testes de integração."""

    ENVIRONMENT: str = "test"
    DATABASE_URL: str = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_test"
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_test"
    PRISMA_DATABASE_URL: str = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_test"

    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800
    DATABASE_ECHO: bool = False

    RATE_LIMIT_ENABLED: bool = False
    SEND_EMAILS: bool = False
    testing: bool = True
    SECURE_COOKIES: bool = False
    SECURE_HEADERS: bool = False

    class Config:
        env_file = ".env.test"
        extra = "allow"


test_settings = TestSettings()


def test_testing_flag_is_true():
    """Valida se a flag de teste está ativa nas configurações de teste."""
    assert (
        test_settings.testing is True
    ), "Expected `testing` to be True in test settings"


def test_db_url_is_test_db():
    """Garante que os testes não rodam no banco de dados de produção ou dev."""
    assert "sila_test" in test_settings.DATABASE_URL
