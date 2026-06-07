class BiDomainError(Exception):
    pass


class BiNumeroInvalidoError(BiDomainError):
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Numero de BI invalido: {numero}")


class BiNaoEncontradoError(BiDomainError):
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"BI nao encontrado: {numero}")


class BiIntegracaoIndisponivelError(BiDomainError):
    def __init__(self, fonte: str = "desconhecida"):
        self.fonte = fonte
        super().__init__(f"Fonte de verificacao de BI indisponivel: {fonte}")
