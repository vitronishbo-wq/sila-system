"""AGT Real API Client with httpx and retry logic"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
)
from .agt_exceptions import (
    AGTException,
    AGTTimeoutError,
    AGTAuthenticationError,
    AGTNotFoundError,
    AGTRateLimitError,
    AGTValidationError,
)
from .agt_rate_limiter import AGTRateLimiter


class AGTAPIClient:
    """Real AGT API client with retry logic and rate limiting"""
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._rate_limiter = AGTRateLimiter()
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._get_headers()
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard API headers"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'SILATaxpayerModule/1.0',
        }
    
    def _ensure_client(self):
        """Ensure client is initialized"""
        if not self._client:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._get_headers()
            )
    
    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response with error mapping"""
        try:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                errors = response.json().get('errors', [response.text])
                raise AGTValidationError(f"Validation failed", errors=errors)
            elif response.status_code == 401:
                raise AGTAuthenticationError("Invalid API key or credentials")
            elif response.status_code == 404:
                raise AGTNotFoundError(f"Resource not found: {response.url}")
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise AGTRateLimitError(f"Rate limited, retry after {retry_after}s", retry_after=retry_after)
            elif response.status_code >= 500:
                raise AGTException(f"Server error: {response.status_code}", code=response.status_code)
            else:
                raise AGTException(f"Unexpected status: {response.status_code}", code=response.status_code)
        except httpx.JSONDecodeError:
            raise AGTException(f"Invalid JSON response: {response.text}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((AGTException, httpx.RequestError)),
    )
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        self._ensure_client()
        
        try:
            # Apply rate limiting
            await self._rate_limiter.acquire(endpoint)
            
            url = f"{endpoint}" if endpoint.startswith('/') else f"/{endpoint}"
            response = await self._client.request(method, url, **kwargs)
            return await self._handle_response(response)
        except httpx.TimeoutException as e:
            raise AGTTimeoutError(f"Request timeout after {self.timeout}s") from e
        except httpx.RequestError as e:
            raise AGTException(f"Request failed: {str(e)}") from e
    
    async def validate_nif(self, nif: str) -> bool:
        """Validate NIF format and existence"""
        try:
            result = await self._request('GET', f'/nif/{nif}/validate')
            return result.get('valid', False)
        except AGTNotFoundError:
            return False
    
    async def get_taxpayer_data(self, nif: str) -> Optional[Dict[str, Any]]:
        """Get taxpayer data from AGT"""
        try:
            return await self._request('GET', f'/taxpayers/{nif}')
        except AGTNotFoundError:
            return None
    
    async def get_taxpayer_status(self, nif: str) -> Optional[str]:
        """Get taxpayer registration status"""
        try:
            data = await self._request('GET', f'/taxpayers/{nif}/status')
            return data.get('status')
        except AGTNotFoundError:
            return None
    
    async def get_tax_debts(
        self,
        nif: str,
        include_paid: bool = False,
        tax_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get tax debts for taxpayer"""
        params = {'include_paid': include_paid}
        if tax_type:
            params['tax_type'] = tax_type
        
        try:
            result = await self._request(
                'GET',
                f'/taxpayers/{nif}/debts',
                params=params
            )
            return result.get('debts', [])
        except AGTNotFoundError:
            return []
    
    async def get_declaration_history(
        self,
        nif: str,
        year: Optional[int] = None,
        tax_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get declaration history"""
        params = {}
        if year:
            params['year'] = year
        if tax_type:
            params['tax_type'] = tax_type
        
        try:
            result = await self._request(
                'GET',
                f'/taxpayers/{nif}/declarations',
                params=params
            )
            return result.get('declarations', [])
        except AGTNotFoundError:
            return []
    
    async def get_payment_history(
        self,
        nif: str,
        year: Optional[int] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get payment history"""
        params = {'limit': limit}
        if year:
            params['year'] = year
        
        try:
            result = await self._request(
                'GET',
                f'/taxpayers/{nif}/payments',
                params=params
            )
            return result.get('payments', [])
        except AGTNotFoundError:
            return []
    
    async def submit_declaration(
        self,
        nif: str,
        declaration_data: Dict[str, Any],
    ) -> str:
        """Submit tax declaration to AGT"""
        payload = {
            'nif': nif,
            'declaration': declaration_data,
            'submitted_at': datetime.utcnow().isoformat(),
        }
        
        result = await self._request(
            'POST',
            '/declarations/submit',
            json=payload
        )
        return result.get('protocol')
    
    async def check_declaration_status(self, protocol: str) -> Dict[str, Any]:
        """Check declaration processing status"""
        return await self._request('GET', f'/declarations/{protocol}/status')
    
    async def update_declaration(
        self,
        protocol: str,
        updates: Dict[str, Any],
    ) -> bool:
        """Update submitted declaration"""
        payload = {
            'updates': updates,
            'updated_at': datetime.utcnow().isoformat(),
        }
        
        result = await self._request(
            'PATCH',
            f'/declarations/{protocol}',
            json=payload
        )
        return result.get('success', False)
    
    async def skip_declaration(self, protocol: str, reason: str) -> bool:
        """Skip/cancel declaration"""
        payload = {
            'reason': reason,
            'skipped_at': datetime.utcnow().isoformat(),
        }
        
        result = await self._request(
            'POST',
            f'/declarations/{protocol}/skip',
            json=payload
        )
        return result.get('success', False)
    
    async def request_certificate(
        self,
        nif: str,
        certificate_type: str,
        year: Optional[int] = None,
    ) -> str:
        """Request certificate from AGT"""
        payload = {
            'nif': nif,
            'certificate_type': certificate_type,
            'year': year,
            'requested_at': datetime.utcnow().isoformat(),
        }
        
        result = await self._request(
            'POST',
            '/certificates/request',
            json=payload
        )
        return result.get('certificate_id')
    
    async def get_certificate_status(self, certificate_id: str) -> Dict[str, Any]:
        """Check certificate generation status"""
        return await self._request('GET', f'/certificates/{certificate_id}/status')
    
    async def download_certificate(self, certificate_id: str) -> bytes:
        """Download certificate file"""
        self._ensure_client()
        
        await self._rate_limiter.acquire(f'/certificates/{certificate_id}/download')
        
        try:
            response = await self._client.get(
                f'/certificates/{certificate_id}/download',
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return response.content
            elif response.status_code == 404:
                raise AGTNotFoundError(f"Certificate {certificate_id} not found")
            else:
                raise AGTException(f"Download failed: {response.status_code}")
        except httpx.TimeoutException:
            raise AGTTimeoutError(f"Download timeout after {self.timeout}s")
    
    async def health_check(self) -> bool:
        """Check AGT API health"""
        try:
            result = await self._request('GET', '/health')
            return result.get('status') == 'healthy'
        except Exception:
            return False
    
    async def close(self):
        """Close HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None
