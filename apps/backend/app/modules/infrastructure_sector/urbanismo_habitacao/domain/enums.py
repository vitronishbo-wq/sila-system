from enum import Enum


class TipoPlanoDiretor(Enum):
    MUNICIPAL = "municipal"
    INTERMUNICIPAL = "intermunicipal"
    REGIONAL = "regional"
    METROPOLITANO = "metropolitano"


class StatusPlanoDiretor(Enum):
    ELABORACAO = "elaboracao"
    CONSULTA_PUBLICA = "consulta_publica"
    AUDIENCIA_PUBLICA = "audiencia_publica"
    APROVADO_CAMARA = "aprovado_camara"
    APROVADO_PREFEITURA = "aprovado_prefeitura"
    SANCIONADO = "sancionado"
    PUBLICADO = "publicado"
    REVOGADO = "revogado"
    ALTERADO = "alterado"


class TipoZona(Enum):
    URBANA = "urbana"
    URBANA_CONSOLIDADA = "urbana_consolidada"
    URBANA_EXPANSAO = "urbana_expansao"
    RURAL = "rural"
    INDUSTRIAL = "industrial"
    COMERCIAL = "comercial"
    RESIDENCIAL = "residencial"
    MISTA = "mista"
    ESPECIAL = "especial"
    PRESERVACAO = "preservacao"
    PROTECAO = "protecao"
    INTERESSE_SOCIAL = "interesse_social"


class UsoPermitido(Enum):
    HABITACIONAL = "habitacional"
    COMERCIAL = "comercial"
    SERVICOS = "servicos"
    INDUSTRIAL = "industrial"
    INSTITUCIONAL = "institucional"
    MISTO = "misto"
    LAZER = "lazer"
    VERDE = "verde"


class TipoOperacaoUrbana(Enum):
    CONCESSAO_URBANISTICA = "concessao_urbanistica"
    PARCERIA_PUBLICO_PRIVADA = "parceria_publico_privada"
    CONSORCIO_IMOBILIARIO = "consorcio_imobiliario"
    OPERACAO_URBANA_CONSORCIADA = "operacao_urbana_consorciada"


class StatusOperacaoUrbana(Enum):
    ELABORACAO = "elaboracao"
    APROVADA = "aprovada"
    EM_EXECUCAO = "em_execucao"
    SUSPENSA = "suspensa"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class TipoParcelamento(Enum):
    LOTEAMENTO = "loteamento"
    DESMEMBRAMENTO = "desmembramento"
    REMEMBRAMENTO = "remembramento"
    DESDOBRO = "desdobro"
    UNIFICACAO = "unificacao"


class StatusParcelamento(Enum):
    ELABORACAO = "elaboracao"
    EM_ANALISE = "em_analise"
    APROVADO = "aprovado"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class TipoLoteamento(Enum):
    ABERTO = "aberto"
    FECHADO = "fechado"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    MISTO = "misto"


class StatusLoteamento(Enum):
    PROPOSTO = "proposto"
    APROVADO = "aprovado"
    EM_IMPLANTACAO = "em_implantacao"
    SUSPENSO = "suspenso"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class StatusLicencaUrbanistica(Enum):
    REQUERIDA = "requerida"
    EM_ANALISE = "em_analise"
    PENDENTE_DOCUMENTACAO = "pendente_documentacao"
    DEFERIDA = "deferida"
    INDEFERIDA = "indeferida"
    CANCELADA = "cancelada"
    VENCIDA = "vencida"


class TipoAlvara(Enum):
    CONSTRUCAO = "construcao"
    REFORMA = "reforma"
    AMPLIACAO = "ampliacao"
    DEMOLICAO = "demolicao"
    FUNCIONAMENTO = "funcionamento"
    LOCALIZACAO = "localizacao"


class StatusAlvara(Enum):
    REQUERIDO = "requerido"
    EM_ANALISE = "em_analise"
    PENDENCIA = "pendencia"
    DEFERIDO = "deferido"
    INDEFERIDO = "indeferido"
    CANCELADO = "cancelado"
    VENCIDO = "vencido"


class TipoHabiteSe(Enum):
    TOTAL = "total"
    PARCIAL = "parcial"
    PROVISORIO = "provisorio"
    DEFINITIVO = "definitivo"


class StatusHabiteSe(Enum):
    REQUERIDO = "requerido"
    EM_VISTORIA = "em_vistoria"
    APROVADO = "aprovado"
    REPROVADO = "reprovado"
    EMITIDO = "emitido"
    CANCELADO = "cancelado"
    VENCIDO = "vencido"


class TipoProgramaHabitacional(Enum):
    MINHA_CASA_MINHA_VIDA = "minha_casa_minha_vida"
    CASA_VERDE_AMARELA = "casa_verde_amarela"
    ARRENDAMENTO_RESIDENCIAL = "arrendamento_residencial"
    MORADIA_CIDADA = "moradia_cidada"
    SUBSIDIO_MORADIA = "subsidio_moradia"
    CARTA_CREDITO = "carta_credito"


class FaixaRenda(Enum):
    FAIXA_1 = "faixa_1"
    FAIXA_2 = "faixa_2"
    FAIXA_3 = "faixa_3"
    FAIXA_4 = "faixa_4"
    FAIXA_5 = "faixa_5"


class StatusSelecao(Enum):
    INSCRITO = "inscrito"
    HABILITADO = "habilitado"
    SELECIONADO = "selecionado"
    CONTEMPLADO = "contemplado"
    SUPLENTE = "suplente"
    DESCLASSIFICADO = "desclassificado"
    DESISTENTE = "desistente"
    CONTRATADO = "contratado"
    ENTREGUE = "entregue"


class TipoAssentamento(Enum):
    FAVELA = "favela"
    OCUPACAO = "ocupacao"
    CORTICO = "cortico"
    COMUNIDADE = "comunidade"
    LOTEAMENTO_IRREGULAR = "loteamento_irregular"
    CONJUNTO_HABITACIONAL = "conjunto_habitacional"


class TipoReassentamento(Enum):
    VOLUNTARIO = "voluntario"
    INVOLUNTARIO = "involuntario"
    PROVISORIO = "provisorio"
    DEFINITIVO = "definitivo"


class TipoRemocao(Enum):
    REMOCAO = "remocao"
    RELOCACAO = "relocacao"
    REASSENTAMENTO = "reassentamento"
    INDENIZACAO = "indenizacao"
    AUXILIO_MORADIA = "auxilio_moradia"
    ALUGUEL_SOCIAL = "aluguel_social"


class StatusZoneamento(Enum):
    ELABORACAO = "elaboracao"
    EM_CONSULTA = "em_consulta"
    APROVADO = "aprovado"
    VIGENTE = "vigente"
    SUSPENSO = "suspenso"
    REVOGADO = "revogado"
