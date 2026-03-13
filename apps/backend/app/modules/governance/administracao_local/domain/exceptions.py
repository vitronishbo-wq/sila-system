class AdministracaoLocalException(Exception):
    """Base exception for the module"""
    pass

class AdministradorNaoEncontrado(AdministracaoLocalException):

    def __init__(self, admin_id: str):
        self.admin_id = admin_id
        super().__init__(f'Administrador com ID {admin_id} não encontrado')