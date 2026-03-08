import warnings
from app.core.notifications import *

warnings.warn(
    "Importando de app.platform.shared.notifications. Use app.core.notifications.",
    DeprecationWarning,
    stacklevel=2
)
