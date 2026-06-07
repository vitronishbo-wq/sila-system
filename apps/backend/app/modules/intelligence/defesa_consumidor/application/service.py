class DefesaConsumidorService:
    """Application service entrypoint for module use cases."""

    def __init__(self, reclamacao_service):
        self.reclamacoes = reclamacao_service
