class TransportesLogisticaError(Exception):
    pass

class ViagemNotFoundError(TransportesLogisticaError):
    pass

class ViagemConflictError(TransportesLogisticaError):
    pass

class InvalidViagemStateError(TransportesLogisticaError):
    pass

class FrotaNotFoundError(TransportesLogisticaError):
    pass

class FrotaAlreadyExistsError(TransportesLogisticaError):
    pass

class LinhaNotFoundError(TransportesLogisticaError):
    pass

class LinhaAlreadyExistsError(TransportesLogisticaError):
    pass

class VeiculoNotFoundError(TransportesLogisticaError):
    pass

class VeiculoAlreadyExistsError(TransportesLogisticaError):
    pass

class BilhetagemNotFoundError(TransportesLogisticaError):
    pass