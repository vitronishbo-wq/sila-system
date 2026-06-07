"""
Ponte de integração entre TransferenciaService e AutomationEngine (PASSO 13 & 14)

Este módulo integra o serviço de transferência com o motor de automação
que utiliza RabbitMQ para processar eventos de transferência em tempo real.
"""

import logging
from typing import Any
from uuid import UUID

from foundation.automation.automator import AutomationEngine

logger = logging.getLogger(__name__)


class TransferAutomationBridge:
    """Integra TransferenciaService com AutomationEngine via message bus."""

    def __init__(self, automation_engine: AutomationEngine | None = None):
        """
        Inicializa a ponte.

        Args:
            automation_engine: Instância do AutomationEngine. Se None, cria uma nova.
        """
        self.engine = automation_engine or AutomationEngine()

    def request_transfer_async(
        self,
        student_id: UUID | str,
        target_school: str | UUID,
        target_class: str | UUID,
        academic_year: int,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Solicita uma transferência de forma assíncrona via PASSO 13.

        Publica o evento `transfer_requested` para ser processado:
        1. transfer_requested → Validação inicial
        2. transfer_validated → Execução da transferência
        3. transfer_completed ou transfer_failed

        Args:
            student_id: ID do aluno
            target_school: ID ou nome da escola destino
            target_class: ID ou nome da turma destino
            academic_year: Ano letivo
            metadata: Metadados adicionais (origem, motivo, etc)

        Returns:
            Dict com status "scheduled", "rejected" ou "executed"
        """
        request = {
            "student_id": str(student_id),
            "target_school": str(target_school),
            "target_class": str(target_class),
            "academic_year": academic_year,
            "metadata": metadata or {},
        }

        logger.info(
            "Solicitando transferência assíncrona: student_id=%s target_school=%s",
            student_id,
            target_school,
        )

        try:
            result = self.engine.request_transfer(request, async_execute=True)
            logger.info("Transferência agendada: %s", result)
            return result
        except Exception as e:
            logger.exception("Erro ao agendar transferência: %s", e)
            return {"status": "error", "error": str(e)}

    def request_transfer_sync(
        self,
        student_id: UUID | str,
        target_school: str | UUID,
        target_class: str | UUID,
        academic_year: int,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Solicita uma transferência de forma síncrona.

        Aguarda a execução completa do fluxo antes de retornar.

        Args:
            student_id: ID do aluno
            target_school: ID ou nome da escola destino
            target_class: ID ou nome da turma destino
            academic_year: Ano letivo
            metadata: Metadados adicionais

        Returns:
            Dict com status "executed", "rejected" ou "error"
        """
        request = {
            "student_id": str(student_id),
            "target_school": str(target_school),
            "target_class": str(target_class),
            "academic_year": academic_year,
            "metadata": metadata or {},
        }

        logger.info(
            "Solicitando transferência síncrona: student_id=%s target_school=%s",
            student_id,
            target_school,
        )

        try:
            result = self.engine.request_transfer(request, async_execute=False)
            logger.info("Transferência executada: %s", result)
            return result
        except Exception as e:
            logger.exception("Erro ao executar transferência: %s", e)
            return {"status": "error", "error": str(e)}

    def stop(self):
        """Encerra o motor de automação de forma segura."""
        try:
            self.engine.stop()
            logger.info("AutomationEngine encerrado")
        except Exception as e:
            logger.exception("Erro ao encerrar AutomationEngine: %s", e)
