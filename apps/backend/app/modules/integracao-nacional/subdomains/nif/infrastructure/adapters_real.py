import hashlib
import hmac
import json
import logging
from typing import Any, Optional

from apps.backend.app.core.settings import settings
from apps.backend.app.platform.integration.models import ProviderCapability, ProviderStatus
from apps.backend.app.platform.integration.provider_base import ProviderBase
from apps.backend.app.platform.integration.provider_registry import ProviderRegistry

from ..domain.exceptions import NifNaoEncontradoError
from ..domain.models import NifData, NifStatus, NifTipoContribuinte, NifVerificationResult
from ..application.ports.nif_provider_port import NifProviderPort

logger = logging.getLogger(__name__)


class NifAGTRealProvider(NifProviderPort, ProviderBase):
    provider_name = "agt"

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: float = 30.0,
    ):
        ProviderBase.__init__(
            self,
            base_url=base_url or settings.AGT_BASE_URL,
            api_key=api_key or settings.AGT_API_KEY,
            timeout=timeout,
        )
        self._api_secret = api_secret or settings.AGT_API_SECRET

    def _headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        message = f"{method}:{path}:{body}"
        signature = hmac.new(
            self._api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "X-AGT-Api-Key": self.api_key,
            "X-AGT-Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def health_check(self) -> dict[str, Any]:
        return await self._request("GET", "/health", headers=self._headers("GET", "/health"))

    def _parse_nif_data(self, data: dict) -> NifData:
        return NifData(
            nif=data.get("nif", ""),
            full_name=data.get("full_name", ""),
            tipo=NifTipoContribuinte(data.get("tipo", "singular")),
            status=NifStatus(data.get("status", "ativo")),
            bi_numero=data.get("bi_numero"),
            email=data.get("email"),
            morada=data.get("morada"),
            telefone=data.get("telefone"),
            atividade_economica=data.get("atividade_economica"),
            regime_iva=data.get("regime_iva"),
        )

    async def validar_nif(self, nif: str) -> NifVerificationResult:
        result = await self._request(
            "GET", f"/contribuintes/{nif}/validar",
            headers=self._headers("GET", f"/contribuintes/{nif}/validar"),
        )
        if result.get("status") == "not_found":
            raise NifNaoEncontradoError(nif)
        return NifVerificationResult(
            nif=nif,
            valido=result.get("valido", False),
            status=NifStatus(result.get("status", "ativo")),
            contribuinte_encontrado=result.get("encontrado", False),
            dados=self._parse_nif_data(result.get("dados", {})),
            fonte="agt",
        )

    async def consultar_nif(self, nif: str) -> Optional[NifData]:
        result = await self._request(
            "GET", f"/contribuintes/{nif}",
            headers=self._headers("GET", f"/contribuintes/{nif}"),
        )
        if result.get("status") == "not_found":
            return None
        return self._parse_nif_data(result.get("dados", result))

    async def verificar_status(self, nif: str) -> NifStatus:
        result = await self._request(
            "GET", f"/contribuintes/{nif}/status",
            headers=self._headers("GET", f"/contribuintes/{nif}/status"),
        )
        return NifStatus(result.get("status", "nao_encontrado"))


def create_nif_provider() -> NifProviderPort:
    from apps.backend.app.platform.integration.helpers import is_placeholder_key

    has_creds = settings.AGT_API_KEY and settings.AGT_API_SECRET

    if settings.PROVIDER_MODE == "homologation" and has_creds:
        ProviderRegistry.register(
            "agt", ProviderCapability.TAX_VERIFICATION,
            status=ProviderStatus.HOMOLOGATION, version="1.0.0",
            mock_reason="Homologação institucional — credenciais de staging",
        )
        logger.info("nif_provider=homologation (AGT)")
        return NifAGTRealProvider()

    if has_creds:
        if is_placeholder_key(settings.AGT_API_KEY) or is_placeholder_key(settings.AGT_API_SECRET):
            ProviderRegistry.register(
                "agt", ProviderCapability.TAX_VERIFICATION,
                status=ProviderStatus.MOCK_LIVE, version="0.0.0",
                mock_reason="MOCK ao vivo — credenciais com placeholder",
            )
            logger.info("nif_provider=mock_live (placeholder)")
            from .adapters import NifAGTMockAdapter
            return NifAGTMockAdapter()
        ProviderRegistry.register(
            "agt", ProviderCapability.TAX_VERIFICATION,
            status=ProviderStatus.REAL, version="1.0.0",
        )
        logger.info("nif_provider=real (AGT)")
        return NifAGTRealProvider()

    ProviderRegistry.register(
        "agt", ProviderCapability.TAX_VERIFICATION,
        status=ProviderStatus.MOCK, version="0.0.0",
        mock_reason="Sem credenciais configuradas",
    )
    logger.info("nif_provider=mock (sem credenciais)")
    from .adapters import NifAGTMockAdapter
    return NifAGTMockAdapter()
