"""
Testes de Cross-Module Integration: Sanitation → Monitoring → Notifications

Este teste valida o fluxo completo de integração entre:
1. Módulo Sanitation (criação de registros de saneamento)
2. Módulo Monitoring (geração de alertas e métricas)
3. Módulo Notifications (envio de notificações para stakeholders)

Fluxo de Negócio:
- Registro de problema de saneamento → Monitoramento automático → Notificação stakeholders
"""

from datetime import UTC, datetime, timedelta

import pytest


# Mock imports para evitar dependências de FastAPI
class MockSanitationService:
    """Mock do SanitationService para testes."""

    VALID_SERVICE_TYPES = [
        "Coleta de Lixo",
        "Tratamento de Água",
        "Manutenção de Rede",
        "Contaminação Química",
        "Limpeza Pública",
        "Desinfecção",
    ]

    VALID_STATUSES = ["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "CANCELADO"]
    PRIORITIES = ["BAIXA", "MEDIA", "ALTA"]

    def __init__(self):
        self.records = []
        self.alerts_generated = []

    async def create_record(self, record_data):
        """Cria registro de saneamento."""
        if not await self.validate_record_data(record_data):
            raise ValueError("Dados do registro inválidos")

        record = {
            "id": len(self.records) + 1,
            **record_data,
            "created_at": datetime.now(UTC),
            "status": "PENDENTE",
        }
        self.records.append(record)

        # Simula geração de alerta para problemas críticos
        if record_data.get("priority") == "ALTA":
            await self._generate_critical_alert(record)

        return record

    async def validate_record_data(self, data):
        """Valida dados do registro."""
        required_fields = ["service_type", "location", "priority"]
        return all(field in data for field in required_fields)

    async def _generate_critical_alert(self, record):
        """Gera alerta crítico automaticamente."""
        alert = {
            "id": len(self.alerts_generated) + 1,
            "source_module": "sanitation",
            "record_id": record["id"],
            "severity": "CRITICAL",
            "message": f"Problema crítico de saneamento: {record['service_type']}",
            "location": record["location"],
            "timestamp": datetime.now(UTC),
        }
        self.alerts_generated.append(alert)
        return alert


class MockMonitoringService:
    """Mock do MonitoringService para testes."""

    def __init__(self):
        self.alerts = []
        self.metrics = []
        self.notifications_sent = []

    async def create_alert(self, alert_data):
        """Cria alerta de monitoramento."""
        alert = {
            "id": len(self.alerts) + 1,
            **alert_data,
            "created_at": datetime.now(UTC),
            "status": "ACTIVE",
        }
        self.alerts.append(alert)

        # Simula envio de notificação para alertas críticos
        if alert_data.get("severity") in ["HIGH", "CRITICAL"]:
            await self._trigger_notification(alert)

        return alert

    async def create_metric(self, metric_data):
        """Cria métrica de monitoramento."""
        metric = {
            "id": len(self.metrics) + 1,
            **metric_data,
            "timestamp": datetime.now(UTC),
        }
        self.metrics.append(metric)
        return metric

    async def _trigger_notification(self, alert):
        """Dispara notificação baseada no alerta."""
        notification = {
            "alert_id": alert["id"],
            "type": "ALERT_NOTIFICATION",
            "message": alert["message"],
            "severity": alert["severity"],
            "timestamp": datetime.now(UTC),
        }
        self.notifications_sent.append(notification)
        return notification

    async def get_active_alerts(self, source_module=None):
        """Obtém alertas ativos."""
        if source_module:
            return [
                a
                for a in self.alerts
                if a.get("source_module") == source_module and a["status"] == "ACTIVE"
            ]
        return [a for a in self.alerts if a["status"] == "ACTIVE"]


class MockNotificationService:
    """Mock do NotificationService para testes."""

    def __init__(self):
        self.notifications = []
        self.delivery_queue = []
        self.templates = {
            "SANITATION_ALERT": {
                "subject": "Alerta de Saneamento - {severity}",
                "body": "Problema detectado em {location}: {message}",
            },
            "CRITICAL_ESCALATION": {
                "subject": "ESCALAÇÃO CRÍTICA - {service_type}",
                "body": "Problema crítico requer intervenção imediata: {details}",
            },
        }

    async def send_notification(self, notification_data):
        """Envia notificação."""
        notification = {
            "id": len(self.notifications) + 1,
            **notification_data,
            "sent_at": datetime.now(UTC),
            "status": "SENT",
        }
        self.notifications.append(notification)

        # Simula entrega
        await self._process_delivery(notification)
        return notification

    async def send_bulk_notification(self, notifications_data):
        """Envia notificações em lote."""
        results = []
        for data in notifications_data:
            result = await self.send_notification(data)
            results.append(result)
        return results

    async def _process_delivery(self, notification):
        """Processa entrega da notificação."""
        delivery = {
            "notification_id": notification["id"],
            "channel": notification.get("channel", "EMAIL"),
            "status": "DELIVERED",
            "delivered_at": datetime.now(UTC),
        }
        self.delivery_queue.append(delivery)
        return delivery

    async def get_notification_stats(self, date_range=None):
        """Obtém estatísticas de notificações."""
        total = len(self.notifications)
        delivered = len([d for d in self.delivery_queue if d["status"] == "DELIVERED"])

        return {
            "total_sent": total,
            "total_delivered": delivered,
            "delivery_rate": delivered / total if total > 0 else 0,
            "date_range": date_range,
        }


class TestSanitationMonitoringNotificationFlow:
    """Testes de integração do fluxo Sanitation → Monitoring → Notifications."""

    @pytest.fixture
    def sanitation_service(self):
        """Fixture para SanitationService."""
        return MockSanitationService()

    @pytest.fixture
    def monitoring_service(self):
        """Fixture para MonitoringService."""
        return MockMonitoringService()

    @pytest.fixture
    def notification_service(self):
        """Fixture para NotificationService."""
        return MockNotificationService()

    @pytest.fixture
    def sample_sanitation_record(self):
        """Dados de exemplo para registro de saneamento."""
        return {
            "service_type": "Contaminação Química",
            "location": "Bairro Industrial, Luanda",
            "priority": "ALTA",
            "description": "Vazamento de produto químico detectado",
            "reported_by": "João Silva",
            "contact_phone": "+244 923 456 789",
        }

    @pytest.fixture
    def sample_stakeholders(self):
        """Stakeholders para notificação."""
        return [
            {
                "id": 1,
                "name": "Departamento de Saneamento",
                "email": "sanitation@sila.gov.ao",
                "role": "RESPONSIBLE",
            },
            {
                "id": 2,
                "name": "Autoridade Ambiental",
                "email": "environment@sila.gov.ao",
                "role": "SUPERVISOR",
            },
        ]

    # Testes do Fluxo Principal
    @pytest.mark.asyncio
    async def test_complete_sanitation_alert_flow(
        self,
        sanitation_service,
        monitoring_service,
        notification_service,
        sample_sanitation_record,
        sample_stakeholders,
    ):
        """Testa fluxo completo: registro → alerta → notificação."""

        # 1. Criar registro de saneamento crítico
        record = await sanitation_service.create_record(sample_sanitation_record)

        assert record["id"] is not None
        assert record["status"] == "PENDENTE"
        assert record["priority"] == "ALTA"

        # 2. Verificar geração automática de alerta
        assert len(sanitation_service.alerts_generated) == 1
        sanitation_alert = sanitation_service.alerts_generated[0]

        # 3. Criar alerta formal no sistema de monitoramento
        monitoring_alert = await monitoring_service.create_alert(
            {
                "source_module": "sanitation",
                "record_id": record["id"],
                "severity": "CRITICAL",
                "message": sanitation_alert["message"],
                "location": record["location"],
                "source": "automatic_detection",
            }
        )

        assert monitoring_alert["id"] is not None
        assert monitoring_alert["severity"] == "CRITICAL"

        # 4. Verificar disparo automático de notificação
        assert len(monitoring_service.notifications_sent) == 1
        monitoring_service.notifications_sent[0]

        # 5. Enviar notificações formais para stakeholders
        stakeholder_notifications = []
        for stakeholder in sample_stakeholders:
            notification = await notification_service.send_notification(
                {
                    "recipient_id": stakeholder["id"],
                    "recipient_email": stakeholder["email"],
                    "recipient_name": stakeholder["name"],
                    "type": "SANITATION_ALERT",
                    "channel": "EMAIL",
                    "subject": f"Alerta Crítico: {record['service_type']}",
                    "body": f"Problema detectado em {record['location']}: {record['description']}",
                    "priority": "HIGH",
                    "alert_id": monitoring_alert["id"],
                }
            )
            stakeholder_notifications.append(notification)

        # 6. Verificar entregas
        assert len(stakeholder_notifications) == len(sample_stakeholders)
        assert len(notification_service.delivery_queue) == len(sample_stakeholders)

        # 7. Verificar estatísticas
        stats = await notification_service.get_notification_stats()
        assert stats["total_sent"] == len(sample_stakeholders)
        assert stats["total_delivered"] == len(sample_stakeholders)
        assert stats["delivery_rate"] == 1.0

    @pytest.mark.asyncio
    async def test_sanitation_metrics_monitoring_integration(
        self, sanitation_service, monitoring_service
    ):
        """Testa integração de métricas entre saneamento e monitoramento."""

        # Criar múltiplos registros para gerar métricas
        records_data = [
            {
                "service_type": "Coleta de Lixo",
                "location": "Bairro Central",
                "priority": "MEDIA",
            },
            {
                "service_type": "Tratamento de Água",
                "location": "Zona Norte",
                "priority": "BAIXA",
            },
            {
                "service_type": "Manutenção de Rede",
                "location": "Bairro Sul",
                "priority": "ALTA",
            },
        ]

        created_records = []
        for data in records_data:
            record = await sanitation_service.create_record(data)
            created_records.append(record)

        # Gerar métricas de monitoramento
        metrics = await monitoring_service.create_metric(
            {
                "source_module": "sanitation",
                "metric_type": "service_requests",
                "total_records": len(created_records),
                "by_priority": {"ALTA": 1, "MEDIA": 1, "BAIXA": 1},
                "by_service_type": {
                    "Coleta de Lixo": 1,
                    "Tratamento de Água": 1,
                    "Manutenção de Rede": 1,
                },
            }
        )

        assert metrics["id"] is not None
        assert metrics["total_records"] == 3
        assert metrics["by_priority"]["ALTA"] == 1

    @pytest.mark.asyncio
    async def test_escalation_flow_critical_sanitation_issue(
        self, sanitation_service, monitoring_service, notification_service
    ):
        """Testa fluxo de escalonamento para problemas críticos."""

        # Criar registro crítico
        critical_record = await sanitation_service.create_record(
            {
                "service_type": "Contaminação Química",
                "location": "Escola Primária Central",
                "priority": "ALTA",
                "description": "Vazamento tóxico próximo à área infantil",
                "risk_level": "CRITICAL",
            }
        )

        # Gerar alerta crítico
        critical_alert = await monitoring_service.create_alert(
            {
                "source_module": "sanitation",
                "record_id": critical_record["id"],
                "severity": "CRITICAL",
                "message": "RISCO IMINENTE: Contaminação em área escolar",
                "location": critical_record["location"],
                "escalation_required": True,
                "response_time_minutes": 30,
            }
        )

        # Enviar notificação de escalonamento
        escalation_notification = await notification_service.send_notification(
            {
                "recipient_id": "emergency_response",
                "recipient_email": "emergency@sila.gov.ao",
                "type": "CRITICAL_ESCALATION",
                "channel": "SMS",
                "subject": "ESCALAÇÃO CRÍTICA - Resposta Imediata",
                "body": f"EMERGÊNCIA: {critical_alert['message']} em {critical_alert['location']}",
                "priority": "URGENT",
                "requires_acknowledgment": True,
                "response_deadline": datetime.now(UTC) + timedelta(minutes=30),
            }
        )

        assert escalation_notification["priority"] == "URGENT"
        assert escalation_notification["requires_acknowledgment"] is True

    @pytest.mark.asyncio
    async def test_bulk_notification_sanitation_campaign(self, notification_service):
        """Testa envio em lote para campanha de saneamento."""

        # Preparar notificações em lote
        bulk_notifications = [
            {
                "recipient_id": f"citizen_{i}",
                "recipient_email": f"citizen{i}@example.com",
                "type": "SANITATION_CAMPAIGN",
                "channel": "EMAIL",
                "subject": "Campanha de Limpeza Urbana",
                "body": "Participe da campanha de limpeza neste fim de semana",
            }
            for i in range(100)
        ]

        # Enviar em lote
        results = await notification_service.send_bulk_notification(bulk_notifications)

        assert len(results) == 100
        assert all(r["status"] == "SENT" for r in results)
        assert len(notification_service.delivery_queue) == 100

    @pytest.mark.asyncio
    async def test_monitoring_dashboard_integration(self, monitoring_service):
        """Testa integração com dashboard de monitoramento."""

        # Criar alertas de diferentes severidades
        alerts_data = [
            {"severity": "LOW", "source_module": "sanitation"},
            {"severity": "MEDIUM", "source_module": "sanitation"},
            {"severity": "HIGH", "source_module": "sanitation"},
            {"severity": "CRITICAL", "source_module": "sanitation"},
        ]

        for alert_data in alerts_data:
            await monitoring_service.create_alert(
                {
                    **alert_data,
                    "message": f"Alerta {alert_data['severity']}",
                    "location": "Test Location",
                }
            )

        # Obter alertas ativos do módulo sanitation
        active_alerts = await monitoring_service.get_active_alerts("sanitation")

        assert len(active_alerts) == 4

        # Verificar distribuição por severidade
        severity_counts = {}
        for alert in active_alerts:
            severity = alert["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        assert severity_counts["LOW"] == 1
        assert severity_counts["MEDIUM"] == 1
        assert severity_counts["HIGH"] == 1
        assert severity_counts["CRITICAL"] == 1

    @pytest.mark.asyncio
    async def test_error_handling_cross_module_integration(
        self, sanitation_service, monitoring_service, notification_service
    ):
        """Testa tratamento de erros na integração entre módulos."""

        # Testar falha na criação de registro
        with pytest.raises(ValueError, match="Dados do registro inválidos"):
            await sanitation_service.create_record(
                {
                    "service_type": "Coleta de Lixo"
                    # Faltando campos obrigatórios
                }
            )

        # Verificar que nenhum alerta foi gerado
        assert len(sanitation_service.alerts_generated) == 0
        assert len(monitoring_service.alerts) == 0
        assert len(notification_service.notifications) == 0

    @pytest.mark.asyncio
    async def test_performance_large_volume_integration(
        self, sanitation_service, monitoring_service, notification_service
    ):
        """Testa performance com grande volume de dados."""

        import time

        start_time = time.time()

        # Criar 1000 registros
        records = []
        for i in range(1000):
            record = await sanitation_service.create_record(
                {
                    "service_type": "Coleta de Lixo",
                    "location": f"Location {i}",
                    "priority": "MEDIA" if i % 2 == 0 else "ALTA",
                }
            )
            records.append(record)

        # Gerar métricas
        metrics = await monitoring_service.create_metric(
            {
                "source_module": "sanitation",
                "metric_type": "bulk_processing",
                "total_processed": len(records),
                "processing_time_seconds": time.time() - start_time,
            }
        )

        # Verificar performance
        processing_time = time.time() - start_time
        assert processing_time < 5.0  # Deve processar em menos de 5 segundos
        assert len(records) == 1000
        assert metrics["total_processed"] == 1000
