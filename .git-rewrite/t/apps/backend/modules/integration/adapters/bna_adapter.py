"""BNA (Banco Nacional de Angola) Adapter for SILA Integration Module"""

from datetime import datetime
from typing import Any, Dict, Optional

import requests

from config import settings


class BNAAdapter:
    """Adapter for interacting with Banco Nacional de Angola APIs"""

    def __init__(
        self, api_key: str = settings.BNA_API_KEY, base_url: str = settings.BNA_API_URL
    ):
        self.api_key = api_key
        self.base_url = base_url

        # Only initialize session for non-mock environments
        if settings.ENVIRONMENT not in ["development", "testing"]:
            self.session = requests.Session()
            self.session.headers.update(
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
            )

    def get_exchange_rates(self, currency: Optional[str] = None) -> Dict[str, Any]:
        """Get current exchange rates from BNA"""
        # Mock data for development/testing environments
        if settings.ENVIRONMENT in ["development", "testing"]:
            print(
                f"[{settings.ENVIRONMENT.upper()} MODE] Returning mocked BNA rates..."
            )
            MOCK_RATES = {"USD": 830.25, "EUR": 880.10, "ZAR": 45.50, "GBP": 1020.75}
            if currency:
                return {currency: MOCK_RATES.get(currency, 850.00)}
            return MOCK_RATES

        # Real API call for production/staging
        endpoint = f"{self.base_url}/v1/exchange-rates"
        params = {"currency": currency} if currency else None

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch exchange rates: {str(e)}")

    def get_currency_history(
        self, currency: str, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Get historical currency data"""
        # Mock data for development/testing environments
        if settings.ENVIRONMENT in ["development", "testing"]:
            print(
                f"[{settings.ENVIRONMENT.upper()} MODE] Returning mocked BNA history..."
            )
            return {
                "currency": currency,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "rates": [
                    {"date": "2025-10-01", "rate": 830.25},
                    {"date": "2025-10-15", "rate": 835.50},
                    {"date": "2025-10-24", "rate": 840.75},
                ],
            }

        # Real API call for production/staging
        endpoint = f"{self.base_url}/v1/currency-history/{currency}"
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch currency history: {str(e)}")

    def verify_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Verify a transaction with BNA"""
        # Mock data for development/testing environments
        if settings.ENVIRONMENT in ["development", "testing"]:
            print(
                f"[{settings.ENVIRONMENT.upper()} MODE] Returning mocked transaction verification..."
            )
            return {
                "transaction_id": transaction_id,
                "status": "completed",
                "amount": 1000.00,
                "currency": "AOA",
                "timestamp": "2025-10-24T10:00:00Z",
            }

        # Real API call for production/staging
        endpoint = f"{self.base_url}/v1/transactions/verify/{transaction_id}"

        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to verify transaction: {str(e)}")
