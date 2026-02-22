"""Compatibility shim: re-export CRUD functions for the justice module.

Tests and other modules expect `app.modules.justice.crud` to exist. The
real implementation lives in `services/justice_service.py`. This shim
re-exports the public API to preserve backward compatibility.
"""

from .services import justice_service as _svc

# Re-export functions
create_certificate = _svc.create_certificate
get_certificate = _svc.get_certificate
get_certificates = _svc.get_certificates
update_certificate = _svc.update_certificate
delete_certificate = _svc.delete_certificate

__all__ = [
    "create_certificate",
    "get_certificate",
    "get_certificates",
    "update_certificate",
    "delete_certificate",
]
