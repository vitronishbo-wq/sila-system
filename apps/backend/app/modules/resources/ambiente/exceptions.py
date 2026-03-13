"""Excecoes do modulo ambiente."""

class AmbienteError(Exception):
    """Erro base do modulo."""

class ProprietarioNotFoundError(AmbienteError):
    """Proprietario nao encontrado."""

class ProprietarioAlreadyExistsError(AmbienteError):
    """Proprietario com documento ja cadastrado."""

class ImovelNotFoundError(AmbienteError):
    """Imovel rural nao encontrado."""

class CARNotFoundError(AmbienteError):
    """CAR nao encontrado."""

class CARAlreadyExistsError(AmbienteError):
    """Ja existe CAR para o imovel informado."""

class LicencaNotFoundError(AmbienteError):
    """Licenca ambiental nao encontrada."""

class LicencaAlreadyExistsError(AmbienteError):
    """Ja existe licenca ativa para este CAR e tipo."""

class EstudoNotFoundError(AmbienteError):
    """Estudo ambiental nao encontrado."""

class CondicionanteNotFoundError(AmbienteError):
    """Condicionante nao encontrada."""

class FiscalizacaoNotFoundError(AmbienteError):
    """Fiscalizacao nao encontrada."""

class AutoInfracaoNotFoundError(AmbienteError):
    """Auto de infracao nao encontrado."""

class EmbargoNotFoundError(AmbienteError):
    """Embargo nao encontrado."""

class MultaNotFoundError(AmbienteError):
    """Multa nao encontrada."""