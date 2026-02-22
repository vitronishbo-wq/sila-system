"""
Testes unitários para o módulo de notificações

Foco em lógica crítica de negócio:
- NotificationService: criação, busca, processamento de templates
- Validação de dados e canais de notificação
- Processamento de templates com variáveis
- Controle de prioridades e agendamento
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from modules.notifications.schemas.notifications import (
    NotificationCreate,
    NotificationFilters,
    NotificationStatistics,
)

# Importar as classes que queremos testar
from modules.notifications.services.notification_service import (
    NotificationService,
)


class TestNotificationService:
    """Testes para NotificationService - lógica crítica de notificações"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock de sessão de banco de dados assíncrona"""
        return AsyncMock()

    @pytest.fixture
    def sample_notification_data(self):
        """Dados de exemplo para notificação"""
        return NotificationCreate(
            recipient_id=uuid4(),
            recipient_email="test@example.com",
            recipient_phone="+5511999999999",
            notification_type="info",
            priority="normal",
            subject="Teste de Notificação",
            body="Este é um teste de notificação",
            channels=["email", "sms"],
            scheduled_at=None,
            variables={},
            metadata={},
        )

    def test_priority_to_int_mapping(self):
        """Testar conversão de prioridade string para int"""
        # Testar prioridades válidas
        assert NotificationService._priority_to_int("low") == 2
        assert NotificationService._priority_to_int("normal") == 5
        assert NotificationService._priority_to_int("high") == 8
        assert NotificationService._priority_to_int("urgent") == 9
        assert NotificationService._priority_to_int("critical") == 10

        # Testar prioridade inválida (deve retornar normal)
        assert NotificationService._priority_to_int("invalid") == 5

    def test_process_template_without_template(self, sample_notification_data):
        """Testar processamento de template quando não há template"""
        subject, body = NotificationService._process_template(
            template=None,
            variables=sample_notification_data.variables,
            fallback_subject=sample_notification_data.subject,
            fallback_body=sample_notification_data.body,
        )

        assert subject == sample_notification_data.subject
        assert body == sample_notification_data.body

    def test_process_template_with_variables(self):
        """Testar processamento de template com variáveis"""
        template_subject = "Olá {name}, você tem {count} mensagens"
        template_body = (
            "Prezado {name}, você recebeu {count} novas mensagens no sistema."
        )

        variables = {"name": "João", "count": 5}

        subject, body = NotificationService._process_template(
            template=MagicMock(subject=template_subject, body=template_body),
            variables=variables,
            fallback_subject="Fallback Subject",
            fallback_body="Fallback Body",
        )

        assert subject == "Olá João, você tem 5 mensagens"
        assert body == "Prezado João, você recebeu 5 novas mensagens no sistema."

    def test_process_template_missing_variables(self):
        """Testar processamento com variáveis faltantes (deve manter placeholders)"""
        template_subject = "Olá {name}, você tem {count} mensagens"
        template_body = "Prezado {name}, você recebeu {count} mensagens."

        variables = {"name": "João"}  # count está faltando

        subject, body = NotificationService._process_template(
            template=MagicMock(subject=template_subject, body=template_body),
            variables=variables,
            fallback_subject="Fallback",
            fallback_body="Fallback",
        )

        # Placeholders não substituídos devem permanecer
        assert "{count}" in subject
        assert "{count}" in body
        assert "João" in subject  # Variável existente deve ser substituída

    @pytest.mark.asyncio
    async def test_create_notification_success(
        self, mock_db_session, sample_notification_data
    ):
        """Testar criação de notificação bem-sucedida"""
        sender_id = uuid4()

        # Mock template
        mock_template = MagicMock()
        mock_template.id = uuid4()
        mock_template.is_active = True
        mock_template.usage_count = 0

        # Mock recipient settings
        mock_settings = MagicMock()
        mock_settings.email_notifications = True
        mock_settings.sms_notifications = True

        # Mock notification
        mock_notification = MagicMock()
        mock_notification.id = uuid4()
        mock_notification.recipient_id = sample_notification_data.recipient_id
        mock_notification.subject = sample_notification_data.subject
        mock_notification.body = sample_notification_data.body
        mock_notification.channels = ["email", "sms"]
        mock_notification.status = "pending"
        mock_notification.created_at = datetime.utcnow()

        # Mock queue item
        mock_queue = MagicMock()
        mock_queue.notification_id = mock_notification.id
        mock_queue.priority = 5
        mock_queue.scheduled_for = datetime.utcnow()

        # Configurar mocks
        mock_db_session.query.return_value.filter.return_value.first.side_effect = [
            mock_template,  # Template lookup
            mock_settings,  # Settings lookup
        ]
        mock_db_session.add.side_effect = lambda x: setattr(x, "id", uuid4())
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()

        with patch.object(NotificationService, "_notification_to_dict") as mock_to_dict:
            mock_to_dict.return_value = {
                "id": mock_notification.id,
                "recipient_id": sample_notification_data.recipient_id,
                "subject": sample_notification_data.subject,
                "status": "pending",
            }

            result = await NotificationService.create_notification(
                db=mock_db_session,
                notification_data=sample_notification_data,
                sender_id=sender_id,
            )

            # Verificações
            assert result.id == mock_notification.id
            assert result.subject == sample_notification_data.subject
            mock_db_session.add.assert_called()  # Notification added
            mock_db_session.commit.assert_called()

    @pytest.mark.asyncio
    async def test_create_notification_no_channels_enabled(
        self, mock_db_session, sample_notification_data
    ):
        """Testar erro quando nenhum canal está habilitado"""
        sender_id = uuid4()

        # Mock settings with all channels disabled
        mock_settings = MagicMock()
        mock_settings.email_notifications = False
        mock_settings.sms_notifications = False
        mock_settings.push_notifications = False
        mock_settings.in_app_notifications = False

        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_settings
        )

        with pytest.raises(ValueError, match="Nenhum canal habilitado"):
            await NotificationService.create_notification(
                db=mock_db_session,
                notification_data=sample_notification_data,
                sender_id=sender_id,
            )

    @pytest.mark.asyncio
    async def test_create_notification_template_not_found(
        self, mock_db_session, sample_notification_data
    ):
        """Testar erro quando template não é encontrado"""
        sender_id = uuid4()

        # Configurar para template não encontrado
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError, match="Template não encontrado"):
            await NotificationService.create_notification(
                db=mock_db_session,
                notification_data=sample_notification_data,
                sender_id=sender_id,
            )

    @pytest.mark.asyncio
    async def test_get_user_notifications_basic(self, mock_db_session):
        """Testar busca básica de notificações do usuário"""
        user_id = uuid4()

        # Mock notifications
        mock_notifications = [
            MagicMock(
                id=uuid4(), subject="Notificação 1", created_at=datetime.utcnow()
            ),
            MagicMock(
                id=uuid4(),
                subject="Notificação 2",
                created_at=datetime.utcnow() - timedelta(hours=1),
            ),
        ]

        # Mock query chain
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = mock_notifications
        mock_query.count.return_value = 2

        mock_db_session.query.return_value = mock_query

        with patch.object(NotificationService, "_notification_to_dict") as mock_to_dict:
            mock_to_dict.side_effect = [
                {"id": mock_notifications[0].id, "subject": "Notificação 1"},
                {"id": mock_notifications[1].id, "subject": "Notificação 2"},
            ]

            result, total = await NotificationService.get_user_notifications(
                db=mock_db_session, user_id=user_id, page=1, size=10
            )

            assert len(result) == 2
            assert total == 2
            assert result[0].subject == "Notificação 1"
            assert result[1].subject == "Notificação 2"

    @pytest.mark.asyncio
    async def test_get_user_notifications_with_filters(self, mock_db_session):
        """Testar busca com filtros aplicados"""
        user_id = uuid4()
        template_id = uuid4()

        # Mock query chain com filtros
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query  # Aplicar filtros
        mock_query.options.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.all.return_value = [MagicMock()]

        mock_db_session.query.return_value = mock_query

        filters = NotificationFilters(
            notification_type="info",
            status="delivered",
            template_id=template_id,
            read_status=True,
        )

        with patch.object(NotificationService, "_notification_to_dict") as mock_to_dict:
            mock_to_dict.return_value = {"id": uuid4(), "subject": "Filtered"}

            result, total = await NotificationService.get_user_notifications(
                db=mock_db_session, user_id=user_id, filters=filters, page=1, size=10
            )

            # Verificar que filtros foram aplicados (múltiplas chamadas filter)
            assert (
                mock_query.filter.call_count >= 4
            )  # notification_type, status, template_id, read_status

    @pytest.mark.asyncio
    async def test_mark_notification_read_success(self, mock_db_session):
        """Testar marcação de notificação como lida"""
        notification_id = uuid4()
        user_id = uuid4()

        # Mock notification not read yet
        mock_notification = MagicMock()
        mock_notification.id = notification_id
        mock_notification.recipient_id = user_id
        mock_notification.read_at = None
        mock_notification.status = "sent"

        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_notification
        )
        mock_db_session.commit = AsyncMock()

        with patch.object(NotificationService, "_log_user_action") as mock_log:
            mock_log = AsyncMock()

            result = await NotificationService.mark_notification_read(
                db=mock_db_session, notification_id=notification_id, user_id=user_id
            )

            assert result is True
            assert mock_notification.read_at is not None
            assert mock_notification.status == "read"
            mock_db_session.commit.assert_called()

    @pytest.mark.asyncio
    async def test_mark_notification_read_not_found(self, mock_db_session):
        """Testar marcação de notificação inexistente"""
        notification_id = uuid4()
        user_id = uuid4()

        # Notification not found
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        result = await NotificationService.mark_notification_read(
            db=mock_db_session, notification_id=notification_id, user_id=user_id
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_mark_notification_read_already_read(self, mock_db_session):
        """Testar marcação de notificação já lida"""
        notification_id = uuid4()
        user_id = uuid4()

        # Mock notification already read
        mock_notification = MagicMock()
        mock_notification.id = notification_id
        mock_notification.recipient_id = user_id
        mock_notification.read_at = datetime.utcnow() - timedelta(hours=1)
        mock_notification.status = "read"

        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_notification
        )

        result = await NotificationService.mark_notification_read(
            db=mock_db_session, notification_id=notification_id, user_id=user_id
        )

        assert result is True
        # Não deve alterar se já lida
        mock_db_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_notification_statistics(self, mock_db_session):
        """Testar obtenção de estatísticas de notificações"""
        user_id = uuid4()

        # Mock query results
        mock_db_session.query.return_value.filter.return_value.count.side_effect = [
            10,
            3,
            5,
            2,
        ]  # total, delivered, read
        mock_db_session.query.return_value.filter.return_value.with_entities.return_value.group_by.return_value.all.side_effect = [
            [("info", 5), ("warning", 3), ("error", 2)],  # by type
            [("sent", 3), ("delivered", 5), ("read", 2)],  # by status
        ]

        mock_db_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = [
            MagicMock(created_at=datetime.utcnow())
        ]

        result = await NotificationService.get_notification_statistics(
            db=mock_db_session, user_id=user_id
        )

        assert isinstance(result, NotificationStatistics)
        assert result.total_notifications == 10
        assert result.delivery_rate == 50.0  # 5/10 * 100
        assert result.read_rate == 40.0  # 2/5 * 100
        assert "info" in result.notifications_by_type
        assert "sent" in result.notifications_by_status

    @pytest.mark.asyncio
    async def test_get_notification_statistics_empty(self, mock_db_session):
        """Testar estatísticas quando não há notificações"""
        user_id = uuid4()

        # Mock empty results
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0
        mock_db_session.query.return_value.filter.return_value.with_entities.return_value.group_by.return_value.all.return_value = (
            []
        )
        mock_db_session.query.return_value.order_by.return_value.limit.return_value.all.return_value = (
            []
        )

        result = await NotificationService.get_notification_statistics(
            db=mock_db_session, user_id=user_id
        )

        assert result.total_notifications == 0
        assert result.delivery_rate == 0.0
        assert result.read_rate == 0.0
        assert len(result.notifications_by_type) == 0
        assert len(result.recent_activity) == 0

    def test_notification_to_dict_basic(self, mock_db_session):
        """Testar conversão de notification para dict"""
        # Mock notification
        mock_notification = MagicMock()
        mock_notification.id = uuid4()
        mock_notification.recipient_id = uuid4()
        mock_notification.subject = "Test Subject"
        mock_notification.body = "Test Body"
        mock_notification.status = "sent"
        mock_notification.sent_at = datetime.utcnow()

        # Mock sender
        mock_sender = MagicMock()
        mock_sender.full_name = "Test Sender"

        # Mock template
        mock_template = MagicMock()
        mock_template.name = "Test Template"

        # Configurar query chain
        mock_db_session.query.side_effect = [
            MagicMock(),  # Citizen query (sender)
            MagicMock(),  # Template query
        ]
        mock_db_session.query.return_value.filter.return_value.first.side_effect = [
            mock_sender,  # Sender found
            mock_template,  # Template found
        ]

        # Testar conversão
        result = NotificationService._notification_to_dict(
            mock_db_session, mock_notification
        )

        assert result["id"] == mock_notification.id
        assert result["subject"] == "Test Subject"
        assert result["sent_by_name"] == "Test Sender"
        assert result["template_name"] == "Test Template"

    def test_notification_to_dict_no_sender(self, mock_db_session):
        """Testar conversão quando remetente não é encontrado"""
        mock_notification = MagicMock()
        mock_notification.id = uuid4()
        mock_notification.subject = "Test Subject"
        mock_notification.sent_by = uuid4()

        # Configurar para sender não encontrado
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        with patch.object(NotificationService, "_log_user_action"):
            result = NotificationService._notification_to_dict(
                mock_db_session, mock_notification
            )

            assert (
                result["sent_by_name"] == "Sistema"
            )  # Default quando não encontra sender
