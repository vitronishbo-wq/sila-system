"""AGT Webhook Handler for event processing"""

import hmac
import hashlib
import json
from typing import Dict, Any, Callable, Awaitable, Optional
from datetime import datetime
from .agt_exceptions import AGTValidationError


class AGTWebhookHandler:
    """Handle webhooks from AGT with signature verification"""
    
    def __init__(self, webhook_secret: str):
        self.webhook_secret = webhook_secret
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]] = {}
    
    def register_handler(
        self,
        event_type: str,
        handler: Callable[[Dict[str, Any]], Awaitable[None]]
    ):
        """Register handler for event type"""
        self._handlers[event_type] = handler
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature using HMAC-SHA256"""
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    
    async def handle_webhook(
        self,
        payload: str,
        signature: str,
    ) -> None:
        """Process webhook with signature verification"""
        if not self.verify_signature(payload, signature):
            raise AGTValidationError("Invalid webhook signature")
        
        try:
            event = json.loads(payload)
        except json.JSONDecodeError as e:
            raise AGTValidationError(f"Invalid JSON payload: {str(e)}")
        
        event_type = event.get('event_type')
        if not event_type:
            raise AGTValidationError("Missing 'event_type' field")
        
        # Verify event structure
        self._validate_event_structure(event)
        
        # Dispatch to handler
        handler = self._handlers.get(event_type)
        if handler:
            await handler(event)
    
    def _validate_event_structure(self, event: Dict[str, Any]) -> None:
        """Validate event has required fields"""
        required = ['event_type', 'event_id', 'timestamp', 'data']
        missing = [f for f in required if f not in event]
        if missing:
            raise AGTValidationError(f"Missing fields: {', '.join(missing)}")
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(event['timestamp'])
        except (ValueError, TypeError):
            raise AGTValidationError("Invalid timestamp format")
    
    async def handle_declaration_update(
        self,
        event: Dict[str, Any]
    ) -> None:
        """Handle declaration.update event"""
        data = event.get('data', {})
        
        required = ['nif', 'protocol', 'status']
        missing = [f for f in required if f not in data]
        if missing:
            raise AGTValidationError(f"Missing fields in declaration.update: {', '.join(missing)}")
        
        nif = data['nif']
        protocol = data['protocol']
        status = data['status']
        
        # Dispatch to registered handler
        handler = self._handlers.get('declaration.update')
        if handler:
            await handler(event)
    
    async def handle_payment_confirmation(
        self,
        event: Dict[str, Any]
    ) -> None:
        """Handle payment.confirm event"""
        data = event.get('data', {})
        
        required = ['nif', 'reference', 'amount', 'method']
        missing = [f for f in required if f not in data]
        if missing:
            raise AGTValidationError(f"Missing fields in payment.confirm: {', '.join(missing)}")
        
        # Dispatch to registered handler
        handler = self._handlers.get('payment.confirm')
        if handler:
            await handler(event)
    
    async def handle_certificate_issued(
        self,
        event: Dict[str, Any]
    ) -> None:
        """Handle certificate.issued event"""
        data = event.get('data', {})
        
        required = ['nif', 'certificate_id', 'certificate_type']
        missing = [f for f in required if f not in data]
        if missing:
            raise AGTValidationError(f"Missing fields in certificate.issued: {', '.join(missing)}")
        
        # Dispatch to registered handler
        handler = self._handlers.get('certificate.issued')
        if handler:
            await handler(event)
    
    async def handle_debt_created(
        self,
        event: Dict[str, Any]
    ) -> None:
        """Handle debt.created event"""
        data = event.get('data', {})
        
        required = ['nif', 'debt_number', 'amount', 'tax_type', 'due_date']
        missing = [f for f in required if f not in data]
        if missing:
            raise AGTValidationError(f"Missing fields in debt.created: {', '.join(missing)}")
        
        # Dispatch to registered handler
        handler = self._handlers.get('debt.created')
        if handler:
            await handler(event)
    
    async def handle_taxpayer_updated(
        self,
        event: Dict[str, Any]
    ) -> None:
        """Handle taxpayer.updated event"""
        data = event.get('data', {})
        
        required = ['nif']
        missing = [f for f in required if f not in data]
        if missing:
            raise AGTValidationError(f"Missing fields in taxpayer.updated: {', '.join(missing)}")
        
        # Dispatch to registered handler
        handler = self._handlers.get('taxpayer.updated')
        if handler:
            await handler(event)
    
    async def dispatch_event(self, event: Dict[str, Any]) -> None:
        """Generic event dispatch with validation"""
        event_type = event.get('event_type')
        handler = self._handlers.get(event_type)
        
        if handler:
            await handler(event)
        # Silently ignore unhandled event types
