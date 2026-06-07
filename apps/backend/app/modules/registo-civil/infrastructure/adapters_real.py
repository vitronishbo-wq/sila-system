import hashlib
import hmac
import json
import logging
from typing import Any, Optional

from apps.backend.app.core.settings import settings
from apps.backend.app.platform.integration.models import ProviderCapability, ProviderStatus
from apps.backend.app.platform.integration.provider_base import ProviderBase
from apps.backend.app.platform.integration.provider_registry import ProviderRegistry

from ..domain.exceptions import RegistoDuplicadoError, RegistoNaoEncontradoError
from ..domain.models import RegistoCasamento, RegistoNascimento, RegistoObito

logger = logging.getLogger(__name__)


class RegistoCivilRealProvider(ProviderBase):
    provider_name = "registo_civil"

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: float = 30.0,
    ):
        ProviderBase.__init__(
            self,
            base_url=base_url or settings.REGISTO_CIVIL_BASE_URL,
            api_key=api_key or settings.REGISTO_CIVIL_API_KEY,
            timeout=timeout,
        )
        self._api_secret = api_secret or settings.REGISTO_CIVIL_API_SECRET

    def _headers(self, method: str, path: str, body: str = "") -> dict[str, str]:
        message = f"{method}:{path}:{body}"
        signature = hmac.new(
            self._api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "X-Conservatoria-Api-Key": self.api_key,
            "X-Conservatoria-Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def health_check(self) -> dict[str, Any]:
        return await self._request("GET", "/health", headers=self._headers("GET", "/health"))

    async def notificar_obito(self, bi_numero: str, data_obito: str) -> dict[str, Any]:
        body = json.dumps({"bi": bi_numero, "data_obito": data_obito})
        return await self._request(
            "POST", "/obitos/notificar",
            json_data={"bi": bi_numero, "data_obito": data_obito},
            headers=self._headers("POST", "/obitos/notificar", body),
        )

    async def verificar_bi_falecido(self, bi_numero: str) -> bool:
        result = await self._request(
            "GET", f"/obitos/verificar/{bi_numero}",
            headers=self._headers("GET", f"/obitos/verificar/{bi_numero}"),
        )
        return result.get("falecido", False)

    async def sincronizar_nascimento(self, registo_id: str) -> dict[str, Any]:
        return await self._request(
            "POST", f"/nascimentos/{registo_id}/sincronizar",
            headers=self._headers("POST", f"/nascimentos/{registo_id}/sincronizar"),
        )

    async def registar_nascimento(self, registo: RegistoNascimento) -> dict[str, Any]:
        data = {
            "nome_completo": registo.nome_completo,
            "data_nascimento": registo.data_nascimento,
            "genero": registo.genero,
            "naturalidade": registo.naturalidade,
            "nome_pai": registo.nome_pai,
            "nome_mae": registo.nome_mae,
            "provincia": registo.provincia,
            "municipio": registo.municipio,
        }
        body = json.dumps(data)
        return await self._request(
            "POST", "/nascimentos",
            json_data=data,
            headers=self._headers("POST", "/nascimentos", body),
        )

    async def registar_obito(self, registo: RegistoObito) -> dict[str, Any]:
        data = {
            "bi": registo.falecido_bi,
            "data_obito": registo.data_obito,
            "causa": registo.causa,
            "local": registo.local_obito,
            "provincia": registo.provincia,
            "municipio": registo.municipio,
        }
        body = json.dumps(data)
        return await self._request(
            "POST", "/obitos",
            json_data=data,
            headers=self._headers("POST", "/obitos", body),
        )


def create_registo_civil_provider() -> "RegistoCivilRealProvider":
    from apps.backend.app.platform.integration.helpers import is_placeholder_key

    has_creds = settings.REGISTO_CIVIL_API_KEY and settings.REGISTO_CIVIL_API_SECRET

    if settings.PROVIDER_MODE == "homologation" and has_creds:
        ProviderRegistry.register(
            "registo_civil", ProviderCapability.CIVIL_REGISTRY,
            status=ProviderStatus.HOMOLOGATION, version="1.0.0",
            mock_reason="Homologação institucional — credenciais de staging",
        )
        logger.info("registo_civil_provider=homologation (Conservatoria)")
        return RegistoCivilRealProvider()

    if has_creds:
        if is_placeholder_key(settings.REGISTO_CIVIL_API_KEY) or is_placeholder_key(settings.REGISTO_CIVIL_API_SECRET):
            ProviderRegistry.register(
                "registo_civil", ProviderCapability.CIVIL_REGISTRY,
                status=ProviderStatus.MOCK_LIVE, version="0.0.0",
                mock_reason="MOCK ao vivo — credenciais com placeholder",
            )
            logger.info("registo_civil_provider=mock_live (placeholder)")
            from .adapters import RegistoCivilXRoadMockAdapter
            return RegistoCivilXRoadMockAdapter()
        ProviderRegistry.register(
            "registo_civil", ProviderCapability.CIVIL_REGISTRY,
            status=ProviderStatus.REAL, version="1.0.0",
        )
        logger.info("registo_civil_provider=real (Conservatoria)")
        return RegistoCivilRealProvider()

    ProviderRegistry.register(
        "registo_civil", ProviderCapability.CIVIL_REGISTRY,
        status=ProviderStatus.MOCK, version="0.0.0",
        mock_reason="Sem credenciais configuradas",
    )
    logger.info("registo_civil_provider=mock (sem credenciais)")
    from .adapters import RegistoCivilXRoadMockAdapter
    return RegistoCivilXRoadMockAdapter()
