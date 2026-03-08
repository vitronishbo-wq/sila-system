import warnings
from app.core.exceptions import *

warnings.warn(
    "Importando de app.platform.shared.exceptions. Use app.core.exceptions.",
    DeprecationWarning, stacklevel=2
)
