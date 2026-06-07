"""
API Endpoints para transferências com automação real (PASSO 13 & 14)

Estes endpoints integram com RabbitMQ/Kafka via AutomationEngine para
processar transferências de forma assíncrona em tempo real.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.application.automation_bridge import TransferAutomationBridge
from foundation.automation.automator import AutomationEngine

router = APIRouter(prefix="/transferencias/automacao", tags=["Educacao - Transferencias - Automacao"])

# Singleton para AutomationEngine
_automation_engine: AutomationEngine | None = None
_bridge: TransferAutomationBridge | None = None


def get_automation_bridge() -> TransferAutomationBridge:
    """Dependency para obter a ponte de automação."""
    global _bridge
    if _bridge is None:
        global _automation_engine
        _automation_engine = AutomationEngine()
        _bridge = TransferAutomationBridge(_automation_engine)
    return _bridge


class TransferAutomationRequest(BaseModel):
    """Solicitação de transferência automática."""

    student_id: str
    target_school: str
    target_class: str
    academic_year: int
    metadata: dict | None = None


class TransferAutomationResponse(BaseModel):
    """Resposta de transferência automática."""

    status: str  # "scheduled", "executed", "rejected", "error"
    evaluation: dict | None = None
    error: str | None = None


@router.post("/async", response_model=TransferAutomationResponse, status_code=status.HTTP_202_ACCEPTED)
async def request_transfer_async(
    data: TransferAutomationRequest,
    bridge: TransferAutomationBridge = Depends(get_automation_bridge),
    _: dict = Depends(get_current_user),
):
    """
    Solicita uma transferência de forma assíncrona via PASSO 13.

    **PASSO 13: Automação Real com RabbitMQ/Kafka**

    Fluxo:
    1. request_transfer_async() publica `transfer_requested` em RabbitMQ
    2. Automation worker consume e publica `transfer_validated`
    3. Executa a transferência e publica `transfer_completed` ou `transfer_failed`
    4. Se falhar após retries, mensagem vai para DLQ (PASSO 14)

    Returns:
        - status: "scheduled" = agendado com sucesso
        - status: "rejected" = não elegível
        - status: "error" = erro durante agendamento
    """
    try:
        result = bridge.request_transfer_async(
            student_id=data.student_id,
            target_school=data.target_school,
            target_class=data.target_class,
            academic_year=data.academic_year,
            metadata=data.metadata,
        )

        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Erro desconhecido"),
            )

        return TransferAutomationResponse(
            status=result["status"],
            evaluation=result.get("evaluation"),
            error=result.get("error"),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao agendar transferência: {str(e)}",
        ) from e


@router.post("/sync", response_model=TransferAutomationResponse, status_code=status.HTTP_200_OK)
async def request_transfer_sync(
    data: TransferAutomationRequest,
    bridge: TransferAutomationBridge = Depends(get_automation_bridge),
    _: dict = Depends(get_current_user),
):
    """
    Solicita uma transferência de forma síncrona (aguarda conclusão).

    **Para testes e processamento imediato**

    Fluxo:
    1. Valida a transferência
    2. Executa imediatamente (sem RabbitMQ)
    3. Retorna resultado completo

    Returns:
        - status: "executed" = executado com sucesso
        - status: "rejected" = não elegível
        - status: "error" = erro durante execução
    """
    try:
        result = bridge.request_transfer_sync(
            student_id=data.student_id,
            target_school=data.target_school,
            target_class=data.target_class,
            academic_year=data.academic_year,
            metadata=data.metadata,
        )

        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Erro desconhecido"),
            )

        return TransferAutomationResponse(
            status=result["status"],
            evaluation=result.get("evaluation"),
            error=result.get("error"),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar transferência: {str(e)}",
        ) from e


@router.on_event("shutdown")
async def shutdown_automation():
    """Encerra o motor de automação ao desligar a aplicação."""
    global _bridge
    if _bridge is not None:
        try:
            _bridge.stop()
        except Exception:
            pass
