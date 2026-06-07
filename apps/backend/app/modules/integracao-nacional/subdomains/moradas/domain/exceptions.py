class MoradaDomainError(Exception):
    pass


class MoradaInvalidaError(MoradaDomainError):
    def __init__(self, detalhe: str = "Morada invalida"):
        self.detalhe = detalhe
        super().__init__(detalhe)
