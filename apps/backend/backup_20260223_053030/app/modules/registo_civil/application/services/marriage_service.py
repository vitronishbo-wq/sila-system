import logging
from datetime import datetime
from app.modules.registo_civil.application.ports.marriage_repository_port import MarriageRepositoryPort
from app.modules.registo_civil.integrations.fuc_client import FUCClient
from app.modules.registo_civil.domain.models.marriage_record import MarriageRecord

logger = logging.getLogger("sila.registo_civil.service")

class MarriageService:
    def __init__(self, repo: MarriageRepositoryPort, fuc: FUCClient, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.repo = repo
        self.fuc = fuc

    async def register(self, data: dict):
        logger.info(f"Processando registro de casamento: {data.get('spouse1_id')} & {data.get('spouse2_id')}")
        
        record = MarriageRecord(
            spouse1_id=data["spouse1_id"],
            spouse2_id=data["spouse2_id"],
            marriage_date=datetime.fromisoformat(data["marriage_date"]) if isinstance(data["marriage_date"], str) else data["marriage_date"],
            place_of_marriage=data.get("place_of_marriage") or "Não Informado",
            regime=data["regime"]
        )
        await self.repo.save(record)
        
        logger.info(f"Assento de casamento {record.id} registrado com sucesso.")
        return {"success": True, "marriage_id": str(record.id)}
