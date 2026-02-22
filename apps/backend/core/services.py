"""
Serviços básicos para o sistema
"""


class AuthService:
    """Serviço básico de autenticação"""

    @staticmethod
    async def authenticate_user(email: str, password: str):
        """Autenticar usuário - implementação básica"""
        # Esta é uma implementação básica para teste
        return {"user_id": 1, "email": email} if email else None

    @staticmethod
    async def get_current_user(token: str):
        """Obter usuário atual - implementação básica"""
        return {"user_id": 1, "email": "test@example.com"}
