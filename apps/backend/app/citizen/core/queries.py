"""
[DEPRECATED] Consultas territoriais (Legado)

ATENÇÃO: Este módulo foi descontinuado com a introdução do SILA V2 Sovereign Engine.
A lógica de negócio foi migrada para:
1. `app.modules.bi.services.dashboard_service.SovereignDashboardService` (Dashboards)
2. `app.modules.bi_emission_service` (Fluxos de BI)
3. `app.core.workflow.models.request` (Novo modelo de Request)

Qualquer uso deste módulo resultará em erro ou dados incompletos.
Mantenha apenas para referência histórica até migração total do frontend.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID

# Stub classes to prevent ImportErrors
class ProfileQueries:
    """
    [DEPRECATED] Use SovereignDashboardService instead.
    """
    
    @staticmethod
    def get_commune_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Use SovereignDashboardService.get_regional_distribution()")

    @staticmethod
    def get_municipality_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Use SovereignDashboardService.get_regional_distribution()")

    @staticmethod
    def get_province_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Use SovereignDashboardService.get_regional_distribution()")

    @staticmethod
    def get_central_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Use SovereignDashboardService.get_national_overview()")
