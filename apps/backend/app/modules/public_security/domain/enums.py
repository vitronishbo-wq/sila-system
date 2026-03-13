from enum import Enum

class TipoAgente(str, Enum):
    POLICIAL = 'policial'
    MILITAR = 'militar'
    BOMBEIRO = 'bombeiro'
    GUARDA = 'guarda'
    INSPETOR = 'inspetor'
    PERITO = 'perito'
    DELEGADO = 'delegado'
    ESCRIVAO = 'escrivao'
    INVESTIGADOR = 'investigador'

class CargoPolicial(str, Enum):
    DELEGADO = 'delegado'
    AGENTE = 'agente'
    ESCRIVAO = 'escrivao'
    INVESTIGADOR = 'investigador'
    PERITO = 'perito'
    PAPILOSCOPISTA = 'papiloscopista'
    AUXILIAR = 'auxiliar'

class Patente(str, Enum):
    SOLDADO = 'soldado'
    CABO = 'cabo'
    SARGENTO = 'sargento'
    SUBTENENTE = 'subtenente'
    TENENTE = 'tenente'
    CAPITAO = 'capitao'
    MAJOR = 'major'
    TENENTE_CORONEL = 'tenente_coronel'
    CORONEL = 'coronel'
    DELEGADO_GERAL = 'delegado_geral'

class TipoVinculo(str, Enum):
    EFETIVO = 'efetivo'
    COMISSIONADO = 'comissionado'
    TEMPORARIO = 'temporario'
    ESTAGIARIO = 'estagiario'
    RESERVISTA = 'reservista'

class StatusAgente(str, Enum):
    ATIVO = 'ativo'
    AFASTADO = 'afastado'
    LICENCA = 'licenca'
    FERIAS = 'ferias'
    TREINAMENTO = 'treinamento'
    SUSPENSO = 'suspenso'
    APOSENTADO = 'aposentado'
    EXONERADO = 'exonerado'

class TipoUnidadePolicial(str, Enum):
    DELEGACIA = 'delegacia'
    POSTO_POLICIAL = 'posto_policial'
    BATALHAO = 'batalhao'
    COMPANHIA = 'companhia'
    PELOTAO = 'pelotao'
    COMANDO = 'comando'
    BASE_OPERACIONAL = 'base_operacional'

class StatusUnidadePolicial(str, Enum):
    ATIVA = 'ativa'
    MANUTENCAO = 'manutencao'
    INTERDITADA = 'interditada'
    DESATIVADA = 'desativada'

class TipoOcorrencia(str, Enum):
    ROUBO = 'roubo'
    FURTO = 'furto'
    HOMICIDIO = 'homicidio'
    LATROCINIO = 'latrocinio'
    LESAO_CORPORAL = 'lesao_corporal'
    VIOLENCIA_DOMESTICA = 'violencia_domestica'
    TRAFICO = 'trafico'
    POSSE_ARMA = 'posse_arma'
    DIRECAO_PERIGOSA = 'direcao_perigosa'
    EMBRIAGUEZ = 'embriaguez'
    DESAPARECIMENTO = 'desaparecimento'
    AMEACA = 'ameaca'
    DANO = 'dano'
    ESTELIONATO = 'estelionato'
    FALSIDADE = 'falsidade'
    CORRUPCAO = 'corrupcao'

class StatusOcorrencia(str, Enum):
    REGISTRADA = 'registrada'
    EM_ANDAMENTO = 'em_andamento'
    CONCLUIDA = 'concluida'
    ARQUIVADA = 'arquivada'
    REMETIDA_JUSTICA = 'remetida_justica'

class PrioridadeOcorrencia(str, Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'
    CRITICA = 'critica'

class TipoMandado(str, Enum):
    PRISAO = 'prisao'
    BUSCA_APREENSAO = 'busca_apreensao'
    APREENSAO = 'apreensao'
    CONDUCAO_COERCITIVA = 'conducao_coercitiva'
    INTERNACAO = 'internacao'

class StatusMandado(str, Enum):
    EXPEDIDO = 'expedido'
    CUMPRIDO = 'cumprido'
    PENDENTE = 'pendente'
    CANCELADO = 'cancelado'
    VENCIDO = 'vencido'

class StatusInvestigacao(str, Enum):
    ABERTA = 'aberta'
    EM_ANDAMENTO = 'em_andamento'
    CONCLUIDA = 'concluida'
    ARQUIVADA = 'arquivada'
    REMETIDA_JUSTICA = 'remetida_justica'

class TipoProva(str, Enum):
    DOCUMENTAL = 'documental'
    TESTEMUNHAL = 'testemunhal'
    MATERIAL = 'material'
    DIGITAL = 'digital'
    AUDIOVISUAL = 'audiovisual'
    BIOLOGICA = 'biologica'
    BALISTICA = 'balistica'

class StatusProva(str, Enum):
    COLETADA = 'coletada'
    EM_ANALISE = 'em_analise'
    VALIDADA = 'validada'
    DESCARTADA = 'descartada'

class StatusCadeiaCustodia(str, Enum):
    INICIADA = 'iniciada'
    EM_TRANSITO = 'em_transito'
    ARMAZENADA = 'armazenada'
    ENCERRADA = 'encerrada'
    ROMPIDA = 'rompida'

class TipoLaudo(str, Enum):
    CRIMINALISTICO = 'criminalistico'
    BALISTICO = 'balistico'
    TOXICOLOGICO = 'toxicologico'
    DNA = 'dna'
    PAPILOSCOPICO = 'papiloscopico'
    DOCUMENTOSCOPICO = 'documentoscopico'
    INFORMATICA = 'informatica'
    MEDICO_LEGAL = 'medico_legal'

class StatusLaudo(str, Enum):
    EM_ELABORACAO = 'em_elaboracao'
    EMITIDO = 'emitido'
    RETIFICADO = 'retificado'
    CANCELADO = 'cancelado'

class TipoVestigio(str, Enum):
    MATERIAL_BIOLOGICO = 'material_biologico'
    IMPRESSAO_DIGITAL = 'impressao_digital'
    RESIDUO_BALISTICO = 'residuo_balistico'
    DOCUMENTO = 'documento'
    MIDIA_DIGITAL = 'midia_digital'
    OBJETO = 'objeto'
    OUTRO = 'outro'

class StatusVestigio(str, Enum):
    COLETADO = 'coletado'
    EM_ANALISE = 'em_analise'
    PRESERVADO = 'preservado'
    DESCARTADO = 'descartado'

class TipoEvidencia(str, Enum):
    FISICA = 'fisica'
    DOCUMENTAL = 'documental'
    DIGITAL = 'digital'
    TESTEMUNHAL = 'testemunhal'
    PERICIAL = 'pericial'

class StatusEvidencia(str, Enum):
    REGISTRADA = 'registrada'
    EM_VALIDACAO = 'em_validacao'
    VALIDADA = 'validada'
    INUTILIZADA = 'inutilizada'