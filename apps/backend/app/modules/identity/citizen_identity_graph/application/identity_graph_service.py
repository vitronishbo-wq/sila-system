class IdentityGraphService:

    def __init__(self, repository):
        self.repository = repository

    async def create_citizen_node(

        self,
        identity_id: str,
        citizen_id: str,
        name: str,
        birth_date: str,

    ):

        node = {

            "identity_id": identity_id,
            "citizen_id": citizen_id,
            "name": name,
            "birth_date": birth_date,

        }

        await self.repository.save(node)

        return node
