import warnings
from app.core.services.base_request_service import BaseRequestService

warnings.warn(
    "Importando BaseRequestService de app.platform.shared. Use app.core.services.",
    DeprecationWarning,
    stacklevel=2
)
