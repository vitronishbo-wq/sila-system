"""Root conftest.py - Configures pytest and Python path for all tests."""

import sys
import os
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

# Importar todos os modelos para registá-los no SQLAlchemy Registry
# Isto previne erros de "Mapper failed to initialize" durante os testes
try:
    # Core Base
    from core.db.base_class import Base

    # Identity & Access
    from apps.backend.app.modules.identity.models.user import User
    from apps.backend.app.modules.identity.models.identity import Identity

    # Location
    from apps.backend.app.modules.location.models.region import Region

    # Payments
    from apps.backend.app.modules.payment.models import Payment, PaymentTransaction, Refund

    # Document Management (se existir)
    # from apps.backend.app.modules.document.models import Document

except ImportError as e:
    # Log silencioso se os módulos ainda não estiverem todos implementados
    print(f"Aviso durante carregamento de modelos em conftest.py: {e}")


def pytest_configure(config):
    """Configurações adicionais do Pytest."""
    config.addinivalue_line(
        "markers", "asyncio: mark test to run as an asyncio test"
    )
