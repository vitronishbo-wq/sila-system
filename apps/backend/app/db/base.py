from app.core.database import Base

# IMPORTAR MODELOS PARA REGISTRAR NO METADATA

# IAM Models
from app.core.iam.infrastructure.models.user_model import UserModel, UserRoleModel
from app.core.iam.infrastructure.models.role_model import RoleModel, RolePermissionModel
from app.core.iam.infrastructure.models.permission_model import PermissionModel, UserPermissionModel
from app.core.iam.infrastructure.models.session_model import SessionModel, RefreshTokenModel
from app.core.iam.infrastructure.models.audit_model import AuditLogModel
# Core audit model (application-level audit table)
from app.core.audit_legacy import AuditLog

# Citizen models (ensure registration during lazy import)
from app.citizen.core.models import CitizenFUC

# Identidade Civil: garantir registro dos modelos para Alembic
from app.modules.identidade_civil.domain.models.bi_record import BIRecord
from app.modules.identidade_civil.infrastructure.repositories.identity_request_repository import IdentityRequestModel

from app.modules.saude_primaria.infrastructure.db.healthcare_model import (
	HealthcareRequestModel,
	MaternalRecordModel,
	PostNatalRecordModel,
	ChronicMonitoringModel,
	NutritionRecordModel,
	PsychologySessionModel,
	HealthAlertModel,
)

# Service Requests Models (Bloco 12 - Enterprise Grade)
from app.modules.service_requests.infrastructure.models.service_request_model import ServiceRequestModel
from app.modules.service_requests.infrastructure.models.attachment_model import AttachmentModel
from app.modules.service_requests.infrastructure.models.request_event_model import RequestEventModel

# Saúde Primária Models (Bloco 13 - Enterprise Grade)
from app.modules.saude_primaria.infrastructure.models.appointment_model import AppointmentModel
from app.modules.saude_primaria.infrastructure.models.prescription_model import PrescriptionModel
from app.modules.saude_primaria.infrastructure.models.medical_record_model import MedicalRecordModel
from app.modules.saude_primaria.infrastructure.models.vaccine_model import VaccineModel, VaccineDoseModel
from app.modules.saude_primaria.infrastructure.models.health_unit_model import HealthUnitModel, HealthProfessionalModel
from app.modules.saude_primaria.infrastructure.models.exam_request_model import ExamRequestModel

# Workflow models
from app.modules.workflow.infrastructure.models.workflow_definition_model import WorkflowDefinitionModel
from app.modules.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
from app.modules.workflow.infrastructure.models.workflow_transition_model import WorkflowTransitionModel
from app.modules.workflow.infrastructure.models.workflow_instance_model import WorkflowInstanceModel
from app.modules.workflow.infrastructure.models.workflow_task_model import WorkflowTaskModel
from app.modules.workflow.infrastructure.models.workflow_history_model import WorkflowHistoryModel

# outros módulos (adicionar depois se necessário)
# from app.modules.identidade_civil....
# from app.modules.registo_civil....
# Financas Models (Bloco Finanças)
from app.modules.financas.infrastructure.models.invoice_model import InvoiceModel
from app.modules.financas.infrastructure.models.payment_model import PaymentModel
from app.modules.financas.infrastructure.models.audit_log_model import FinancialAuditModel

# Taxpayer module (AGT) - imported lazily in `_register_taxpayer_models` to avoid circular imports

__all__ = [
	"Base",
	"CitizenFUC",
	# IAM
	"UserModel",
	"UserRoleModel",
	"RoleModel",
	"RolePermissionModel",
	"PermissionModel",
	"UserPermissionModel",
	"SessionModel",
	"RefreshTokenModel",
	"AuditLogModel",
	# Saúde
	"HealthcareRequestModel",
	"MaternalRecordModel",
	"PostNatalRecordModel",
	"ChronicMonitoringModel",
	"NutritionRecordModel",
	"PsychologySessionModel",
	"HealthAlertModel",
	# Service Requests (Bloco 12)
	"ServiceRequestModel",
	"AttachmentModel",
	"RequestEventModel",
	# Saúde Primária (Bloco 13)
	"AppointmentModel",
	"PrescriptionModel",
	"MedicalRecordModel",
	"VaccineModel",
	"VaccineDoseModel",
	"HealthUnitModel",
	"HealthProfessionalModel",
	"ExamRequestModel",
	# Workflow
	"WorkflowDefinitionModel",
	"WorkflowStateModel",
	"WorkflowTransitionModel",
	"WorkflowInstanceModel",
	"WorkflowTaskModel",
	"WorkflowHistoryModel",
	# Taxpayer (registered lazily)
]


# Lazy import function for Statistics models to avoid circular imports
def _register_statistics_models():
	"""Lazy load statistics models to avoid circular import"""
	try:
		from app.modules.statistics.infrastructure.models.statistic_model import StatisticModel
		from app.modules.statistics.infrastructure.models.timeseries_model import TimeSeriesModel
		from app.modules.statistics.infrastructure.models.aggregation_model import AggregationModel
		return StatisticModel, TimeSeriesModel, AggregationModel
	except ImportError:
		return None, None, None


def _register_taxpayer_models():
	"""Lazy load taxpayer models to avoid circular import during runtime.
	Note: the direct import above ensures Alembic sees the model for autogenerate.
	"""
	try:
		from app.modules.taxpayer.infrastructure.models.taxpayer_model import TaxpayerModel
		return TaxpayerModel
	except ImportError:
		return None
