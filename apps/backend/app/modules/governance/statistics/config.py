from dataclasses import dataclass

@dataclass(frozen=True)
class EstatisticaConfig:
    default_page_size: int = 20
    max_page_size: int = 100
    max_export_rows: int = 100000
    timeseries_limit_default: int = 200
config = EstatisticaConfig()