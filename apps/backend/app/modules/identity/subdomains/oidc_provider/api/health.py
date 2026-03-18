from fastapi import APIRouter
from apps.backend.app.modules.identity.subdomains.oidc_provider.infrastructure.jwks import load_provider_config, get_provider_keys
router = APIRouter()

def module_name():
    parts = __name__.split('.')
    try:
        return f'{parts[3]}.{parts[4]}'
    except Exception:
        return __name__

@router.get('/health')
def health():
    return {'status': 'ok', 'module': module_name()}

@router.get('/health/oidc')
def oidc_health():
    """Health check for OIDC provider - verifies keys and configuration are available"""
    try:
        config = load_provider_config()
        keys = get_provider_keys()
        return {'status': 'ok', 'module': module_name(), 'issuer': config.issuer, 'algorithm': config.algorithm, 'keys_available': True}
    except Exception as e:
        return {'status': 'error', 'module': module_name(), 'error': str(e), 'keys_available': False}