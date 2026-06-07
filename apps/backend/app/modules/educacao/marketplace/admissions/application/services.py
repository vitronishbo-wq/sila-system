"""Application services for Admissions subdomain"""
from typing import Optional, Any, List

from .ports import (
    AdmissionRepositoryPort,
    EligibilityValidatorPort,
    DocumentVerificationPort,
)


class AdmissionService:
    """Serviço de aplicação para Admissions"""
    
    def __init__(
        self,
        admission_repo: AdmissionRepositoryPort,
        eligibility_validator: EligibilityValidatorPort,
        document_verification: DocumentVerificationPort,
    ):
        self.admission_repo = admission_repo
        self.eligibility_validator = eligibility_validator
        self.document_verification = document_verification
    
    async def process_admission(self, citizen_id: str, opportunity_id: str) -> str:
        """Processar admissão automática"""
        # Criar registro de admissão
        admission_id = await self.admission_repo.create_admission(citizen_id, opportunity_id)
        
        # Validar elegibilidade
        eligibility = await self.eligibility_validator.validate_eligibility(
            citizen_id, 
            opportunity_id
        )
        
        if not eligibility.get("eligible"):
            await self.admission_repo.update_admission_status(admission_id, "rejected")
            raise ValueError("Applicant is not eligible")
        
        # Verificar documentos obrigatórios
        # TODO: Obter documentos obrigatórios da oportunidade
        required_docs = []
        docs_result = await self.document_verification.verify_documents(citizen_id, required_docs)
        
        if not docs_result.get("verified"):
            await self.admission_repo.update_admission_status(admission_id, "pending_documents")
            return admission_id
        
        # Aprovar
        await self.admission_repo.update_admission_status(admission_id, "approved")
        return admission_id
    
    async def get_admission_status(self, admission_id: str) -> Optional[Any]:
        """Obter status de admissão"""
        return await self.admission_repo.get_admission(admission_id)
