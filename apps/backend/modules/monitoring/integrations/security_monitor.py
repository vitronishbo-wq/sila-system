from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..models.alert import AlertCategory, AlertSeverity, AlertType
from ..models.audit_log import AuditAction, AuditLevel
from ..services.alert_service import AlertService
from ..services.audit_service import AuditService

class SecurityMonitor:
    """Monitorização de segurança assíncrona para o SILA-System."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit_service = AuditService(db)
        self.alert_service = AlertService(db)

    async def monitor_login_attempts(
        self,
        user_id: Optional[int],
        user_email: str,
        ip_address: str,
        user_agent: str,
        success: bool,
        failure_reason: Optional[str] = None,
    ):
        await self.audit_service.log_user_action(
            user_id=user_id,
            user_email=user_email,
            action=AuditAction.LOGIN,
            module="auth",
            description=f"Tentativa de login {'bem-sucedida' if success else 'falhou'}",
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=failure_reason,
            additional_data={"failure_reason": failure_reason},
        )

        if not success:
            await self._check_failed_login_patterns(user_email, ip_address)

    async def monitor_privilege_escalation(
        self,
        user_id: int,
        user_email: str,
        old_role: str,
        new_role: str,
        changed_by_user_id: int,
        ip_address: Optional[str] = None,
    ):
        await self.audit_service.log_user_action(
            user_id=changed_by_user_id,
            action=AuditAction.UPDATE,
            module="auth",
            description=f"Escala de privilégio: {user_email} de {old_role} para {new_role}",
            resource_type="user_role",
            resource_id=user_id,
            ip_address=ip_address,
            success=True,
            additional_data={"old_role": old_role, "new_role": new_role},
        )
        await self._create_privilege_escalation_alert(user_email, old_role, new_role, changed_by_user_id)

    async def _check_failed_login_patterns(self, user_email: str, ip_address: str):
        recent_time = datetime.utcnow() - timedelta(hours=1)
        # Lógica de contagem assíncrona para detecção de Brute Force
        count = await self.audit_service.count_failed_logins(user_email, recent_time)
        
        if count >= 5:
            await self._create_brute_force_alert(user_email, ip_address, count)

    async def _create_brute_force_alert(self, user_email: str, ip_address: str, count: int):
        from ..schemas import AlertCreate
        alert = AlertCreate(
            alert_type=AlertType.MULTIPLE_LOGIN_FAILURES,
            severity=AlertSeverity.HIGH,
            category=AlertCategory.SECURITY,
            title=f"Ataque de força bruta detectado: {user_email}",
            description=f"{count} falhas de login em 1 hora a partir do IP {ip_address}",
            source_module="security"
        )
        await self.alert_service.create_alert(alert)

    async def _create_privilege_escalation_alert(self, email, old, new, by):
        from ..schemas import AlertCreate
        alert = AlertCreate(
            alert_type=AlertType.SUSPICIOUS_ACTIVITY,
            severity=AlertSeverity.CRITICAL,
            category=AlertCategory.SECURITY,
            title="Alteração crítica de privilégios",
            description=f"Utilizador {email} promovido de {old} para {new} por ID {by}",
            source_module="security"
        )
        await self.alert_service.create_alert(alert)