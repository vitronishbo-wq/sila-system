import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config.settings import settings
from ..models.notification import Notification, NotificationType, NotificationStatus
from ..tasks import send_notification_task


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        # Configuração do Jinja2
        template_dir = settings.BASE_DIR / "templates" / "emails"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Renderiza um template HTML com o contexto fornecido."""
        template = self.jinja_env.get_template(template_name)
        # Adiciona variáveis globais úteis
        context.setdefault("now", datetime.utcnow())
        return template.render(**context)

    async def create_and_queue(
        self,
        user_id: UUID,
        type_: NotificationType,
        title: str,
        message: str = "",
        template_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Notification:
        # Se um template for fornecido, renderiza a mensagem
        if template_name:
            rendered_message = self.render_template(template_name, context or {})
            message = rendered_message

        final_metadata = metadata or {}
        if template_name:
            final_metadata["template_name"] = template_name
            # Remove objects that are not JSON serializable (like 'now' datetime)
            if context:
                final_metadata["template_context"] = {
                    k: v for k, v in context.items() if k != "now"
                }

        notification = Notification(
            user_id=user_id,
            type=type_,
            title=title,
            message=message,
            metadata_=final_metadata,
        )
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)

        # Dispara a task do Celery para processamento em background
        send_notification_task.delay(str(notification.id))

        return notification

    async def send_email(self, to_email: str, title: str, message: str) -> bool:
        if not hasattr(settings, "SMTP_HOST") or not settings.SMTP_HOST:
            # Modo dev: simula envio
            print(f"[SIMULATION] Sending email to {to_email}: {title}")
            return True

        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = title
        # Tenta detectar se a mensagem é HTML
        is_html = message.strip().startswith("<")

        if is_html:
            msg.attach(MIMEText(message, "html", "utf-8"))
        else:
            msg.attach(MIMEText(message, "plain", "utf-8"))

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                if settings.SMTP_USER:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False

    async def dispatch_pending(self):
        """Task para ser chamada por background job (ex: Celery beat)"""
        from apps.backend.modules.identity.models.user import User  # lazy import

        result = await self.db.execute(
            select(Notification).where(Notification.status == NotificationStatus.PENDING)
        )
        notifications = result.scalars().all()

        for notif in notifications:
            user = await self.db.get(User, notif.user_id)
            if not user or not user.email:
                notif.status = NotificationStatus.FAILED
                continue

            success = await self.send_email(user.email, notif.title, notif.message)
            notif.status = NotificationStatus.SENT if success else NotificationStatus.FAILED
            if not success:
                notif.retry_count += 1
            notif.sent_at = datetime.utcnow() if success else None

        await self.db.commit()
