"""Root conftest.py - Configures pytest and Python path for all tests."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "apps" / "backend"))
sys.path.insert(0, str(project_root / "scripts"))

# Ensure imports work correctly
os.chdir(project_root)

# Import all models to register them with SQLAlchemy
try:
    from apps.backend.modules.payment.models import Payment, PaymentTransaction, Refund
except ImportError:
    pass
