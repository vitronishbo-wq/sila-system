"""Compatibility namespace for legacy app.modules.operations imports."""
HealthStatus = dict

async def startup() -> None:
    return None

async def shutdown() -> None:
    return None

def health_check() -> HealthStatus:
    return {'status': 'ok'}