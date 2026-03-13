import jwt
from datetime import datetime, timedelta


class SovereignJWT:

    def __init__(self, private_key):

        self.private_key = private_key

    def issue_token(

        self,
        identity_id: str,
        roles: list,

    ):

        payload = {

            "sub": identity_id,
            "roles": roles,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=12),

        }

        token = jwt.encode(
            payload,
            self.private_key,
            algorithm="RS256",
        )

        return token

    def verify(self, token, public_key):

        return jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
        )
