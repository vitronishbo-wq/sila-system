"""Legacy repository module. Prefer infrastructure.repositories package."""
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.sqlalchemy_kpi_repository import SQLAlchemyKPIRepository
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.sqlalchemy_metrica_repository import SQLAlchemyMetricaRepository
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.sqlalchemy_timeseries_repository import SQLAlchemyTimeSeriesRepository
__all__ = ['SQLAlchemyMetricaRepository', 'SQLAlchemyKPIRepository', 'SQLAlchemyTimeSeriesRepository']