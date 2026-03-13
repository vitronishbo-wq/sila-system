from fastapi import Request, HTTPException


class SovereignAuthGateway:

    def __init__(self, authenticator, policy_engine):

        self.authenticator = authenticator
        self.policy_engine = policy_engine

    async def protect(

        self,
        request: Request,
        service_name: str,

    ):

        payload = await self.authenticator.authenticate(request)

        roles = payload.get("roles", [])

        allowed = self.policy_engine.authorize(

            service_name,
            roles

        )

        if not allowed:
            raise HTTPException(

                status_code=403,
                detail="access denied"

            )

        return payload
