from app.modules.governance.administracao_local.application.dto import AdministradorDTO

class ListAdministradoresQuery:
    pass

class GetAdministradorByIdQuery:

    def __init__(self, id: str):
        self.id = id