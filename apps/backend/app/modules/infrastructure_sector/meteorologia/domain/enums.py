from enum import StrEnum

class AlertSeverity(StrEnum):
    """Niveis de severidade de alertas meteorologicos."""
    LOW = 'LOW'
    MODERATE = 'MODERATE'
    HIGH = 'HIGH'
    EXTREME = 'EXTREME'

class AlertType(StrEnum):
    """Tipos de alertas meteorologicos."""
    HEAT_WAVE = 'HEAT_WAVE'
    DROUGHT = 'DROUGHT'
    HEAVY_RAIN = 'HEAVY_RAIN'
    STRONG_WIND = 'STRONG_WIND'
    FROST = 'FROST'
    STORM = 'STORM'

class StationStatus(StrEnum):
    """Status de estacao meteorologica."""
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    MAINTENANCE = 'MAINTENANCE'
    OFFLINE = 'OFFLINE'

class ObservationType(StrEnum):
    """Tipos de observacao meteorologica."""
    SURFACE = 'SURFACE'
    UPPER_AIR = 'UPPER_AIR'
    RADAR = 'RADAR'
    SATELLITE = 'SATELLITE'
    MARINE = 'MARINE'