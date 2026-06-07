"""
Testes de Cross-Module Integration: Health → Monitoring → Notifications

Este teste valida o fluxo completo de integração entre:
1. Módulo Health (gestão de pacientes e registros médicos)
2. Módulo Monitoring (alertas de saúde e métricas)
3. Módulo Notifications (comunicação com pacientes e profissionais)

Fluxo de Negócio:
- Registro médico → Monitoramento de sinais vitais → Alertas automáticos → Notificações
"""

import asyncio
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest


class MockHealthService:
    """Mock do HealthService para testes."""

    def __init__(self):
        self.patients = []
        self.medical_records = []
        self.vital_signs = []
        self.appointments = []

    async def register_patient(self, patient_data):
        """Registra novo paciente."""
        patient = {
            "id": len(self.patients) + 1,
            **patient_data,
            "registered_at": datetime.now(UTC),
            "status": "ACTIVE",
        }
        self.patients.append(patient)
        return patient

    async def create_medical_record(self, record_data):
        """Cria registro médico."""
        record = {
            "id": len(self.medical_records) + 1,
            **record_data,
            "created_at": datetime.now(UTC),
        }
        self.medical_records.append(record)
        return record

    async def record_vital_signs(self, patient_id, vital_data):
        """Registra sinais vitais do paciente."""
        patient = next((p for p in self.patients if p["id"] == patient_id), None)
        if not patient:
            raise ValueError("Paciente não encontrado")

        vital_sign = {
            "id": len(self.vital_signs) + 1,
            "patient_id": patient_id,
            **vital_data,
            "recorded_at": datetime.now(UTC),
        }
        self.vital_signs.append(vital_sign)

        # Verificar se há alertas críticos
        alerts = self._check_vital_signs_alerts(vital_sign)
        return vital_sign, alerts

    async def schedule_appointment(self, appointment_data):
        """Agenda consulta médica."""
        appointment = {
            "id": len(self.appointments) + 1,
            **appointment_data,
            "created_at": datetime.now(UTC),
            "status": "SCHEDULED",
        }
        self.appointments.append(appointment)
        return appointment

    def _check_vital_signs_alerts(self, vital_sign):
        """Verifica alertas nos sinais vitais."""
        alerts = []

        # Verificar pressão arterial
        systolic = vital_sign.get("blood_pressure_systolic", 120)
        diastolic = vital_sign.get("blood_pressure_diastolic", 80)

        if systolic > 180 or diastolic > 120:
            alerts.append(
                {
                    "type": "HYPERTENSION_CRISIS",
                    "severity": "CRITICAL",
                    "message": "Crise hipertensiva detectada",
                }
            )
        elif systolic > 140 or diastolic > 90:
            alerts.append(
                {
                    "type": "HYPERTENSION",
                    "severity": "HIGH",
                    "message": "Hipertensão detectada",
                }
            )

        # Verificar frequência cardíaca
        heart_rate = vital_sign.get("heart_rate", 70)
        if heart_rate > 120 or heart_rate < 40:
            alerts.append(
                {
                    "type": "HEART_RATE_ABNORMAL",
                    "severity": "HIGH",
                    "message": "Frequência cardíaca anormal",
                }
            )

        # Verificar temperatura
        temperature = vital_sign.get("temperature", 36.5)
        if temperature > 39.0:
            alerts.append(
                {
                    "type": "HIGH_FEVER",
                    "severity": "MEDIUM",
                    "message": "Febre alta detectada",
                }
            )

        # Verificar saturação de oxigênio
        oxygen_saturation = vital_sign.get("oxygen_saturation", 98)
        if oxygen_saturation < 90:
            alerts.append(
                {
                    "type": "HYPOXIA",
                    "severity": "CRITICAL",
                    "message": "Hipoxia detectada - saturação baixa",
                }
            )

        return alerts

    async def get_patient_history(self, patient_id):
        """Obtém histórico completo do paciente."""
        patient = next((p for p in self.patients if p["id"] == patient_id), None)
        if not patient:
            raise ValueError("Paciente não encontrado")

        records = [r for r in self.medical_records if r["patient_id"] == patient_id]
        vitals = [v for v in self.vital_signs if v["patient_id"] == patient_id]
        appointments = [a for a in self.appointments if a["patient_id"] == patient_id]

        return {
            "patient": patient,
            "medical_records": records,
            "vital_signs": vitals,
            "appointments": appointments,
        }


class MockHealthMonitoringService:
    """Mock do MonitoringService especializado para saúde."""

    def __init__(self, health_service=None):
        self.health_alerts = []
        self.monitoring_sessions = []
        self.escalation_rules = []
        self.health_service = health_service

    async def create_health_alert(self, alert_data):
        """Cria alerta de saúde."""
        alert = {
            "id": len(self.health_alerts) + 1,
            **alert_data,
            "created_at": datetime.now(UTC),
            "status": "ACTIVE",
        }
        self.health_alerts.append(alert)

        # Verificar regras de escalonamento
        if alert["severity"] in ["HIGH", "CRITICAL"]:
            await self._check_escalation_rules(alert)

        return alert

    async def start_monitoring_session(self, session_data):
        """Inicia sessão de monitoramento."""
        session = {
            "id": len(self.monitoring_sessions) + 1,
            **session_data,
            "started_at": datetime.now(UTC),
            "status": "ACTIVE",
        }
        self.monitoring_sessions.append(session)
        return session

    async def analyze_trends(self, patient_id, time_range_hours=24):
        """Analisa tendências de saúde do paciente."""
        vitals = []
        if self.health_service is not None:
            cutoff = datetime.now(UTC) - timedelta(hours=time_range_hours)
            vitals = [
                v
                for v in self.health_service.vital_signs
                if v["patient_id"] == patient_id and v["recorded_at"] >= cutoff
            ]

        bp_trend = "STABLE"
        hr_trend = "STABLE"
        overall_risk = "LOW"
        if len(vitals) >= 2:
            first_systolic = vitals[0].get("blood_pressure_systolic", 120)
            last_systolic = vitals[-1].get("blood_pressure_systolic", 120)
            if last_systolic > first_systolic:
                bp_trend = "INCREASING"
            elif last_systolic < first_systolic:
                bp_trend = "DECREASING"

            first_hr = vitals[0].get("heart_rate", 70)
            last_hr = vitals[-1].get("heart_rate", 70)
            if last_hr > first_hr:
                hr_trend = "INCREASING"
            elif last_hr < first_hr:
                hr_trend = "DECREASING"

            max_systolic = max(v.get("blood_pressure_systolic", 120) for v in vitals)
            max_diastolic = max(v.get("blood_pressure_diastolic", 80) for v in vitals)
            if max_systolic >= 180 or max_diastolic >= 120:
                overall_risk = "HIGH"
            elif max_systolic >= 140 or max_diastolic >= 90:
                overall_risk = "MEDIUM"
            else:
                overall_risk = "LOW"

        trends = {
            "patient_id": patient_id,
            "time_range_hours": time_range_hours,
            "blood_pressure_trend": bp_trend,
            "heart_rate_trend": hr_trend,
            "temperature_trend": "STABLE",
            "overall_risk": overall_risk,
            "recommendations": [
                "Continuar monitoramento",
                "Agendar consulta de acompanhamento",
            ],
        }
        return trends

    async def _check_escalation_rules(self, alert):
        """Verifica regras de escalonamento."""
        if alert["severity"] == "CRITICAL":
            escalation = {
                "alert_id": alert["id"],
                "escalated_to": "EMERGENCY_RESPONSE",
                "escalated_at": datetime.now(UTC),
                "reason": "Critical health alert requires immediate response",
            }
            self.escalation_rules.append(escalation)

    async def get_active_health_alerts(self, patient_id=None):
        """Obtém alertas de saúde ativos."""
        if patient_id:
            return [
                a
                for a in self.health_alerts
                if a["patient_id"] == patient_id and a["status"] == "ACTIVE"
            ]
        return [a for a in self.health_alerts if a["status"] == "ACTIVE"]


class MockHealthNotificationService:
    """Mock do NotificationService especializado para saúde."""

    def __init__(self):
        self.notifications = []
        self.emergency_alerts = []
        self.appointment_reminders = []
        self.health_campaigns = []

    async def send_health_alert(self, notification_data):
        """Envia alerta de saúde."""
        notification = {
            "id": len(self.notifications) + 1,
            **notification_data,
            "sent_at": datetime.now(UTC),
            "type": "HEALTH_ALERT",
        }
        self.notifications.append(notification)
        return notification

    async def send_emergency_alert(self, emergency_data):
        """Envia alerta de emergência."""
        alert = {
            "id": len(self.emergency_alerts) + 1,
            **emergency_data,
            "sent_at": datetime.now(UTC),
            "priority": "URGENT",
            "type": "EMERGENCY",
        }
        self.emergency_alerts.append(alert)
        return alert

    async def send_appointment_reminder(self, reminder_data):
        """Envia lembrete de consulta."""
        reminder = {
            "id": len(self.appointment_reminders) + 1,
            **reminder_data,
            "sent_at": datetime.now(UTC),
            "type": "APPOINTMENT_REMINDER",
        }
        self.appointment_reminders.append(reminder)
        return reminder

    async def send_health_campaign(self, campaign_data):
        """Envia campanha de saúde."""
        campaign = {
            "id": len(self.health_campaigns) + 1,
            **campaign_data,
            "sent_at": datetime.now(UTC),
            "type": "HEALTH_CAMPAIGN",
        }
        self.health_campaigns.append(campaign)
        return campaign

    async def send_bulk_health_notifications(self, notifications_data):
        """Envia notificações de saúde em lote."""
        results = []
        for data in notifications_data:
            if data.get("priority") == "URGENT":
                result = await self.send_emergency_alert(data)
            else:
                result = await self.send_health_alert(data)
            results.append(result)
        return results

    async def get_notification_statistics(self, date_range=None):
        """Obtém estatísticas de notificações de saúde."""
        total = len(self.notifications) + len(self.emergency_alerts)
        urgent = len(self.emergency_alerts)
        appointments = len(self.appointment_reminders)
        campaigns = len(self.health_campaigns)

        return {
            "total_notifications": total,
            "urgent_alerts": urgent,
            "appointment_reminders": appointments,
            "health_campaigns": campaigns,
            "date_range": date_range,
        }


class TestHealthMonitoringNotificationFlow:
    """Testes de integração do fluxo Health → Monitoring → Notifications."""

    @pytest.fixture
    def health_service(self):
        """Fixture para HealthService."""
        return MockHealthService()

    @pytest.fixture
    def monitoring_service(self, health_service):
        """Fixture para HealthMonitoringService."""
        return MockHealthMonitoringService(health_service=health_service)

    @pytest.fixture
    def notification_service(self):
        """Fixture para HealthNotificationService."""
        return MockHealthNotificationService()

    @pytest.fixture
    def sample_patient_data(self):
        """Dados de exemplo para paciente."""
        return {
            "name": "João Santos",
            "email": "joao.santos@email.com",
            "phone": "+244 923 456 789",
            "date_of_birth": "1985-06-15",
            "blood_type": "O+",
            "emergency_contact": "+244 923 111 222",
        }

    @pytest.fixture
    def sample_vital_signs(self):
        """Dados de exemplo para sinais vitais."""
        return {
            "blood_pressure_systolic": 185,
            "blood_pressure_diastolic": 125,
            "heart_rate": 95,
            "temperature": 36.8,
            "oxygen_saturation": 94,
            "respiratory_rate": 18,
        }

    # Testes do Fluxo Principal
    @pytest.mark.asyncio
    async def test_complete_critical_health_alert_flow(
        self,
        health_service,
        monitoring_service,
        notification_service,
        sample_patient_data,
        sample_vital_signs,
    ):
        """Testa fluxo completo: paciente crítico → alerta → notificação de emergência."""

        # 1. Registrar paciente
        patient = await health_service.register_patient(sample_patient_data)
        assert patient["id"] is not None
        assert patient["status"] == "ACTIVE"

        # 2. Registrar sinais vitais críticos
        vital_sign, alerts = await health_service.record_vital_signs(
            patient["id"], sample_vital_signs
        )

        assert vital_sign["id"] is not None
        assert len(alerts) > 0

        # 3. Criar alertas no sistema de monitoramento
        monitoring_alerts = []
        for alert in alerts:
            monitoring_alert = await monitoring_service.create_health_alert(
                {
                    "patient_id": patient["id"],
                    "alert_type": alert["type"],
                    "severity": alert["severity"],
                    "message": alert["message"],
                    "vital_sign_id": vital_sign["id"],
                    "source": "automatic_monitoring",
                }
            )
            monitoring_alerts.append(monitoring_alert)

        # 4. Verificar alertas críticos
        critical_alerts = [a for a in monitoring_alerts if a["severity"] == "CRITICAL"]
        assert len(critical_alerts) > 0

        # 5. Enviar notificações de emergência
        emergency_notifications = []
        for alert in critical_alerts:
            emergency_notification = await notification_service.send_emergency_alert(
                {
                    "patient_id": patient["id"],
                    "patient_name": patient["name"],
                    "emergency_contact": patient["emergency_contact"],
                    "alert_type": alert["alert_type"],
                    "message": f"EMERGÊNCIA MÉDICA: {alert['message']}",
                    "location": "Hospital Central",
                    "required_action": "IMMEDIATE_MEDICAL_ATTENTION",
                    "channels": ["SMS", "PHONE_CALL", "EMAIL"],
                }
            )
            emergency_notifications.append(emergency_notification)

        # 6. Verificar notificações enviadas
        assert len(emergency_notifications) == len(critical_alerts)
        assert all(n["priority"] == "URGENT" for n in emergency_notifications)

        # 7. Iniciar sessão de monitoramento contínuo
        monitoring_session = await monitoring_service.start_monitoring_session(
            {
                "patient_id": patient["id"],
                "session_type": "CONTINUOUS_MONITORING",
                "duration_minutes": 60,
                "alert_thresholds": {
                    "blood_pressure_systolic_max": 180,
                    "blood_pressure_diastolic_max": 120,
                    "oxygen_saturation_min": 90,
                },
            }
        )

        assert monitoring_session["status"] == "ACTIVE"

    @pytest.mark.asyncio
    async def test_appointment_reminder_system(
        self,
        health_service,
        monitoring_service,
        notification_service,
        sample_patient_data,
    ):
        """Testa sistema de lembretes de consultas."""

        # 1. Registrar paciente
        patient = await health_service.register_patient(sample_patient_data)

        # 2. Agendar consulta
        appointment_date = datetime.now(UTC) + timedelta(days=2)
        appointment = await health_service.schedule_appointment(
            {
                "patient_id": patient["id"],
                "doctor_id": str(uuid4()),
                "specialty": "Cardiologia",
                "scheduled_date": appointment_date,
                "reason": "Consulta de acompanhamento",
            }
        )

        assert appointment["status"] == "SCHEDULED"

        # 3. Criar alerta de monitoramento para lembrete
        await monitoring_service.create_health_alert(
            {
                "patient_id": patient["id"],
                "alert_type": "APPOINTMENT_REMINDER",
                "severity": "LOW",
                "message": "Lembrete de consulta médica",
                "appointment_id": appointment["id"],
                "scheduled_date": appointment_date,
            }
        )

        # 4. Enviar lembrete de consulta
        reminder_notification = await notification_service.send_appointment_reminder(
            {
                "patient_id": patient["id"],
                "patient_name": patient["name"],
                "patient_email": patient["email"],
                "appointment_date": appointment_date,
                "specialty": appointment["specialty"],
                "message": f"Lembrete: Sua consulta de {appointment['specialty']} está agendada para {appointment_date}",
                "channels": ["EMAIL", "SMS"],
            }
        )

        assert reminder_notification["type"] == "APPOINTMENT_REMINDER"

    @pytest.mark.asyncio
    async def test_health_trend_monitoring(
        self,
        health_service,
        monitoring_service,
        notification_service,
        sample_patient_data,
    ):
        """Testa monitoramento de tendências de saúde."""

        # 1. Registrar paciente e criar histórico
        patient = await health_service.register_patient(sample_patient_data)

        # 2. Registrar múltiplas medições de sinais vitais
        vital_signs_data = [
            {
                "blood_pressure_systolic": 130,
                "blood_pressure_diastolic": 85,
                "heart_rate": 72,
            },
            {
                "blood_pressure_systolic": 135,
                "blood_pressure_diastolic": 88,
                "heart_rate": 75,
            },
            {
                "blood_pressure_systolic": 140,
                "blood_pressure_diastolic": 90,
                "heart_rate": 78,
            },
            {
                "blood_pressure_systolic": 145,
                "blood_pressure_diastolic": 92,
                "heart_rate": 82,
            },
        ]

        for _i, vital_data in enumerate(vital_signs_data):
            await health_service.record_vital_signs(patient["id"], vital_data)
            # Simular intervalo de tempo
            await asyncio.sleep(0.01)

        # 3. Analisar tendências
        trends = await monitoring_service.analyze_trends(patient["id"])

        assert trends["patient_id"] == patient["id"]
        assert trends["blood_pressure_trend"] == "INCREASING"
        assert trends["overall_risk"] in ["MEDIUM", "HIGH"]

        # 4. Criar alerta de tendência
        await monitoring_service.create_health_alert(
            {
                "patient_id": patient["id"],
                "alert_type": "TREND_ANALYSIS",
                "severity": "MEDIUM",
                "message": "Tendência de aumento da pressão arterial detectada",
                "trends": trends,
            }
        )

        # 5. Enviar notificação de tendência
        trend_notification = await notification_service.send_health_alert(
            {
                "patient_id": patient["id"],
                "patient_name": patient["name"],
                "patient_email": patient["email"],
                "alert_type": "TREND_ALERT",
                "message": "Análise de tendências indica necessidade de acompanhamento",
                "recommendations": trends["recommendations"],
                "channels": ["EMAIL"],
            }
        )

        assert trend_notification["type"] == "HEALTH_ALERT"

    @pytest.mark.asyncio
    async def test_bulk_health_campaign(self, notification_service):
        """Testa campanha de saúde em massa."""

        # 1. Preparar lista de pacientes para campanha
        campaign_patients = [
            {
                "patient_id": f"patient_{i}",
                "patient_email": f"patient{i}@email.com",
                "patient_name": f"Paciente {i}",
            }
            for i in range(50)
        ]

        # 2. Criar notificações da campanha
        campaign_notifications = [
            {
                "patient_id": patient["patient_id"],
                "patient_email": patient["patient_email"],
                "patient_name": patient["patient_name"],
                "campaign_type": "VACCINATION_REMINDER",
                "message": "Lembrete: Mantenha suas vacinas em dia",
                "priority": "LOW",
            }
            for patient in campaign_patients
        ]

        # 3. Enviar campanha em lote
        results = await notification_service.send_bulk_health_notifications(campaign_notifications)

        assert len(results) == 50
        assert all(r["type"] in ["HEALTH_ALERT", "EMERGENCY"] for r in results)

    @pytest.mark.asyncio
    async def test_cross_module_error_handling(
        self, health_service, monitoring_service, notification_service
    ):
        """Testa tratamento de erros entre módulos de saúde."""

        # 1. Tentar registrar sinais vitais de paciente inexistente
        with pytest.raises(Exception):
            await health_service.record_vital_signs(
                999, {"blood_pressure_systolic": 120, "blood_pressure_diastolic": 80}
            )

        # 2. Tentar obter histórico de paciente inexistente
        with pytest.raises(ValueError, match="Paciente não encontrado"):
            await health_service.get_patient_history(999)

        # 3. Verificar que nenhum alerta foi gerado
        active_alerts = await monitoring_service.get_active_health_alerts()
        assert len(active_alerts) == 0

    @pytest.mark.asyncio
    async def test_multi_patient_monitoring(
        self, health_service, monitoring_service, notification_service
    ):
        """Testa monitoramento simultâneo de múltiplos pacientes."""

        # 1. Registrar múltiplos pacientes
        patients = []
        for i in range(5):
            patient_data = {
                "name": f"Paciente {i}",
                "email": f"patient{i}@email.com",
                "phone": f"+244 923 456 78{i}",
                "date_of_birth": "1990-01-01",
                "blood_type": "A+",
            }
            patient = await health_service.register_patient(patient_data)
            patients.append(patient)

        # 2. Registrar sinais vitais para todos os pacientes
        all_alerts = []
        for patient in patients:
            vital_sign, alerts = await health_service.record_vital_signs(
                patient["id"],
                {
                    "blood_pressure_systolic": 150 + (patients.index(patient) * 5),
                    "blood_pressure_diastolic": 95 + (patients.index(patient) * 3),
                    "heart_rate": 75,
                    "temperature": 36.5,
                    "oxygen_saturation": 96,
                },
            )
            all_alerts.extend(alerts)

        # 3. Criar alertas de monitoramento
        monitoring_alerts = []
        for i, patient in enumerate(patients):
            if i < len(all_alerts):
                alert = await monitoring_service.create_health_alert(
                    {
                        "patient_id": patient["id"],
                        "alert_type": all_alerts[i]["type"],
                        "severity": all_alerts[i]["severity"],
                        "message": all_alerts[i]["message"],
                    }
                )
                monitoring_alerts.append(alert)

        # 4. Enviar notificações para pacientes com alertas
        notifications = []
        for i, alert in enumerate(monitoring_alerts):
            if i < len(patients):
                notification = await notification_service.send_health_alert(
                    {
                        "patient_id": patients[i]["id"],
                        "patient_name": patients[i]["name"],
                        "patient_email": patients[i]["email"],
                        "alert_type": alert["alert_type"],
                        "message": alert["message"],
                        "severity": alert["severity"],
                    }
                )
                notifications.append(notification)

        # 5. Verificar resultados
        assert len(patients) == 5
        assert len(monitoring_alerts) == 5
        assert len(notifications) == 5

        # 6. Verificar estatísticas
        stats = await notification_service.get_notification_statistics()
        assert stats["total_notifications"] >= 5
