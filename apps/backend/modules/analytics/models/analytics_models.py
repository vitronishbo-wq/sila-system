"""
Modelos SQLAlchemy para o módulo de Analytics.

Define entidades principais para métricas, dashboards, relatórios,
alertas e cache de métricas.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, backref

from config.database import Base
from ..schemas.analytics_schemas import (
    DashboardType,
    MetricCategory,
    MetricType,
    ReportFormat,
    ReportType,
)


class Metric(Base):
    __tablename__ = "analytics_metrics"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(Enum(MetricCategory), nullable=False, index=True)
    metric_type = Column(Enum(MetricType), nullable=False)
    unit = Column(String(50), nullable=False)
    aggregation_function = Column(String(50), nullable=False)

    refresh_interval_seconds = Column(Integer, default=300, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"), nullable=False)

    last_calculated_at = Column(DateTime)
    current_value = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("created_metrics", lazy="dynamic"),
    )
    values = relationship(
        "MetricValue", back_populates="metric", cascade="all, delete-orphan"
    )
    dashboards = relationship(
        "DashboardMetric", back_populates="metric", cascade="all, delete-orphan"
    )
    alert_rules = relationship(
        "AlertRule", back_populates="metric", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Metric(id={self.id}, name='{self.name}', category={self.category})>"


class MetricValue(Base):
    __tablename__ = "analytics_metric_values"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    metric_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_metrics.id"), nullable=False
    )
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    extra_data = Column(JSON, name="metadata")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    metric = relationship("Metric", back_populates="values")

    def __repr__(self):
        return f"<MetricValue(id={self.id}, metric_id={self.metric_id}, value={self.value})>"


class Dashboard(Base):
    __tablename__ = "analytics_dashboards"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    dashboard_type = Column(Enum(DashboardType), nullable=False, index=True)

    is_public = Column(Boolean, default=False, nullable=False)
    refresh_interval_seconds = Column(Integer, default=300, nullable=False)
    layout_config = Column(JSON)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"), nullable=False)
    last_accessed_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("created_dashboards", lazy="dynamic"),
    )
    metrics = relationship(
        "DashboardMetric", back_populates="dashboard", cascade="all, delete-orphan"
    )
    access_logs = relationship(
        "DashboardAccessLog", back_populates="dashboard", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Dashboard(id={self.id}, name='{self.name}', type={self.dashboard_type})>"
        )


class DashboardMetric(Base):
    __tablename__ = "analytics_dashboard_metrics"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    dashboard_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_dashboards.id"), nullable=False
    )
    metric_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_metrics.id"), nullable=False
    )

    display_order = Column(Integer, default=0, nullable=False)
    chart_type = Column(String(50))
    color_scheme = Column(String(50))
    custom_title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    dashboard = relationship("Dashboard", back_populates="metrics")
    metric = relationship("Metric", back_populates="dashboards")

    def __repr__(self):
        return f"<DashboardMetric(id={self.id}, dashboard_id={self.dashboard_id}, metric_id={self.metric_id})>"


class DashboardAccessLog(Base):
    __tablename__ = "analytics_dashboard_access_logs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    dashboard_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_dashboards.id"), nullable=False
    )
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"), nullable=False)
    access_duration_seconds = Column(Integer)
    filters_applied = Column(JSON)
    data_exported = Column(Boolean, default=False, nullable=False)
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    dashboard = relationship("Dashboard", back_populates="access_logs")
    user = relationship(
        "Citizen", backref=backref("dashboard_access_logs", lazy="dynamic")
    )

    def __repr__(self):
        return f"<DashboardAccessLog(id={self.id}, dashboard_id={self.dashboard_id}, user_id={self.user_id})>"


class Report(Base):
    __tablename__ = "analytics_reports"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    report_type = Column(Enum(ReportType), nullable=False, index=True)
    is_scheduled = Column(Boolean, default=False, nullable=False)
    format = Column(Enum(ReportFormat), default=ReportFormat.PDF, nullable=False)
    file_path = Column(String(1000))
    file_size = Column(Integer)
    last_generated_at = Column(DateTime)
    generation_duration_seconds = Column(Float)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("created_reports", lazy="dynamic"),
    )
    executions = relationship(
        "ReportExecution", back_populates="report", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Report(id={self.id}, name='{self.name}', type={self.report_type})>"


class ReportExecution(Base):
    __tablename__ = "analytics_report_executions"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    report_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_reports.id"), nullable=False
    )
    status = Column(String(20), default="pending", nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    execution_time_seconds = Column(Float)
    data_points_processed = Column(Integer, default=0, nullable=False)
    file_size_bytes = Column(Integer)
    time_range = Column(String(50))
    filters_applied = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    report = relationship("Report", back_populates="executions")

    def __repr__(self):
        return f"<ReportExecution(id={self.id}, report_id={self.report_id}, status={self.status})>"


class AlertRule(Base):
    __tablename__ = "analytics_alert_rules"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    metric_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_metrics.id"), nullable=False
    )
    condition = Column(String(50), nullable=False)
    threshold_value = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    notification_channels = Column(JSON)
    cooldown_minutes = Column(Integer, default=15, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_triggered_at = Column(DateTime)
    trigger_count = Column(Integer, default=0, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    metric = relationship("Metric", back_populates="alert_rules")
    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("created_alert_rules", lazy="dynamic"),
    )
    alerts = relationship(
        "Alert", back_populates="alert_rule", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<AlertRule(id={self.id}, name='{self.name}', condition={self.condition})>"
        )


class Alert(Base):
    __tablename__ = "analytics_alerts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    alert_rule_id = Column(
        PGUUID(as_uuid=True), ForeignKey("analytics_alert_rules.id"), nullable=False
    )
    metric_value = Column(Float, nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, index=True)
    acknowledged_at = Column(DateTime)
    acknowledged_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"))
    resolved_at = Column(DateTime)
    extra_data = Column(JSON, name="metadata")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    alert_rule = relationship("AlertRule", back_populates="alerts")
    acknowledger = relationship(
        "Citizen", backref=backref("acknowledged_alerts", lazy="dynamic")
    )

    def __repr__(self):
        return f"<Alert(id={self.id}, severity={self.severity}, metric_value={self.metric_value})>"


class ScheduledReport(Base):
    __tablename__ = "analytics_scheduled_reports"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, index=True)
    report_type = Column(Enum(ReportType), nullable=False, index=True)
    schedule_cron = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    format = Column(Enum(ReportFormat), default=ReportFormat.PDF, nullable=False)
    filters = Column(JSON)
    last_executed_at = Column(DateTime)
    next_execution_at = Column(DateTime)
    execution_count = Column(Integer, default=0, nullable=False)
    recipients = Column(JSON, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("scheduled_reports", lazy="dynamic"),
    )
    executions = relationship(
        "ScheduledReportExecution",
        back_populates="scheduled_report",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<ScheduledReport(id={self.id}, name='{self.name}', schedule='{self.schedule_cron}')>"


class ScheduledReportExecution(Base):
    __tablename__ = "analytics_scheduled_report_executions"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    scheduled_report_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("analytics_scheduled_reports.id"),
        nullable=False,
    )
    status = Column(String(20), default="pending", nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    execution_time_seconds = Column(Float)
    file_size_bytes = Column(Integer)
    delivery_status = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    scheduled_report = relationship("ScheduledReport", back_populates="executions")

    def __repr__(self):
        return f"<ScheduledReportExecution(id={self.id}, scheduled_report_id={self.scheduled_report_id}, status={self.status})>"


class AnalyticsCache(Base):
    __tablename__ = "analytics_cache"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    cache_key = Column(String(255), nullable=False, unique=True, index=True)
    data = Column(JSON, nullable=False)
    data_size_bytes = Column(Integer)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_by = Column(PGUUID(as_uuid=True), ForeignKey("citizens.id"))
    access_count = Column(Integer, default=0, nullable=False)
    last_accessed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    creator = relationship(
        "Citizen",
        foreign_keys=[created_by],
        backref=backref("analytics_cache_entries", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<AnalyticsCache(id={self.id}, key='{self.cache_key}', expires_at={self.expires_at})>"


# Índices adicionais para otimização
Index("idx_metrics_category_type", Metric.category, Metric.metric_type)
Index("idx_metrics_active_last_calc", Metric.is_active, Metric.last_calculated_at)
Index(
    "idx_metric_values_metric_timestamp", MetricValue.metric_id, MetricValue.timestamp
)
Index("idx_metric_values_timestamp", MetricValue.timestamp)
Index("idx_dashboards_type_public", Dashboard.dashboard_type, Dashboard.is_public)
Index("idx_dashboards_created_by", Dashboard.created_by)
Index("idx_dashboards_last_accessed", Dashboard.last_accessed_at)
Index(
    "idx_dashboard_metrics_dashboard_order",
    DashboardMetric.dashboard_id,
    DashboardMetric.display_order,
)
Index("idx_reports_type_scheduled", Report.report_type, Report.is_scheduled)
Index("idx_reports_created_by", Report.created_by)
Index("idx_reports_last_generated", Report.last_generated_at)
Index("idx_alert_rules_metric_active", AlertRule.metric_id, AlertRule.is_active)
Index(
    "idx_alert_rules_severity_triggered",
    AlertRule.severity,
    AlertRule.last_triggered_at,
)
Index("idx_alerts_severity_acknowledged", Alert.severity, Alert.acknowledged_at)
Index("idx_alerts_created_at", Alert.created_at)
Index(
    "idx_scheduled_reports_active_next",
    ScheduledReport.is_active,
    ScheduledReport.next_execution_at,
)
Index("idx_scheduled_reports_created_by", ScheduledReport.created_by)
Index("idx_cache_key_expires", AnalyticsCache.cache_key, AnalyticsCache.expires_at)
Index("idx_cache_last_accessed", AnalyticsCache.last_accessed_at)

