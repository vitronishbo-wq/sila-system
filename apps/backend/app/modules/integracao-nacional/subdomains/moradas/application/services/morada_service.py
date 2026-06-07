from ...application.ports.morada_provider_port import (
    MoradaProviderPort,
)
from ...domain.exceptions import MoradaInvalidaError
from ...domain.models import (
    Morada,
    MoradaNormalizada,
    MoradaValidationResult,
)

PROVINCIAS_ANGOLA = [
    "BENGO", "BENGUELA", "BIE", "CABINDA", "CUANDO CUBANGO",
    "CUANZA NORTE", "CUANZA SUL", "CUNENE", "HUAMBO", "HUILLA",
    "LUANDA", "LUNDA NORTE", "LUNDA SUL", "MALANJE", "MOXICO",
    "NAMIBE", "UIGE", "ZAIRE",
]


class MoradaService:
    def __init__(self, provider: MoradaProviderPort | None = None):
        self._provider = provider

    def _normalizar_provincia(self, provincia: str) -> str | None:
        p = provincia.strip().upper()
        for pv in PROVINCIAS_ANGOLA:
            if pv.startswith(p) or p in pv:
                return pv
        return provincia.upper() if provincia else None

    async def normalizar(self, endereco: str) -> MoradaNormalizada:
        if not endereco or len(endereco.strip()) < 5:
            raise MoradaInvalidaError("Endereco muito curto")
        partes = [p.strip() for p in endereco.split(",")]
        morada = Morada(
            linha1=partes[0] if partes else endereco,
            bairro=partes[1] if len(partes) > 1 else None,
            municipio=partes[2] if len(partes) > 2 else "",
            provincia=self._normalizar_provincia(partes[-1]) if len(partes) > 1 else None,
        )
        if self._provider:
            return await self._provider.geocodificar(morada)
        return MoradaNormalizada(
            original=endereco,
            linha1=morada.linha1,
            bairro=morada.bairro,
            municipio=morada.municipio,
            provincia=morada.provincia,
            confidence=0.5,
        )

    async def validar(self, endereco: str) -> MoradaValidationResult:
        problemas: list[str] = []
        if not endereco or len(endereco.strip()) < 5:
            problemas.append("Endereco demasiado curto")
        partes = [p.strip() for p in endereco.split(",")]
        if len(partes) < 2:
            problemas.append("Formato esperado: rua, bairro, municipio, provincia")
        if len(partes) >= 2:
            provincia = self._normalizar_provincia(partes[-1])
            if not provincia:
                problemas.append("Provincia nao reconhecida")
        return MoradaValidationResult(
            valida=len(problemas) == 0,
            confianca=1.0 - (len(problemas) * 0.25),
            problemas=problemas,
        )
