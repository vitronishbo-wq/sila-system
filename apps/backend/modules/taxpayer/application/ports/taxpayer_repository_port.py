from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from uuid import UUID
from datetime import date

from ...domain.entities.taxpayer import Taxpayer
from ...domain.value_objects.nif import NIF


class TaxpayerRepositoryPort(ABC):
    """Interface do repositório de contribuintes"""
    
    # Taxpayer operations
    @abstractmethod
    async def save(self, taxpayer: Taxpayer) -> Taxpayer:
        """Salva um contribuinte"""
        pass
    
    @abstractmethod
    async def find_by_id(self, taxpayer_id: UUID) -> Optional[Taxpayer]:
        """Busca contribuinte por ID"""
        pass
    
    @abstractmethod
    async def find_by_nif(self, nif: str) -> Optional[Taxpayer]:
        """Busca contribuinte por NIF"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Taxpayer]:
        """Busca contribuinte por email"""
        pass
    
    @abstractmethod
    async def find_by_phone(self, phone: str) -> Optional[Taxpayer]:
        """Busca contribuinte por telefone"""
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100, filters: dict = None) -> Tuple[List[Taxpayer], int]:
        """Lista todos os contribuintes com paginação"""
        pass
    
    @abstractmethod
    async def update_status(self, taxpayer_id: UUID, status: str, updated_by: UUID) -> Optional[Taxpayer]:
        """Atualiza status do contribuinte"""
        pass
    
    # Declaration operations
    @abstractmethod
    async def save_declaration(self, declaration) -> None:
        """Salva uma declaração"""
        pass
    
    @abstractmethod
    async def find_declaration_by_id(self, declaration_id: UUID) -> Optional[object]:
        """Busca declaração por ID"""
        pass
    
    @abstractmethod
    async def find_declaration_by_number(self, declaration_number: str) -> Optional[object]:
        """Busca declaração por número"""
        pass
    
    @abstractmethod
    async def find_declarations_by_taxpayer(self, taxpayer_id: UUID, year: Optional[int] = None,
                                      skip: int = 0, limit: int = 100) -> Tuple[List[object], int]:
        """Busca declarações de um contribuinte"""
        pass
    
    @abstractmethod
    async def find_declarations_by_period(self, tax_type: str, year: int, month: Optional[int] = None) -> List[object]:
        """Busca declarações por período"""
        pass
    
    @abstractmethod
    async def update_declaration_status(self, declaration_id: UUID, status: str, processed_by: Optional[UUID] = None) -> Optional[object]:
        """Atualiza status da declaração"""
        pass
    
    # Debt operations
    @abstractmethod
    async def save_debt(self, debt) -> None:
        """Salva uma dívida"""
        pass
    
    @abstractmethod
    async def find_debt_by_id(self, debt_id: UUID) -> Optional[object]:
        """Busca dívida por ID"""
        pass
    
    @abstractmethod
    async def find_debt_by_number(self, debt_number: str) -> Optional[object]:
        """Busca dívida por número"""
        pass
    
    @abstractmethod
    async def find_debts_by_taxpayer(self, taxpayer_id: UUID, include_paid: bool = False,
                               skip: int = 0, limit: int = 100) -> Tuple[List[object], int]:
        """Busca dívidas de um contribuinte"""
        pass
    
    @abstractmethod
    async def find_overdue_debts(self, reference_date: Optional[date] = None) -> List[object]:
        """Busca dívidas vencidas"""
        pass
    
    @abstractmethod
    async def update_debt_after_payment(self, debt_id: UUID, payment_amount: float) -> Optional[object]:
        """Atualiza dívida após pagamento"""
        pass
    
    # Payment operations
    @abstractmethod
    async def save_payment(self, payment) -> None:
        """Salva um pagamento"""
        pass
    
    @abstractmethod
    async def find_payment_by_id(self, payment_id: UUID) -> Optional[object]:
        """Busca pagamento por ID"""
        pass
    
    @abstractmethod
    async def find_payment_by_number(self, payment_number: str) -> Optional[object]:
        """Busca pagamento por número"""
        pass
    
    @abstractmethod
    async def find_payments_by_taxpayer(self, taxpayer_id: UUID, skip: int = 0, limit: int = 100) -> Tuple[List[object], int]:
        """Busca pagamentos de um contribuinte"""
        pass
    
    @abstractmethod
    async def find_payments_by_debt(self, debt_id: UUID) -> List[object]:
        """Busca pagamentos de uma dívida"""
        pass
    
    # Certificate operations
    @abstractmethod
    async def save_certificate(self, certificate) -> None:
        """Salva um certificado"""
        pass
    
    @abstractmethod
    async def find_certificate_by_id(self, certificate_id: UUID) -> Optional[object]:
        """Busca certificado por ID"""
        pass
    
    @abstractmethod
    async def find_certificate_by_number(self, certificate_number: str) -> Optional[object]:
        """Busca certificado por número"""
        pass
    
    @abstractmethod
    async def find_certificates_by_taxpayer(self, taxpayer_id: UUID, certificate_type: Optional[str] = None,
                                      skip: int = 0, limit: int = 100) -> Tuple[List[object], int]:
        """Busca certificados de um contribuinte"""
        pass
    
    @abstractmethod
    async def find_valid_certificate(self, taxpayer_id: UUID, certificate_type: str) -> Optional[object]:
        """Busca certificado válido"""
        pass
