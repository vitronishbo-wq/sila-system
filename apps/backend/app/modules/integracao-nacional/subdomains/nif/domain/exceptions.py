class NifDomainError(Exception):
    pass


class NifNumeroInvalidoError(NifDomainError):
    def __init__(self, nif: str):
        self.nif = nif
        super().__init__(f"Numero de NIF invalido: {nif}")


class NifNaoEncontradoError(NifDomainError):
    def __init__(self, nif: str):
        self.nif = nif
        super().__init__(f"NIF nao encontrado: {nif}")
