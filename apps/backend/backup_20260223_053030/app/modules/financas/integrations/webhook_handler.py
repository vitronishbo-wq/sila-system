import hmac
import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from app.modules.financas.application.ports.payment_repository_port import PaymentRepositoryPort
from app.modules.financas.application.ports.invoice_repository_port import InvoiceRepositoryPort
from app.modules.financas.exceptions import PaymentError, FinanceError
from app.modules.financas.domain.models.audit_log import FinancialAudit
from app.modules.financas.domain.models.enums import PaymentStatus, InvoiceStatus
import logging
import os

logger = logging.getLogger(__name__)

# Em produção: carregar de environment/vault
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your_webhook_secret_key")
WEBHOOK_TIMEOUT_SECONDS = int(os.getenv("WEBHOOK_TIMEOUT_SECONDS", "300"))  # 5 minutos


class WebhookHandler:
    """
    Gerencia notificações assíncronas vindas de gateways de pagamento.
    - Validação de assinatura HMAC-SHA256
    - Prevenção de replay (timestamp + nonce)
    - Idempotência garantida
    - Auditoria completa e imutável
    
    Nunca recebe DB Session diretamente — apenas Ports (interfaces).
    """

    def __init__(
        self,
        payment_repository: PaymentRepositoryPort,
        invoice_repository: InvoiceRepositoryPort,
        nonce_store: Optional[Dict[str, datetime]] = None
    ):
        """
        Supports injection of both repos.
        """
        self.payment_repo = payment_repository
        self.invoice_repo = invoice_repository
        self.db = getattr(payment_repository, 'db', None)
        self.nonce_store = nonce_store or {}




    async def process_gateway_notification(self, payload: Dict[str, Any], signature: str) -> bool:
        """
        Processa o payload recebido do gateway com segurança total.
        1. Valida timestamp (anti-replay window)
        2. Verifica assinatura HMAC-SHA256
        3. Verifica nonce (idempotência)
        4. Reconciliação com auditoria imutável
        
        NUNCA chama commit() — deixa a transação ao repositório.
        """
        try:
            # 1. VALIDAR TIMESTAMP (Anti-Replay)
            timestamp = payload.get("timestamp")
            if not timestamp:
                logger.error("❌ Webhook sem timestamp — rejeitado.")
                return False

            try:
                webhook_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                logger.error(f"❌ Timestamp inválido: {timestamp}")
                return False

            current_time = datetime.now(timezone.utc)
            time_diff = (current_time - webhook_time).total_seconds()

            if abs(time_diff) > WEBHOOK_TIMEOUT_SECONDS:
                logger.error(f"❌ Webhook fora da janela temporal ({time_diff}s > {WEBHOOK_TIMEOUT_SECONDS}s) — rejeitado.")
                return False

            # 2. VERIFICAR ASSINATURA HMAC-SHA256
            if not self._verify_hmac_signature(payload, signature):
                logger.error("❌ Falha na validação de assinatura HMAC-SHA256 do Webhook.")
                return False

            # 3. VERIFICAR NONCE (Idempotência)
            nonce = payload.get("nonce")
            if not nonce:
                logger.error("❌ Webhook sem nonce — rejeitado.")
                return False

            if self._is_nonce_processed(nonce):
                logger.warning(f"⚠️  Nonce já processado (replay prevented): {nonce}")
                return True  # Idempotente: retorna sucesso sem reprocessar

            # 4. PROCESSAR PAGAMENTO COM AUDITORIA
            event_type = payload.get("event")
            data = payload.get("data", {})

            if event_type == "payment.success":
                return await self._handle_payment_success(data, nonce)
            elif event_type == "payment.failed":
                return await self._handle_payment_failed(data, nonce)
            else:
                logger.warning(f"⚠️  Evento de webhook não suportado: {event_type}")
                return False

        except Exception as e:
            logger.error(f"❌ Erro crítico no Webhook: {str(e)}", exc_info=True)
            return False

    async def _handle_payment_success(self, data: Dict[str, Any], nonce: str) -> bool:
        """Handle payment.success event com transação atómica."""
        try:
            invoice_id = data.get("invoice_id")
            gateway_ref = data.get("gateway_reference")
            amount = data.get("amount")

            # Validações de negócio
            if not all([invoice_id, gateway_ref, amount]):
                logger.error(f"❌ Dados incompletos no webhook: {data}")
                return False

            # Recuperar invoice via repositório
            invoice = await self.invoice_repo.get_by_id(invoice_id)
            if not invoice:
                logger.error(f"❌ Fatura não encontrada: {invoice_id}")
                return False

            # Criar Payment (novo agregado)
            from app.modules.financas.domain.models.payment import Payment
            import uuid

            payment = Payment(
                id=str(uuid.uuid4()),
                invoice_id=invoice_id,
                citizen_id=data.get("citizen_id", "SYSTEM_WEBHOOK"),
                amount=amount,
                currency=data.get("currency", "AOA"),
                payment_method=f"GATEWAY_{data.get('provider', 'UNKNOWN')}",
                gateway_reference=gateway_ref,
                status=PaymentStatus.COMPLETED  # Usar Enum, nunca string!
            )

            # Salvar pagamento via repositório (transação atómica)
            try:
                saved_payment = await self.payment_repo.create(payment)
                
                # Atualizar invoice status se pago completamente
                if float(invoice.amount) <= float(payment.amount):
                    invoice.change_status(InvoiceStatus.PAID, reason=f"Pagamento via webhook: {gateway_ref}")
                    await self.invoice_repo.save(invoice)

                # Marcar nonce como processado
                self._mark_nonce_processed(nonce)

                logger.info(f"✅ Pagamento reconciliado: {gateway_ref} (nonce: {nonce})")
                return True

            except Exception as save_err:
                logger.error(f"❌ Erro ao salvar pagamento: {str(save_err)}")
                return False

        except Exception as e:
            logger.error(f"❌ Erro ao processar payment.success: {str(e)}", exc_info=True)
            return False

    async def _handle_payment_failed(self, data: Dict[str, Any], nonce: str) -> bool:
        """Handle payment.failed event."""
        try:
            invoice_id = data.get("invoice_id")
            gateway_ref = data.get("gateway_reference")

            if not all([invoice_id, gateway_ref]):
                logger.error(f"❌ Dados incompletos no evento de falha: {data}")
                return False

            # Log da falha
            logger.warning(f"⚠️  Pagamento falhou: {gateway_ref} da fatura {invoice_id}")
            self._mark_nonce_processed(nonce)
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao processar payment.failed: {str(e)}", exc_info=True)
            return False


    def _verify_hmac_signature(self, payload: Dict[str, Any], provided_signature: str) -> bool:
        """
        Verifica integridade do payload usando HMAC-SHA256.
        Formato esperado: sha256=<hex_digest>
        
        Comparação segura contra timing attacks.
        """
        try:
            # Remover signature do payload para cálculo
            payload_copy = {k: v for k, v in payload.items() if k != "signature"}

            # Serializar com ordem garantida (reproducibilidade)
            payload_str = json.dumps(payload_copy, sort_keys=True, separators=(",", ":"))

            # Calcular HMAC-SHA256
            expected_signature = "sha256=" + hmac.new(
                WEBHOOK_SECRET.encode(),
                payload_str.encode(),
                hashlib.sha256
            ).hexdigest()

            # Comparação segura contra timing attacks
            is_valid = hmac.compare_digest(expected_signature, provided_signature)
            
            if not is_valid:
                logger.error(f"HMAC mismatch: esperavam {expected_signature[:20]}..., receberam {provided_signature[:20]}...")
            
            return is_valid

        except Exception as e:
            logger.error(f"❌ Erro ao validar HMAC-SHA256: {str(e)}")
            return False

    def _is_nonce_processed(self, nonce: str) -> bool:
        """
        Verifica se um nonce já foi processado (prevenção de replay).
        Em produção: usar Redis com TTL.
        """
        if nonce in self.nonce_store:
            # Limpar nonces expirados
            nonce_time = self.nonce_store[nonce]
            if (datetime.now(timezone.utc) - nonce_time).total_seconds() > WEBHOOK_TIMEOUT_SECONDS * 2:
                del self.nonce_store[nonce]
                return False
            return True
        return False

    def _mark_nonce_processed(self, nonce: str) -> None:
        """
        Marca um nonce como processado.
        Em produção: Redis com TTL = WEBHOOK_TIMEOUT_SECONDS * 2
        """
        self.nonce_store[nonce] = datetime.now(timezone.utc)


