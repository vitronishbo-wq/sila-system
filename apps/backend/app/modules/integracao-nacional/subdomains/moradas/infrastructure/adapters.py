from ..application.ports.morada_provider_port import (
    MoradaProviderPort,
)
from ..domain.models import (
    Morada,
    MoradaNormalizada,
    MoradaValidationResult,
)


class MoradaGeoAdapter(MoradaProviderPort):
    async def geocodificar(self, morada: Morada) -> MoradaNormalizada:
        return MoradaNormalizada(
            original=f"{morada.linha1}, {morada.bairro or ''}, {morada.municipio}, {morada.provincia}",
            linha1=morada.linha1,
            bairro=morada.bairro,
            municipio=morada.municipio,
            provincia=morada.provincia,
            confidence=0.7,
        )

    async def validar(self, morada: Morada) -> MoradaValidationResult:
        problemas = []
        if not morada.provincia:
            problemas.append("Provincia nao informada")
        if not morada.municipio:
            problemas.append("Municipio nao informado")
        return MoradaValidationResult(valida=len(problemas) == 0, confianca=0.7, problemas=problemas)

    async def obter_provincias(self) -> list[str]:
        return [
            "BENGO", "BENGUELA", "BIE", "CABINDA", "CUANDO CUBANGO",
            "CUANZA NORTE", "CUANZA SUL", "CUNENE", "HUAMBO", "HUILLA",
            "LUANDA", "LUNDA NORTE", "LUNDA SUL", "MALANJE", "MOXICO",
            "NAMIBE", "UIGE", "ZAIRE",
        ]

    async def obter_municipios(self, provincia: str) -> list[str]:
        return []
