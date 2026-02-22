"""
Configuração centralizada para o SILA System
Única fonte de verdade para todas as configurações.

Uso:
    from app.core.settings import settings
    
    # Acessar propriedades
    settings.DATABASE_URL
    settings.API_BASE_URL
    settings.get_cors_origins()
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


class Settings(BaseSettings):
    """Configurações da aplicação - Single Source of Truth"""
    
    # ==================== DATABASE ====================
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "sila_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Trumanmarcelo_1983")
    DB_NAME: str = os.getenv("DB_NAME", "sila_system")
    # RAW_DATABASE_URL permite sobrescrever totalmente a URL construída
    # Ex.: export DATABASE_URL="postgresql+asyncpg://user:pass@127.0.0.1:5432/sila_system_test"
    RAW_DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)
    
    @property
    def DATABASE_URL(self) -> str:
        """Construir a URL do banco dinamicamente"""
        # Se a variável de ambiente DATABASE_URL (mapeada em RAW_DATABASE_URL)
        # estiver presente, usamo-la em prioridade. Suporte para prefixo
        # 'postgresql://' é convertido para 'postgresql+asyncpg://'.
        if self.RAW_DATABASE_URL:
            url = self.RAW_DATABASE_URL
            if url.startswith("postgresql://"):
                return url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def DB_CONNECTION_STRING(self) -> str:
        """String de conexão BD (para scripts)"""
        return f"{self.DB_HOST}:{self.DB_PORT}"
    
    # ==================== API ====================
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_ENV: str = os.getenv("API_ENV", "development")
    
    @property
    def API_BASE_URL(self) -> str:
        """URL base da API"""
        return f"http://{self.API_HOST}:{self.API_PORT}"
    
    # ==================== EXTERNAL SERVICES ====================
    # Base URL do FUC (serviço de consulta de cidadão)
    FUC_BASE_URL: str = os.getenv("FUC_BASE_URL", "http://127.0.0.1:9000")
    # ==================== FRONTEND ====================
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "127.0.0.1")
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "5173"))
    
    @property
    def FRONTEND_BASE_URL(self) -> str:
        """URL base do frontend"""
        return f"http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}"
    
    # ==================== CORS ====================
    def get_cors_origins(self) -> List[str]:
        """CORS origins dinâmico baseado em configuração"""
        return [
            self.FRONTEND_BASE_URL,
            f"http://localhost:{self.FRONTEND_PORT}",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost",
            "http://127.0.0.1",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            # Docker aliases
            "http://frontend:3000",
            "http://frontend:5173",
        ]
    
    # Legacy property for backwards compatibility
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return self.get_cors_origins()
    
    # ==================== AUTH ====================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "Trumanmarcelo_1983_SILA_SECRET_KEY_2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "90"))
    
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        """Compatibilidade reversa: converte dias para minutos"""
        return self.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60
    
    # ==================== VITE CONFIG ====================
    VITE_API_URL: str = os.getenv("VITE_API_URL", "http://127.0.0.1:8000")
    VITE_APP_NAME: str = os.getenv("VITE_APP_NAME", "SILA System")
    VITE_APP_ENV: str = os.getenv("VITE_APP_ENV", "development")
    
    @property
    def VITE_PROXY_TARGET(self) -> str:
        """Target do proxy do Vite para API"""
        return self.API_BASE_URL
    
    # ==================== EXPORT HELPERS ====================
    def to_dict(self) -> Dict[str, Any]:
        """Exportar todas as configurações como dicionário"""
        return {
            "api": {
                "host": self.API_HOST,
                "port": self.API_PORT,
                "base_url": self.API_BASE_URL,
            },
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
            "cors_origins": self.get_cors_origins(),
            "vite_proxy_target": self.VITE_PROXY_TARGET,
            "external_services": {
                "fuc_base_url": self.FUC_BASE_URL,
            },
        }
    
    def print_config(self) -> None:
        """Imprimir configuração para debug"""
        import json
        print(json.dumps(self.to_dict(), indent=2))
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Instância global
settings = Settings()

# ==================== EXPORTS DE COMPATIBILIDADE ====================
# Para código legado que importava de ports_config.py
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
    "vite_proxy_target"
    , "fuc_base_url"
]


if __name__ == "__main__":
    # Script para verificar configuração
    settings.print_config()
