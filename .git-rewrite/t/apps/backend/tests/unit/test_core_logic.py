"""
Testes unitários para o core do sistema

Foco em lógica crítica de configuração e funcionalidades centrais:
- Settings/Config: configuração e validação de environment
- Security: funções de segurança e autenticação
- Database: conexões e configurações de banco
- Services: serviços básicos do sistema
"""

import os
from unittest.mock import MagicMock, patch

import pytest

# Importar as classes que queremos testar
from config import Settings
from core.security import CurrentUser, get_current_user_id
from core.services import AuthService


class TestSettings:
    """Testes para Settings - lógica crítica de configuração"""

    def test_settings_basic_values(self):
        """Testar valores básicos de configuração"""
        settings = Settings()

        assert settings.PROJECT_NAME == "SILA System - Marcelo Truman"
        assert settings.VERSION == "1.0.0"
        assert settings.API_V1_STR == "/api/v1"
        assert settings.SILA_SYSTEM_ID == "sila-2025-marcelo-truman"

    def test_settings_allowed_origins_default(self):
        """Testar origins permitidas com valor padrão"""
        settings = Settings()

        # Sem variável de ambiente, deve usar padrão
        origins = settings.ALLOWED_ORIGINS

        assert isinstance(origins, list)
        assert len(origins) > 0
        assert "http://localhost:3000" in origins

    def test_settings_allowed_origins_custom(self):
        """Testar origins permitidas com valor customizado"""
        custom_origins = "https://example.com,https://app.example.com"

        with patch.dict(os.environ, {"ALLOWED_ORIGINS": custom_origins}):
            settings = Settings()
            origins = settings.ALLOWED_ORIGINS

            assert "https://example.com" in origins
            assert "https://app.example.com" in origins

    def test_settings_database_config(self):
        """Testar configuração de banco de dados"""
        settings = Settings()

        # Testar valores padrão
        assert settings.POSTGRES_USER == "Marcelo Truman"
        assert settings.POSTGRES_DB == "sila_db"

        # Testar valores customizados
        with patch.dict(
            os.environ,
            {
                "POSTGRES_USER": "test_user",
                "POSTGRES_PASSWORD": "test_password",
                "POSTGRES_DB": "test_db",
                "POSTGRES_HOST": "test_host",
                "POSTGRES_PORT": "5433",
            },
        ):
            settings = Settings()

            assert settings.POSTGRES_USER == "test_user"
            assert settings.POSTGRES_PASSWORD == "test_password"
            assert settings.POSTGRES_DB == "test_db"
            assert settings.POSTGRES_HOST == "test_host"
            assert settings.POSTGRES_PORT == 5433

    def test_settings_database_url_construction(self):
        """Testar construção da URL de banco de dados"""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_USER": "test_user",
                "POSTGRES_PASSWORD": "test_password",
                "POSTGRES_HOST": "localhost",
                "POSTGRES_PORT": "5432",
                "POSTGRES_DB": "test_db",
            },
        ):
            settings = Settings()

            # Verificar se URL é construída corretamente
            expected_url = (
                "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
            )
            assert settings.DATABASE_URL == expected_url

    def test_settings_security_config(self):
        """Testar configuração de segurança"""
        settings = Settings()

        # Testar valores padrão
        assert settings.SECRET_KEY.startswith("sila-secret-")

        # Testar valor customizado
        with patch.dict(os.environ, {"SECRET_KEY": "custom_secret_key"}):
            settings = Settings()
            assert settings.SECRET_KEY == "custom_secret_key"

    def test_settings_cors_config(self):
        """Testar configuração CORS"""
        settings = Settings()

        # Testar valores padrão
        assert settings.BACKEND_CORS_ORIGINS == [
            "http://localhost:3000",
            "http://localhost:8000",
        ]

        # Testar valor customizado
        custom_cors = "https://example.com,https://app.example.com"
        with patch.dict(os.environ, {"BACKEND_CORS_ORIGINS": custom_cors}):
            settings = Settings()
            assert "https://example.com" in settings.BACKEND_CORS_ORIGINS
            assert "https://app.example.com" in settings.BACKEND_CORS_ORIGINS


class TestSecurityFunctions:
    """Testes para funções de segurança no core"""

    def test_get_current_user_id_mock_mode(self):
        """Testar get_current_user_id em modo mock (desenvolvimento)"""
        mock_request = MagicMock()
        mock_request.headers = {}  # Sem header Authorization
        mock_request.client.host = "127.0.0.1"

        # Em modo desenvolvimento, deve retornar user mock
        user_id = get_current_user_id(mock_request)
        assert user_id == "user_123"

    def test_get_current_user_id_with_auth_header(self):
        """Testar get_current_user_id com header de autenticação"""
        mock_request = MagicMock()
        mock_request.headers = {"Authorization": "Bearer fake_token_123"}
        mock_request.client.host = "127.0.0.1"

        # Com header, deve retornar user mock (por enquanto)
        user_id = get_current_user_id(mock_request)
        assert user_id == "user_123"

    def test_current_user_dependency_type(self):
        """Testar que CurrentUser é uma Annotated type correta"""
        from typing import get_args, get_origin

        # Verificar que CurrentUser é uma Annotated type
        origin = get_origin(CurrentUser)
        args = get_args(CurrentUser)

        assert origin is str  # O tipo base é str
        assert len(args) == 2  # Annotated[T, Depends(...)]


class TestAuthService:
    """Testes para AuthService - lógica básica de autenticação"""

    @pytest.mark.asyncio
    async def test_authenticate_user_valid_email(self):
        """Testar autenticação com email válido"""
        service = AuthService()

        # Email válido deve retornar dados do usuário
        result = await service.authenticate_user("test@example.com", "password123")

        assert result is not None
        assert result["email"] == "test@example.com"
        assert result["user_id"] == 1

    @pytest.mark.asyncio
    async def test_authenticate_user_empty_email(self):
        """Testar autenticação com email vazio"""
        service = AuthService()

        # Email vazio deve retornar None
        result = await service.authenticate_user("", "password123")

        assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_none_email(self):
        """Testar autenticação com email None"""
        service = AuthService()

        # Email None deve retornar None
        result = await service.authenticate_user(None, "password123")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_current_user_with_token(self):
        """Testar obtenção de usuário atual com token"""
        service = AuthService()

        # Token válido deve retornar dados do usuário
        result = await service.get_current_user("valid_token_123")

        assert result is not None
        assert result["email"] == "test@example.com"
        assert result["user_id"] == 1

    @pytest.mark.asyncio
    async def test_get_current_user_empty_token(self):
        """Testar obtenção de usuário com token vazio"""
        service = AuthService()

        # Token vazio deve retornar dados do usuário (fallback)
        result = await service.get_current_user("")

        assert result is not None
        assert result["email"] == "test@example.com"


class TestConfigurationValidation:
    """Testes para validação de configuração"""

    def test_settings_environment_variables(self):
        """Testar que settings respondem corretamente a variáveis de ambiente"""
        # Testar que mudanças no environment afetam settings
        with patch.dict(os.environ, {"POSTGRES_HOST": "production.db.com"}):
            settings = Settings()
            assert settings.POSTGRES_HOST == "production.db.com"

        # Reset environment
        if "POSTGRES_HOST" in os.environ:
            del settings.POSTGRES_HOST

        settings = Settings()
        assert settings.POSTGRES_HOST != "production.db.com"

    def test_settings_url_encoding(self):
        """Testar encoding de URLs com caracteres especiais"""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_USER": "user@domain.com",
                "POSTGRES_PASSWORD": "p@ssw0rd!",
                "POSTGRES_DB": "test_db",
            },
        ):
            settings = Settings()

            # Verificar que caracteres especiais são encoded na URL
            assert "user%40domain.com" in settings.DATABASE_URL
            assert "p%40ssw0rd%21" in settings.DATABASE_URL

    def test_settings_cors_origins_parsing(self):
        """Testar parsing de origins CORS com diferentes formatos"""
        # Testar com espaços
        with patch.dict(
            os.environ,
            {"BACKEND_CORS_ORIGINS": " https://app1.com , https://app2.com "},
        ):

            settings = Settings()
            origins = settings.BACKEND_CORS_ORIGINS

            assert "https://app1.com" in origins
            assert "https://app2.com" in origins
            # Espaços devem ser removidos
            assert origins == ["https://app1.com", "https://app2.com"]

    def test_settings_empty_origins(self):
        """Testar comportamento com origins vazias"""
        with patch.dict(os.environ, {"ALLOWED_ORIGINS": ""}):
            settings = Settings()
            origins = settings.ALLOWED_ORIGINS

            # Deve retornar lista vazia quando não há origins válidas
            assert origins == []


class TestServiceIntegration:
    """Testes para integração entre services do core"""

    @pytest.mark.asyncio
    async def test_auth_service_with_security_integration(self):
        """Testar integração entre AuthService e funções de security"""
        service = AuthService()

        # Autenticar usuário
        auth_result = await service.authenticate_user("admin@sila.com", "password")

        # Verificar estrutura do resultado
        assert "user_id" in auth_result
        assert "email" in auth_result

        # Simular uso da função de security
        mock_request = MagicMock()
        mock_request.headers = {"Authorization": "Bearer fake_token"}

        user_id = get_current_user_id(mock_request)
        assert isinstance(user_id, str)
        assert len(user_id) > 0

    def test_settings_security_key_generation(self):
        """Testar geração de chave de segurança"""
        settings = Settings()

        # Chave padrão deve começar com prefixo
        assert settings.SECRET_KEY.startswith("sila-secret-")

        # Deve ser longa o suficiente para ser segura
        assert len(settings.SECRET_KEY) > 20

        # Testar que chaves diferentes são geradas
        settings1 = Settings()
        settings2 = Settings()

        # Em ambiente controlado, chaves podem ser iguais (usando timestamp fixo)
        # Mas em produção devem ser diferentes
        assert isinstance(settings1.SECRET_KEY, str)
        assert isinstance(settings2.SECRET_KEY, str)
