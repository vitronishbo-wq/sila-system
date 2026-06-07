"""Identity module security infrastructure - exports centralized auth components"""

from apps.backend.core.auth import JWTHandler

SovereignJWT = JWTHandler
__all__ = ["SovereignJWT", "JWTHandler"]
