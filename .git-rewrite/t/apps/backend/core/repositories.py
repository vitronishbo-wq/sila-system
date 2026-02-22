"""
Repositórios básicos para o sistema
"""


class UserRepository:
    """Repositório básico de usuários"""

    @staticmethod
    async def get_by_email(email: str):
        """Buscar usuário por email"""
        return None  # Implementação básica


# Instância global
user_repo = UserRepository()
