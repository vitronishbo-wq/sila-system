from app.core.observability import trace
from typing import Dict, Any, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from ...integrations.citizen_fuc_client import CitizenFUCClient
from ...domain.models.identity_request import IdentityRequest
from ...domain.models.bi_event import BIEvent, BIEventType
from ...infrastructure.repositories.identity_request_repository import IdentityRequestRepository
from ...infrastructure.logging_config import logger_alter
from ...exceptions import BusinessRuleException, SovereigntyValidationException
from .bi_event_handler import handle_bi_event


class AlterDataService:
    """
    Serviço especializado em 'Alteração de Dados no BI' (Código 003).
    
    PRINCÍPIO DE SOBERANIA: No SILA, a Identidade Civil não altera dados do cidadão.
    Este serviço sincroniza (espelha) a verdade do FUC no contexto do documento de identidade.
    
    DEPENDÊNCIAS INJETADAS:
    - ir_repository: Persistência de processos administrativos
    - fuc_client: Validação de soberania
    """

    def __init__(
        self,
        session: AsyncSession,
        fuc_client: Optional[CitizenFUCClient] = None,
    ):
        self.ir_repository = IdentityRequestRepository(session)
        self.fuc_client = fuc_client or CitizenFUCClient()

    @trace()
    async def execute_data_sync(
        self,
        citizen_fuc_id: str,
        operator_id: str,
        updated_fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Executa o workflow do serviço 003:
        1. Cria objeto de orquestração (Request)
        2. Consulta a verdade soberana (FUC)
        3. Valida se os dados solicitados são consistentes com o FUC
        4. Regista facto imutável (BI_PROJECTION_SYNCED)
        5. Dispara efeitos colaterais via Event Handler
        """
        request_id = uuid.uuid4()
        
        async with logger_alter.audit_context(
            "BI_DATA_SYNC",
            audit_id=str(request_id),
            citizen_fuc_id=citizen_fuc_id,
            operator_id=operator_id,
            fields=list(updated_fields.keys()),
        ) as audit:
            logger_alter.info(
                "Iniciando sincronismo de dados com FUC",
                citizen_fuc_id=citizen_fuc_id,
                fields=list(updated_fields.keys()),
            )

            # 1. Orquestração Administrativa
            identity_request = IdentityRequest(
                id=request_id,
                citizen_fuc_id=citizen_fuc_id,
                service_code="003",
                status="pending_fuc_validation",
                notes=[f"[{operator_id}] Solicitação de sincronismo de dados"],
            )

            try:
                # 2. Consulta à Projeção de Soberania (Read-Only Bridge)
                projection = await self.fuc_client.get_citizen_by_id(citizen_fuc_id)

                if not projection:
                    identity_request.status = "rejected"
                    identity_request.notes.append(
                        "[SYSTEM] Cidadão não localizado no FUC"
                    )
                    await self.ir_repository.save(identity_request)
                    
                    raise SovereigntyValidationException(
                        detail=f"Cidadão {citizen_fuc_id} não encontrado no FUC"
                    )

                # 3. Validação de Consistência
                mismatches = []
                for field, value in updated_fields.items():
                    fuc_value = getattr(projection, field, None)
                    if fuc_value != value:
                        mismatches.append(
                            f"{field}: FUC=[{fuc_value}], Pedido=[{value}]"
                        )

                if mismatches:
                    identity_request.status = "rejected"
                    identity_request.notes.append(
                        f"[SYSTEM] Divergência de soberania detectada: {len(mismatches)} Campo(s)"
                    )
                    await self.ir_repository.save(identity_request)
                    
                    logger_alter.warning(
                        "Divergência detectada entre solicitação e FUC",
                        citizen_fuc_id=citizen_fuc_id,
                        mismatches=mismatches,
                    )
                    raise BusinessRuleException(
                        detail="Dados divergem da base soberana FUC"
                    )

                # 4. Registro do Facto Imutável (Event Sourcing)
                event = BIEvent.create(
                    aggregate_id=str(request_id),
                    event_type=BIEventType.BI_PROJECTION_SYNCED,
                    operator_id=operator_id,
                    payload={
                        "service_code": "003",
                        "fuc_id": citizen_fuc_id,
                        "fields_synced": list(updated_fields.keys()),
                        "projection_timestamp": projection.sync_timestamp.isoformat(),
                    },
                )

                # 5. Despacho de Evento (Efeitos Colaterais)
                await handle_bi_event(event)
                logger_alter.info(
                    "Evento de sincronismo registrado",
                    event_id=str(event.id),
                )

                # 6. Conclusão do Processo
                identity_request.status = "completed"
                identity_request.notes.append(
                    "[SYSTEM] Sincronização com FUC concluída com sucesso"
                )
                await self.ir_repository.save(identity_request)

                logger_alter.info(
                    "Sincronismo de dados concluído com sucesso",
                    request_id=str(request_id),
                    citizen_fuc_id=citizen_fuc_id,
                )

                return {
                    "success": True,
                    "request_id": str(request_id),
                    "event_id": str(event.id),
                    "status": "completed",
                    "message": "Dados de identidade sincronizados com sucesso.",
                }

            except Exception as e:
                logger_alter.error(
                    "Erro durante sincronismo de dados",
                    citizen_fuc_id=citizen_fuc_id,
                    error=str(e),
                    exc_info=True,
                )
                identity_request.status = "cancelled"
                identity_request.notes.append(f"[SYSTEM] Erro: {str(e)}")
                await self.ir_repository.save(identity_request)
                raise

