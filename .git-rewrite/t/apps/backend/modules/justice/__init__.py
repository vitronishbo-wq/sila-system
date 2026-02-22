"""Justice module.

This package contains the justice-related subpackages and exports.

IMPORTANT:
The package intentionally avoids eager top-level imports of submodules
to prevent circular import issues when submodules import the package
itself (a common pattern for 'app.modules.*').

Submodules (crud, models, routes, schemas, services) should be imported
explicitly by consumers or using the helpers below.
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

__all__ = [
    "models",
    "schemas",
    "crud",
    "services",
    "routes",
]


def _lazy_import(name: str):
    """Dynamically import and return a submodule of this package.

    This helper avoids importing everything at package import time and
    prevents circular import errors when submodules reference the
    parent package.
    """
    import importlib

    module_name = f"{__name__}.{name}"
    return importlib.import_module(module_name)


def models_module():
    return _lazy_import("models")


def schemas_module():
    return _lazy_import("schemas")


def crud_module():
    return _lazy_import("crud")


def services_module():
    return _lazy_import("services")


def routes_module():
    return _lazy_import("routes")


# PEP 562: provide module-level __getattr__ to allow lazy attribute access
# like `from modules.justice import crud` without doing eager imports.
def __getattr__(name: str):
    if name in __all__:
        mod = _lazy_import(name)
        if mod is None:
            raise ImportError(
                f"Could not import submodule {name} of package {__name__}"
            )
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    return sorted(list(globals().keys()) + __all__)


# Service: Mediação de Conflitos / Conflict Mediation
# Service: Assistência Jurídica Gratuita / Free Legal Assistance
# Service: Registo Criminal / Criminal Record
# Service: Habeas Corpus / Habeas Corpus
# Service: Mandado de Segurança / Security Order

# Serviço: Defensor Público / Public Defender

# Serviço: Cartório Distribuidor / Distribution Office

# Serviço: Execução Fiscal / Tax Execution

# Serviço: Penhora de Bens / Asset Seizure

# Serviço: Leilão Judicial / Judicial Auction
