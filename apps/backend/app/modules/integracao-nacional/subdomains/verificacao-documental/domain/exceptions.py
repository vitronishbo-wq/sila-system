class DocumentoDomainError(Exception):
    pass


class TipoDocumentoNaoSuportadoError(DocumentoDomainError):
    def __init__(self, tipo: str):
        self.tipo = tipo
        super().__init__(f"Tipo de documento nao suportado: {tipo}")


class DocumentoInvalidoError(DocumentoDomainError):
    def __init__(self, motivo: str = "Documento invalido"):
        self.motivo = motivo
        super().__init__(motivo)
