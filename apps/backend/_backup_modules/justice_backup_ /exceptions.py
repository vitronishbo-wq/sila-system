from apps.backend.app.modules.justice.justica.domain.exceptions import AdvogadoNaoEncontradoException, JusticaException, MagistradoNaoEncontradoException, ParteInvalidaException, ProcessoNaoEncontradoException, RecursoForaPrazoException, SentencaJaProferidaException

class JusticaError(Exception):
    pass

class CitizenNotFoundError(JusticaError):
    pass

class TribunalNotFoundError(JusticaError):
    pass

class VaraNotFoundError(JusticaError):
    pass

class ProcessoNotFoundError(JusticaError):
    pass

class ParteProcessualAlreadyExistsError(JusticaError):
    pass

class ParteProcessualNotFoundError(JusticaError):
    pass

class AdvogadoAlreadyExistsError(JusticaError):
    pass

class AdvogadoNotFoundError(JusticaError):
    pass

class MagistradoAlreadyExistsError(JusticaError):
    pass

class MagistradoNotFoundError(JusticaError):
    pass

class DespachoNotFoundError(JusticaError):
    pass

class SentencaNotFoundError(JusticaError):
    pass

class SentencaAlreadyExistsError(JusticaError):
    pass

class RecursoNotFoundError(JusticaError):
    pass