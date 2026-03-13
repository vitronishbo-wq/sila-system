class DefesaConsumidorException(Exception):

    def __init__(self, message: str, code: str='DC_ERROR', status_code: int=400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)

class ReclamacaoNaoEncontradaException(DefesaConsumidorException):

    def __init__(self, reclamacao_id: int):
        super().__init__(f'Reclamacao {reclamacao_id} nao encontrada', 'DC_RECLAMACAO_NOT_FOUND', 404)

class ReclamacaoJaEncerradaException(DefesaConsumidorException):

    def __init__(self, reclamacao_id: int):
        super().__init__(f'Reclamacao {reclamacao_id} ja esta encerrada', 'DC_RECLAMACAO_ALREADY_CLOSED', 400)

class ProtocoloDuplicadoException(DefesaConsumidorException):

    def __init__(self, protocolo: str):
        super().__init__(f'Protocolo {protocolo} ja existe', 'DC_PROTOCOLO_DUPLICADO', 409)