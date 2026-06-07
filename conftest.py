"""Root conftest.py - Configures pytest and Python path for all tests."""

import importlib
import os
import sys
from pathlib import Path

# Adiciona a raiz do projeto e os caminhos dos módulos ao PYTHONPATH
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "apps" / "backend"))
sys.path.insert(0, str(project_root / "scripts"))

# Garante que o diretório de trabalho é a raiz para resolução de caminhos relativos
os.chdir(project_root)

# Configura o ambiente como teste antes de qualquer outra importação
os.environ["ENVIRONMENT"] = "test"

import tempfile
import uuid

policy_store_file = os.path.join(
    tempfile.gettempdir(),
    f"pytest_policy_store_{uuid.uuid4().hex}.json",
)
os.environ.setdefault("POLICY_STORE_PATH", policy_store_file)

policy_audit_file = os.path.join(
    tempfile.gettempdir(),
    f"pytest_policy_audit_{uuid.uuid4().hex}.log",
)
os.environ.setdefault("POLICY_AUDIT_PATH", policy_audit_file)

OPTIONAL_MODEL_MODULES = (
    "apps.backend.app.modules.identity.domain.models.identity",
    "apps.backend.app.modules.identity.infrastructure.models",
    "apps.backend.app.modules.payment.infrastructure.orm",
    "apps.backend.app.core.db.base_class",
)


def _preload_optional_modules() -> None:
    """Best-effort model preloading without coupling pytest to stale module paths."""
    for module_name in OPTIONAL_MODEL_MODULES:
        try:
            importlib.import_module(module_name)
        except Exception:
            continue


_preload_optional_modules()


def pytest_configure(config):
    """Configurações adicionais do Pytest."""
    config.addinivalue_line("markers", "asyncio: mark test to run as an asyncio test")
