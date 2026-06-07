"""Application services for Booking subdomain"""
from typing import Optional, Any

from .ports import (
    BookingRepositoryPort,
    EnrollmentServicePort,
    VacancyManagementPort,
)


class BookingService:
    """Serviço de aplicação para Booking"""
    
    def __init__(
        self,
        booking_repo: BookingRepositoryPort,
        enrollment: EnrollmentServicePort,
        vacancy: VacancyManagementPort,
    ):
        self.booking_repo = booking_repo
        self.enrollment = enrollment
        self.vacancy = vacancy
    
    async def reserve_vacancy(self, citizen_id: str, opportunity_id: str) -> str:
        """Reservar vaga"""
        # Verificar disponibilidade
        available = await self.vacancy.check_availability(opportunity_id)
        if available <= 0:
            raise ValueError("No vacancies available")
        
        # Reservar vaga
        reserved = await self.vacancy.reserve_vacancy(opportunity_id)
        if not reserved:
            raise ValueError("Failed to reserve vacancy")
        
        # Criar booking
        return await self.booking_repo.create_booking(citizen_id, opportunity_id)
    
    async def get_booking(self, booking_id: str) -> Optional[Any]:
        """Obter detalhes da reserva"""
        return await self.booking_repo.get_booking(booking_id)
    
    async def auto_enroll(self, booking_id: str) -> str:
        """Efetuar pré-matrícula automática"""
        return await self.enrollment.auto_enroll(booking_id)
