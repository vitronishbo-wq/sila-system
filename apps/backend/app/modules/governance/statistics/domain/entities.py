"""Legacy entities module. Prefer domain.models package."""
from apps.backend.app.modules.governance.statistics.domain.models.kpi import KPI
from apps.backend.app.modules.governance.statistics.domain.models.metrica import Metrica
from apps.backend.app.modules.governance.statistics.domain.models.timeseries import TimeSeries
__all__ = ['Metrica', 'KPI', 'TimeSeries']