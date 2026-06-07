import asyncio
import logging
import os
import random

from apps.backend.app.modules.economy.financas.exceptions import FUCError

logger = logging.getLogger(__name__)


class FUCClient:
    """
    Shared client for the Ficheiro Unico do Cidadao (FUC).

    This implementation is currently a resilient mock/stub used in development
    and non-production flows while the external contract is consolidated.
    """

    def __init__(self, base_url: str = None, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.base_url = base_url or os.getenv("FUC_SERVICE_URL", "http://fuc-api.sila.gov.ao")

    async def validate_citizen(self, citizen_id: str) -> bool:
        logger.info("FUC_CLIENT: validating citizen_id=%s", citizen_id)
        await asyncio.sleep(random.uniform(0.1, 0.8))
        if random.random() < 0.02:
            logger.error(
                "FUC_CLIENT: transient communication failure for citizen_id=%s", citizen_id
            )
            raise FUCError(
                "O serviço central de validação de cidadãos está temporariamente indisponível."
            )
        if citizen_id.upper().startswith("INVALID"):
            return False
        if len(citizen_id) < 5:
            return False
        if citizen_id.endswith("99"):
            return False
        return True

    async def get_citizen_data(self, citizen_id: str) -> dict | None:
        try:
            is_valid = await self.validate_citizen(citizen_id)
            if not is_valid:
                return None
            return {
                "id": citizen_id,
                "full_name": "Antonio Manuel dos Santos (Identidade Validada)",
                "tax_id": citizen_id,
                "fiscal_status": "REGULAR",
                "residence": "Luanda, Angola",
                "last_updated": "2024-03-15T09:45:00Z",
                "metadata": {"source": "FUC_SILA_GATEWAY_V2", "authority": "DNIC_ANGOLA"},
            }
        except FUCError:
            raise
        except Exception as exc:
            logger.exception("FUC_CLIENT: unexpected error querying citizen_id=%s", citizen_id)
            raise FUCError(
                f"Erro interno no processamento da consulta ao Ficheiro Unico: {str(exc)}"
            ) from exc
