"""Modulo de Seguranca Publica."""

__all__ = ["api", "application", "domain", "infrastructure"]
HealthStatus = dict


async def startup() -> None:
    return None


async def shutdown() -> None:
    return None


def health_check() -> HealthStatus:
    return {"status": "ok"}
