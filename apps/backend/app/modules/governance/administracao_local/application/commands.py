from apps.backend.app.modules.governance.administracao_local.application.dto import CreateAdministradorDTO

class CreateAdministradorCommand:

    def __init__(self, data: CreateAdministradorDTO):
        self.data = data