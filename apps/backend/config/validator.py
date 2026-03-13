"""
Configuration validation utilities for SILA system.
"""

from typing import Any, List, Tuple
from urllib.parse import urlparse
from .settings import settings

class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass

class SettingsValidator:
    """Comprehensive settings validator for SILA system."""
    
    def __init__(self, settings_instance: Any = None):
        self.settings = settings_instance or settings
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Executa todas as validações de sistema."""
        self._validate_database_settings()
        self._validate_security_settings()
        self._validate_redis_settings()
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_database_settings(self) -> None:
        try:
            parsed = urlparse(self.settings.DATABASE_URL)
            if parsed.scheme not in ["postgresql", "postgresql+asyncpg"]:
                self.errors.append("DATABASE_URL deve usar protocolo PostgreSQL")
        except Exception as e:
            self.errors.append(f"Falha na validação da URL do DB: {str(e)}")

    def _validate_security_settings(self) -> None:
        if len(self.settings.SECRET_KEY) < 32:
            self.errors.append("SECRET_KEY deve ter pelo menos 32 caracteres")

    def _validate_redis_settings(self) -> None:
        if not self.settings.REDIS_URL.startswith("redis://"):
            self.errors.append("REDIS_URL deve usar protocolo redis://")

def print_validation_report():
    """Gera um relatório de validação no console."""
    validator = SettingsValidator(settings)
    is_valid, errors, warnings = validator.validate()
    
    print("\n--- SILA SYSTEM CONFIGURATION REPORT ---")
    if warnings:
        for w in warnings: print(f"⚠️  WARNING: {w}")
    if errors:
        for e in errors: print(f"❌ ERROR: {e}")
    
    if is_valid:
        print("✅ Configuration is valid.")
    else:
        print("❌ Configuration is invalid!")
    print("---------------------------------------\n")
    return is_valid

def validate_configuration():
    """Função de entrada para validar e travar o boot se houver erro crítico."""
    if not print_validation_report():
        raise ConfigurationError("A configuração do sistema é inválida. Verifique os logs.")
    return True
