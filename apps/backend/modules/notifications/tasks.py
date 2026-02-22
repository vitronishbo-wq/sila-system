import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

from core.celery.app import celery_app
from config.settings import settings
from modules.notifications.models.notification import Notification, NotificationStatus
from modules.identity.models.user import User
from datetime import timedelta
from sqlalchemy import delete


async def _send_notification_async(notification_id: str):
    """Lógica interna assíncrona para processar o envio."""
    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    async with AsyncSession(engine) as db:
        # Busca a notificação pelo ID
        result = await db.execute(
            select(Notification).where(Notification.id == UUID(notification_id))
        )
        notification = result.scalars().first()

        if not notification or notification.status != NotificationStatus.PENDING:
            return {"status": "skipped", "reason": "not_found_or_not_pending"}

        # Busca o usuário para obter o email
        user = await db.get(User, notification.user_id)
        if not user or not user.email:
            notification.status = NotificationStatus.FAILED
            notification.retry_count += 1
            await db.commit()
            return {"status": "failed", "reason": "no_user_email"}

        # Configuração do e-mail
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = user.email
        msg["Subject"] = notification.title
        # Tenta detectar se a mensagem é HTML
        is_html = notification.message.strip().startswith("<")

        if is_html:
            msg.attach(MIMEText(notification.message, "html", "utf-8"))
        else:
            msg.attach(MIMEText(notification.message, "plain", "utf-8"))

        # Envio SMTP (síncrono, mas rodando dentro de asyncio.run)
        try:
            # Em produção, SMTP_HOST deve estar configurado
            if not settings.SMTP_HOST:
                print(f"[SIMULATION] Email background to {user.email}: {notification.title}")
                success = True
            else:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    if settings.SMTP_TLS:
                        server.starttls()
                    if settings.SMTP_USER:
                        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                success = True
        except Exception as exc:
            # Re-lança para o wrapper do Celery lidar com o retry
            raise exc

        # Atualiza o registro da notificação
        notification.status = NotificationStatus.SENT if success else NotificationStatus.FAILED
        if success:
            notification.sent_at = datetime.utcnow()
        else:
            notification.retry_count += 1

        await db.commit()
        return {"status": "sent" if success else "failed"}


@celery_app.task(bind=True, max_retries=5, default_retry_delay=60)
def send_notification_task(self, notification_id: str):
    """Task do Celery que encapsula a lógica assíncrona."""
    try:
        # Executa a lógica assíncrona dentro do worker síncrono
        return asyncio.run(_send_notification_async(notification_id))
    except Exception as exc:
        # Retry automático em caso de erro transiente
        raise self.retry(exc=exc)


@celery_app.task
def cleanup_old_notifications():
    """Remove notificações lidas com mais de 30 dias."""
    return asyncio.run(_cleanup_old_notifications_async())


async def _cleanup_old_notifications_async():
    cutoff = datetime.utcnow() - timedelta(days=30)
    engine = create_async_engine(settings.ASYNC_DATABASE_URL)
    async with AsyncSession(engine) as db:
        await db.execute(
            delete(Notification)
            .where(Notification.read == True, Notification.created_at < cutoff)
        )
        await db.commit()
    return {"status": "cleanup_completed", "cutoff": cutoff.isoformat()}
