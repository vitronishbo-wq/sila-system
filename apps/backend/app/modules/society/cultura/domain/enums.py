from enum import StrEnum


class TipoAgenteCultural(StrEnum):
    ARTISTA = "artista"
    PRODUTOR = "produtor"
    GESTOR = "gestor"
    CURADOR = "curador"
    EDUCADOR = "educador"
    PESQUISADOR = "pesquisador"
    TECNICO = "tecnico"


class TipoArtista(StrEnum):
    MUSICO = "musico"
    DANCARINO = "dancarino"
    ATOR = "ator"
    PINTOR = "pintor"
    ESCULTOR = "escultor"
    ARTESAO = "artesao"
    ESCRITOR = "escritor"
    POETA = "poeta"
    CINEASTA = "cineasta"
    FOTOGRAFO = "fotografo"


class TipoPatrimonio(StrEnum):
    MATERIAL = "material"
    IMATERIAL = "imaterial"
    ARQUEOLOGICO = "arqueologico"
    HISTORICO = "historico"
    ARTISTICO = "artistico"
    PAISAGISTICO = "paisagistico"


class StatusTombamento(StrEnum):
    PROPOSTO = "proposto"
    EM_ANALISE = "em_analise"
    TOMBADO = "tombado"
    CANCELADO = "cancelado"
    REVOGADO = "revogado"


class TipoEventoCultural(StrEnum):
    FESTIVAL = "festival"
    MOSTRA = "mostra"
    EXPOSICAO = "exposicao"
    FEIRA = "feira"
    ESPETACULO = "espetaculo"
    OFICINA = "oficina"


class StatusEventoCultural(StrEnum):
    RASCUNHO = "rascunho"
    PUBLICADO = "publicado"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class TipoGrupoArtistico(StrEnum):
    BANDA = "banda"
    COMPANHIA = "companhia"
    COLETIVO = "coletivo"
    CORAL = "coral"
    ORQUESTRA = "orquestra"


class CategoriaPatrimonioImaterial(StrEnum):
    FESTA_POPULAR = "festa_popular"
    RITUAL = "ritual"
    TRADICAO = "tradicao"
    SABER_TRADICIONAL = "saber_tradicional"
    EXPRESSAO_ORAL = "expressao_oral"
    MUSICA_TRADICIONAL = "musica_tradicional"
    DANCA_TRADICIONAL = "danca_tradicional"


class StatusPatrimonioImaterial(StrEnum):
    PROPOSTO = "proposto"
    EM_ANALISE = "em_analise"
    REGISTRADO = "registrado"
    SUSPENSO = "suspenso"


class TipoEspacoCultural(StrEnum):
    TEATRO = "teatro"
    MUSEU = "museu"
    CENTRO_CULTURAL = "centro_cultural"
    BIBLIOTECA = "biblioteca"
    GALERIA = "galeria"
    CINEMA = "cinema"
    AUDITORIO = "auditorio"
    SALA_EXPOSICAO = "sala_exposicao"


class TipoProjetoCultural(StrEnum):
    PRODUCAO = "producao"
    CIRCULACAO = "circulacao"
    FORMACAO = "formacao"
    PRESERVACAO = "preservacao"
    PESQUISA = "pesquisa"
    DIFUSAO = "difusao"
    FOMENTO = "fomento"


class NaturezaProjetoCultural(StrEnum):
    ARTISTICA = "artistica"
    CULTURAL = "cultural"
    EDUCATIVA = "educativa"
    SOCIAL = "social"
    TECNICA = "tecnica"


class StatusProjetoCultural(StrEnum):
    RASCUNHO = "rascunho"
    SUBMETIDO = "submetido"
    EM_ANALISE = "em_analise"
    APROVADO = "aprovado"
    REPROVADO = "reprovado"
    CONTRATADO = "contratado"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDO = "concluido"
    PRESTACAO_CONTAS = "prestacao_contas"
    ARQUIVADO = "arquivado"


class TipoEditalCultural(StrEnum):
    FOMENTO = "fomento"
    PREMIO = "premio"
    RESIDENCIA = "residencia"
    CIRCULACAO = "circulacao"
    PRODUCAO = "producao"
    PESQUISA = "pesquisa"
    FORMACAO = "formacao"


class FaseEditalCultural(StrEnum):
    PUBLICADO = "publicado"
    INSCRICOES_ABERTAS = "inscricoes_abertas"
    INSCRICOES_ENCERRADAS = "inscricoes_encerradas"
    EM_ANALISE = "em_analise"
    RESULTADO_PRELIMINAR = "resultado_preliminar"
    PRAZO_RECURSOS = "prazo_recursos"
    RESULTADO_FINAL = "resultado_final"
    CONTRATACAO = "contratacao"
    CONCLUIDO = "concluido"
