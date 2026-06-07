"""
Tests for Citizen Documents API endpoints
Testa integração com service adapters e validação de segurança
"""

from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest
from apps.backend.app.main import app
from fastapi.testclient import TestClient

from apps.backend.app.modules.justice.civil_registry.adapters import (
    AttestationServiceAdapter,
    CertificateServiceAdapter,
    FinancesServiceAdapter,
    NotificationServiceAdapter,
    RequestTrackingServiceAdapter,
)

client = TestClient(app)

CITIZEN_ID = str(uuid4())
TOKEN_HEADER = {"X-Token": f"citizen:{CITIZEN_ID}"}


class TestCertificateEndpoints:
    """Testa endpoints de certificados"""

    @pytest.mark.asyncio
    async def test_get_certificates_success(self):
        """Deve retornar certificados do cidadão"""

        with patch("apps.backend.app.api.deps.get_current_user") as mock_user:
            mock_user.return_value = {"citizen_id": CITIZEN_ID, "role": "citizen"}

            with patch.object(
                CertificateServiceAdapter, "get_certificates_by_citizen", new_callable=AsyncMock
            ) as mock_certs:
                mock_certs.return_value = [
                    {"id": str(uuid4()), "type": "nascimento", "date": "2024-01-01"}
                ]

                # TODO: Implementar chamada ao endpoint quando FastAPI async estiver configurado

    # NOTA: Testes de autenticação consolidados em tests/test_auth_consolidated.py
    # Veja: test_all_endpoints_require_authentication() para validação unificada de 20+ endpoints
    # Economia: -60 linhas duplicadas, -28 testes espalhados em múltiplos arquivos


class TestAttestationEndpoints:
    """Testa endpoints de atestados

    NOTA: Testes de autenticação consolidados em tests/test_auth_consolidated.py
    """

    pass


class TestFinancesEndpoints:
    """Testa endpoints de faturas e pagamentos

    Testes de autenticação consolidados em: tests/test_auth_consolidated.py
    """

    pass


class TestRequestTrackingEndpoints:
    """Testa endpoints de tracking de solicitações

    Testes de autenticação consolidados em: tests/test_auth_consolidated.py
    """

    pass


class TestNotificationEndpoints:
    """Testa endpoints de notificações

    Testes de autenticação consolidados em: tests/test_auth_consolidated.py
    """

    pass


class TestServiceAdaptersStructure:
    """Testa que service adapters têm estrutura correta"""

    def test_certificate_adapter_has_required_methods(self):
        """CertificateServiceAdapter deve ter os métodos obrigatórios"""

        adapter = CertificateServiceAdapter(Mock())
        assert hasattr(adapter, "get_certificates_by_citizen")
        assert hasattr(adapter, "request_certificate")

    def test_attestation_adapter_has_required_methods(self):
        """AttestationServiceAdapter deve ter os métodos obrigatórios"""

        adapter = AttestationServiceAdapter(Mock())
        assert hasattr(adapter, "get_attestations_by_citizen")
        assert hasattr(adapter, "request_attestation")

    def test_finances_adapter_has_required_methods(self):
        """FinancesServiceAdapter deve ter os métodos obrigatórios"""

        adapter = FinancesServiceAdapter(Mock())
        assert hasattr(adapter, "get_invoices_by_citizen")
        assert hasattr(adapter, "get_payments_by_citizen")

    def test_request_tracking_adapter_has_required_methods(self):
        """RequestTrackingServiceAdapter deve ter os métodos obrigatórios"""

        adapter = RequestTrackingServiceAdapter(Mock())
        assert hasattr(adapter, "get_citizen_requests")
        assert hasattr(adapter, "get_request_detail")

    def test_notification_adapter_has_required_methods(self):
        """NotificationServiceAdapter deve ter os métodos obrigatórios"""

        adapter = NotificationServiceAdapter(Mock())
        assert hasattr(adapter, "get_notifications")
        assert hasattr(adapter, "mark_as_read")


class TestAdapterIntegration:
    """Testa que adapters retornam estruturas esperadas"""

    @pytest.mark.asyncio
    async def test_certificate_adapter_returns_list(self):
        """get_certificates_by_citizen deve retornar lista"""

        adapter = CertificateServiceAdapter(Mock())
        result = await adapter.get_certificates_by_citizen(uuid4())
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_attestation_adapter_returns_list(self):
        """get_attestations_by_citizen deve retornar lista"""

        adapter = AttestationServiceAdapter(Mock())
        result = await adapter.get_attestations_by_citizen(uuid4())
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_finances_adapter_returns_dict(self):
        """get_invoices_by_citizen deve retornar dict com chaves esperadas"""

        adapter = FinancesServiceAdapter(Mock())
        result = await adapter.get_invoices_by_citizen(uuid4())
        assert isinstance(result, dict)
        assert "citizen_id" in result
        assert "invoices" in result

    @pytest.mark.asyncio
    async def test_notification_adapter_returns_dict(self):
        """get_notifications deve retornar dict com chaves esperadas"""

        adapter = NotificationServiceAdapter(Mock())
        result = await adapter.get_notifications(uuid4())
        assert isinstance(result, dict)
        assert "citizen_id" in result
        assert "notifications" in result
