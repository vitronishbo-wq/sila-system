import uuid


class UserService:

    def __init__(self, repository):

        self.repository = repository

    async def create_user_identity(

        self,
        identity_id: str,
        citizen_id: str,

    ):

        user = {

            "id": str(uuid.uuid4()),
            "identity_id": identity_id,
            "citizen_id": citizen_id,
            "status": "ACTIVE",

        }

        await self.repository.create(user)

        return user
