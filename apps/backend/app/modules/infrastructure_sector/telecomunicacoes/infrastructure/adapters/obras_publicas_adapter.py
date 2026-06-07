from __future__ import annotations


class ObrasPublicasAdapter:
    """Adapter para validacao de licencas de obras de infraestrutura."""

    async def validar_licenca(self, codigo_licenca: str) -> bool:
        _ = codigo_licenca
        return True
