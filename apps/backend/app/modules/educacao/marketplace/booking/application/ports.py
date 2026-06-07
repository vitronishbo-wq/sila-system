"""Domain ports (interfaces) for Booking subdomain"""
from abc import ABC, abstractmethod
from typing import Optional, Any


class BookingRepositoryPort(ABC):
    """Port para acesso a reservas"""
    
    @abstractmethod
    async def create_booking(self, citizen_id: str, opportunity_id: str) -> str:
        """Criar nova reserva"""
        pass
    
    @abstractmethod
    async def get_booking(self, booking_id: str) -> Optional[Any]:
        """Obter detalhes da reserva"""
        pass
    
    @abstractmethod
    async def cancel_booking(self, booking_id: str) -> None:
        """Cancelar reserva"""
        pass


class EnrollmentServicePort(ABC):
    """Port para serviço de matrícula"""
    
    @abstractmethod
    async def auto_enroll(self, booking_id: str) -> str:
        """Efetuar pré-matrícula automática"""
        pass
    
    @abstractmethod
    async def get_enrollment_status(self, enrollment_id: str) -> dict:
        """Obter status de matrícula"""
        pass


class VacancyManagementPort(ABC):
    """Port para gerenciamento de vagas"""
    
    @abstractmethod
    async def check_availability(self, opportunity_id: str) -> int:
        """Verificar vagas disponíveis"""
        pass
    
    @abstractmethod
    async def reserve_vacancy(self, opportunity_id: str) -> bool:
        """Reservar vaga"""
        pass
