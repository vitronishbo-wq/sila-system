from enum import StrEnum


class TipoAgenteProtecao(StrEnum):
    BOMBEIRO = "bombeiro"
    SOCORRISTA = "socorrista"
    VOLUNTARIO = "voluntario"
    COORDENADOR = "coordenador"
    AGENTE_DEFESA_CIVIL = "agente_defesa_civil"


class CargoBombeiro(StrEnum):
    SOLDADO = "soldado"
    CABO = "cabo"
    SARGENTO = "sargento"
    TENENTE = "tenente"
    CAPITAO = "capitao"
    MAJOR = "major"
    TENENTE_CORONEL = "tenente_coronel"
    CORONEL = "coronel"
    COMANDANTE = "comandante"


class StatusAgenteProtecao(StrEnum):
    ATIVO = "ativo"
    AFASTADO = "afastado"
    LICENCA = "licenca"
    APOSENTADO = "aposentado"
    DESLIGADO = "desligado"


class StatusCorporacao(StrEnum):
    ATIVA = "ativa"
    EM_REESTRUTURACAO = "em_reestruturacao"
    INTERDITADA = "interditada"
    DESATIVADA = "desativada"


class TipoOcorrenciaEmergencial(StrEnum):
    INCENDIO_URBANO = "incendio_urbano"
    INCENDIO_FLORESTAL = "incendio_florestal"
    DESABAMENTO = "desabamento"
    DESLIZAMENTO = "deslizamento"
    INUNDACAO = "inundacao"
    ENCHENTE = "enchente"
    ALAGAMENTO = "alagamento"
    SECA = "seca"
    TEMPESTADE = "tempestade"
    ACIDENTE_TRANSPORTE = "acidente_transporte"
    ACIDENTE_QUIMICO = "acidente_quimico"
    EXPLOSAO = "explosao"
    ROMPIMENTO_BARRAGEM = "rompimento_barragem"
    RESGATE = "resgate"
    SALVAMENTO = "salvamento"
    ATENDIMENTO_PRE_HOSPITALAR = "atendimento_pre_hospitalar"


class StatusOcorrenciaEmergencial(StrEnum):
    RECEBIDA = "recebida"
    EM_ATENDIMENTO = "em_atendimento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
    FALSO_ALARME = "falso_alarme"


class PrioridadeAtendimento(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class StatusDespacho(StrEnum):
    GERADO = "gerado"
    EM_DESLOCAMENTO = "em_deslocamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class StatusAtendimento(StrEnum):
    INICIADO = "iniciado"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"
