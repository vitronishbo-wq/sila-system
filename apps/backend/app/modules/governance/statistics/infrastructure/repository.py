"""Legacy repository module. Prefer infrastructure.repositories package."""
from app.modules.governance.statistics.infrastructure.repositories.sqlalchemy_kpi_repository import SQLAlchemyKPIRepository
from app.modules.governance.statistics.infrastructure.repositories.sqlalchemy_metrica_repository import SQLAlchemyMetricaRepository
from app.modules.governance.statistics.infrastructure.repositories.sqlalchemy_timeseries_repository import SQLAlchemyTimeSeriesRepository
__all__ = ['SQLAlchemyMetricaRepository', 'SQLAlchemyKPIRepository', 'SQLAlchemyTimeSeriesRepository']