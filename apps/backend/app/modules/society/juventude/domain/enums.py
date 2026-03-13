from enum import Enum

class FaixaEtaria(str, Enum):
    JOVEM_15_17 = '15_17'
    JOVEM_18_24 = '18_24'
    JOVEM_25_29 = '25_29'
    JOVEM_30_35 = '30_35'

class Escolaridade(str, Enum):
    SEM_ESCOLARIDADE = 'sem_escolaridade'
    FUNDAMENTAL_INCOMPLETO = 'fundamental_incompleto'
    FUNDAMENTAL_COMPLETO = 'fundamental_completo'
    MEDIO_INCOMPLETO = 'medio_incompleto'
    MEDIO_COMPLETO = 'medio_completo'
    SUPERIOR_INCOMPLETO = 'superior_incompleto'
    SUPERIOR_COMPLETO = 'superior_completo'
    POS_GRADUACAO = 'pos_graduacao'

class SituacaoOcupacional(str, Enum):
    ESTUDA = 'estuda'
    TRABALHA = 'trabalha'
    ESTUDA_TRABALHA = 'estuda_trabalha'
    DESEMPREGADO = 'desempregado'
    PROCURA_EMPREGO = 'procura_emprego'
    NAO_ESTUDA_NAO_TRABALHA = 'nao_estuda_nao_trabalha'

class TipoAuxilio(str, Enum):
    TRANSPORTE = 'transporte'
    ALIMENTACAO = 'alimentacao'
    MORADIA = 'moradia'
    SAUDE = 'saude'
    PSICOLOGICO = 'psicologico'
    MATERIAL_ESCOLAR = 'material_escolar'
    UNIFORME = 'uniforme'
    TECNOLOGICO = 'tecnologico'

class StatusBeneficio(str, Enum):
    ATIVO = 'ativo'
    SUSPENSO = 'suspenso'
    CANCELADO = 'cancelado'
    CONCLUIDO = 'concluido'
    AGUARDANDO = 'aguardando'

class TipoPrograma(str, Enum):
    APRENDIZAGEM = 'aprendizagem'
    ESTAGIO = 'estagio'
    PRIMEIRO_EMPREGO = 'primeiro_emprego'
    EMPREENDEDORISMO = 'empreendedorismo'
    INTERCAMBIO = 'intercambio'
    VOLUNTARIADO = 'voluntariado'
    CAPACITACAO = 'capacitacao'
    LIDERANCA = 'lideranca'

class StatusPrograma(str, Enum):
    PLANEADO = 'planeado'
    INSCRICOES_ABERTAS = 'inscricoes_abertas'
    ATIVO = 'ativo'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'

class StatusFormacao(str, Enum):
    INSCRITO = 'inscrito'
    EM_ANDAMENTO = 'em_andamento'
    CONCLUIDA = 'concluida'
    REPROVADA = 'reprovada'
    CANCELADA = 'cancelada'

class TipoVulnerabilidade(str, Enum):
    BAIXA_RENDA = 'baixa_renda'
    SITUACAO_RUA = 'situacao_rua'
    ACOLHIMENTO = 'acolhimento'
    MEDIDA_SOCIOEDUCATIVA = 'medida_socioeducativa'
    EGRESSO_SISTEMA = 'egresso_sistema'
    VIOLENCIA_DOMESTICA = 'violencia_domestica'
    TRABALHO_INFANTIL = 'trabalho_infantil'
    EXPLORACAO_SEXUAL = 'exploracao_sexual'
    DEPENDENCIA_QUIMICA = 'dependencia_quimica'
    SAUDE_MENTAL = 'saude_mental'
    GRAVIDEZ_PRECOCE = 'gravidez_precoce'
    DEFICIENCIA = 'deficiencia'

class RiscoSocial(str, Enum):
    BAIXO = 'baixo'
    MEDIO = 'medio'
    ALTO = 'alto'
    CRITICO = 'critico'

class SituacaoJovem(str, Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    EM_ACOMPANHAMENTO = 'em_acompanhamento'
    EGRESSO = 'egresso'

class NivelEscolaridade(str, Enum):
    FUNDAMENTAL = 'fundamental'
    MEDIO = 'medio'
    SUPERIOR = 'superior'
    POS = 'pos'

class TipoBolsa(str, Enum):
    PERMANENCIA = 'permanencia'
    MERITO = 'merito'
    PESQUISA = 'pesquisa'
    EXTENSAO = 'extensao'

class AreaInteresse(str, Enum):
    AGRICULTURA = 'agricultura'
    SAUDE = 'saude'
    EDUCACAO = 'educacao'
    TECNOLOGIA = 'tecnologia'
    EMPREENDEDORISMO = 'empreendedorismo'
    CULTURA = 'cultura'
    DESPORTO = 'desporto'
    AMBIENTE = 'ambiente'

class StatusInscricao(str, Enum):
    PENDENTE = 'pendente'
    CONFIRMADA = 'confirmada'
    CANCELADA = 'cancelada'
    CONCLUIDA = 'concluida'

class StatusFluxo(str, Enum):
    PENDENTE = 'pendente'
    CONFIRMADA = 'confirmada'
    EM_ANALISE = 'em_analise'
    APROVADA = 'aprovada'
    REJEITADA = 'rejeitada'
    CONCLUIDA = 'concluida'
    CANCELADA = 'cancelada'

class StatusEstagio(str, Enum):
    PLANEADO = 'planeado'
    ATIVO = 'ativo'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'

class StatusIntercambio(str, Enum):
    SOLICITADO = 'solicitado'
    APROVADO = 'aprovado'
    EM_EXECUCAO = 'em_execucao'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'

class TipoEvento(str, Enum):
    FEIRA = 'feira'
    FORUM = 'forum'
    WORKSHOP = 'workshop'
    HACKATHON = 'hackathon'
    CAMPANHA = 'campanha'

class StatusEvento(str, Enum):
    PLANEADO = 'planeado'
    INSCRICOES_ABERTAS = 'inscricoes_abertas'
    ENCERRADO = 'encerrado'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'

class TipoMentoria(str, Enum):
    CARREIRA = 'carreira'
    ACADEMICA = 'academica'
    EMPREENDEDORISMO = 'empreendedorismo'
    PSICOSSOCIAL = 'psicossocial'

class StatusMentoria(str, Enum):
    ATIVA = 'ativa'
    PAUSADA = 'pausada'
    CONCLUIDA = 'concluida'
    CANCELADA = 'cancelada'

class TipoSaudeJuvenil(str, Enum):
    FISICA = 'fisica'
    MENTAL = 'mental'
    REPRODUTIVA = 'reprodutiva'
    NUTRICIONAL = 'nutricional'

class StatusAcompanhamento(str, Enum):
    ABERTO = 'aberto'
    EM_CURSO = 'em_curso'
    ENCERRADO = 'encerrado'
    SUSPENSO = 'suspenso'

class StatusEmpreendimento(str, Enum):
    IDEIA = 'ideia'
    INCUBACAO = 'incubacao'
    OPERACAO = 'operacao'
    ENCERRADO = 'encerrado'

class StatusVoluntariado(str, Enum):
    INSCRITO = 'inscrito'
    ATIVO = 'ativo'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'

class StatusPoliticaJuventude(str, Enum):
    RASCUNHO = 'rascunho'
    ATIVA = 'ativa'
    SUSPENSA = 'suspensa'
    CONCLUIDA = 'concluida'