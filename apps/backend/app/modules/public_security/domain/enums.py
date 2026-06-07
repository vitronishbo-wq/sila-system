from enum import StrEnum


class TipoAgente(StrEnum):
    POLICIAL = "policial"
    MILITAR = "militar"
    BOMBEIRO = "bombeiro"
    GUARDA = "guarda"
    INSPETOR = "inspetor"
    PERITO = "perito"
    DELEGADO = "delegado"
    ESCRIVAO = "escrivao"
    INVESTIGADOR = "investigador"


class CargoPolicial(StrEnum):
    DELEGADO = "delegado"
    AGENTE = "agente"
    ESCRIVAO = "escrivao"
    INVESTIGADOR = "investigador"
    PERITO = "perito"
    PAPILOSCOPISTA = "papiloscopista"
    AUXILIAR = "auxiliar"


class Patente(StrEnum):
    SOLDADO = "soldado"
    CABO = "cabo"
    SARGENTO = "sargento"
    SUBTENENTE = "subtenente"
    TENENTE = "tenente"
    CAPITAO = "capitao"
    MAJOR = "major"
    TENENTE_CORONEL = "tenente_coronel"
    CORONEL = "coronel"
    DELEGADO_GERAL = "delegado_geral"


class TipoVinculo(StrEnum):
    EFETIVO = "efetivo"
    COMISSIONADO = "comissionado"
    TEMPORARIO = "temporario"
    ESTAGIARIO = "estagiario"
    RESERVISTA = "reservista"


class StatusAgente(StrEnum):
    ATIVO = "ativo"
    AFASTADO = "afastado"
    LICENCA = "licenca"
    FERIAS = "ferias"
    TREINAMENTO = "treinamento"
    SUSPENSO = "suspenso"
    APOSENTADO = "aposentado"
    EXONERADO = "exonerado"


class TipoUnidadePolicial(StrEnum):
    DELEGACIA = "delegacia"
    POSTO_POLICIAL = "posto_policial"
    BATALHAO = "batalhao"
    COMPANHIA = "companhia"
    PELOTAO = "pelotao"
    COMANDO = "comando"
    BASE_OPERACIONAL = "base_operacional"


class StatusUnidadePolicial(StrEnum):
    ATIVA = "ativa"
    MANUTENCAO = "manutencao"
    INTERDITADA = "interditada"
    DESATIVADA = "desativada"


class TipoOcorrencia(StrEnum):
    ROUBO = "roubo"
    FURTO = "furto"
    HOMICIDIO = "homicidio"
    LATROCINIO = "latrocinio"
    LESAO_CORPORAL = "lesao_corporal"
    VIOLENCIA_DOMESTICA = "violencia_domestica"
    TRAFICO = "trafico"
    POSSE_ARMA = "posse_arma"
    DIRECAO_PERIGOSA = "direcao_perigosa"
    EMBRIAGUEZ = "embriaguez"
    DESAPARECIMENTO = "desaparecimento"
    AMEACA = "ameaca"
    DANO = "dano"
    ESTELIONATO = "estelionato"
    FALSIDADE = "falsidade"
    CORRUPCAO = "corrupcao"


class StatusOcorrencia(StrEnum):
    REGISTRADA = "registrada"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    ARQUIVADA = "arquivada"
    REMETIDA_JUSTICA = "remetida_justica"


class PrioridadeOcorrencia(StrEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class TipoMandado(StrEnum):
    PRISAO = "prisao"
    BUSCA_APREENSAO = "busca_apreensao"
    APREENSAO = "apreensao"
    CONDUCAO_COERCITIVA = "conducao_coercitiva"
    INTERNACAO = "internacao"


class StatusMandado(StrEnum):
    EXPEDIDO = "expedido"
    CUMPRIDO = "cumprido"
    PENDENTE = "pendente"
    CANCELADO = "cancelado"
    VENCIDO = "vencido"


class StatusInvestigacao(StrEnum):
    ABERTA = "aberta"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    ARQUIVADA = "arquivada"
    REMETIDA_JUSTICA = "remetida_justica"


class TipoProva(StrEnum):
    DOCUMENTAL = "documental"
    TESTEMUNHAL = "testemunhal"
    MATERIAL = "material"
    DIGITAL = "digital"
    AUDIOVISUAL = "audiovisual"
    BIOLOGICA = "biologica"
    BALISTICA = "balistica"


class StatusProva(StrEnum):
    COLETADA = "coletada"
    EM_ANALISE = "em_analise"
    VALIDADA = "validada"
    DESCARTADA = "descartada"


class StatusCadeiaCustodia(StrEnum):
    INICIADA = "iniciada"
    EM_TRANSITO = "em_transito"
    ARMAZENADA = "armazenada"
    ENCERRADA = "encerrada"
    ROMPIDA = "rompida"


class TipoLaudo(StrEnum):
    CRIMINALISTICO = "criminalistico"
    BALISTICO = "balistico"
    TOXICOLOGICO = "toxicologico"
    DNA = "dna"
    PAPILOSCOPICO = "papiloscopico"
    DOCUMENTOSCOPICO = "documentoscopico"
    INFORMATICA = "informatica"
    MEDICO_LEGAL = "medico_legal"


class StatusLaudo(StrEnum):
    EM_ELABORACAO = "em_elaboracao"
    EMITIDO = "emitido"
    RETIFICADO = "retificado"
    CANCELADO = "cancelado"


class TipoVestigio(StrEnum):
    MATERIAL_BIOLOGICO = "material_biologico"
    IMPRESSAO_DIGITAL = "impressao_digital"
    RESIDUO_BALISTICO = "residuo_balistico"
    DOCUMENTO = "documento"
    MIDIA_DIGITAL = "midia_digital"
    OBJETO = "objeto"
    OUTRO = "outro"


class StatusVestigio(StrEnum):
    COLETADO = "coletado"
    EM_ANALISE = "em_analise"
    PRESERVADO = "preservado"
    DESCARTADO = "descartado"


class TipoEvidencia(StrEnum):
    FISICA = "fisica"
    DOCUMENTAL = "documental"
    DIGITAL = "digital"
    TESTEMUNHAL = "testemunhal"
    PERICIAL = "pericial"


class StatusEvidencia(StrEnum):
    REGISTRADA = "registrada"
    EM_VALIDACAO = "em_validacao"
    VALIDADA = "validada"
    INUTILIZADA = "inutilizada"
