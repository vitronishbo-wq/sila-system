from fastapi import Request, HTTPException


class RequestAuthenticator:

    def __init__(self, token_service):

        self.token_service = token_service

    async def authenticate(self, request: Request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(status_code=401, detail="missing token")

        token = auth_header.replace("Bearer ", "")

        payload = self.token_service.verify(token)

        if not payload:
            raise HTTPException(status_code=401, detail="invalid token")

        return payload
