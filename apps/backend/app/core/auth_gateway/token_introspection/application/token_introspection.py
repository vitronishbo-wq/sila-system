import jwt


class TokenIntrospection:

    def __init__(self, public_key):

        self.public_key = public_key

    def verify(self, token):

        try:

            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"],
            )

            return payload

        except Exception:

            return None
