"""
Configuração centralizada para o SILA System
Única fonte de verdade para todas as configurações.

Uso:
    from apps.backend.app.core.settings import settings

    # Acessar propriedades
    settings.DATABASE_URL
    settings.API_BASE_URL
    settings.get_cors_origins()
"""

from typing import Any

from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL, make_url


class Settings(BaseSettings):
    """Configurações da aplicação - Single Source of Truth"""

    DATABASE_URL: str
    REDIS_URL: str
    GMX_ENV_LOADED: str = "0"
    GMX_ENV_SOURCE: str = ""

    @property
    def _parsed_database_url(self) -> URL:
        return make_url(self.DATABASE_URL)

    @property
    def _parsed_redis_url(self) -> URL:
        return make_url(self.REDIS_URL)

    @property
    def runtime_env_loaded(self) -> bool:
        return self.GMX_ENV_LOADED == "1"

    def require_runtime_bootstrap(self) -> None:
        if self.runtime_env_loaded:
            return
        raise RuntimeError(
            "Ambiente não inicializado via loader oficial (GMX_ENV_LOADED=1). "
            "Execute via ./gmx run-local, make run-local ou carregue scripts/dev/load_runtime_env.sh antes."
        )

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Alias explícito para manter compatibilidade com código legado."""
        return self.DATABASE_URL

    @property
    def DB_HOST(self) -> str:
        return self._parsed_database_url.host or ""

    @property
    def DB_PORT(self) -> int:
        return self._parsed_database_url.port or 5432

    @property
    def DB_USER(self) -> str:
        return self._parsed_database_url.username or ""

    @property
    def DB_PASSWORD(self) -> str:
        return self._parsed_database_url.password or ""

    @property
    def DB_NAME(self) -> str:
        return self._parsed_database_url.database or ""

    @property
    def REDIS_HOST(self) -> str:
        return self._parsed_redis_url.host or ""

    @property
    def REDIS_PORT(self) -> int:
        return self._parsed_redis_url.port or 6379

    @property
    def REDIS_DB(self) -> int:
        database = self._parsed_redis_url.database
        if database in (None, ""):
            return 0
        return int(str(database))

    @property
    def DB_CONNECTION_STRING(self) -> str:
        """String de conexão BD derivada da URL final."""
        return f"{self.DB_HOST}:{self.DB_PORT}"

    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_ENV: str = "development"

    @property
    def API_BASE_URL(self) -> str:
        """URL base da API"""
        return f"http://{self.API_HOST}:{self.API_PORT}"

    FUC_BASE_URL: str = "http://127.0.0.1:9000"
    MULTICAIXA_BASE_URL: str = "https://api.multicaixa.co.ao/v1"
    MULTICAIXA_API_KEY: str = ""
    MULTICAIXA_MERCHANT_ID: str = ""
    MULTICAIXA_WEBHOOK_SECRET: str = ""
    AGT_BASE_URL: str = "https://api.agt.min-fin.gov.ao/v1"
    AGT_API_KEY: str = ""
    AGT_API_SECRET: str = ""
    XROAD_BASE_URL: str = "https://xroad.mai.gov.ao/api/v1"
    XROAD_API_KEY: str = ""
    XROAD_API_SECRET: str = ""
    REGISTO_CIVIL_BASE_URL: str = "https://conservatoria.minjus.gov.ao/api/v1"
    REGISTO_CIVIL_API_KEY: str = ""
    REGISTO_CIVIL_API_SECRET: str = ""

    # Provider mode: "production" | "homologation" | "development"
    PROVIDER_MODE: str = "development"

    FRONTEND_HOST: str = "127.0.0.1"
    FRONTEND_PORT: int = 3000
    # Environment variable name used to provide comma-separated paths to exclude from metrics
    OBS_EXCLUDE_PATHS_ENV_NAME: str = "OBS_EXCLUDE_PATHS"
    # OpenTelemetry / OTLP
    OTEL_EXPORTER_OTLP_ENDPOINT: str = ""  # e.g. http://otel-collector:4317
    OTEL_SERVICE_NAME: str = "sila-backend"
    # Instrumentation toggles
    OBS_INSTRUMENT_SQL: bool = False
    OBS_INSTRUMENT_REDIS: bool = False

    @property
    def FRONTEND_BASE_URL(self) -> str:
        """URL base do frontend"""
        return f"http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}"

    def get_cors_origins(self) -> list[str]:
        """CORS origins dinâmico baseado em configuração"""
        return [
            self.FRONTEND_BASE_URL,
            f"http://localhost:{self.FRONTEND_PORT}",
            f"http://host.docker.internal:{self.FRONTEND_PORT}",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://host.docker.internal:5173",
            "http://localhost",
            "http://127.0.0.1",
            "http://host.docker.internal",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://host.docker.internal:3000",
            "http://frontend:3000",
            "http://frontend:5173",
        ]

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return self.get_cors_origins()

    SECRET_KEY: str = "Trumanmarcelo_1983_SILA_SECRET_KEY_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 90

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        """Compatibilidade reversa: converte dias para minutos"""
        return self.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60

    KEYCLOAK_ISSUER: str = ""
    KEYCLOAK_JWKS_URL: str = ""
    KEYCLOAK_CLIENT_ID: str = ""
    VITE_API_URL: str = "http://127.0.0.1:8000/api/v1"
    VITE_APP_NAME: str = "SILA System"
    VITE_APP_ENV: str = "development"

    @property
    def VITE_PROXY_TARGET(self) -> str:
        """Target do proxy do Vite para API"""
        return self.API_BASE_URL

    def to_dict(self) -> dict[str, Any]:
        """Exportar todas as configurações como dicionário"""
        return {
            "api": {"host": self.API_HOST, "port": self.API_PORT, "base_url": self.API_BASE_URL},
            "frontend": {
                "host": self.FRONTEND_HOST,
                "port": self.FRONTEND_PORT,
                "base_url": self.FRONTEND_BASE_URL,
            },
            "database": {
                "host": self.DB_HOST,
                "port": self.DB_PORT,
                "connection_string": self.DB_CONNECTION_STRING,
            },
            "redis": {
                "host": self.REDIS_HOST,
                "port": self.REDIS_PORT,
                "db": self.REDIS_DB,
                "url": self.REDIS_URL,
            },
            "runtime": {
                "gmx_env_loaded": self.GMX_ENV_LOADED,
                "gmx_env_source": self.GMX_ENV_SOURCE,
            },
            "cors_origins": self.get_cors_origins(),
            "vite_proxy_target": self.VITE_PROXY_TARGET,
            "external_services": {"fuc_base_url": self.FUC_BASE_URL},
        }

    def print_config(self) -> None:
        """Imprimir configuração para debug"""
        import json

        print(json.dumps(self.to_dict(), indent=2))

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
api_base_url = settings.API_BASE_URL
frontend_base_url = settings.FRONTEND_BASE_URL
db_connection_string = settings.DB_CONNECTION_STRING
cors_origins = settings.get_cors_origins()
vite_proxy_target = settings.VITE_PROXY_TARGET
fuc_base_url = settings.FUC_BASE_URL
__all__ = [
    "settings",
    "api_base_url",
    "frontend_base_url",
    "db_connection_string",
    "cors_origins",
    "vite_proxy_target",
    "fuc_base_url",
]
if __name__ == "__main__":
    settings.print_config()
