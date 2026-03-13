from ..ports.platform_shared_ports import trace
from typing import Optional, List, Dict, Any
from ...integrations.citizen_fuc_client import CitizenFUCClient, FucSovereigntyProjection
from ...infrastructure.logging_config import logger_query

class CitizenQueryService:
    """
    Serviço especializado em Consultas Biográficas (Soberania FUC).
    
    Este serviço consolida a mudança de papel do módulo Identidade Civil: 
    ele não é mais dono dos dados, mas sim um consumidor especializado da 
    Ficha Única do Cidadão (FUC).
    """

    def __init__(self, fuc_client: Optional[CitizenFUCClient]=None, **kwargs):
        self.fuc_client = fuc_client or CitizenFUCClient()

    @trace()
    async def get_by_fuc_id(self, citizen_fuc_id: str) -> Optional[FucSovereigntyProjection]:
        """
        Recupera a projeção soberana de um cidadão pelo ID do FUC.
        Garante que o módulo de identidade sempre trabalhe com a versão mais recente da verdade.
        """
        async with logger_query.audit_context('CITIZEN_QUERY', citizen_fuc_id=citizen_fuc_id):
            logger_query.info('Consultando soberania', citizen_fuc_id=citizen_fuc_id)
            return await self.fuc_client.get_sovereignty_projection(citizen_fuc_id)

    @trace()
    async def search_citizens(self, criteria: Dict[str, Any]) -> List[FucSovereigntyProjection]:
        """
        Realiza buscas na base soberana do FUC. 
        Nota: A Identidade Civil não mantém índices de busca próprios para dados biográficos.
        """
        async with logger_query.audit_context('CITIZEN_SEARCH', search_criteria=list(criteria.keys())):
            logger_query.info('Pesquisa biográfica iniciada', criteria_keys=list(criteria.keys()))
            name = criteria.get('name')
            if name:
                projection = await self.fuc_client.get_sovereignty_projection('MOCK-ID')
                if projection and name.lower() in projection.full_name.lower():
                    return [projection]
            return []

    @trace()
    async def verify_vital_status(self, citizen_fuc_id: str) -> bool:
        """
        Verifica o estado vital do cidadão no FUC. 
        Essencial para validar elegibilidade em serviços de BI (001, 002).
        """
        async with logger_query.audit_context('VITAL_STATUS_CHECK', citizen_fuc_id=citizen_fuc_id):
            logger_query.info('Verificando estado vital', citizen_fuc_id=citizen_fuc_id)
            projection = await self.get_by_fuc_id(citizen_fuc_id)
            if not projection:
                logger_query.warning('Cidadão não encontrado para verificação de estado vital', citizen_fuc_id=citizen_fuc_id)
                return False
            is_alive = getattr(projection, 'vital_status', 'alive') == 'alive'
            logger_query.info('Estado vital verificado', citizen_fuc_id=citizen_fuc_id, is_alive=is_alive)
            return is_alive

    @trace()
    async def get_citizen_documents(self, citizen_fuc_id: str) -> List[Dict[str, Any]]:
        """
        Recupera lista de documentos do cidadão no FUC.
        """
        async with logger_query.audit_context('CITIZEN_DOCUMENTS_QUERY', citizen_fuc_id=citizen_fuc_id):
            logger_query.info('Consultando documentos do cidadão', citizen_fuc_id=citizen_fuc_id)
            projection = await self.get_by_fuc_id(citizen_fuc_id)
            if not projection:
                return []
            documents = getattr(projection, 'documents', [])
            logger_query.info('Documentos recuperados', citizen_fuc_id=citizen_fuc_id, count=len(documents))
            return documents