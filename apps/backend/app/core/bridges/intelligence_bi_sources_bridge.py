"""Bridge for intelligence BI integrations to consume shared domain sources."""
from app.modules.economy.financas.infrastructure.models.invoice_model import InvoiceModel
from app.modules.economy.financas.infrastructure.models.payment_model import PaymentModel
from app.modules.economy.financas.public_budget.infrastructure.models.despesa_model import DespesaModel
from app.modules.economy.financas.public_budget.infrastructure.models.orcamento_model import OrcamentoModel
from app.modules.economy.financas.public_budget.infrastructure.models.receita_model import ReceitaModel
from app.modules.governance.statistics.integrations.data_sources import DataSources as StatisticsDataSources
__all__ = ['DespesaModel', 'InvoiceModel', 'OrcamentoModel', 'PaymentModel', 'ReceitaModel', 'StatisticsDataSources']