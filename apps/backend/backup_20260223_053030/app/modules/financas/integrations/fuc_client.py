import asyncio
import logging
import random
import os
from typing import Dict, Optional
from app.modules.financas.exceptions import FUCError

logger = logging.getLogger(__name__)

class FUCClient:
    """
    Cliente de integração com o Ficheiro Único do Cidadão (FUC).
    Garante que o cidadão existe e está em situação regular no Estado antes de permitir
    a emissão de faturas ou processamento de pagamentos no sistema SILA.
    """
    
    def __init__(self, base_url: str = None, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        # A URL base é configurada via variável de ambiente para flexibilidade entre ambientes (Dev/Prod)
        self.base_url = base_url or os.getenv("FUC_SERVICE_URL", "http://fuc-api.sila.gov.ao")

    async def validate_citizen(self, citizen_id: str) -> bool:
        """
        Valida se o identificador do cidadão (BI/NIF) é válido e se ele está em situação regular no Estado.
        Simula uma chamada de API assíncrona ao barramento de serviços governamentais central.
        
        Args:
            citizen_id: O identificador único do cidadão (Ex: Número do Bilhete de Identidade).
            
        Returns:
            bool: True se o cidadão for válido e estiver em situação regular, False caso contrário.
            
        Raises:
            FUCError: Em caso de falha técnica de comunicação ou indisponibilidade do serviço.
        """
        logger.info(f"FUC_CLIENT: Iniciando validação para o identificador: {citizen_id}")
        
        # Simulação de latência de rede realista (100ms a 800ms) para chamadas externas
        await asyncio.sleep(random.uniform(0.1, 0.8))
        
        # Simulação de erro de rede intermitente (2% de chance de falha técnica)
        if random.random() < 0.02:
            logger.error(f"FUC_CLIENT: Falha na comunicação com o barramento governamental (FUC) para o ID: {citizen_id}")
            raise FUCError("O serviço central de validação de cidadãos está temporariamente indisponível.")

        # Regras de Negócio de Simulação (Protocolo SILA):
        # 1. IDs que começam com 'INVALID' são rejeitados explicitamente pelo mock.
        if citizen_id.upper().startswith("INVALID"):
            logger.warning(f"FUC_CLIENT: Cidadão {citizen_id} rejeitado pelo Ficheiro Único (ID Inválido).")
            return False
            
        # 2. Validação básica de formato (mínimo de caracteres).
        if len(citizen_id) < 5:
            logger.warning(f"FUC_CLIENT: Identificador {citizen_id} não cumpre os requisitos mínimos de formato.")
            return False
            
        # 3. Simulação de restrição administrativa. IDs terminados em '99' simulam cidadãos bloqueados.
        if citizen_id.endswith("99"):
            logger.warning(f"FUC_CLIENT: Cidadão {citizen_id} possui impedimentos fiscais ativos no FUC.")
            return False

        logger.info(f"FUC_CLIENT: Validação do cidadão {citizen_id} concluída com SUCESSO.")
        return True

    async def get_citizen_data(self, citizen_id: str) -> Optional[Dict]:
        """
        Recupera metadados detalhados do cidadão a partir do FUC para enriquecimento de faturas.
        
        Args:
            citizen_id: Identificador único do cidadão.
            
        Returns:
            Optional[Dict]: Dicionário com dados do perfil ou None se o cidadão for inválido.
        """
        try:
            is_valid = await self.validate_citizen(citizen_id)
            if not is_valid:
                return None
                
            # Simulação de payload de resposta do barramento governamental
            return {
                "id": citizen_id,
                "full_name": "António Manuel dos Santos (Identidade Validada)",
                "tax_id": citizen_id,
                "fiscal_status": "REGULAR",
                "residence": "Luanda, Angola",
                "last_updated": "2024-03-15T09:45:00Z",
                "metadata": {
                    "source": "FUC_SILA_GATEWAY_V2",
                    "authority": "DNIC_ANGOLA"
                }
            }
        except FUCError:
            # Re-lança para ser tratado pela camada de aplicação
            raise
        except Exception as e:
            logger.exception(f"FUC_CLIENT: Erro crítico ao processar consulta de dados para {citizen_id}")
            raise FUCError(f"Erro interno no processamento da consulta ao Ficheiro Único: {str(e)}")
