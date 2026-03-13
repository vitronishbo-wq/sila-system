from __future__ import annotations
from enum import Enum

class TipoBeneficio(str, Enum):
    BOLSA_FAMILIA = 'bolsa_familia'
    BPC_IDOSO = 'bpc_idoso'
    BPC_PCD = 'bpc_pcd'
    AUXILIO_EMERGENCIAL = 'auxilio_emergencial'
    AUXILIO_NUTRICIONAL = 'auxilio_nutricional'

class SituacaoBeneficiario(str, Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    SUSPENSO = 'suspenso'

class FaixaVulnerabilidade(str, Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'
    EXTREMA = 'extrema'

class TipoAtendimento(str, Enum):
    SOCIAL = 'social'
    PSICOLOGICO = 'psicologico'
    JURIDICO = 'juridico'
    ENCAMINHAMENTO = 'encaminhamento'

class PublicoAlvo(str, Enum):
    FAMILIA_BAIXA_RENDA = 'familia_baixa_renda'
    CRIANCA_RISCO = 'crianca_risco'
    IDOSO = 'idoso'
    PCD = 'pcd'
    SITUACAO_RUA = 'situacao_rua'
    JUVENTUDE = 'juventude'

class ResultadoVisita(str, Enum):
    FAVORAVEL = 'favoravel'
    DESFAVORAVEL = 'desfavoravel'
    RETORNO_NECESSARIO = 'retorno_necessario'

class StatusBeneficio(str, Enum):
    SOLICITADO = 'solicitado'
    APROVADO = 'aprovado'
    NEGADO = 'negado'
    SUSPENSO = 'suspenso'
    ENCERRADO = 'encerrado'

class StatusProgramaSocial(str, Enum):
    RASCUNHO = 'rascunho'
    ATIVO = 'ativo'
    SUSPENSO = 'suspenso'
    ENCERRADO = 'encerrado'

class StatusCadastroUnico(str, Enum):
    PENDENTE_VALIDACAO = 'pendente_validacao'
    ATIVO = 'ativo'
    INATIVO = 'inativo'

class StatusAcompanhamento(str, Enum):
    ATIVO = 'ativo'
    ENCERRADO = 'encerrado'