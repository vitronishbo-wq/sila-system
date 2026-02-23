from abc import ABC, abstractmethod


class PasswordHasherPort(ABC):
    """Interface para hashing de senhas"""
    
    @abstractmethod
    def hash(self, password: str) -> str:
        """Gera hash da senha"""
        pass
    
    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Verifica se senha corresponde ao hash"""
        pass
    
    @abstractmethod
    def needs_rehash(self, password_hash: str) -> bool:
        """Verifica se hash precisa ser atualizado"""
        pass


class TokenProviderPort(ABC):
    """Interface para geração/validação de JWT"""
    
    @abstractmethod
    def create_access_token(self, user_id: str, roles: list, permissions: list) -> str:
        """Gera access token"""
        pass
    
    @abstractmethod
    def create_refresh_token(self, user_id: str) -> str:
        """Gera refresh token"""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """Verifica e decodifica token"""
        pass
    
    @abstractmethod
    def get_user_id_from_token(self, token: str) -> str:
        """Extrai user_id do token"""
        pass
