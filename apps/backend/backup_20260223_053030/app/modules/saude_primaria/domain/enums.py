from enum import Enum

class HealthcareServiceType(str, Enum):
    """Mapeamento dos serviços de saúde primária (SILA v3)"""
    CONSULTA_GERAL = "022_consulta_medica_geral"
    CONSULTA_ESPECIALIZADA = "023_consulta_medica_especializada"
    SAUDE_MATERNO_INFANTIL = "029_atendimento_de_saude_materno_infantil"
    PLANEAMENTO_FAMILIAR = "030_planeamento_familiar"
    ASSISTENCIA_PRE_NATAL = "032_assistencia_pre_natal"
    ASSISTENCIA_POS_NATAL = "033_assistencia_pos_natal"
    ACONSELHAMENTO_NUTRICIONAL = "035_aconselhamento_nutricional"
    APOIO_PSICOLOGICO = "040_apoio_psicologico_comunitario"
    ACOMPANHAMENTO_CRONICOS = "0968_acompanhamento_de_doentes_cronicos"
    ALERTAS_SAUDE = "0969_alertas_de_saude_personalizados"
    EDUCACAO_ALIMENTAR = "756_educacao_alimentar_comunitaria"
    MONITORIZACAO_NUTRICIONAL = "758_monitorizacao_nutricional_comunitaria"

class AppointmentStatus(str, Enum):
    """Estados do ciclo de vida de um atendimento"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    MISSED = "missed"
    NO_SHOW = "no_show"
    
    # Aliases
    AGENDADA = "scheduled"
    CONFIRMADA = "confirmed"
    CONCLUIDA = "completed"
    CANCELADA = "cancelled"

class AppointmentType(str, Enum):
    """Tipos de atendimento"""
    ROUTINE = "routine"
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    PREVENTIVE = "preventive"
    EMERGENCY = "emergency"

class PriorityLevel(str, Enum):
    """Níveis de prioridade"""
    LOW = "low"
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class MaternalRiskLevel(str, Enum):
    """Níveis de risco para vigilância maternal"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ChronicSeverity(str, Enum):
    """Gravidade para acompanhamento de doentes crónicos"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

class NotificationChannel(str, Enum):
    """Canais de comunicação para alertas de saúde"""
    SMS = "sms"
    EMAIL = "email"
    APP = "app"

class PrescriptionStatus(str, Enum):
    """Estados de uma prescrição"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class MedicationType(str, Enum):
    """Tipos de medicação"""
    ANTIBIOTIC = "antibiotic"
    ANALGESIC = "analgesic"
    ANTI_INFLAMMATORY = "anti_inflammatory"
    ANTIHYPERTENSIVE = "antihypertensive"
    ANTIDIABETIC = "antidiabetic"
    CARDIOVASCULAR = "cardiovascular"
    OCCASIONAL = "occasional"
    OTHER = "other"

class ExamStatus(str, Enum):
    """Estados de um exame"""
    REQUESTED = "requested"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESULTS_READY = "results_ready"

class HealthUnitType(str, Enum):
    """Tipos de unidade de saúde"""
    CLINIC = "clinic"
    HEALTH_CENTER = "health_center"
    HOSPITAL = "hospital"
    MOBILE_UNIT = "mobile_unit"
    OTHER = "other"

class VaccineStatus(str, Enum):
    """Estados de uma vacinação"""
    SCHEDULED = "scheduled"
    APPLIED = "applied"
    ADMINISTERED = "administered"
    MISSED = "missed"
    CONTRAINDICATED = "contraindicated"
    EXPIRED = "expired"
