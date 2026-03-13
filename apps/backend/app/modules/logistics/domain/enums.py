from enum import Enum

class ModalTransporte(str, Enum):
    RODOVIARIO = 'rodoviario'
    FERROVIARIO = 'ferroviario'
    AEROVIARIO = 'aeroviario'
    HIDROVIARIO = 'hidroviario'
    DUTOVIARIO = 'dutoviario'
    MULTIMODAL = 'multimodal'

class TipoVia(str, Enum):
    RODOVIA = 'rodovia'
    FERROVIA = 'ferrovia'
    HIDROVIA = 'hidrovia'
    DUTOVIA = 'dutovia'
    AEROVIA = 'aerovia'

class ClassificacaoVia(str, Enum):
    FEDERAL = 'federal'
    ESTADUAL = 'estadual'
    MUNICIPAL = 'municipal'
    PARTICULAR = 'particular'

class TipoPavimento(str, Enum):
    ASFALTO = 'asfalto'
    CONCRETO = 'concreto'
    TERRA = 'terra'
    PEDRA = 'pedra'
    PARALELEPIPEDO = 'paralelepipedo'

class TipoTerminal(str, Enum):
    RODOVIARIO = 'rodoviario'
    FERROVIARIO = 'ferroviario'
    AEROPORTUARIO = 'aeroportuario'
    PORTUARIO = 'portuario'
    HIDROVIARIO = 'hidroviario'
    INTERMODAL = 'intermodal'
    LOGISTICO = 'logistico'

class TipoVeiculo(str, Enum):
    ONIBUS = 'onibus'
    MICRO_ONIBUS = 'micro_onibus'
    VAN = 'van'
    TAXI = 'taxi'
    CAMINHAO = 'caminhao'
    CARRETA = 'carreta'
    BITREM = 'bitrem'
    RODOTREM = 'rodotrem'
    LOCOMOTIVA = 'locomotiva'
    VAGAO = 'vagao'
    NAVIO = 'navio'
    BARCA = 'barca'
    BALSA = 'balsa'
    FERRY = 'ferry'
    AVIAO = 'aviao'
    HELICOPTERO = 'helicoptero'
    DRONE = 'drone'

class TipoCarga(str, Enum):
    GRANEL_SOLIDO = 'granel_solido'
    GRANEL_LIQUIDO = 'granel_liquido'
    GRANEL_GASOSO = 'granel_gasoso'
    CARGA_GERAL = 'carga_geral'
    CONTEINER = 'conteiner'
    CARGA_PERIGOSA = 'carga_perigosa'
    CARGA_VIVA = 'carga_viva'
    CARGA_FRIGORIFICADA = 'carga_frigorificada'
    CARGA_EXCEPCIONAL = 'carga_excepcional'
    ENCOMENDA = 'encomenda'
    PACOTE = 'pacote'
    DOCUMENTO = 'documento'

class TipoConteiner(str, Enum):
    DRY = 'dry'
    REEFER = 'reefer'
    TANK = 'tank'
    OPEN_TOP = 'open_top'
    FLAT_RACK = 'flat_rack'
    PLATFORM = 'platform'
    HIGH_CUBE = 'high_cube'

class TipoViagem(str, Enum):
    URBANA = 'urbana'
    INTERMUNICIPAL = 'intermunicipal'
    INTERESTADUAL = 'interestadual'
    INTERNACIONAL = 'internacional'
    FRETAMENTO = 'fretamento'
    TURISMO = 'turismo'

class StatusViagem(str, Enum):
    PROGRAMADA = 'programada'
    CONFIRMADA = 'confirmada'
    EM_ANDAMENTO = 'em_andamento'
    CONCLUIDA = 'concluida'
    CANCELADA = 'cancelada'
    ATRASADA = 'atrasada'
    INTERROMPIDA = 'interrompida'

class StatusFrota(str, Enum):
    ATIVA = 'ativa'
    INATIVA = 'inativa'
    SUSPENSA = 'suspensa'

class StatusLinha(str, Enum):
    ATIVA = 'ativa'
    INATIVA = 'inativa'
    SUSPENSA = 'suspensa'
    EM_IMPLANTACAO = 'em_implantacao'

class StatusVeiculoOperacional(str, Enum):
    ATIVO = 'ativo'
    EM_MANUTENCAO = 'em_manutencao'
    INATIVO = 'inativo'
    BLOQUEADO = 'bloqueado'

class StatusReconciliacaoFinanceira(str, Enum):
    PENDENTE = 'pendente'
    CONFIRMADO = 'confirmado'
    REJEITADO = 'rejeitado'

class TipoTarifa(str, Enum):
    PUBLICA = 'publica'
    ESTUDANTE = 'estudante'
    IDOSO = 'idoso'
    PCD = 'pcd'
    VALE_TRANSPORTE = 'vale_transporte'
    PASSAPORTE = 'passaporte'
    INTEGRACAO = 'integracao'

class TipoIntegracao(str, Enum):
    TEMPORAL = 'temporal'
    ESPACIAL = 'espacial'
    TARIFARIA = 'tarifaria'
    MODAL = 'modal'

class TipoOutorga(str, Enum):
    CONCESSAO = 'concessao'
    PERMISSAO = 'permissao'
    AUTORIZACAO = 'autorizacao'

class TipoFiscalizacao(str, Enum):
    ROTINA = 'rotina'
    DENUNCIA = 'denuncia'
    OPERACAO_ESPECIAL = 'operacao_especial'
    BLITZ = 'blitz'
    PESAGEM = 'pesagem'
    DOCUMENTACAO = 'documentacao'

class TipoAutoInfracao(str, Enum):
    EXCESSO_VELOCIDADE = 'excesso_velocidade'
    EXCESSO_PESO = 'excesso_peso'
    DOCUMENTACAO_IRREGULAR = 'documentacao_irregular'
    LICENCA_VENCIDA = 'licenca_vencida'
    ITINERARIO_IRREGULAR = 'itinerario_irregular'
    HORARIO_DESCUMPRIDO = 'horario_descumprido'
    PARADA_IRREGULAR = 'parada_irregular'
    EMBARQUE_DESEMBARQUE_IRREGULAR = 'embarque_desembarque_irregular'
    VEICULO_IRREGULAR = 'veiculo_irregular'
    CONDUTOR_IRREGULAR = 'condutor_irregular'
    CARGA_IRREGULAR = 'carga_irregular'
    DOCUMENTO_FISCAL_IRREGULAR = 'documento_fiscal_irregular'