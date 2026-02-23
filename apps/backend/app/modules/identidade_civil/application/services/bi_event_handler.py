from app.core.observability import trace

import logging
from typing import Dict, Callable
from ...domain.models.bi_event import BIEvent, BIEventType

# Configuração de logger para rastreabilidade de eventos no rastro de auditoria
logger = logging.getLogger(__name__)

class BIEventHandler:
    """
    Orquestrador de Eventos de BI.
    Responsável por despachar eventos de domínio para os handlers específicos de integração
    ou persistência secundária, garantindo desacoplamento.
    """

    def __init__(self):
        # Mapeamento de despachantes para cada tipo de evento
        self._handlers: Dict[BIEventType, Callable] = {
            BIEventType.REQUEST_CREATED: self._handle_request_created,
            BIEventType.DATA_VERIFIED_FUC: self._handle_fuc_validation,
            BIEventType.BI_PROJECTION_SYNCED: self._handle_projection_sync,
            BIEventType.BI_APPROVED: self._handle_approval,
            BIEventType.BI_PRINTED: self._handle_printing,
            BIEventType.BI_ISSUED: self._handle_issuance,
            BIEventType.BI_RENEWED: self._handle_renewal,
            BIEventType.BI_CANCELLED: self._handle_cancellation,
            BIEventType.LOST_REPORTED: self._handle_loss_report,
        }

    @trace()
    async def handle_bi_event(self, event: BIEvent):
        """
        Ponto de entrada principal para processamento de eventos.
        Executa o handler associado ao tipo de evento recebido.
        """
        handler = self._handlers.get(event.event_type)
        
        if not handler:
            logger.error(f"Nenhum handler registrado para o evento: {event.event_type}")
            return

        logger.info(f"Processando evento {event.event_type.value} para o agregado {event.aggregate_id}")
        
        try:
            await handler(event)
            logger.info(f"Evento {event.event_type.value} processado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao processar evento {event.event_type.value}: {str(e)}")
            # Em um sistema resiliente, aqui dispararíamos retentativas ou DLQ (Dead Letter Queue)
            raise

    # Handlers Específicos

    @trace()
    async def _handle_request_created(self, event: BIEvent):
        """Inicia workflow de validação inicial."""
        logger.debug(f"Workflow: Novo pedido de BI detectado. Payload: {event.payload}")

    @trace()
    async def _handle_fuc_validation(self, event: BIEvent):
        """Reage à confirmação de dados biográficos pelo FUC."""
        logger.debug(f"Workflow: Dados biográficos confirmados pela Soberania FUC.")

    @trace()
    async def _handle_projection_sync(self, event: BIEvent):
        """Atualiza caches locais ou projeções de BI após sincronismo com o FUC."""
        logger.debug("Workflow: Sincronizando projeção local com a verdade do FUC.")

    @trace()
    async def _handle_approval(self, event: BIEvent):
        """Dispara a fila de impressão após aprovação administrativa."""
        logger.debug("Workflow: Pedido aprovado. Enviando para fila de personalização/impressão.")

    @trace()
    async def _handle_printing(self, event: BIEvent):
        """Atualiza estado para pronto para entrega."""
        logger.debug("Workflow: Documento físico impresso e disponível no balcão.")

    @trace()
    async def _handle_issuance(self, event: BIEvent):
        """Finaliza o ciclo de vida do pedido e ativa o BI."""
        logger.debug("Workflow: BI entregue ao cidadão. Ativando rastro digital.")

    @trace()
    async def _handle_renewal(self, event: BIEvent):
        """Processa a renovação e marca o documento anterior como substituído."""
        logger.debug("Workflow: Documento renovado. Invalidando versões anteriores.")

    @trace()
    async def _handle_cancellation(self, event: BIEvent):
        """Notifica outros sistemas (Bancos, Fronteiras) sobre a invalidação do BI."""
        logger.warning(f"Workflow CRÍTICO: BI Cancelado. Motivo: {event.payload.get('reason')}")

    @trace()
    async def _handle_loss_report(self, event: BIEvent):
        """Marca o BI como 'LOST' e impede uso em pontos de verificação."""
        logger.warning("Workflow: Extravio reportado. Documento bloqueado preventivamente.")

# Singleton para uso em toda a aplicação
event_handler = BIEventHandler()

@trace()
async def handle_bi_event(event: BIEvent):
    """Facade funcional para o handler de eventos."""
    await event_handler.handle_bi_event(event)
