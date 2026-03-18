"""Infrastructure adapters for Governance module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.governance.domain.repositories import IGovernanceRepository
GovernanceAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Governance', repository_interface=IGovernanceRepository)
__all__ = ['GovernanceAdapter']