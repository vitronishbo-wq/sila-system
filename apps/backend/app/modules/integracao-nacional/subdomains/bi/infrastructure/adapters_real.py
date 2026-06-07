import hashlib
import hmac
import json
import logging
from typing import Any, Optional

from apps.backend.app.core.settings import settings
from apps.backend.app.platform.integration.models import ProviderCapability, ProviderStatus
from apps.backend.app.platform.integration.provider_base import ProviderBase
from apps.backend.app.platform.integration.provider_registry import ProviderRegistry

from ..domain.exceptions import BiNaoEncontradoError
from ..domain.models import BilheteIdentidade, BiStatus, BiTipo, BiVerificationResult
from ..application.ports.bi_provider_port import BiProviderPort

logger = logging.getLogger(__name__)


class BiXRoadRealProvider(BiProviderPort, ProviderBase):
    provider_name = "xroad_bi"

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: float = 30.0,
    ):
        ProviderBase.__init__(
            self,
            base_url=base_url or settings.XROAD_BASE_URL,
            api_key=api_key or settings.XROAD_API_KEY,
            timeout=timeout,
        )
        self._api_secret = api_secret or settings.XROAD_API_SECRET

    def _headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        message = f"{method}:{path}:{body}"
        signature = hmac.new(
            self._api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "X-XRoad-Api-Key": self.api_key,
            "X-XRoad-Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def health_check(self) -> dict[str, Any]:
        return await self._request("GET", "/health", headers=self._headers("GET", "/health"))

    def _parse_bi(self, data: dict) -> BilheteIdentidade:
        return BilheteIdentidade(
            numero=data.get("numero", ""),
            full_name=data.get("full_name", ""),
            birth_date=data.get("birth_date", ""),
            gender=data.get("gender", ""),
            filiation_pai=data.get("filiation_pai"),
            filiation_mae=data.get("filiation_mae"),
            nationality=data.get("nationality", "ANGOLANA"),
            tipo=BiTipo(data.get("tipo", "normal")),
            status=BiStatus(data.get("status", "valido")),
            emission_date=data.get("emission_date"),
            expiration_date=data.get("expiration_date"),
            emission_place=data.get("emission_place"),
            nif=data.get("nif"),
        )

    async def validar_bi(self, bi_numero: str) -> BiVerificationResult:
        result = await self._request(
            "GET", f"/bi/{bi_numero}/validar",
            headers=self._headers("GET", f"/bi/{bi_numero}/validar"),
        )
        if result.get("status") == "not_found":
            raise BiNaoEncontradoError(bi_numero)
        return BiVerificationResult(
            bi_numero=bi_numero,
            valido=result.get("valido", False),
            status=BiStatus(result.get("status", "nao_encontrado")),
            cidadao_encontrado=result.get("encontrado", False),
            dados=self._parse_bi(result.get("dados", {})),
            fonte="xroad",
        )

    async def consultar_bi(self, bi_numero: str) -> Optional[BilheteIdentidade]:
        result = await self._request(
            "GET", f"/bi/{bi_numero}",
            headers=self._headers("GET", f"/bi/{bi_numero}"),
        )
        if result.get("status") == "not_found":
            return None
        return self._parse_bi(result.get("dados", result))

    async def verificar_biometria(self, bi_numero: str, fingerprint_hash: str) -> bool:
        body = json.dumps({"fingerprint_hash": fingerprint_hash})
        result = await self._request(
            "POST", f"/bi/{bi_numero}/biometria",
            json_data={"fingerprint_hash": fingerprint_hash},
            headers=self._headers("POST", f"/bi/{bi_numero}/biometria", body),
        )
        return result.get("valido", False)

    async def verificar_status(self, bi_numero: str) -> BiStatus:
        result = await self._request(
            "GET", f"/bi/{bi_numero}/status",
            headers=self._headers("GET", f"/bi/{bi_numero}/status"),
        )
        return BiStatus(result.get("status", "nao_encontrado"))


def create_bi_provider() -> BiProviderPort:
    from apps.backend.app.platform.integration.helpers import is_placeholder_key

    has_creds = settings.XROAD_API_KEY and settings.XROAD_API_SECRET

    if settings.PROVIDER_MODE == "homologation" and has_creds:
        ProviderRegistry.register(
            "xroad_bi", ProviderCapability.IDENTITY_VERIFICATION,
            status=ProviderStatus.HOMOLOGATION, version="1.0.0",
            mock_reason="Homologação institucional — credenciais de staging",
        )
        logger.info("bi_provider=homologation (XRoad)")
        return BiXRoadRealProvider()

    if has_creds:
        if is_placeholder_key(settings.XROAD_API_KEY) or is_placeholder_key(settings.XROAD_API_SECRET):
            ProviderRegistry.register(
                "xroad_bi", ProviderCapability.IDENTITY_VERIFICATION,
                status=ProviderStatus.MOCK_LIVE, version="0.0.0",
                mock_reason="MOCK ao vivo — credenciais com placeholder",
            )
            logger.info("bi_provider=mock_live (placeholder)")
            from .adapters import BiXRoadMockAdapter
            return BiXRoadMockAdapter()
        ProviderRegistry.register(
            "xroad_bi", ProviderCapability.IDENTITY_VERIFICATION,
            status=ProviderStatus.REAL, version="1.0.0",
        )
        logger.info("bi_provider=real (XRoad)")
        return BiXRoadRealProvider()

    ProviderRegistry.register(
        "xroad_bi", ProviderCapability.IDENTITY_VERIFICATION,
        status=ProviderStatus.MOCK, version="0.0.0",
        mock_reason="Sem credenciais configuradas",
    )
    logger.info("bi_provider=mock (sem credenciais)")
    from .adapters import BiXRoadMockAdapter
    return BiXRoadMockAdapter()
