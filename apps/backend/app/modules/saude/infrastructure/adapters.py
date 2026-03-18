"""Infrastructure adapters for Saude module"""
from apps.backend.core.adapters.adapter_factory import AdapterFactory
from apps.backend.app.modules.saude.domain.repositories import ISaudeRepository
SaudeAdapter = AdapterFactory.create_infrastructure_adapter(module_name='Saude', repository_interface=ISaudeRepository)
__all__ = ['SaudeAdapter']