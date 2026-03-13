"""Legacy entities module. Prefer domain.models package."""
from app.modules.governance.statistics.domain.models.kpi import KPI
from app.modules.governance.statistics.domain.models.metrica import Metrica
from app.modules.governance.statistics.domain.models.timeseries import TimeSeries
__all__ = ['Metrica', 'KPI', 'TimeSeries']