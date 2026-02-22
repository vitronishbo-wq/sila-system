import logging
from datetime import datetime
from app.modules.registo_civil.application.ports.birth_repository_port import BirthRepositoryPort
from app.modules.registo_civil.integrations.fuc_client import FUCClient
from app.modules.registo_civil.domain.models.birth_record import BirthRecord

logger = logging.getLogger("sila.registo_civil.service")

class BirthService:
    def __init__(self, repo: BirthRepositoryPort, fuc: FUCClient, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.repo = repo
        self.fuc = fuc

    async def register(self, data: dict):
        logger.info(f"Processando registro de nascimento: {data.get('nub')}")
        
        # Criação/Link no FUC
        citizen_id = await self.fuc.create_or_link(data)
        
        # Criar Registro de Domínio
        record = BirthRecord(
            nub=data["nub"],
            full_name=data["full_name"],
            date_of_birth=datetime.fromisoformat(data["date_of_birth"]) if isinstance(data["date_of_birth"], str) else data["date_of_birth"],
            place_of_birth=data["place_of_birth"],
            father_name=data.get("father_name"),
            mother_name=data.get("mother_name"),
            mother_id=data.get("mother_id"),
            father_id=data.get("father_id")
        )
        
        await self.repo.save(record)
        
        logger.info(f"Registro de nascimento concluído com sucesso para {record.full_name}")
        return {"success": True, "nub": record.nub, "citizen_id": citizen_id}
