"""Bridge for intelligence BI integrations to consume shared domain sources."""
try:
    from apps.backend.app.modules.economy.financas.infrastructure.models.invoice_model import InvoiceModel
except Exception:
    InvoiceModel = None
try:
    from apps.backend.app.modules.economy.financas.infrastructure.models.payment_model import PaymentModel
except Exception:
    PaymentModel = None
try:
    from apps.backend.app.modules.economy.public_budget.infrastructure.models.despesa_model import DespesaModel
    from apps.backend.app.modules.economy.public_budget.infrastructure.models.orcamento_model import OrcamentoModel
    from apps.backend.app.modules.economy.public_budget.infrastructure.models.receita_model import ReceitaModel
except Exception:
    DespesaModel = None
    OrcamentoModel = None
    ReceitaModel = None
from apps.backend.app.modules.governance.statistics.integrations.data_sources import DataSources as StatisticsDataSources
__all__ = ['DespesaModel', 'InvoiceModel', 'OrcamentoModel', 'PaymentModel', 'ReceitaModel', 'StatisticsDataSources']