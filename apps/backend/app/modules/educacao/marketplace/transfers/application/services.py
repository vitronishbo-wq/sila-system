"""Application services for Transfers subdomain"""
from typing import Optional, Any, List

from .ports import (
    TransferRepositoryPort,
    CurriculumValidatorPort,
    TransferValidatorPort,
)


class TransferService:
    """Serviço de aplicação para Transfers"""
    
    def __init__(
        self,
        transfer_repo: TransferRepositoryPort,
        curriculum_validator: CurriculumValidatorPort,
        transfer_validator: TransferValidatorPort,
    ):
        self.transfer_repo = transfer_repo
        self.curriculum_validator = curriculum_validator
        self.transfer_validator = transfer_validator
    
    async def request_transfer(
        self,
        citizen_id: str,
        source_institution_id: str,
        destination_institution_id: str,
        source_program_id: str,
        destination_program_id: str,
    ) -> str:
        """Solicitar transferência"""
        # Validar compatibilidade curricular
        compat = await self.curriculum_validator.check_compatibility(
            source_program_id, 
            destination_program_id
        )
        if not compat.get("compatible"):
            raise ValueError("Programs are not compatible")
        
        # Validar transferência
        validation = await self.transfer_validator.validate_transfer_request(
            citizen_id,
            source_institution_id,
            destination_institution_id,
        )
        if not validation.get("valid"):
            raise ValueError(f"Invalid transfer: {validation.get('errors')}")
        
        # Criar solicitação
        transfer_data = {
            "citizen_id": citizen_id,
            "source_institution_id": source_institution_id,
            "destination_institution_id": destination_institution_id,
            "source_program_id": source_program_id,
            "destination_program_id": destination_program_id,
        }
        
        return await self.transfer_repo.create_transfer_request(transfer_data)
    
    async def check_compatibility(
        self,
        source_program_id: str,
        destination_program_id: str,
    ) -> dict:
        """Verificar compatibilidade"""
        return await self.curriculum_validator.check_compatibility(
            source_program_id,
            destination_program_id,
        )
