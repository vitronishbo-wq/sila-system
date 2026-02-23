from typing import Optional, List, Dict, Any
from ...services.citizen_query_service import CitizenQueryService

class CitizenService:
    """
    [REFATORADO] Serviço de transição para o módulo de Identidade Civil.
    
    Toda a lógica de 'propriedade' de dados foi removida. 
    Este serviço agora delega consultas ao CitizenQueryService, que consome o FUC.
    Lógicas de CREATE/UPDATE foram eliminadas para garantir a Single Source of Truth.
    """

    def __init__(self, query_service: Optional[CitizenQueryService] = None, **kwargs):
        self.query_service = query_service or CitizenQueryService()

    async def get_citizen(self, citizen_id: str) -> Optional[Any]:
        """Proxy para consulta soberana no FUC."""
        return await self.query_service.get_by_fuc_id(citizen_id)

    async def find_all(self, name_filter: Optional[str] = None) -> List[Any]:
        """Proxy para busca na base do FUC."""
        criteria = {"name": name_filter} if name_filter else {}
        return await self.query_service.search_citizens(criteria)

    # Métodos como 'create_citizen' ou 'update_citizen' foram REMOVIDOS.
    # Qualquer alteração biográfica deve ocorrer no módulo core do FUC.
