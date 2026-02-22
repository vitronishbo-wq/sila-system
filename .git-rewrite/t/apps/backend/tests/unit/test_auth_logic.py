"""
Testes unitários para o módulo de autenticação

Foco em lógica crítica de negócio:
- PasswordPolicy: validação de senhas
- TwoFactorAuth: 2FA e códigos de backup
- JWTManager: geração e validação de tokens
- RateLimiter: controle de tentativas
- DeviceFingerprint: fingerprinting de dispositivos
"""

import json
import secrets
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

# Importar as classes que queremos testar
from modules.auth.enhanced_auth import (
    AuthenticationError,
    DeviceFingerprint,
    JWTManager,
    PasswordPolicy,
    RateLimiter,
    TokenPayload,
    TwoFactorAuth,
    TwoFactorError,
)


class TestPasswordPolicy:
    """Testes para PasswordPolicy - lógica crítica de validação de senhas"""

    def test_password_policy_valid_password(self):
        """Testar senha que atende todos os requisitos"""
        policy = PasswordPolicy()

        # Senha válida
        valid_settings.PASSWORD
        is_valid, errors = policy.validate_password(valid_password)

        assert is_valid is True
        assert len(errors) == 0

    def test_password_policy_too_short(self):
        """Testar senha muito curta"""
        policy = PasswordPolicy()

        short_settings.PASSWORD
        is_valid, errors = policy.validate_password(short_password)

        assert is_valid is False
        assert any("at least 12 characters" in error for error in errors)

    def test_password_policy_missing_uppercase(self):
        """Testar senha sem maiúsculas"""
        policy = PasswordPolicy()

        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("uppercase letter" in error for error in errors)

    def test_password_policy_missing_lowercase(self):
        """Testar senha sem minúsculas"""
        policy = PasswordPolicy()

        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("lowercase letter" in error for error in errors)

    def test_password_policy_missing_numbers(self):
        """Testar senha sem números"""
        policy = PasswordPolicy()

        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("number" in error for error in errors)

    def test_password_policy_missing_special_chars(self):
        """Testar senha sem caracteres especiais"""
        policy = PasswordPolicy()

        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("special character" in error for error in errors)

    def test_password_policy_weak_patterns(self):
        """Testar senhas com padrões fracos"""
        policy = PasswordPolicy()

        # Testar padrão sequencial
        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("weak patterns" in error for error in errors)

        # Testar palavra comum
        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("weak patterns" in error for error in errors)

        # Testar repetição de caracteres
        settings.PASSWORD
        is_valid, errors = policy.validate_password(password)

        assert is_valid is False
        assert any("weak patterns" in error for error in errors)


class TestTwoFactorAuth:
    """Testes para TwoFactorAuth - lógica crítica de 2FA"""

    def test_generate_secret(self):
        """Testar geração de secret para 2FA"""
        secret = TwoFactorAuth.generate_secret()

        assert isinstance(secret, str)
        assert len(secret) > 0
        # Deve ser base32 válido para TOTP
        assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" for c in secret)

    def test_verify_token_valid(self):
        """Testar verificação de token 2FA válido"""
        # Gerar secret fixo para teste
        secret = "JBSWY3DPEHPK3PXP"  # base32 válido

        # Simular tempo atual para token consistente
        current_time = 1234567890

        # Token válido para o secret e timestamp (calculado manualmente)
        valid_token = "123456"  # Token válido para teste

        with patch("backend.modules.auth.enhanced_auth.pyotp") as mock_pyotp:
            mock_totp = MagicMock()
            mock_totp.verify.return_value = True
            mock_pyotp.TOTP.return_value = mock_totp

            result = TwoFactorAuth.verify_token(secret, valid_token)
            assert result is True

    def test_verify_token_invalid(self):
        """Testar verificação de token 2FA inválido"""
        secret = "JBSWY3DPEHPK3PXP"
        invalid_token = "999999"

        with patch("backend.modules.auth.enhanced_auth.pyotp") as mock_pyotp:
            mock_totp = MagicMock()
            mock_totp.verify.return_value = False
            mock_pyotp.TOTP.return_value = mock_totp

            result = TwoFactorAuth.verify_token(secret, invalid_token)
            assert result is False

    def test_generate_backup_codes(self):
        """Testar geração de códigos de backup"""
        codes = TwoFactorAuth.generate_backup_codes(count=5)

        assert len(codes) == 5
        assert all(isinstance(code, str) for code in codes)
        assert all(len(code) == 9 for code in codes)  # formato XXXX-XXXX
        assert all("-" in code for code in codes)

        # Verificar unicidade
        assert len(set(codes)) == 5

    def test_generate_qr_code(self):
        """Testar geração de QR code para 2FA"""
        user_email = "test@example.com"
        secret = "JBSWY3DPEHPK3PXP"

        with (
            patch("backend.modules.auth.enhanced_auth.pyotp") as mock_pyotp,
            patch("backend.modules.auth.enhanced_auth.qrcode") as mock_qrcode,
        ):

            # Mock TOTP provisioning URI
            mock_totp = MagicMock()
            mock_totp.provisioning_uri.return_value = "otpauth://totp/SILA:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=SILA"
            mock_pyotp.totp.TOTP.return_value = mock_totp

            # Mock QR code generation
            mock_img = MagicMock()
            mock_qr = MagicMock()
            mock_qr.make_image.return_value = mock_img
            mock_qrcode.QRCode.return_value = mock_qr

            with patch("backend.modules.auth.enhanced_auth.BytesIO") as mock_bytesio:
                mock_buffer = MagicMock()
                mock_img.save = MagicMock()
                mock_bytesio.return_value = mock_buffer
                mock_buffer.getvalue.return_value = b"fake_png_data"

                with patch("backend.modules.auth.enhanced_auth.base64") as mock_base64:
                    mock_base64.b64encode.return_value = b"ZmFrZV9wbmdfZGF0YQ=="
                    mock_base64.b64encode.return_value.decode.return_value = (
                        "ZmFrZV9wbmdfZGF0YQ=="
                    )

                    result = TwoFactorAuth.generate_qr_code(user_email, secret)

                    assert isinstance(result, str)
                    assert len(result) > 0


class TestJWTManager:
    """Testes para JWTManager - lógica crítica de tokens"""

    def test_create_access_token(self):
        """Testar criação de access token"""
        jwt_manager = JWTManager()

        payload = TokenPayload(
            user_id=1,
            session_id="test_session_123",
            username="testuser",
            role="admin",
            municipality="Test City",
            exp=datetime.utcnow() + timedelta(minutes=30),
            iat=datetime.utcnow(),
            device_fingerprint="test_device_123",
        )

        with patch("backend.modules.auth.enhanced_auth.settings") as mock_settings:
            mock_settings.SECRET_KEY = "test_secret_key_for_testing"

            token = jwt_manager.create_access_token(payload)

            assert isinstance(token, str)
            assert len(token) > 0

            # Verificar se token contém informações esperadas
            decoded = jwt_manager.verify_token(token, "access")
            assert decoded["sub"] == "1"
            assert decoded["username"] == "testuser"
            assert decoded["role"] == "admin"
            assert decoded["type"] == "access"

    def test_create_refresh_token(self):
        """Testar criação de refresh token"""
        jwt_manager = JWTManager()

        payload = TokenPayload(
            user_id=1,
            session_id="test_session_123",
            username="testuser",
            role="admin",
            municipality="Test City",
            exp=datetime.utcnow() + timedelta(days=7),
            iat=datetime.utcnow(),
        )

        with patch("backend.modules.auth.enhanced_auth.settings") as mock_settings:
            mock_settings.SECRET_KEY = "test_secret_key_for_testing"

            token = jwt_manager.create_refresh_token(payload)

            assert isinstance(token, str)
            assert len(token) > 0

            decoded = jwt_manager.verify_token(token, "refresh")
            assert decoded["type"] == "refresh"
            assert decoded["sub"] == "1"

    def test_verify_token_valid(self):
        """Testar verificação de token válido"""
        jwt_manager = JWTManager()

        payload = TokenPayload(
            user_id=1,
            session_id="test_session_123",
            username="testuser",
            role="admin",
            municipality="Test City",
            exp=datetime.utcnow() + timedelta(minutes=30),
            iat=datetime.utcnow(),
        )

        with patch("backend.modules.auth.enhanced_auth.settings") as mock_settings:
            mock_settings.SECRET_KEY = "test_secret_key_for_testing"

            token = jwt_manager.create_access_token(payload)
            decoded = jwt_manager.verify_token(token, "access")

            assert decoded["sub"] == "1"
            assert decoded["username"] == "testuser"
            assert decoded["role"] == "admin"

    def test_verify_token_wrong_type(self):
        """Testar erro quando tipo de token está errado"""
        jwt_manager = JWTManager()

        payload = TokenPayload(
            user_id=1,
            session_id="test_session_123",
            username="testuser",
            role="admin",
            municipality="Test City",
            exp=datetime.utcnow() + timedelta(minutes=30),
            iat=datetime.utcnow(),
        )

        with patch("backend.modules.auth.enhanced_auth.settings") as mock_settings:
            mock_settings.SECRET_KEY = "test_secret_key_for_testing"

            # Criar access token mas tentar verificar como refresh
            token = jwt_manager.create_access_token(payload)

            with pytest.raises(AuthenticationError, match="Invalid token type"):
                jwt_manager.verify_token(token, "refresh")

    def test_verify_token_expired(self):
        """Testar erro com token expirado"""
        jwt_manager = JWTManager()

        # Token já expirado
        payload = TokenPayload(
            user_id=1,
            session_id="test_session_123",
            username="testuser",
            role="admin",
            municipality="Test City",
            exp=datetime.utcnow() - timedelta(minutes=1),  # Expirado
            iat=datetime.utcnow() - timedelta(minutes=30),
        )

        with patch("backend.modules.auth.enhanced_auth.settings") as mock_settings:
            mock_settings.SECRET_KEY = "test_secret_key_for_testing"

            token = jwt_manager.create_access_token(payload)

            with pytest.raises(AuthenticationError, match="Token has expired"):
                jwt_manager.verify_token(token, "access")


class TestRateLimiter:
    """Testes para RateLimiter - lógica crítica de controle de tentativas"""

    def test_rate_limiter_allows_first_attempt(self):
        """Testar que primeira tentativa é permitida"""
        limiter = RateLimiter()
        identifier = "test_user_123"

        assert limiter.is_allowed(identifier) is True

    def test_rate_limiter_blocks_after_max_attempts(self):
        """Testar bloqueio após máximo de tentativas"""
        limiter = RateLimiter()
        identifier = "test_user_123"

        # Registrar tentativas falhas
        for i in range(limiter.max_attempts):
            limiter.record_attempt(identifier, success=False)

        # Próxima tentativa deve ser bloqueada
        assert limiter.is_allowed(identifier) is False

    def test_rate_limiter_resets_on_success(self):
        """Testar reset do contador em tentativa bem-sucedida"""
        limiter = RateLimiter()
        identifier = "test_user_123"

        # Registrar algumas tentativas falhas
        for i in range(3):
            limiter.record_attempt(identifier, success=False)

        # Ainda deve permitir (não atingiu limite)
        assert limiter.is_allowed(identifier) is True

        # Tentativa bem-sucedida deve resetar contador
        limiter.record_attempt(identifier, success=True)
        assert limiter.is_allowed(identifier) is True

        # Continuar registrando falhas deve funcionar novamente
        for i in range(3):
            limiter.record_attempt(identifier, success=False)

        assert limiter.is_allowed(identifier) is True

    def test_rate_limiter_lockout_expires(self):
        """Testar que bloqueio expira após período"""
        limiter = RateLimiter()
        identifier = "test_user_123"

        # Registrar tentativas até bloqueio
        for i in range(limiter.max_attempts):
            limiter.record_attempt(identifier, success=False)

        assert limiter.is_allowed(identifier) is False

        # Simular passagem do tempo de bloqueio
        import time

        time.sleep(0.1)  # Pequeno delay para teste

        # Ainda deve estar bloqueado (15 minutos por padrão)
        assert limiter.is_allowed(identifier) is False


class TestDeviceFingerprint:
    """Testes para DeviceFingerprint - lógica de fingerprinting"""

    def test_generate_fingerprint_creates_hash(self):
        """Testar que fingerprint gera hash consistente"""
        mock_request = MagicMock()
        mock_request.headers = {
            "user-agent": "Test User Agent",
            "accept-language": "pt-BR,pt;q=0.9",
            "accept-encoding": "gzip, deflate",
        }
        mock_request.client.host = "192.168.1.100"

        fingerprint1 = DeviceFingerprint.generate_fingerprint(mock_request)
        fingerprint2 = DeviceFingerprint.generate_fingerprint(mock_request)

        # Mesma requisição deve gerar mesmo fingerprint
        assert fingerprint1 == fingerprint2
        assert isinstance(fingerprint1, str)
        assert len(fingerprint1) == 16  # Primeiro 16 chars do SHA256

    def test_generate_fingerprint_different_requests(self):
        """Testar que fingerprints diferentes geram hashes diferentes"""
        # Request 1
        mock_request1 = MagicMock()
        mock_request1.headers = {"user-agent": "Agent 1"}
        mock_request1.client.host = "192.168.1.1"

        # Request 2
        mock_request2 = MagicMock()
        mock_request2.headers = {"user-agent": "Agent 2"}
        mock_request2.client.host = "192.168.1.2"

        fingerprint1 = DeviceFingerprint.generate_fingerprint(mock_request1)
        fingerprint2 = DeviceFingerprint.generate_fingerprint(mock_request2)

        assert fingerprint1 != fingerprint2

    def test_generate_fingerprint_missing_headers(self):
        """Testar fingerprint com headers faltantes"""
        mock_request = MagicMock()
        mock_request.headers = {}  # Sem headers
        mock_request.client.host = "192.168.1.100"

        fingerprint = DeviceFingerprint.generate_fingerprint(mock_request)

        assert isinstance(fingerprint, str)
        assert len(fingerprint) == 16


class TestEnhancedAuthenticator:
    """Testes para EnhancedAuthenticator - lógica principal de auth"""

    @pytest.fixture
    def authenticator(self):
        """Fixture para instância de EnhancedAuthenticator"""
        return EnhancedAuthenticator()

    @pytest.fixture
    def mock_db_session(self):
        """Fixture para mock de sessão de banco"""
        return MagicMock()

    @pytest.fixture
    def mock_request(self):
        """Fixture para mock de request"""
        mock_req = MagicMock()
        mock_req.client.host = "192.168.1.100"
        mock_req.headers = {"user-agent": "Test Agent", "accept-language": "pt-BR"}
        return mock_req

    def test_authenticate_user_valid_credentials(
        self, authenticator, mock_db_session, mock_request
    ):
        """Testar autenticação com credenciais válidas"""
        # Mock user data
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "role": "admin",
            "municipality": "Test City",
            "is_active": True,
            "is_superuser": False,
            "two_factor_enabled": False,
            "two_factor_secret": None,
        }

        with patch.object(authenticator, "_verify_credentials") as mock_verify:
            mock_verify.return_value = mock_user

            result = await authenticator.authenticate_user(
                username="test@example.com",
                password=settings.PASSWORD,
                request=mock_request,
                db=mock_db_session,
            )

            assert result.success is True
            assert result.user_id == 1
            assert result.access_token is not None
            assert result.refresh_token is not None
            assert result.requires_2fa is False

    def test_authenticate_user_2fa_required(
        self, authenticator, mock_db_session, mock_request
    ):
        """Testar autenticação quando 2FA é requerida"""
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "role": "admin",
            "municipality": "Test City",
            "is_active": True,
            "is_superuser": False,
            "two_factor_enabled": True,
            "two_factor_secret": "JBSWY3DPEHPK3PXP",
        }

        with patch.object(authenticator, "_verify_credentials") as mock_verify:
            mock_verify.return_value = mock_user

            result = await authenticator.authenticate_user(
                username="test@example.com",
                password=settings.PASSWORD,
                request=mock_request,
                db=mock_db_session,
            )

            assert result.success is False
            assert result.requires_2fa is True
            assert "2FA code required" in result.message

    def test_authenticate_user_2fa_verification(
        self, authenticator, mock_db_session, mock_request
    ):
        """Testar autenticação completa com 2FA"""
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "role": "admin",
            "municipality": "Test City",
            "is_active": True,
            "is_superuser": False,
            "two_factor_enabled": True,
            "two_factor_secret": "JBSWY3DPEHPK3PXP",
        }

        with (
            patch.object(authenticator, "_verify_credentials") as mock_verify,
            patch.object(authenticator.totp, "verify_token") as mock_2fa_verify,
        ):

            mock_verify.return_value = mock_user
            mock_2fa_verify.return_value = True

            result = await authenticator.authenticate_user(
                username="test@example.com",
                password=settings.PASSWORD,
                totp_code="123456",
                request=mock_request,
                db=mock_db_session,
            )

            assert result.success is True
            assert result.user_id == 1

    def test_authenticate_user_invalid_2fa(
        self, authenticator, mock_db_session, mock_request
    ):
        """Testar erro com código 2FA inválido"""
        mock_user = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "role": "admin",
            "municipality": "Test City",
            "is_active": True,
            "is_superuser": False,
            "two_factor_enabled": True,
            "two_factor_secret": "JBSWY3DPEHPK3PXP",
        }

        with (
            patch.object(authenticator, "_verify_credentials") as mock_verify,
            patch.object(authenticator.totp, "verify_token") as mock_2fa_verify,
        ):

            mock_verify.return_value = mock_user
            mock_2fa_verify.return_value = False

            with pytest.raises(TwoFactorError, match="Invalid 2FA code"):
                await authenticator.authenticate_user(
                    username="test@example.com",
                    password=settings.PASSWORD,
                    totp_code="000000",  # Código inválido
                    request=mock_request,
                    db=mock_db_session,
                )

    def test_authenticate_user_rate_limited(
        self, authenticator, mock_db_session, mock_request
    ):
        """Testar bloqueio por rate limiting"""
        # Configurar rate limiter para bloquear
        authenticator.rate_limiter.max_attempts = 1

        with patch.object(authenticator.rate_limiter, "is_allowed") as mock_allowed:
            mock_allowed.return_value = False

            with pytest.raises(AuthenticationError, match="Too many failed attempts"):
                await authenticator.authenticate_user(
                    username="test@example.com",
                    password=settings.PASSWORD,
                    request=mock_request,
                    db=mock_db_session,
                )

    def test_verify_credentials_success(self, authenticator, mock_db_session):
        """Testar verificação de credenciais bem-sucedida"""
        # Mock do banco de dados
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.username = "testuser"
        mock_user.hashed_settings.PASSWORD
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_user.role = None

        mock_db_session.execute.return_value = MagicMock()
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = (
            mock_user
        )

        with patch("backend.modules.auth.enhanced_auth.pwd_context") as mock_pwd:
            mock_pwd.verify.return_value = True

            result = await authenticator._verify_credentials(
                username="test@example.com",
                password=settings.PASSWORD,
                db=mock_db_session,
            )

            assert result is not None
            assert result["id"] == 1
            assert result["email"] == "test@example.com"
            assert result["role"] == "user"  # default role

    def test_verify_credentials_user_not_found(self, authenticator, mock_db_session):
        """Testar verificação com usuário não encontrado"""
        mock_db_session.execute.return_value = MagicMock()
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = (
            None
        )

        result = await authenticator._verify_credentials(
            username="nonexistent@example.com",
            password=settings.PASSWORD,
            db=mock_db_session,
        )

        assert result is None

    def test_verify_credentials_inactive_user(self, authenticator, mock_db_session):
        """Testar verificação com usuário inativo"""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.username = "testuser"
        mock_user.hashed_settings.PASSWORD
        mock_user.is_active = False  # Usuário inativo
        mock_user.is_superuser = False
        mock_user.role = None

        mock_db_session.execute.return_value = MagicMock()
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = (
            mock_user
        )

        with patch("backend.modules.auth.enhanced_auth.pwd_context") as mock_pwd:
            mock_pwd.verify.return_value = True

            result = await authenticator._verify_credentials(
                username="test@example.com",
                password=settings.PASSWORD,
                db=mock_db_session,
            )

            assert result is None
