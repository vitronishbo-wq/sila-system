from __future__ import annotations

from enum import StrEnum


class TipoBeneficio(StrEnum):
    BOLSA_FAMILIA = "bolsa_familia"
    BPC_IDOSO = "bpc_idoso"
    BPC_PCD = "bpc_pcd"
    AUXILIO_EMERGENCIAL = "auxilio_emergencial"
    AUXILIO_NUTRICIONAL = "auxilio_nutricional"


class SituacaoBeneficiario(StrEnum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"


class FaixaVulnerabilidade(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    EXTREMA = "extrema"


class TipoAtendimento(StrEnum):
    SOCIAL = "social"
    PSICOLOGICO = "psicologico"
    JURIDICO = "juridico"
    ENCAMINHAMENTO = "encaminhamento"


class PublicoAlvo(StrEnum):
    FAMILIA_BAIXA_RENDA = "familia_baixa_renda"
    CRIANCA_RISCO = "crianca_risco"
    IDOSO = "idoso"
    PCD = "pcd"
    SITUACAO_RUA = "situacao_rua"
    JUVENTUDE = "juventude"


class ResultadoVisita(StrEnum):
    FAVORAVEL = "favoravel"
    DESFAVORAVEL = "desfavoravel"
    RETORNO_NECESSARIO = "retorno_necessario"


class StatusBeneficio(StrEnum):
    SOLICITADO = "solicitado"
    APROVADO = "aprovado"
    NEGADO = "negado"
    SUSPENSO = "suspenso"
    ENCERRADO = "encerrado"


class StatusProgramaSocial(StrEnum):
    RASCUNHO = "rascunho"
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    ENCERRADO = "encerrado"


class StatusCadastroUnico(StrEnum):
    PENDENTE_VALIDACAO = "pendente_validacao"
    ATIVO = "ativo"
    INATIVO = "inativo"


class StatusAcompanhamento(StrEnum):
    ATIVO = "ativo"
    ENCERRADO = "encerrado"
