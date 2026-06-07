from enum import Enum


class TipoProdutor(Enum):
    PEQUENO = "pequeno"
    MEDIO = "medio"
    GRANDE = "grande"
    FAMILIAR = "familiar"
    EMPRESARIAL = "empresarial"
    COOPERATIVA = "cooperativa"


class StatusProdutor(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    PENDENTE = "pendente"
    SUSPENSO = "suspenso"


class TipoPropriedade(Enum):
    PROPRIO = "proprio"
    ARRENDADO = "arrendado"
    PARCERIA = "parceria"
    POSSE = "posse"


class TipoCultura(Enum):
    ANUAL = "anual"
    PERENE = "perene"
    HORTALICA = "hortalica"
    FRUTICULTURA = "fruticultura"
    GRAOS = "graos"
    FORRAGEIRA = "forrageira"


class StatusSafra(Enum):
    PLANEJADA = "planejada"
    EM_ANDAMENTO = "em_andamento"
    COLHIDA = "colhida"
    PERDIDA = "perdida"


class TipoInsumo(Enum):
    SEMENTE = "semente"
    MUDA = "muda"
    FERTILIZANTE = "fertilizante"
    DEFENSIVO = "defensivo"
    ADUBO = "adubo"
    COMBUSTIVEL = "combustivel"


class StatusEstoque(Enum):
    NORMAL = "normal"
    BAIXO = "baixo"
    ZERADO = "zerado"


class TipoOperacao(Enum):
    PREPARO_SOLO = "preparo_solo"
    PLANTIO = "plantio"
    IRRIGACAO = "irrigacao"
    ADUBACAO = "adubacao"
    APLICACAO_DEFENSIVO = "aplicacao_defensivo"
    COLHEITA = "colheita"


class SeveridadeOcorrencia(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class StatusOcorrencia(Enum):
    ABERTA = "aberta"
    EM_TRATAMENTO = "em_tratamento"
    RESOLVIDA = "resolvida"


class StatusCertificacao(Enum):
    SOLICITADA = "solicitada"
    APROVADA = "aprovada"
    REPROVADA = "reprovada"
    VENCIDA = "vencida"


class StatusCredito(Enum):
    SOLICITADO = "solicitado"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    DESEMBOLSADO = "desembolsado"


class StatusAssistencia(Enum):
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"


class TipoZonaAgricola(Enum):
    PRODUCAO_INTENSIVA = "producao_intensiva"
    USO_MISTO = "uso_misto"
    PASTAGEM = "pastagem"
    SILVICULTURA = "silvicultura"
    PROTECAO_AMBIENTAL = "protecao_ambiental"


class AptidaoSolo(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"
    RESTRITA = "restrita"


class StatusZoneamento(Enum):
    ATIVO = "ativo"
    EM_REVISAO = "em_revisao"
    REVOGADO = "revogado"


class StatusCadastroAmbiental(Enum):
    PENDENTE = "pendente"
    COM_PENDENCIA = "com_pendencia"
    VALIDADO = "validado"


class StatusTalhao(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class StatusPlantio(Enum):
    PLANEJADO = "planejado"
    EXECUTADO = "executado"
    CANCELADO = "cancelado"


class TipoEquipamento(Enum):
    TRATOR = "trator"
    COLHEITADEIRA = "colheitadeira"
    PULVERIZADOR = "pulverizador"
    IRRIGACAO = "irrigacao"
    IMPLEMENTO = "implemento"


class StatusEquipamento(Enum):
    DISPONIVEL = "disponivel"
    EM_USO = "em_uso"
    EM_MANUTENCAO = "em_manutencao"
    INATIVO = "inativo"
