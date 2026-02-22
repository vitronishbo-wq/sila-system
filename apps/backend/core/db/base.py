# core/db/base.py
"""
Centraliza o registro de todos os modelos para o Base.metadata.
Usado pelo Alembic para detectar tabelas existentes.
"""

from config.database import Base

# Modelos de Identidade (mais críticos para FKs)
try:
    from modules.identity.models.user import User  # noqa: F401
    from modules.identity.models.identity import Identity  # noqa: F401
except ImportError as e:
    print(f"Aviso: Falha ao importar módulos de identidade: {e}")

# Módulos de Localização
try:
    from modules.location.models.region import Region  # noqa: F401
    from modules.location.models.hierarchy import ProvinceModel, MunicipalityModel, CommuneModel  # noqa: F401
except ImportError as e:
    print(f"Aviso: Falha ao importar módulos de localização: {e}")

# Módulos de Pagamento e Notificações
try:
    from modules.payment.models.payment import Payment  # noqa: F401
    from modules.payment.models.transaction import PaymentTransaction  # noqa: F401
    from modules.payment.models.refund import Refund  # noqa: F401
    from modules.notifications.models.notification import Notification  # noqa: F401
    from modules.documents.models.documents import Document, DocumentFolder, DocumentVersion  # noqa: F401
    from modules.audit.models import AuditLog  # noqa: F401
    from modules.citizenship.models.citizen import Citizen  # noqa: F401
    from modules.citizenship.models.citizenship_models import CitizenshipService, ServiceRequest, ServiceRequestHistory  # noqa: F401
    from modules.citizenship.models.atualizacao_bi import AtualizacaoBI, AtualizacaoBIDocument  # noqa: F401
except ImportError as e:
    print(f"Aviso: Falha ao importar módulos de pagamento/notificações/audit/citizenship: {e}")

__all__ = ["Base"]
