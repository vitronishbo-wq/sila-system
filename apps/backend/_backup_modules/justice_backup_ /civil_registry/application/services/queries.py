from typing import Dict, Any

class ProfileQueries:
    """
    [DEPRECATED] Use SovereignDashboardService instead.
    """

    @staticmethod
    def get_commune_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError('Use SovereignDashboardService.get_regional_distribution()')

    @staticmethod
    def get_municipality_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError('Use SovereignDashboardService.get_regional_distribution()')

    @staticmethod
    def get_province_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError('Use SovereignDashboardService.get_regional_distribution()')

    @staticmethod
    def get_central_dashboard(*args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError('Use SovereignDashboardService.get_national_overview()')