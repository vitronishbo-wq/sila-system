"""Serviço de integração com FUC (Ficheiro Único do Cidadão).

Este serviço é responsável por:
1. Validar cidadãos contra a base FUC
2. Recuperar dados consolidados do cidadão
3. Disparar eventos de sucesso/falha
4. Registrar operações em auditoria
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from app.citizen.enums import CitizenStatus
from app.citizen.exceptions import CitizenNotFoundError
from app.core.events import (
    EventPublisher, CitizenValidated, CitizenValidationFailed
)
from app.core.helpers import safe_get, safe_isoformat

logger = logging.getLogger(__name__)


class CitizenService:
    """Serviço para validação e recuperação de dados de cidadãos no FUC."""
    
    def __init__(self, db_session=None, event_publisher: Optional[EventPublisher] = None, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db_session
        self.event_publisher = event_publisher or EventPublisher
        self._citizen_cache: Dict[str, Dict[str, Any]] = {}
    
    async def get_citizen_data(self, citizen_id: str) -> Dict[str, Any]:
        """
        Busca dados consolidados do cidadão no FUC (Banco de Dados REAL).
        """
        if not citizen_id:
            raise CitizenNotFoundError("ID do cidadão não fornecido")
        
        from app.citizen.core.models import CitizenFUC
        from sqlalchemy import select
        
        # Query REAL ao Banco de Dados
        try:
            # Converter para UUID se necessário
            import uuid
            c_uuid = uuid.UUID(citizen_id) if isinstance(citizen_id, str) else citizen_id
            
            stmt = select(CitizenFUC).where(CitizenFUC.citizen_id == c_uuid)
            result = await self.db.execute(stmt)
            citizen = result.scalars().first()
            
            if not citizen:
                raise CitizenNotFoundError(f"Cidadão com ID {citizen_id} não encontrado no FUC.")
            
            # Converter model para dict (para manter compatibilidade com interface existente)
            citizen_data = {
                "id": str(citizen.citizen_id),
                "full_name": citizen.full_name,
                "status": safe_get(citizen, "vital_status", "ACTIVE"),
                "document_type": "BI", # Campo derivado ou fixo por enquanto
                "document_number": safe_get(citizen, "document_number"),
                "birth_date": safe_isoformat(safe_get(citizen, "birth_date")),
                "gender": safe_get(citizen, "gender"),
                "nationality": safe_get(citizen, "nationality"),
                "email": safe_get(citizen, "email"),
                "phone": safe_get(citizen, "phone"),
                "nif": safe_get(citizen, "nif"),
                "vital_status": safe_get(citizen, "vital_status"),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            self._citizen_cache[citizen_id] = citizen_data
            return citizen_data
            
        except ValueError:
            raise CitizenNotFoundError(f"ID inválido: {citizen_id}")
        except Exception as e:
            logger.error(f"Erro ao buscar cidadão {citizen_id}: {e}")
            raise
    
    async def validate_citizen(self, citizen_id: str) -> bool:
        """
        Valida se um cidadão existe e está ATIVO no FUC.
        
        Critérios de validação:
        - Cidadão deve existir na base FUC
        - Status deve ser ACTIVE
        - Não deve estar suspenso ou falecido
        
        Args:
            citizen_id: ID do cidadão a validar
            
        Returns:
            True se válido, False caso contrário
        """
        try:
            citizen_data = await self.get_citizen_data(citizen_id)
            
            # Validação de status
            status = citizen_data.get("status")
            
            if status != CitizenStatus.ACTIVE:
                logger.warning(
                    f"Cidadão {citizen_id} validação falhou: "
                    f"status={status}, esperado={CitizenStatus.ACTIVE}"
                )
                
                # Disparar evento de falha
                event = CitizenValidationFailed(
                    citizen_id=citizen_id,
                    reason=f"STATUS_INACTIVE",
                    details={
                        "current_status": status,
                        "expected_status": CitizenStatus.ACTIVE
                    }
                )
                await self.event_publisher.publish(event)
                
                # Registrar em auditoria REAL
                from app.core.audit import audit_log
                await audit_log(
                    action="CITIZEN_VALIDATION_FAILED",
                    resource_id=citizen_id,
                    resource_type="CitizenFUC",
                    new_value={
                        "reason": "STATUS_INACTIVE",
                        "current_status": status
                    },
                    db=self.db
                )
                
                return False
            
            # Disparar evento de sucesso
            event = CitizenValidated(
                citizen_id=citizen_id,
                status=status,
                full_name=citizen_data.get("full_name", ""),
                document_type=citizen_data.get("document_type", "")
            )
            await self.event_publisher.publish(event)
            
            # Registrar sucesso em auditoria REAL
            from app.core.audit import audit_log
            await audit_log(
                action="CITIZEN_VALIDATION_SUCCESS",
                resource_id=citizen_id,
                resource_type="CitizenFUC",
                new_value={
                    "status": status,
                    "full_name": citizen_data.get("full_name")
                },
                db=self.db
            )
            
            logger.info(f"Cidadão {citizen_id} validado com sucesso")
            return True
            
        except CitizenNotFoundError as e:
            logger.error(f"Cidadão {citizen_id} não encontrado no FUC: {str(e)}")
            
            event = CitizenValidationFailed(
                citizen_id=citizen_id,
                reason="NOT_FOUND",
                details={"error": str(e)}
            )
            await self.event_publisher.publish(event)
            
            from app.core.audit import audit_log
            await audit_log(
                action="CITIZEN_NOT_FOUND",
                resource_id=citizen_id,
                resource_type="CitizenFUC",
                new_value={"error": str(e)},
                db=self.db
            )
            
            return False
            
        except Exception as e:
            logger.exception(f"Erro inesperado ao validar cidadão {citizen_id}: {str(e)}")
            
            event = CitizenValidationFailed(
                citizen_id=citizen_id,
                reason="INTERNAL_ERROR",
                details={"error": str(e), "type": type(e).__name__}
            )
            await self.event_publisher.publish(event)
            
            from app.core.audit import audit_log
            await audit_log(
                action="CITIZEN_VALIDATION_ERROR",
                resource_id=citizen_id,
                resource_type="CitizenFUC",
                new_value={"error": str(e), "type": type(e).__name__},
                db=self.db
            )
            
            return False
    
    def get_citizen_from_cache(self, citizen_id: str) -> Optional[Dict[str, Any]]:
        """Recupera dados de cidadão do cache local."""
        return self._citizen_cache.get(citizen_id)
    
    def clear_cache(self) -> None:
        """Limpa cache de cidadãos (para testes)."""
        self._citizen_cache.clear()
