"""CRUD operations for monitoring module."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from modules.monitoring.models.alert import (
    Alert,
    AlertCategory,
    AlertSeverity,
    AlertStatus,
)
from modules.monitoring.models.audit_log import AuditLog
from modules.monitoring.models.system_metric import SystemMetric
from modules.monitoring.schemas.monitoring_crud import (
    AlertCreate,
    AlertFilter,
    AlertInDB,
    AlertUpdate,
    AuditLogCreate,
    AuditLogInDB,
    SystemMetricCreate,
    SystemMetricInDB,
)
from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class AlertCRUD:
    """CRUD operations for system alerts."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # Standard CRUD Operations
    async def create(self, obj_in: AlertCreate) -> AlertInDB:
        """Create a new alert."""
        db_obj = Alert(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return AlertInDB.model_validate(db_obj)

    async def get(self, id: int) -> Optional[AlertInDB]:
        """Get alert by ID."""
        result = await self.db.execute(select(Alert).where(Alert.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            return AlertInDB.model_validate(obj)
        return None

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[AlertStatus] = None,
        severity: Optional[AlertSeverity] = None,
    ) -> List[AlertInDB]:
        """Get multiple alerts with optional filtering."""
        query = select(Alert).order_by(desc(Alert.created_at))

        if status:
            query = query.where(Alert.status == status)

        if severity:
            query = query.where(Alert.severity == severity)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    async def update(self, id: int, obj_in: AlertUpdate) -> Optional[AlertInDB]:
        """Update alert record."""
        result = await self.db.execute(select(Alert).where(Alert.id == id))
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        # Update last_updated timestamp
        db_obj.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(db_obj)
        return AlertInDB.model_validate(db_obj)

    async def remove(self, id: int) -> Optional[AlertInDB]:
        """Remove alert record."""
        result = await self.db.execute(select(Alert).where(Alert.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return AlertInDB.model_validate(obj)
        return None

    # Advanced Query Operations
    async def get_by_status(self, status: AlertStatus) -> List[AlertInDB]:
        """Get alerts by status."""
        result = await self.db.execute(
            select(Alert).where(Alert.status == status).order_by(desc(Alert.created_at))
        )
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_severity(self, severity: AlertSeverity) -> List[AlertInDB]:
        """Get alerts by severity."""
        result = await self.db.execute(
            select(Alert)
            .where(Alert.severity == severity)
            .order_by(desc(Alert.created_at))
        )
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_category(self, category: AlertCategory) -> List[AlertInDB]:
        """Get alerts by category."""
        result = await self.db.execute(
            select(Alert)
            .where(Alert.category == category)
            .order_by(desc(Alert.created_at))
        )
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_active_alerts(self, hours: int = 24) -> List[AlertInDB]:
        """Get active alerts from the last N hours."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        result = await self.db.execute(
            select(Alert)
            .where(
                and_(
                    Alert.status == AlertStatus.ACTIVE, Alert.created_at >= cutoff_time
                )
            )
            .order_by(desc(Alert.created_at))
        )
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_critical_alerts(self) -> List[AlertInDB]:
        """Get all critical alerts."""
        result = await self.db.execute(
            select(Alert)
            .where(
                and_(
                    Alert.severity == AlertSeverity.CRITICAL,
                    Alert.status.in_([AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED]),
                )
            )
            .order_by(desc(Alert.created_at))
        )
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    async def search(self, filters: AlertFilter) -> List[AlertInDB]:
        """Search alerts with multiple filters."""
        query = select(Alert).order_by(desc(Alert.created_at))

        if filters.alert_type:
            query = query.where(Alert.alert_type == filters.alert_type)

        if filters.severity:
            query = query.where(Alert.severity == filters.severity)

        if filters.category:
            query = query.where(Alert.category == filters.category)

        if filters.status:
            query = query.where(Alert.status == filters.status)

        if filters.source:
            query = query.where(Alert.source.ilike(f"%{filters.source}%"))

        if filters.title:
            query = query.where(Alert.title.ilike(f"%{filters.title}%"))

        if filters.date_from:
            query = query.where(Alert.created_at >= filters.date_from)

        if filters.date_to:
            query = query.where(Alert.created_at <= filters.date_to)

        # Apply pagination
        if filters.skip:
            query = query.offset(filters.skip)
        if filters.limit:
            query = query.limit(filters.limit)

        result = await self.db.execute(query)
        return [AlertInDB.model_validate(obj) for obj in result.scalars().all()]

    # Statistics and Analytics
    async def get_alert_statistics(
        self, hours: int = 24, category: Optional[AlertCategory] = None
    ) -> Dict[str, Any]:
        """Get alert statistics."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        query = select(
            func.count(Alert.id).label("total_alerts"),
            func.count(func.distinct(Alert.alert_type)).label("unique_types"),
        ).where(Alert.created_at >= cutoff_time)

        if category:
            query = query.where(Alert.category == category)

        result = await self.db.execute(query)
        stats = result.first()

        # Get breakdown by severity
        severity_query = (
            select(Alert.severity, func.count(Alert.id).label("count"))
            .where(
                and_(
                    Alert.created_at >= cutoff_time,
                    Alert.category == category if category else True,
                )
            )
            .group_by(Alert.severity)
        )

        severity_result = await self.db.execute(severity_query)
        severity_breakdown = {row.severity: row.count for row in severity_result}

        return {
            "total_alerts": stats.total_alerts or 0,
            "unique_types": stats.unique_types or 0,
            "severity_breakdown": severity_breakdown,
            "period_hours": hours,
        }

    async def get_by_severity_breakdown(self, hours: int = 24) -> Dict[str, int]:
        """Get alert breakdown by severity."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        result = await self.db.execute(
            select(Alert.severity, func.count(Alert.id).label("count"))
            .where(Alert.created_at >= cutoff_time)
            .group_by(Alert.severity)
        )

        return {row.severity: row.count for row in result}

    async def get_top_alert_types(
        self, hours: int = 24, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get most frequent alert types."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        result = await self.db.execute(
            select(
                Alert.alert_type,
                func.count(Alert.id).label("count"),
                func.avg(
                    func.extract("epoch", Alert.resolved_at - Alert.created_at)
                ).label("avg_resolution_time"),
            )
            .where(Alert.created_at >= cutoff_time)
            .group_by(Alert.alert_type)
            .order_by(desc("count"))
            .limit(limit)
        )

        return [
            {
                "alert_type": row.alert_type,
                "count": row.count,
                "avg_resolution_time": float(row.avg_resolution_time or 0),
            }
            for row in result
        ]

    # Alert Management Operations
    async def acknowledge_alert(
        self, alert_id: int, acknowledged_by: str
    ) -> Optional[AlertInDB]:
        """Acknowledge an alert."""
        return await self.update(
            alert_id,
            AlertUpdate(
                status=AlertStatus.ACKNOWLEDGED,
                acknowledged_by=acknowledged_by,
                acknowledged_at=datetime.utcnow(),
            ),
        )

    async def resolve_alert(
        self, alert_id: int, resolved_by: str, resolution_notes: Optional[str] = None
    ) -> Optional[AlertInDB]:
        """Resolve an alert."""
        return await self.update(
            alert_id,
            AlertUpdate(
                status=AlertStatus.RESOLVED,
                resolved_by=resolved_by,
                resolved_at=datetime.utcnow(),
                resolution_notes=resolution_notes,
            ),
        )

    async def escalate_alert(
        self, alert_id: int, escalated_to: str, escalation_reason: str
    ) -> Optional[AlertInDB]:
        """Escalate an alert."""
        return await self.update(
            alert_id,
            AlertUpdate(
                status=AlertStatus.ESCALATED,
                escalated_to=escalated_to,
                escalated_at=datetime.utcnow(),
                escalation_reason=escalation_reason,
            ),
        )

    # Batch Operations
    async def create_batch(self, objects_in: List[AlertCreate]) -> List[AlertInDB]:
        """Create multiple alerts in batch."""
        db_objects = [Alert(**obj.model_dump()) for obj in objects_in]
        self.db.add_all(db_objects)
        await self.db.commit()

        for obj in db_objects:
            await self.db.refresh(obj)

        return [AlertInDB.model_validate(obj) for obj in db_objects]

    async def resolve_batch(
        self, alert_ids: List[int], resolved_by: str
    ) -> List[AlertInDB]:
        """Resolve multiple alerts."""
        resolved_objects = []

        for alert_id in alert_ids:
            resolved = await self.resolve_alert(alert_id, resolved_by)
            if resolved:
                resolved_objects.append(resolved)

        return resolved_objects


class SystemMetricCRUD:
    """CRUD operations for system metrics."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: SystemMetricCreate) -> SystemMetricInDB:
        """Create a new system metric."""
        db_obj = SystemMetric(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return SystemMetricInDB.model_validate(db_obj)

    async def get_latest_metrics(
        self, metric_type: str, limit: int = 100
    ) -> List[SystemMetricInDB]:
        """Get latest metrics by type."""
        result = await self.db.execute(
            select(SystemMetric)
            .where(SystemMetric.metric_type == metric_type)
            .order_by(desc(SystemMetric.timestamp))
            .limit(limit)
        )
        return [SystemMetricInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_metrics_by_timerange(
        self, metric_type: str, start_time: datetime, end_time: datetime
    ) -> List[SystemMetricInDB]:
        """Get metrics within a time range."""
        result = await self.db.execute(
            select(SystemMetric)
            .where(
                and_(
                    SystemMetric.metric_type == metric_type,
                    SystemMetric.timestamp >= start_time,
                    SystemMetric.timestamp <= end_time,
                )
            )
            .order_by(SystemMetric.timestamp)
        )
        return [SystemMetricInDB.model_validate(obj) for obj in result.scalars().all()]


class AuditLogCRUD:
    """CRUD operations for audit logs."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: AuditLogCreate) -> AuditLogInDB:
        """Create a new audit log entry."""
        db_obj = AuditLog(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return AuditLogInDB.model_validate(db_obj)

    async def get_by_user(self, user_id: str, limit: int = 100) -> List[AuditLogInDB]:
        """Get audit logs for a specific user."""
        result = await self.db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
        )
        return [AuditLogInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_action(self, action: str, limit: int = 100) -> List[AuditLogInDB]:
        """Get audit logs by action type."""
        result = await self.db.execute(
            select(AuditLog)
            .where(AuditLog.action == action)
            .order_by(desc(AuditLog.timestamp))
            .limit(limit)
        )
        return [AuditLogInDB.model_validate(obj) for obj in result.scalars().all()]


# Factory functions for dependency injection
def get_alert_crud(db: AsyncSession) -> AlertCRUD:
    """Get alert CRUD instance."""
    return AlertCRUD(db)


def get_system_metric_crud(db: AsyncSession) -> SystemMetricCRUD:
    """Get system metric CRUD instance."""
    return SystemMetricCRUD(db)


def get_audit_log_crud(db: AsyncSession) -> AuditLogCRUD:
    """Get audit log CRUD instance."""
    return AuditLogCRUD(db)


# Main monitoring CRUD factory
def get_monitoring_crud(db: AsyncSession) -> Dict[str, Any]:
    """Get all monitoring CRUD instances."""
    return {
        "alert": get_alert_crud(db),
        "system_metric": get_system_metric_crud(db),
        "audit_log": get_audit_log_crud(db),
    }


__all__ = [
    "AlertCRUD",
    "SystemMetricCRUD",
    "AuditLogCRUD",
    "get_alert_crud",
    "get_system_metric_crud",
    "get_audit_log_crud",
    "get_monitoring_crud",
]
