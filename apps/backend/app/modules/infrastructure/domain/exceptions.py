"""Excecoes do modulo obras publicas."""

class ObrasPublicasError(Exception):
    """Erro base do modulo."""

class ObraNotFoundError(ObrasPublicasError):
    """Obra nao encontrada."""

class ObraAlreadyExistsError(ObrasPublicasError):
    """Ja existe obra com o mesmo codigo."""

class ProjetoNotFoundError(ObrasPublicasError):
    """Projeto nao encontrado."""

class ProjetoAlreadyExistsError(ObrasPublicasError):
    """Ja existe projeto equivalente cadastrado."""

class LicitacaoNotFoundError(ObrasPublicasError):
    """Licitacao nao encontrada."""

class LicitacaoAlreadyExistsError(ObrasPublicasError):
    """Ja existe licitacao com o mesmo numero."""

class EditalNotFoundError(ObrasPublicasError):
    """Edital nao encontrado."""

class EditalAlreadyExistsError(ObrasPublicasError):
    """Ja existe edital com o mesmo numero."""