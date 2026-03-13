from enum import Enum

class TipoObra(Enum):
    CONSTRUCAO = 'construcao'
    REFORMA = 'reforma'
    AMPLIACAO = 'ampliacao'
    RESTAURO = 'restauro'
    DEMOLICAO = 'demolicao'
    URBANIZACAO = 'urbanizacao'
    PAVIMENTACAO = 'pavimentacao'
    PONTES = 'pontes'
    VIADUTOS = 'viadutos'
    TUNEIS = 'tuneis'
    BARRAGENS = 'barragens'
    CANAIS = 'canais'
    DRENAGEM = 'drenagem'
    SANEAMENTO = 'saneamento'
    HIDRAULICA = 'hidraulica'
    ELETRICA = 'eletrica'
    COMUNICACAO = 'comunicacao'

class NaturezaObra(Enum):
    NOVA = 'nova'
    EXISTENTE = 'existente'
    SUBSTITUICAO = 'substituicao'

class StatusObra(Enum):
    PROJETO = 'projeto'
    LICITACAO = 'licitacao'
    CONTRATADA = 'contratada'
    EM_EXECUCAO = 'em_execucao'
    PARALISADA = 'paralisada'
    SUSPENSA = 'suspensa'
    EMBARGADA = 'embargada'
    CONCLUIDA = 'concluida'
    ENTREGUE = 'entregue'
    CANCELADA = 'cancelada'
    ABANDONADA = 'abandonada'

class TipoLicitacao(Enum):
    CONCORRENCIA = 'concorrencia'
    TOMADA_PRECOS = 'tomada_precos'
    CONVITE = 'convite'
    PREGAO = 'pregao'
    CONCURSO = 'concurso'
    LEILAO = 'leilao'
    DISPENSA = 'dispensa'
    INEXIGIBILIDADE = 'inexigibilidade'

class StatusLicitacao(Enum):
    EDITAL_PUBLICADO = 'edital_publicado'
    RECEBENDO_PROPOSTAS = 'recebendo_propostas'
    PROPOSTAS_ENTREGUES = 'propostas_entregues'
    EM_ANALISE = 'em_analise'
    HABILITACAO = 'habilitacao'
    RECURSOS = 'recursos'
    ADJUDICADA = 'adjudicada'
    HOMOLOGADA = 'homologada'
    DESERTA = 'deserta'
    FRACASSADA = 'fracassada'
    REVOGADA = 'revogada'
    ANULADA = 'anulada'

class TipoContrato(Enum):
    EMPREITADA_GLOBAL = 'empreitada_global'
    EMPREITADA_PRECO_UNITARIO = 'empreitada_preco_unitario'
    TAREFA = 'tarefa'
    ADMINISTRACAO = 'administracao'

class StatusContrato(Enum):
    ASSINADO = 'assinado'
    EM_VIGOR = 'em_vigor'
    SUSPENSO = 'suspenso'
    RESCINDIDO = 'rescindido'
    CONCLUIDO = 'concluido'
    ARQUIVADO = 'arquivado'

class TipoAditivo(Enum):
    PRAZO = 'prazo'
    VALOR = 'valor'
    OBJETO = 'objeto'
    AMBOS = 'ambos'

class TipoMedicao(Enum):
    MENSAL = 'mensal'
    QUINZENAL = 'quinzenal'
    SEMANAL = 'semanal'
    POR_ETAPA = 'por_etapa'

class TipoOcorrencia(Enum):
    ACIDENTE = 'acidente'
    ACIDENTE_FATAL = 'acidente_fatal'
    INTERCORRENCIA_TECNICA = 'intercorrencia_tecnica'
    PROBLEMA_QUALIDADE = 'problema_qualidade'
    FALTA_MATERIAL = 'falta_material'
    GREVE = 'greve'
    CHUVA = 'chuva'
    OUTROS = 'outros'

class TipoProjeto(Enum):
    BASICO = 'basico'
    EXECUTIVO = 'executivo'
    COMPLEMENTAR = 'complementar'
    REVISAO = 'revisao'

class StatusProjeto(Enum):
    ELABORACAO = 'elaboracao'
    APROVADO = 'aprovado'
    EM_EXECUCAO = 'em_execucao'
    CONCLUIDO = 'concluido'
    ARQUIVADO = 'arquivado'

class StatusEdital(Enum):
    PUBLICADO = 'publicado'
    IMPUGNADO = 'impugnado'
    RETIFICADO = 'retificado'
    SUSPENSO = 'suspenso'
    REVOGADO = 'revogado'
    ENCERRADO = 'encerrado'