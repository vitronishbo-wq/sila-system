"""Excecoes do modulo transportes e logistica."""

class TransportesLogisticaError(Exception):
    """Erro base do modulo."""

class ViagemNotFoundError(TransportesLogisticaError):
    """Viagem nao encontrada."""

class ViagemConflictError(TransportesLogisticaError):
    """Conflito de agenda para o veiculo ou rota."""

class InvalidViagemStateError(TransportesLogisticaError):
    """Transicao de estado invalida para viagem."""

class FrotaNotFoundError(TransportesLogisticaError):
    """Frota nao encontrada."""

class FrotaAlreadyExistsError(TransportesLogisticaError):
    """Ja existe frota com o mesmo codigo."""

class InvalidFrotaStateError(TransportesLogisticaError):
    """Transicao de estado invalida para frota."""

class LinhaNotFoundError(TransportesLogisticaError):
    """Linha nao encontrada."""

class LinhaAlreadyExistsError(TransportesLogisticaError):
    """Ja existe linha com o mesmo codigo."""

class VeiculoNotFoundError(TransportesLogisticaError):
    """Veiculo nao encontrado."""

class VeiculoAlreadyExistsError(TransportesLogisticaError):
    """Ja existe veiculo com a mesma placa."""

class BilhetagemNotFoundError(TransportesLogisticaError):
    """Evento de bilhetagem nao encontrado."""