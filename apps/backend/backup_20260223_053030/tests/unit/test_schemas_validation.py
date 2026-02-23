"""
Testes unitários para schemas e validação de dados

Foco em lógica crítica de validação:
- Token schemas: validação de tokens JWT
- User schemas: validação de dados de usuário
- Password validation: regras de senha
- Input sanitization: limpeza e validação de inputs
"""

import pytest
from pydantic import ValidationError

# Importar schemas que queremos testar
from core.schemas import (
    RefreshTokenRequest,
    RefreshTokenResponse,
    Token,
    UserCreate,
    UserInDB,
)


class TestTokenSchemas:
    """Testes para schemas de token"""

    def test_token_schema_valid(self):
        """Testar schema de token válido"""
        token_data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer",
            "expires_in": 3600
        }

        token = Token(**token_data)

        assert token.access_token == token_data["access_token"]
        assert token.token_type == "bearer"
        assert token.expires_in == 3600

    def test_token_schema_default_values(self):
        """Testar valores padrão do schema de token"""
        token_data = {
            "access_token": "fake_token"
        }

        token = Token(**token_data)

        assert token.token_type == "bearer"  # Valor padrão
        assert token.expires_in is None      # Valor padrão

    def test_token_schema_invalid_type(self):
        """Testar schema de token com tipo inválido"""
        token_data = {
            "access_token": "fake_token",
            "token_type": "invalid_type"  # Tipo inválido
        }

        with pytest.raises(ValidationError):
            Token(**token_data)

    def test_refresh_token_request_valid(self):
        """Testar schema de request de refresh token válido"""
        request_data = {
            "refresh_token": "refresh_token_123456"
        }

        request = RefreshTokenRequest(**request_data)

        assert request.refresh_token == "refresh_token_123456"

    def test_refresh_token_request_empty_token(self):
        """Testar schema com refresh token vazio"""
        request_data = {
            "refresh_token": ""
        }

        with pytest.raises(ValidationError):
            RefreshTokenRequest(**request_data)

    def test_refresh_token_response_valid(self):
        """Testar schema de response de refresh token"""
        response_data = {
            "access_token": "new_access_token",
            "token_type": "bearer",
            "expires_in": 1800
        }

        response = RefreshTokenResponse(**response_data)

        assert response.access_token == "new_access_token"
        assert response.token_type == "bearer"
        assert response.expires_in == 1800


class TestUserSchemas:
    """Testes para schemas de usuário"""

    def test_user_create_valid(self):
        """Testar schema de criação de usuário válido"""
        user_data = {
            "email": "test@example.com",
            "password": "SecureP@ssw0rd123",
            "full_name": "Test User"
        }

        user = UserCreate(**user_data)

        assert user.email == "test@example.com"
        assert user.password == "SecureP@ssw0rd123"
        assert user.full_name == "Test User"

    def test_user_create_minimal(self):
        """Testar schema de criação com dados mínimos"""
        user_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        user = UserCreate(**user_data)

        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name is None  # Campo opcional

    def test_user_create_invalid_email(self):
        """Testar schema com email inválido"""
        user_data = {
            "email": "invalid_email",
            "password": "password123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_empty_password(self):
        """Testar schema com senha vazia"""
        user_data = {
            "email": "test@example.com",
            "password": ""
        }

        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_in_db_valid(self):
        """Testar schema de usuário no banco de dados"""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "password": "hashed_password",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False
        }

        user = UserInDB(**user_data)

        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_superuser is False

    def test_user_in_db_defaults(self):
        """Testar valores padrão do schema UserInDB"""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "password": "hashed_password"
        }

        user = UserInDB(**user_data)

        assert user.is_active is True   # Valor padrão
        assert user.is_superuser is False  # Valor padrão
        assert user.full_name is None   # Campo opcional sem valor


class TestDataValidation:
    """Testes para validação de dados em geral"""

    def test_email_format_validation(self):
        """Testar validação de formato de email"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "admin+tag@example.org",
            "123@test-domain.com"
        ]

        invalid_emails = [
            "invalid_email",
            "@example.com",
            "test@",
            "test.example.com",
            ""
        ]

        for email in valid_emails:
            user = UserCreate(email=email, password=settings.PASSWORD)
            assert user.email == email

        for email in invalid_emails:
            with pytest.raises(ValidationError):
                UserCreate(email=email, password=settings.PASSWORD)

    def test_password_requirements(self):
        """Testar requisitos básicos de senha"""
        # Senhas válidas
        valid_passwords = [
            "ValidP@ssw0rd",
            "MySecure123!",
            "Complex-P@ss1"
        ]

        # Senhas inválidas (muito curtas, sem caracteres especiais, etc.)
        invalid_passwords = [
            "",           # Vazia
            "short",      # Muito curta
            "12345678",   # Só números
            "password",   # Só minúsculas
            "PASSWORD",   # Só maiúsculas
        ]

        for password in valid_passwords:
            user = UserCreate(email="test@example.com", passwordtest@example.com", password""Testar requisitos de comprimento de tokens"""
        # Tokens válidos (comprimento razoável)
        valid_tokens = [
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            "short_token_123",
            "a" * 100  # Token longo mas válido
        ]

        # Tokens inválidos
        invalid_tokens = [
            "",  # Token vazio
        ]

        for token in valid_tokens:
            token_obj = Token(access_token=token)
            assert token_obj.access_token == token

        for token in invalid_tokens:
            with pytest.raises(ValidationError):
                Token(access_token=token)


class TestSchemaSerialization:
    """Testes para serialização de schemas"""

    def test_token_to_dict(self):
        """Testar conversão de Token para dict"""
        token = Token(
            access_token="fake_token_123",
            token_type="bearer",
            expires_in=3600
        )

        token_dict = token.dict()

        assert token_dict["access_token"] == "fake_token_123"
        assert token_dict["token_type"] == "bearer"
        assert token_dict["expires_in"] == 3600

    def test_user_to_dict(self):
        """Testar conversão de User para dict"""
        user = UserInDB(
            id=1,
            email="test@example.com",
            password=settings.PASSWORD,
            full_name="Test User",
            is_active=True,
            is_superuser=False
        )

        user_dict = user.dict()

        assert user_dict["id"] == 1
        assert user_dict["email"] == "test@example.com"
        assert user_dict["is_active"] is True
        assert user_dict["is_superuser"] is False

    def test_user_create_without_optional_fields(self):
        """Testar UserCreate sem campos opcionais"""
        user = UserCreate(
            email="test@example.com",
            settings.PASSWORD
        )

        user_dict = user.dict()

        assert "full_name" not in user_dict or user_dict["full_name"] is None

    def test_schema_exclude_fields(self):
        """Testar exclusão de campos sensíveis na serialização"""
        user = UserInDB(
            id=1,
            email="test@example.com",
            password=settings.PASSWORD,  # Campo sensível
            full_name="Test User"
        )

        # Serializar excluindo password
        user_dict = user.dict(exclude={"password"})

        assert "password" not in user_dict
        assert user_dict["email"] == "test@example.com"
        assert user_dict["id"] == 1
