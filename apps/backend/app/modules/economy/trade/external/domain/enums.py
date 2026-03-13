from __future__ import annotations
from enum import Enum

class TipoOperador(Enum):
    EXPORTADOR = 'exportador'
    IMPORTADOR = 'importador'
    EXPORTADOR_IMPORTADOR = 'exportador_importador'
    DESPACHANTE = 'despachante'
    AGENTE_CARGA = 'agente_carga'
    TRANSPORTADOR = 'transportador'

class TipoPessoa(Enum):
    FISICA = 'fisica'
    JURIDICA = 'juridica'

class RegimeExportacao(Enum):
    DEFINITIVA = 'definitiva'
    TEMPORARIA = 'temporaria'
    DRAWBACK = 'drawback'
    REEXPORTACAO = 'reexportacao'

class RegimeImportacao(Enum):
    DEFINITIVA = 'definitiva'
    TEMPORARIA = 'temporaria'
    ADMISSAO_TEMPORARIA = 'admissao_temporaria'
    DRAWBACK = 'drawback'

class StatusHabilitacao(Enum):
    PENDENTE = 'pendente'
    HABILITADO = 'habilitado'
    SUSPENSO = 'suspenso'
    CANCELADO = 'cancelado'
    BLOQUEADO = 'bloqueado'

class TipoNCM(Enum):
    NCM = 'ncm'
    HS = 'hs'
    SH = 'sh'

class Incoterm(Enum):
    EXW = 'exw'
    FCA = 'fca'
    FAS = 'fas'
    FOB = 'fob'
    CFR = 'cfr'
    CIF = 'cif'
    CPT = 'cpt'
    CIP = 'cip'
    DPU = 'dpu'
    DAP = 'dap'
    DDP = 'ddp'

class ModalTransporte(Enum):
    MARITIMO = 'maritimo'
    AEREO = 'aereo'
    RODOVIARIO = 'rodoviario'
    FERROVIARIO = 'ferroviario'
    FLUVIAL = 'fluvial'
    MULTIMODAL = 'multimodal'

class TipoDeclaracao(Enum):
    DE = 'de'
    DI = 'di'
    DU = 'du'
    RE = 're'
    RI = 'ri'

class StatusDeclaracao(Enum):
    REGISTRADA = 'registrada'
    PARAMETRIZADA = 'parametrizada'
    EM_CONFERENCIA = 'em_conferencia'
    FISCALIZADA = 'fiscalizada'
    DESPACHADA = 'despachada'
    CANCELADA = 'cancelada'
    RETIDA = 'retida'

class CanalParametrizacao(Enum):
    VERDE = 'verde'
    AMARELO = 'amarelo'
    VERMELHO = 'vermelho'
    CINZA = 'cinza'

class TipoDrawback(Enum):
    SUSPENSAO = 'suspensao'
    ISENCAO = 'isencao'
    RESTITUICAO = 'restituicao'
    VERDE_AMARELO = 'verde_amarelo'

class TipoPagamentoInternacional(Enum):
    CARTA_CREDITO = 'carta_credito'
    COBRANCA_DOCUMENTARIA = 'cobranca_documentaria'
    REMESSA = 'remessa'
    SAQUE = 'saque'
    TRANSFERENCIA = 'transferencia'
    ORDEM_PAGAMENTO = 'ordem_pagamento'
    CHEQUE = 'cheque'

class TipoGarantia(Enum):
    BANK_GUARANTEE = 'bank_guarantee'
    PERFORMANCE_BOND = 'performance_bond'
    BID_BOND = 'bid_bond'
    ADVANCE_PAYMENT_BOND = 'advance_payment_bond'
    WARRANTY_BOND = 'warranty_bond'
    STANDBY_LC = 'standby_lc'

class StatusRadar(Enum):
    HABILITADO = 'habilitado'
    SUSPENSO = 'suspenso'
    CANCELADO = 'cancelado'
    BLOQUEADO = 'bloqueado'
    PENDENTE = 'pendente'