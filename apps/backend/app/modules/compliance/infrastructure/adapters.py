"""Infrastructure adapters for Compliance module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.compliance.domain.repositories import IComplianceRepository
ComplianceAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Compliance', repository_interface=IComplianceRepository)
__all__ = ['ComplianceAdapter']