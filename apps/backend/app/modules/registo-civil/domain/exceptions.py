class RegistoCivilError(Exception):
    pass


class RegistoNaoEncontradoError(RegistoCivilError):
    def __init__(self, registo_id: str):
        self.registo_id = registo_id
        super().__init__(f"Registo nao encontrado: {registo_id}")


class RegistoDuplicadoError(RegistoCivilError):
    def __init__(self, detalhe: str):
        self.detalhe = detalhe
        super().__init__(f"Registo duplicado: {detalhe}")
