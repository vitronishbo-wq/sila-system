"""
CitizenService — Serviço central de validação e consulta ao FUC.
Ponto único de entrada para qualquer módulo que necessite validar
a elegibilidade de um cidadão antes de operações financeiras ou administrativas.
"""
import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.citizen.enums import CitizenStatus
from app.citizen.exceptions import CitizenNotFoundError
from app.core.events import CitizenValidated, CitizenValidationFailed
from app.citizen.core.audit import ImmutableAuditWriter
from typing import Any as _Any

logger = logging.getLogger(__name__)

# Type alias para handlers de eventos
EventHandler = Callable[[Any], Coroutine[Any, Any, None]]


class CitizenService:
    """
    Serviço de domínio para validação e consulta do Ficheiro Único do Cidadão (FUC).

    Responsabilidades:
    - Consultar dados do cidadão via projeção local ou API FUC externa
    - Validar elegibilidade para operações (financeiras, administrativas)
    - Emitir eventos de domínio (CitizenValidated / CitizenValidationFailed)
    - Registar auditoria imutável de cada validação
    """

    def __init__(
        self,
        db_session: Optional[AsyncSession] = None,
        event_handlers: Optional[List[EventHandler]] = None,
        fuc_adapter: Optional[_Any] = None,
        notification_adapter: Optional[_Any] = None,
    ):
        self.db = db_session
        self._event_handlers: List[EventHandler] = event_handlers or []
        self._audit_writer = ImmutableAuditWriter(db=db_session)
        # Adapters (injected implementations live in infra or other modules)
        self._fuc_adapter = fuc_adapter
        self._notification_adapter = notification_adapter

    async def get_citizen_data(self, citizen_id: str) -> Dict[str, Any]:
        """
        Busca dados do cidadão. Em produção, consulta a tabela `citizen_fuc`
        (projeção) ou fallback para a API FUC externa via CitizenFUCClient.

        Args:
            citizen_id: Identificador único do cidadão (BI, NIF, ou UUID).

        Returns:
            Dict com dados biográficos e status do cidadão.

        Raises:
            CitizenNotFoundError: Se o cidadão não for localizado.
        """
        if not citizen_id or len(citizen_id.strip()) == 0:
            raise CitizenNotFoundError(citizen_id or "")

        # Tentativa via projeção local (DB)
        if self.db:
            from sqlalchemy import select

            result = await self.db.execute(
                select(CitizenFUC).where(CitizenFUC.citizen_id == citizen_id)
            )
            projection = result.scalars().first()
            if projection:
                return {
                    "id": str(projection.citizen_id),
                    "full_name": projection.full_name,
                    "status": CitizenStatus.ACTIVE
                    if projection.vital_status.value == "ALIVE"
                    else CitizenStatus.DECEASED,
                    "vital_status": projection.vital_status.value,
                    "document_type": "BI",
                }

        # If an external FUC adapter is provided, prefer it over the stub.
        if self._fuc_adapter:
            try:
                external = await self._fuc_adapter.get_citizen(UUID(citizen_id))
                if not external:
                    raise CitizenNotFoundError(citizen_id)
                return external
            except CitizenNotFoundError:
                raise
            except Exception:
                # Adapter failed — fall back to internal stub behaviour below
                logger.info(
                    f"CITIZEN_SERVICE: FUC adapter failed for {citizen_id}, using local stub"
                )

        # Fallback: simulação / stub (em produção: CitizenFUCClient)
        logger.info(f"CITIZEN_SERVICE: Consulta local sem resultado, usando stub para {citizen_id}")

        # Regras de simulação (alinhadas com FUCClient existente)
        if citizen_id.upper().startswith("INVALID") or "INEXISTENT" in citizen_id.upper():
            raise CitizenNotFoundError(citizen_id)

        if citizen_id.upper().startswith("DECEASED"):
            return {
                "id": citizen_id,
                "full_name": "Cidadão Falecido (Stub)",
                "status": CitizenStatus.DECEASED,
                "document_type": "BI",
            }

        if citizen_id.upper().startswith("SUSPENDED"):
            return {
                "id": citizen_id,
                "full_name": "Cidadão Suspenso (Stub)",
                "status": CitizenStatus.SUSPENDED,
                "document_type": "BI",
            }

        return {
            "id": citizen_id,
            "full_name": "António Manuel dos Santos",
            "status": CitizenStatus.ACTIVE,
            "document_type": "BI",
        }

    async def validate_citizen(self, citizen_id: str) -> bool:
        """
        Valida se o cidadão está apto para operações financeiras/administrativas.

        Regra de Ouro: apenas cidadãos com status ACTIVE são elegíveis.

        Args:
            citizen_id: Identificador do cidadão.

        Returns:
            True se o cidadão está activo e elegível, False caso contrário.
        """
        try:
            data = await self.get_citizen_data(citizen_id)

            if data["status"] != CitizenStatus.ACTIVE:
                logger.warning(
                    f"CITIZEN_SERVICE: Cidadão {citizen_id} bloqueado — status={data['status']}"
                )
                event = CitizenValidationFailed(
                    citizen_id=citizen_id,
                    reason=f"STATUS_{data['status'].value}",
                    details=data,
                )
                await self._emit_event(event)
                await self._audit_writer.record_validation_failure(event)
                return False

            event = CitizenValidated(
                citizen_id=citizen_id,
                status=data["status"].value,
            )
            await self._emit_event(event)
            await self._audit_writer.record_validation_success(event)

            logger.info(f"CITIZEN_SERVICE: Cidadão {citizen_id} validado com SUCESSO.")
            return True

        except CitizenNotFoundError:
            event = CitizenValidationFailed(
                citizen_id=citizen_id,
                reason="CITIZEN_NOT_FOUND",
                details={},
            )
            await self._emit_event(event)
            await self._audit_writer.record_validation_failure(event)
            return False

        except Exception as e:
            logger.error(f"CITIZEN_SERVICE: Erro crítico ao validar {citizen_id}: {e}")
            event = CitizenValidationFailed(
                citizen_id=citizen_id,
                reason=str(e),
                details={},
            )
            await self._emit_event(event)
            return False

    async def _emit_event(self, event: Any) -> None:
        """Despacha evento para todos os handlers registados."""
        for handler in self._event_handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(
                    f"CITIZEN_EVENT_DISPATCH: Falha no handler para "
                    f"{type(event).__name__}: {e}"
                )
