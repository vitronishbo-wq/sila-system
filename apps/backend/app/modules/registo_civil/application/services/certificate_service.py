from app.core.observability import trace
import logging
import uuid

logger = logging.getLogger("sila.registo_civil.service")

class CertificateService:
    @trace()
    async def issue_birth_certificate(self, citizen_id: str):
        logger.info(f"Emitindo certidão de nascimento para {citizen_id}")
        return {"citizen_id": citizen_id, "type": "BIRTH", "status": "issued", "authenticity_code": str(uuid.uuid4())}

    @trace()
    async def issue_marriage_certificate(self, marriage_id: str):
        logger.info(f"Emitindo certidão de casamento para {marriage_id}")
        return {"marriage_id": marriage_id, "type": "MARRIAGE", "status": "issued", "authenticity_code": str(uuid.uuid4())}

    @trace()
    async def issue_death_certificate(self, citizen_id: str):
        logger.info(f"Emitindo certidão de óbito para {citizen_id}")
        return {"citizen_id": citizen_id, "type": "DEATH", "status": "issued", "authenticity_code": str(uuid.uuid4())}

    @trace()
    async def issue_non_marriage_certificate(self, citizen_id: str):
        logger.info(f"Emitindo certidão de solteiro para {citizen_id}")
        return {"citizen_id": citizen_id, "type": "NON_MARRIAGE", "status": "single", "authenticity_code": str(uuid.uuid4())}

    @trace()
    async def issue_civil_state_certificate(self, citizen_id: str):
        logger.info(f"Emitindo certidão de estado civil para {citizen_id}")
        return {"citizen_id": citizen_id, "type": "CIVIL_STATE", "status": "issued", "authenticity_code": str(uuid.uuid4())}
