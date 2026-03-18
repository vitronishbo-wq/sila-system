from enum import Enum

class InvoiceStatus(str, Enum):
    DRAFT = 'draft'
    ISSUED = 'issued'
    PENDING = 'pending'
    PAID = 'paid'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'
    DISPUTED = 'disputed'

class PaymentMethod(str, Enum):
    CASH = 'cash'
    BANK_TRANSFER = 'bank_transfer'
    CHEQUE = 'cheque'
    DEBIT_CARD = 'debit_card'
    CREDIT_CARD = 'credit_card'
    INSTALLMENT_PLAN = 'installment_plan'
    MULTICAIXA = 'multicaixa'

class PaymentStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    RECONCILED = 'reconciled'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'
    DISPUTED = 'disputed'

class CostCenterCode(str, Enum):
    SAUDE = 'cc001'
    EDUCACAO = 'cc002'
    SEGURANCA = 'cc003'
    TRANSPORTES = 'cc004'
    OBRAS_PUBLICAS = 'cc005'
    ADMINISTRACAO = 'cc999'

class RevenueCode(str, Enum):
    TAXAS_ADMINISTRATIVAS = 'ore001'
    MULTAS_INFRACOES = 'ore002'
    LICENCAS_AUTORIZACOES = 'ore003'
    SERVICOS_TECNICOS = 'ore004'
    ALUGUEL_BENS = 'ore005'
    TAXA_RESIDENCIA = 'ore006'
    OUTRAS_RECEITAS = 'ore999'