"""Security validators for payment module."""

import logging
import re
from typing import Optional
from decimal import Decimal

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class PaymentValidator:
    """Validator for payment operations."""

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate payment amount."""
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor do pagamento deve ser maior que zero",
            )
        if amount > 999999999.99:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor do pagamento excede o limite máximo",
            )
        return True

    @staticmethod
    def validate_currency(currency: str) -> bool:
        """Validate currency code."""
        valid_currencies = ["AOA", "USD", "EUR", "ZAR", "BRL"]
        if currency.upper() not in valid_currencies:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Moeda inválida. Moedas aceitas: {', '.join(valid_currencies)}",
            )
        return True

    @staticmethod
    def validate_reference(reference: str) -> bool:
        """Validate payment reference."""
        if not reference or len(reference) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência deve ter pelo menos 3 caracteres",
            )
        if len(reference) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência não pode exceder 100 caracteres",
            )
        # Allow alphanumeric, hyphens, and underscores
        if not re.match(r"^[a-zA-Z0-9\-_]+$", reference):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referência contém caracteres inválidos",
            )
        return True

    @staticmethod
    def validate_webhook_url(url: str) -> bool:
        """Validate webhook URL."""
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="URL do webhook é inválida",
            )
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address."""
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_pattern.match(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Endereço de email inválido",
            )
        return True

    @staticmethod
    def validate_refund_amount(refund_amount: float, payment_amount: float) -> bool:
        """Validate refund amount."""
        if refund_amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor do reembolso deve ser maior que zero",
            )
        if refund_amount > payment_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valor do reembolso não pode exceder o valor do pagamento",
            )
        return True

    @staticmethod
    def validate_description(description: Optional[str]) -> bool:
        """Validate payment description."""
        if description and len(description) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Descrição não pode exceder 500 caracteres",
            )
        return True

    @staticmethod
    def validate_metadata(metadata: Optional[dict]) -> bool:
        """Validate payment metadata."""
        if metadata:
            if not isinstance(metadata, dict):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Metadados devem ser um objeto JSON",
                )
            # Check size (max 10KB)
            import json

            if len(json.dumps(metadata)) > 10000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Metadados excedem o tamanho máximo de 10KB",
                )
        return True


class RateLimiter:
    """Rate limiter for payment operations."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed."""
        import time

        current_time = time.time()

        if identifier not in self.requests:
            self.requests[identifier] = []

        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time
            for req_time in self.requests[identifier]
            if current_time - req_time < self.window_seconds
        ]

        if len(self.requests[identifier]) >= self.max_requests:
            return False

        self.requests[identifier].append(current_time)
        return True

    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests for identifier."""
        if identifier not in self.requests:
            return self.max_requests

        import time

        current_time = time.time()

        self.requests[identifier] = [
            req_time
            for req_time in self.requests[identifier]
            if current_time - req_time < self.window_seconds
        ]

        return max(0, self.max_requests - len(self.requests[identifier]))


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
