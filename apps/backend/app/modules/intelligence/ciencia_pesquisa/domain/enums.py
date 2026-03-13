from __future__ import annotations
from enum import Enum

class StatusVinculoPesquisador(str, Enum):
    ATIVO = 'ativo'
    AFASTADO = 'afastado'
    SUSPENSO = 'suspenso'
    ENCERRADO = 'encerrado'

class AreaConhecimento(str, Enum):
    CIENCIAS_EXATAS = 'ciencias_exatas'
    CIENCIAS_BIOLOGICAS = 'ciencias_biologicas'
    CIENCIAS_SAUDE = 'ciencias_saude'
    CIENCIAS_AGRARIAS = 'ciencias_agrarias'
    CIENCIAS_SOCIAIS_APLICADAS = 'ciencias_sociais_aplicadas'
    ENGENHARIAS = 'engenharias'
    LINGUISTICA_ARTES = 'linguistica_artes'
    HUMANIDADES = 'humanidades'
    MULTIDISCIPLINAR = 'multidisciplinar'

class NivelFormacao(str, Enum):
    GRADUADO = 'graduado'
    ESPECIALISTA = 'especialista'
    MESTRE = 'mestre'
    DOUTOR = 'doutor'
    POS_DOUTOR = 'pos_doutor'

class TipoVinculoPesquisador(str, Enum):
    EFETIVO = 'efetivo'
    BOLSISTA = 'bolsista'
    COLABORADOR = 'colaborador'
    VISITANTE = 'visitante'
    VOLUNTARIO = 'voluntario'

class TipoInstituicaoPesquisa(str, Enum):
    UNIVERSIDADE = 'universidade'
    INSTITUTO = 'instituto'
    CENTRO_PESQUISA = 'centro_pesquisa'
    LABORATORIO = 'laboratorio'
    FUNDACAO = 'fundacao'
    EMPRESA = 'empresa'

class NaturezaJuridicaInstituicao(str, Enum):
    PUBLICA = 'publica'
    PRIVADA = 'privada'
    COMUNITARIA = 'comunitaria'
    PUBLICO_PRIVADA = 'publico_privada'

class StatusCredenciamentoInstituicao(str, Enum):
    EM_ANALISE = 'em_analise'
    CREDENCIADA = 'credenciada'
    SUSPENSA = 'suspensa'
    DESCREDENCIADA = 'descredenciada'

class StatusProjetoPesquisa(str, Enum):
    RASCUNHO = 'rascunho'
    SUBMETIDO = 'submetido'
    APROVADO = 'aprovado'
    EM_EXECUCAO = 'em_execucao'
    SUSPENSO = 'suspenso'
    ENCERRADO = 'encerrado'
    CANCELADO = 'cancelado'