class CitizenBaseError(Exception):
    """Exceção base para o módulo Citizen."""
    pass


class CitizenValidationError(CitizenBaseError):
    """Lançada quando a validação do cidadão falha (ex: status inválido, FUC rejeitado)."""

    def __init__(self, message: str, citizen_id: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.message = message
        self.citizen_id = citizen_id
        super().__init__(self.message)


class CitizenNotFoundError(CitizenBaseError):
    """Lançada quando o cidadão não existe no repositório de projeções ou na API FUC."""

    def __init__(self, citizen_id: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.citizen_id = citizen_id
        self.message = f"Cidadão '{citizen_id}' não localizado no Ficheiro Único do Cidadão."
        super().__init__(self.message)
