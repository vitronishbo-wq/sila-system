"""Excecoes do modulo gestao fundiaria."""

class GestaoFundiariaError(Exception):
    """Erro base do modulo."""

class ImovelNotFoundError(GestaoFundiariaError):
    """Imovel nao encontrado."""

class ImovelAlreadyExistsError(GestaoFundiariaError):
    """Ja existe imovel com a mesma inscricao imobiliaria."""

class ProprietarioNotFoundError(GestaoFundiariaError):
    """Proprietario nao encontrado."""

class ProprietarioAlreadyExistsError(GestaoFundiariaError):
    """Ja existe proprietario com o mesmo documento."""

class OneracaoNotFoundError(GestaoFundiariaError):
    """Oneracao nao encontrada."""

class OneracaoAlreadyExistsError(GestaoFundiariaError):
    """Ja existe oneracao com o mesmo numero."""

class DesapropriacaoNotFoundError(GestaoFundiariaError):
    """Desapropriacao nao encontrada."""

class DesapropriacaoAlreadyExistsError(GestaoFundiariaError):
    """Ja existe desapropriacao com o mesmo numero de processo."""

class MatriculaImovelNotFoundError(GestaoFundiariaError):
    """Matricula de imovel nao encontrada."""

class MatriculaImovelAlreadyExistsError(GestaoFundiariaError):
    """Ja existe matricula de imovel com o mesmo numero."""

class GeorreferenciamentoNotFoundError(GestaoFundiariaError):
    """Georreferenciamento nao encontrado."""

class GeorreferenciamentoAlreadyExistsError(GestaoFundiariaError):
    """Ja existe georreferenciamento com o mesmo codigo."""