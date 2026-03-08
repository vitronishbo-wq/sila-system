import warnings
from app.core.observability import *

warnings.warn(
    "Importando de app.platform.shared.observability. Use app.core.observability.",
    DeprecationWarning,
    stacklevel=2
)
