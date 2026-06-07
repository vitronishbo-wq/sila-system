class ListAdministradoresQuery:
    pass


class GetAdministradorByIdQuery:
    def __init__(self, id: str):
        self.id = id
