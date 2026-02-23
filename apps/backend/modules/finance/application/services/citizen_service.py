import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from app.domain.enums import CitizenStatus
from app.modules.financas.exceptions import FUCError
from app.citizen.exceptions import CitizenNotFoundError
from app.core.audit import audit_log

logger = logging.getLogger(__name__)


class CitizenService:
    """
    Serviço de Validação de Cidadão para Operações Financeiras.
    Integra com Ficheiro Único do Cidadão (FUC).
    
    REGRAS FINANCEIRAS:
    - Apenas cidadãos ACTIVE podem receber faturas
    - Status DECEASED, SUSPENDED, INACTIVE bloqueiam operações
    - Cache com TTL para otimizar integração FUC
    """
    
    # TTL para cache (em minutos)
    CACHE_TTL_MINUTES = 15
    
    def __init__(self, db_session=None):
        self.db = db_session
        self._cache: Dict[str, Dict[str, Any]] = {}

    async def validate_for_billing(self, citizen_id: str) -> bool:
        """
        Valida se cidadão está ATIVO para operações financeiras.
        
        REGRA: Apenas CitizenStatus.ACTIVE permite faturação.
        
        Retorna True se elegível, False caso contrário.
        Lança FUCError em caso de falha na integração.
        """
        try:
            citizen_data = await self.get_citizen_data(citizen_id)
            is_active = citizen_data.get("status") == CitizenStatus.ACTIVE
            
            if not is_active:
                logger.warning(
                    f"Cidadão {citizen_id} bloqueado para faturação. "
                    f"Status: {citizen_data.get('status')}"
                )
                # Auditoria de Falha (Cross-module)
                if self.db:
                    await audit_log(
                        action="FINANCIAL_VALIDATION_FAILED",
                        actor_id="SYSTEM_FINANCE",
                        resource_id=citizen_id,
                        resource_type="Citizen",
                        new_value={"reason": f"Status {citizen_data.get('status')} não permite faturação"},
                        db=self.db
                    )
            else:
                logger.info(f"Cidadão {citizen_id} validado para faturação")
            
            return is_active
            
        except Exception as e:
            logger.error(f"Erro ao validar cidadão {citizen_id}: {str(e)}")
            raise FUCError("Falha na validação de identidade - tente novamente")

    async def get_citizen_data(self, citizen_id: str) -> Dict[str, Any]:
        """
        Recupera dados oficiais do cidadão do FUC.
        
        Implementa cache com TTL para reduzir chamadas ao FUC.
        Em produção, chamaria repositório de IDENTIDADE CIVIL ou API interna.
        """
        if not citizen_id:
            raise CitizenNotFoundError(citizen_id, reason="ID de cidadão não fornecido")

        # 1. Verificação em cache (com validade)
        cached = self._cache.get(citizen_id)
        if cached and self._is_cache_valid(cached):
            logger.debug(f"Dados do cidadão recuperados do cache: {citizen_id}")
            return cached["data"]

        # 2. Integração FUC (simulado em desenvolvimento)
        # Em produção: await fuc_repository.get_citizen(citizen_id)
        try:
            # Lógica de simulação inteligente para testes/dev
            status = CitizenStatus.ACTIVE
            id_upper = citizen_id.upper()
            if "INACTIVE" in id_upper: status = CitizenStatus.INACTIVE
            elif "DECEASED" in id_upper: status = CitizenStatus.DECEASED
            elif "SUSPENDED" in id_upper: status = CitizenStatus.SUSPENDED

            citizen_data = {
                "citizen_id": citizen_id,
                "full_name": f"Cidadão Validado: {citizen_id}",
                "status": status,
                "is_eligible_for_finance": status == CitizenStatus.ACTIVE
            }

            # 3. Armazenar em cache com timestamp
            self._cache[citizen_id] = {
                "data": citizen_data,
                "timestamp": datetime.utcnow()
            }
            
            logger.debug(f"Dados do cidadão obtidos: {citizen_id}")
            return citizen_data

        except Exception as e:
            logger.error(f"Falha ao obter dados do cidadão {citizen_id}: {str(e)}")
            raise FUCError("Serviço de identidade indisponível")

    def _is_cache_valid(self, cached_entry: Dict[str, Any]) -> bool:
        """Verifica se entrada em cache ainda é válida."""
        timestamp = cached_entry.get("timestamp")
        if not timestamp:
            return False
        
        age = datetime.utcnow() - timestamp
        return age < timedelta(minutes=self.CACHE_TTL_MINUTES)

    def invalidate_cache(self, citizen_id: Optional[str] = None):
        """
        Limpa cache de dados do cidadão.
        
        Se citizen_id: Remove cache específico
        Se None: Limpa todo o cache
        """
        if citizen_id:
            if citizen_id in self._cache:
                self._cache.pop(citizen_id)
                logger.debug(f"Cache invalidado para cidadão: {citizen_id}")
        else:
            self._cache.clear()
            logger.debug("Cache global invalidado")
