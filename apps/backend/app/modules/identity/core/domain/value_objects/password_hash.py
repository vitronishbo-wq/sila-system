import bcrypt


class PasswordHash:
    """Password hash value object for secure credential storage"""

    def __init__(self, hashed: bytes):
        self.hashed = hashed

    @classmethod
    def create(cls, password: str):
        """Create a new password hash from plaintext"""
        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )
        return cls(hashed)

    def verify(self, password: str) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(
            password.encode(),
            self.hashed
        )
