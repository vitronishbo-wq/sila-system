from __future__ import annotations
import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID
from app.modules.infrastructure_sector.meteorologia.application.ports import AlertaServicePort, RequestServicePort
logger = logging.getLogger(__name__)

class AlertaMeteorologicoService(AlertaServicePort):

    def __init__(self, request_service: RequestServicePort | None=None) -> None:
        self.request_service = request_service

    async def publicar_alerta(self, *, estacao_id: UUID, alerta: dict[str, Any], observacao_id: UUID | None=None) -> bool:
        try:
            logger.warning('Alerta meteorologico publicado | estacao=%s observacao=%s tipo=%s severidade=%s mensagem=%s', estacao_id, observacao_id, alerta.get('tipo'), alerta.get('severidade'), alerta.get('mensagem'))
            return True
        except Exception:
            logger.exception('Falha ao publicar alerta meteorologico')
            return False

    async def notificar_defesa_civil(self, *, alertas: list[dict[str, Any]], provincia: str) -> bool:
        if not alertas:
            return True
        if self.request_service is None:
            logger.info('Request service nao configurado; alerta para defesa civil apenas logado (provincia=%s)', provincia)
            return True
        payload = {'tipo': 'ALERTA_METEOROLOGICO', 'provincia': provincia, 'prioridade': 'ALTA' if any((a.get('severidade') in {'HIGH', 'EXTREME'} for a in alertas)) else 'MEDIA', 'dados': {'alertas': alertas, 'timestamp': datetime.now(timezone.utc).isoformat()}}
        return await self.request_service.criar_request(payload)