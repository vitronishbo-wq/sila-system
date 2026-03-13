from enum import Enum

class TipoOutorga(Enum):
    CAPTACAO = 'captacao'
    LANCAMENTO = 'lancamento'
    BARRAMENTO = 'barramento'
    PERFURACAO = 'perfuracao'
    DRENAGEM = 'drenagem'

class StatusOutorga(Enum):
    REQUERIDA = 'requerida'
    EM_ANALISE = 'em_analise'
    DEFERIDA = 'deferida'
    INDEFERIDA = 'indeferida'
    VENCIDA = 'vencida'
    CANCELADA = 'cancelada'
    SUSPENSA = 'suspensa'

class TipoCaptacao(Enum):
    SUPERFICIAL = 'superficial'
    SUBTERRANEA = 'subterranea'
    PLUVIAL = 'pluvial'

class TipoCorpoHidrico(Enum):
    RIO = 'rio'
    LAGO = 'lago'
    LAGOA = 'lagoa'
    ACUDE = 'acude'
    REPRESA = 'represa'
    AQUIFERO = 'aquifero'
    NASCENTE = 'nascente'
    RESERVATORIO = 'reservatorio'

class TipoUso(Enum):
    ABASTECIMENTO_PUBLICO = 'abastecimento_publico'
    INDUSTRIAL = 'industrial'
    IRRIGACAO = 'irrigacao'
    DESSEDENTACAO_ANIMAL = 'dessedentacao_animal'
    GERACAO_ENERGIA = 'geracao_energia'
    MINERACAO = 'mineracao'
    AQUICULTURA = 'aquicultura'
    TURISMO = 'turismo'
    RECREACAO = 'recreacao'

class TipoEfluente(Enum):
    DOMESTICO = 'domestico'
    INDUSTRIAL = 'industrial'
    AGROPECUARIO = 'agropecuario'
    HOSPITALAR = 'hospitalar'
    PLUVIAL = 'pluvial'

class TipoTratamento(Enum):
    PRELIMINAR = 'preliminar'
    PRIMARIO = 'primario'
    SECUNDARIO = 'secundario'
    TERCIARIO = 'terciario'
    LAGOA_ESTABILIZACAO = 'lagoa_estabilizacao'
    REATOR_ANAEROBIO = 'reator_anaerobio'
    LODO_ATIVADO = 'lodo_ativado'

class TipoFiscalizacao(Enum):
    ROTINA = 'rotina'
    DENUNCIA = 'denuncia'
    MONITORAMENTO = 'monitoramento'
    VERIFICACAO = 'verificacao'

class TipoInfraestrutura(Enum):
    BARRAMENTO = 'barramento'
    ACUDE = 'acude'
    REPRESA = 'represa'
    POCO = 'poco'
    CACIMBA = 'cacimba'
    ETA = 'eta'
    ETE = 'ete'
    RESERVATORIO = 'reservatorio'
    ADUTORA = 'adutora'
    REDE_DISTRIBUICAO = 'rede_distribuicao'
    LIGACAO_DOMICILIAR = 'ligacao_domiciliar'
    HIDROMETRO = 'hidrometro'

class StatusInfraestrutura(Enum):
    PLANEJADA = 'planejada'
    OPERACIONAL = 'operacional'
    MANUTENCAO = 'manutencao'
    INTERDITADA = 'interditada'
    INATIVA = 'inativa'

class StatusAbastecimento(Enum):
    PLANEJADO = 'planejado'
    OPERACIONAL = 'operacional'
    INTERROMPIDO = 'interrompido'
    ENCERRADO = 'encerrado'

class CategoriaConsumo(Enum):
    RESIDENCIAL = 'residencial'
    COMERCIAL = 'comercial'
    INDUSTRIAL = 'industrial'
    PUBLICO = 'publico'
    SOCIAL = 'social'

class StatusConsumo(Enum):
    REGISTRADO = 'registrado'
    VALIDADO = 'validado'
    FATURADO = 'faturado'
    CANCELADO = 'cancelado'

class StatusFatura(Enum):
    EMITIDA = 'emitida'
    PAGA = 'paga'
    VENCIDA = 'vencida'
    CANCELADA = 'cancelada'

class MetodoPagamento(Enum):
    TRANSFERENCIA = 'transferencia'
    MULTICAIXA = 'multicaixa'
    DINHEIRO = 'dinheiro'
    DEBITO_DIRETO = 'debito_direto'