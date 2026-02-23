from app.core.observability import trace
import logging
from datetime import datetime
from app.modules.registo_civil.application.ports.death_repository_port import DeathRepositoryPort
from app.modules.registo_civil.integrations.fuc_client import FUCClient
from app.modules.registo_civil.domain.models.death_record import DeathRecord

logger = logging.getLogger("sila.registo_civil.service")

class DeathService:
    def __init__(self, repo: DeathRepositoryPort, fuc: FUCClient, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.repo = repo
        self.fuc = fuc

    @trace()
    async def register(self, data: dict):
        logger.info(f"Processando registro de óbito: {data.get('citizen_id')}")
        
        record = DeathRecord(
            citizen_id=data["citizen_id"],
            death_date=datetime.fromisoformat(data["death_date"]) if isinstance(data["death_date"], str) else data["death_date"],
            place_of_death=data.get("place_of_death") or "Não Informado",
            cause_of_death=data.get("cause_of_death") or "Causas Naturais",
            witnesses=data.get("witnesses")
        )
        await self.repo.save(record)
        
        # Regra: Atualizar status do cidadão no FUC para FALECIDO
        await self.fuc.update_status(data["citizen_id"], "DECEASED")
        
        logger.info(f"Óbito registrado com sucesso para cidadão {record.citizen_id}.")
        return {"success": True, "death_certificate_id": str(record.id)}
