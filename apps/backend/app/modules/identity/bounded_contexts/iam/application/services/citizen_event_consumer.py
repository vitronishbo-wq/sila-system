from app.domain.bridges.identity_bridge import IdentityBridge


class CitizenEventConsumer:

    def __init__(self, identity_bridge: IdentityBridge):

        self.identity_bridge = identity_bridge

    async def handle_birth_event(

        self,
        citizen_id,
        name,
        birth_date,

    ):

        return await self.identity_bridge.create_identity_from_birth(

            citizen_id=citizen_id,
            name=name,
            birth_date=birth_date,

        )
