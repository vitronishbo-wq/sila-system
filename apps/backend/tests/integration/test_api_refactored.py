"""
Testes de integração refatorados - Foco em API

Este arquivo demonstra o padrão refatorado para testes de integração,
focando em interações de API em vez de fluxos end-to-end.
"""

from unittest.mock import patch


class TestAuthenticationAPI:
    """Testes de API focados em autenticação"""

    def test_login_success(self, client, test_user, auth_headers_user):
        """Testa login bem-sucedido com dados válidos"""
        login_data = {"email": test_user.email, "password": "testpassword"}

        response = client.post("/api/v2/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_login_invalid_credentials(self, client):
        """Testa login com credenciais inválidas"""
        login_data = {"email": "invalid@example.com", "password": "wrongpassword"}

        response = client.post("/api/v2/auth/login", json=login_data)

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_login_missing_fields(self, client):
        """Testa login com campos obrigatórios faltando"""
        login_data = {
            "email": "test@example.com"
            # password faltando
        }

        response = client.post("/api/v2/auth/login", json=login_data)

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_protected_endpoint_with_valid_token(self, client, auth_headers_user):
        """Testa acesso a endpoint protegido com token válido"""
        response = client.get("/api/v2/users/me", headers=auth_headers_user)

        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "username" in data

    def test_protected_endpoint_without_token(self, client):
        """Testa acesso a endpoint protegido sem token"""
        response = client.get("/api/v2/users/me")

        assert response.status_code == 401

    def test_protected_endpoint_with_invalid_token(self, client):
        """Testa acesso a endpoint protegido com token inválido"""
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v2/users/me", headers=invalid_headers)

        assert response.status_code == 401


class TestBIUpdateAPI:
    """Testes de API focados em atualizações de BI"""

    def test_create_bi_update_success(self, client, auth_headers_user, sample_bi_update_data):
        """Testa criação de atualização de BI com dados válidos"""
        response = client.post(
            "/api/v2/citizenship/bi-updates",
            json=sample_bi_update_data,
            headers=auth_headers_user,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "pendente"
        assert "id" in data
        assert data["nome_completo"] == sample_bi_update_data["nome_completo"]

    def test_create_bi_update_validation_error(self, client, auth_headers_user):
        """Testa criação de atualização de BI com dados inválidos"""
        invalid_data = {
            "nome_completo": "",  # Nome vazio
            "numero_documento": "123",  # Documento muito curto
            "data_nascimento": "invalid-date",
        }

        response = client.post(
            "/api/v2/citizenship/bi-updates",
            json=invalid_data,
            headers=auth_headers_user,
        )

        assert response.status_code == 422

    def test_list_bi_updates(self, client, auth_headers_user, test_bi_update):
        """Testa listagem de atualizações de BI"""
        response = client.get("/api/v2/citizenship/bi-updates", headers=auth_headers_user)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) > 0

    def test_get_bi_update_by_id(self, client, auth_headers_user, test_bi_update):
        """Testa busca de atualização de BI por ID"""
        response = client.get(
            f"/api/v2/citizenship/bi-updates/{test_bi_update.id}",
            headers=auth_headers_user,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_bi_update.id)

    def test_get_bi_update_not_found(self, client, auth_headers_user):
        """Testa busca de atualização de BI inexistente"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(
            f"/api/v2/citizenship/bi-updates/{fake_id}", headers=auth_headers_user
        )

        assert response.status_code == 404


class TestNotificationAPI:
    """Testes de API focados em notificações"""

    def test_send_notification_success(self, client, auth_headers_admin, sample_notification_data):
        """Testa envio de notificação com dados válidos"""
        response = client.post(
            "/api/v2/notifications/send",
            json=sample_notification_data,
            headers=auth_headers_admin,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "sent"
        assert "id" in data

    def test_send_notification_unauthorized(
        self, client, auth_headers_user, sample_notification_data
    ):
        """Testa envio de notificação sem permissão de administrador"""
        response = client.post(
            "/api/v2/notifications/send",
            json=sample_notification_data,
            headers=auth_headers_user,
        )

        assert response.status_code == 403

    def test_list_notifications(self, client, auth_headers_user, test_notification):
        """Testa listagem de notificações do usuário"""
        response = client.get("/api/v2/notifications", headers=auth_headers_user)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_mark_notification_as_read(self, client, auth_headers_user, test_notification):
        """Testa marcação de notificação como lida"""
        response = client.patch(
            f"/api/v2/notifications/{test_notification.id}/read",
            headers=auth_headers_user,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "read"


class TestExternalAPIIntegration:
    """Testes de integração com APIs externas (mockadas)"""

    def test_sigfe_sync_success(self, client, auth_headers_admin, mock_external_api):
        """Testa sincronização com SIGFE bem-sucedida"""
        sync_data = {"entity_type": "user", "entity_id": "user-123", "action": "create"}

        response = client.post(
            "/api/v2/integration/sigfe/sync", json=sync_data, headers=auth_headers_admin
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "sigfe_id" in data

    def test_external_api_timeout(self, client, auth_headers_admin, mock_external_api):
        """Testa timeout de API externa"""
        # Configurar mock para timeout
        mock_external_api.post("https://api.sigfe.gov.ao/v1/sync").mock(
            side_effect=Exception("Timeout")
        )

        sync_data = {"entity_type": "user", "entity_id": "user-123", "action": "create"}

        response = client.post(
            "/api/v2/integration/sigfe/sync", json=sync_data, headers=auth_headers_admin
        )

        assert response.status_code == 500
        data = response.json()
        assert "error" in data


class TestPerformanceAPI:
    """Testes de performance para APIs críticas"""

    def test_login_performance(
        self, client, test_user, performance_monitor, fast_operation_threshold
    ):
        """Testa performance do endpoint de login"""
        login_data = {"email": test_user.email, "password": "testpassword"}

        performance_monitor.start()
        response = client.post("/api/v2/auth/login", json=login_data)
        performance_monitor.stop()

        assert response.status_code == 200
        performance_monitor.assert_max_duration(fast_operation_threshold)

    def test_bi_update_creation_performance(
        self,
        client,
        auth_headers_user,
        sample_bi_update_data,
        performance_monitor,
        slow_operation_threshold,
    ):
        """Testa performance da criação de atualização de BI"""
        performance_monitor.start()
        response = client.post(
            "/api/v2/citizenship/bi-updates",
            json=sample_bi_update_data,
            headers=auth_headers_user,
        )
        performance_monitor.stop()

        assert response.status_code == 201
        performance_monitor.assert_max_duration(slow_operation_threshold)


class TestValidationAPI:
    """Testes de validação de dados da API"""

    def test_email_validation(self, client, auth_headers_user):
        """Testa validação de email em endpoints"""
        invalid_user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "full_name": "Test User",
        }

        response = client.post("/api/v2/users", json=invalid_user_data, headers=auth_headers_user)

        assert response.status_code == 422
        data = response.json()
        assert "email" in str(data["detail"])

    def test_document_number_validation(self, client, auth_headers_user):
        """Testa validação de número de documento"""
        invalid_bi_data = {
            "nome_completo": "Test User",
            "numero_documento": "123",  # Muito curto
            "data_nascimento": "1990-01-01",
        }

        response = client.post(
            "/api/v2/citizenship/bi-updates",
            json=invalid_bi_data,
            headers=auth_headers_user,
        )

        assert response.status_code == 422

    def test_required_fields_validation(self, client, auth_headers_user):
        """Testa validação de campos obrigatórios"""
        incomplete_data = {
            "nome_completo": "Test User"
            # Campos obrigatórios faltando
        }

        response = client.post(
            "/api/v2/citizenship/bi-updates",
            json=incomplete_data,
            headers=auth_headers_user,
        )

        assert response.status_code == 422


class TestErrorHandlingAPI:
    """Testes de tratamento de erros da API"""

    def test_404_not_found(self, client, auth_headers_user):
        """Testa retorno 404 para recurso inexistente"""
        response = client.get("/api/v2/nonexistent-endpoint", headers=auth_headers_user)
        assert response.status_code == 404

    def test_401_unauthorized(self, client):
        """Testa retorno 401 para acesso não autorizado"""
        response = client.get("/api/v2/users/me")
        assert response.status_code == 401

    def test_403_forbidden(self, client, auth_headers_user):
        """Testa retorno 403 para acesso proibido"""
        response = client.delete("/api/v2/users/all", headers=auth_headers_user)
        assert response.status_code == 403

    def test_422_validation_error(self, client, auth_headers_user):
        """Testa retorno 422 para erro de validação"""
        response = client.post("/api/v2/users", json={}, headers=auth_headers_user)
        assert response.status_code == 422

    def test_500_server_error_handling(self, client, auth_headers_user):
        """Testa tratamento de erro interno do servidor"""
        with patch("modules.users.service.UserService.create_user") as mock_create:
            mock_create.side_effect = Exception("Database error")

            user_data = {
                "email": "test@example.com",
                "username": "testuser",
                "full_name": "Test User",
            }

            response = client.post("/api/v2/users", json=user_data, headers=auth_headers_user)
            assert response.status_code == 500


class TestPaginationAPI:
    """Testes de paginação de endpoints de listagem"""

    def test_pagination_default_values(self, client, auth_headers_user, test_data_factory):
        """Testa valores padrão de paginação"""
        # Criar múltiplos registros
        for _ in range(25):
            test_data_factory.create_user()
            # Simular criação via API (mock)

        response = client.get("/api/v2/users", headers=auth_headers_user)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert len(data["items"]) <= 20  # Default page size

    def test_pagination_custom_page_size(self, client, auth_headers_user):
        """Testa paginação com tamanho de página customizado"""
        params = {"page": 1, "size": 5}
        response = client.get("/api/v2/users", params=params, headers=auth_headers_user)

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 5

    def test_pagination_out_of_bounds(self, client, auth_headers_user):
        """Testa paginação com página fora dos limites"""
        params = {"page": 999, "size": 10}
        response = client.get("/api/v2/users", params=params, headers=auth_headers_user)

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0
