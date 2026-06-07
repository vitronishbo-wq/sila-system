"""
Alert Webhook Handler - Fase 18.2

FastAPI service para processar alertas e orquestrar notificações:
- Slack notifications
- Email alerts
- Webhook integrations
- Alert deduplication
- Severity-based routing
"""

import json
import logging
import os
import smtplib
from collections import defaultdict
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import StrEnum

import httpx
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("alert_handler")
app = FastAPI(
    title="SILA Alert Handler",
    description="Alert processing and notification orchestration",
    version="1.0.0",
)


class AlertSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(StrEnum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class AlertPayload(BaseModel):
    """Payload de alerta recebido"""

    alert_id: str
    type: str
    user_id: str
    tenant_id: str
    severity: AlertSeverity
    score: float
    description: str
    timestamp: datetime
    evidence: dict
    recommended_action: str
    source: str = "elasticsearch"
    tags: list[str] = []


class AlertDeduplicator:
    """Deduplica alertas baseado em fingerprint"""

    def __init__(self, ttl_minutes: int = 60):
        self.ttl_minutes = ttl_minutes
        self.alert_fingerprints = {}

    def get_fingerprint(self, alert: AlertPayload) -> str:
        """Gera fingerprint único do alerta"""
        import hashlib

        data = f"{alert.type}:{alert.user_id}:{alert.tenant_id}:{alert.alert_id}"
        return hashlib.md5(data.encode()).hexdigest()

    def is_duplicate(self, alert: AlertPayload) -> bool:
        """Verifica se alerta é duplicado recente"""
        fp = self.get_fingerprint(alert)
        now = datetime.utcnow()
        if fp in self.alert_fingerprints:
            last_time, count = self.alert_fingerprints[fp]
            age = (now - last_time).total_seconds() / 60
            if age < self.ttl_minutes:
                self.alert_fingerprints[fp] = (now, count + 1)
                return True
            else:
                self.alert_fingerprints[fp] = (now, 1)
                return False
        self.alert_fingerprints[fp] = (now, 1)
        return False


class NotificationManager:
    """Gerencia notificações em múltiplos canais"""

    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.smtp_server = os.getenv("SMTP_SERVER", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("ALERT_FROM_EMAIL", "alerts@sila.ao")
        self.security_emails = os.getenv("SECURITY_EMAIL", "security@sila.ao").split(",")

    async def send_alert(self, alert: AlertPayload):
        """Envia alerta em múltiplos canais baseado na severidade"""
        if alert.severity == AlertSeverity.CRITICAL:
            await self._send_email(alert)
            await self._send_slack(alert, "critical")
        elif alert.severity == AlertSeverity.HIGH:
            await self._send_slack(alert, "high")
        else:
            logger.info(f"Alert {alert.alert_id}: {alert.description}")

    async def _send_slack(self, alert: AlertPayload, channel: str = "general"):
        """Envia notificação para Slack"""
        if not self.slack_webhook:
            logger.warning("Slack webhook not configured")
            return
        color_map = {"critical": "danger", "high": "warning", "medium": "warning", "low": "good"}
        payload = {
            "attachments": [
                {
                    "color": color_map.get(alert.severity.value, "warning"),
                    "title": f"🚨 Alert: {alert.type}",
                    "text": alert.description,
                    "fields": [
                        {"title": "User", "value": alert.user_id, "short": True},
                        {"title": "Tenant", "value": alert.tenant_id, "short": True},
                        {"title": "Severity", "value": alert.severity.value.upper(), "short": True},
                        {"title": "Score", "value": f"{alert.score:.1f}/100", "short": True},
                        {
                            "title": "Recommended Action",
                            "value": alert.recommended_action,
                            "short": False,
                        },
                    ],
                    "footer": "SILA Alert Handler",
                    "ts": int(alert.timestamp.timestamp()),
                }
            ]
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.slack_webhook, json=payload)
                if response.status_code != 200:
                    logger.error(f"Slack notification failed: {response.text}")
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")

    async def _send_email(self, alert: AlertPayload):
        """Envia notificação por email"""
        try:
            msg = MIMEMultipart()
            msg["Subject"] = f"SECURITY CRITICAL ALERT: {alert.type}"
            msg["From"] = self.from_email
            msg["To"] = ", ".join(self.security_emails)
            html_body = f'\n            <html>\n                <body style="font-family: Arial, sans-serif;">\n                    <h2 style="color: #d32f2f;">🚨 SECURITY ALERT (CRITICAL)</h2>\n                    \n                    <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">\n                        <tr style="background-color: #f5f5f5;">\n                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Alert Type</strong></td>\n                            <td style="padding: 10px; border: 1px solid #ddd;">{alert.type}</td>\n                        </tr>\n                        <tr>\n                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>User ID</strong></td>\n                            <td style="padding: 10px; border: 1px solid #ddd;"><code>{alert.user_id}</code></td>\n                        </tr>\n                        <tr style="background-color: #f5f5f5;">\n                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Tenant</strong></td>\n                            <td style="padding: 10px; border: 1px solid #ddd;">{alert.tenant_id}</td>\n                        </tr>\n                        <tr>\n                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Score</strong></td>\n                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>{alert.score:.1f}/100</strong></td>\n                        </tr>\n                        <tr style="background-color: #f5f5f5;">\n                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Timestamp</strong></td>\n                            <td style="padding: 10px; border: 1px solid #ddd;">{alert.timestamp.isoformat()}</td>\n                        </tr>\n                    </table>\n                    \n                    <h3>Description</h3>\n                    <p>{alert.description}</p>\n                    \n                    <h3>Recommended Action</h3>\n                    <p style="background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107;">\n                        <strong>{alert.recommended_action}</strong>\n                    </p>\n                    \n                    <h3>Evidence</h3>\n                    <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 4px;">\n{json.dumps(alert.evidence, indent=2)}\n                    </pre>\n                    \n                    <hr style="margin-top: 30px; margin-bottom: 10px;">\n                    <p style="font-size: 12px; color: #666;">\n                        This is an automated alert from SILA Security System.\n                        Please do not reply to this email.\n                    </p>\n                </body>\n            </html>\n            '
            msg.attach(MIMEText(html_body, "html"))
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            logger.info(f"Email alert sent to {', '.join(self.security_emails)}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")


deduplicator = AlertDeduplicator()
notifier = NotificationManager()
alert_history = []


@app.post("/webhooks/security-alert")
async def security_alert(alert: AlertPayload, background_tasks: BackgroundTasks):
    """Recebe alertas de segurança da Elasticsearch"""
    if deduplicator.is_duplicate(alert):
        logger.debug(f"Alert {alert.alert_id} is duplicate, skipping")
        raise HTTPException(status_code=202, detail="Duplicate alert received")
    alert_history.append(
        {
            **alert.dict(),
            "received_at": datetime.utcnow().isoformat(),
            "status": AlertStatus.NEW.value,
        }
    )
    background_tasks.add_task(notifier.send_alert, alert)
    logger.info(f"Alert {alert.alert_id} received and queued for notification")
    return {"status": "received", "alert_id": alert.alert_id}


@app.post("/webhooks/security-critical")
async def security_critical(alert: AlertPayload, background_tasks: BackgroundTasks):
    """Recebe alertas críticos com escalacao imediata"""
    alert.severity = AlertSeverity.CRITICAL
    background_tasks.add_task(notifier.send_alert, alert)
    logger.critical(f"CRITICAL ALERT: {alert.alert_id} - {alert.description}")
    return {"status": "escalated", "alert_id": alert.alert_id}


@app.post("/webhooks/system-health")
async def system_health(payload: dict):
    """Recebe alertas de saúde do sistema"""
    logger.warning(f"System health alert: {payload}")
    return {"status": "received"}


@app.get("/alerts/history")
async def get_alert_history(limit: int = 100, severity: str | None = None):
    """Retorna histórico de alertas"""
    result = alert_history[-limit:]
    if severity:
        result = [a for a in result if a.get("severity") == severity]
    return {
        "total": len(alert_history),
        "recent": sorted(result, key=lambda x: x["received_at"], reverse=True),
    }


@app.get("/alerts/stats")
async def get_alert_stats():
    """Stats de alertas"""
    by_severity = defaultdict(int)
    by_type = defaultdict(int)
    for alert in alert_history:
        by_severity[alert.get("severity", "unknown")] += 1
        by_type[alert.get("type", "unknown")] += 1
    return {
        "total_alerts": len(alert_history),
        "by_severity": dict(by_severity),
        "by_type": dict(by_type),
        "last_24h": len(
            [
                a
                for a in alert_history
                if (datetime.utcnow() - datetime.fromisoformat(a["received_at"])).days < 1
            ]
        ),
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "alerts_in_queue": len(alert_history),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
