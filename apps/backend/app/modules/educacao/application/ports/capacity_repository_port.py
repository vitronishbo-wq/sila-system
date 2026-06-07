from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class CapacityRepositoryPort(ABC):
    """Porta para persistencia de capacidade institucional com lock transacional pessimista.
    
    REGRA CRÍTICA: "Nunca confiar em: capacity_total - capacity_used sem lock transacional"
    Todas as operações de cálculo de disponibilidade DEVEM usar with_for_update().
    """

    @abstractmethod
    async def save(self, capacity_data: dict) -> dict:
        """Salvar registro de capacidade com validação de UNIQUE constraint (institution_id, grade, shift)."""
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter capacidade por UUID."""
        pass

    @abstractmethod
    async def get_by_institution_grade_shift(
        self, institution_id: UUID, grade: str, shift: str, for_update: bool = False
    ) -> dict | None:
        """Obter capacidade específica COM opção de lock pessimista.
        
        CRÍTICO: PASSO 6 - Para operações de reserva, sempre usar for_update=True
        dentro de uma transação explícita para evitar race conditions.
        """
        pass

    @abstractmethod
    async def list_capacities(self, institution_id: UUID) -> list[dict]:
        """Listar todas as capacidades de uma instituição."""
        pass

    @abstractmethod
    async def reserve_capacity(
        self, institution_id: UUID, grade: str, shift: str, quantity: int
    ) -> dict | None:
        """Reservar vagas com lock transacional pessimista.
        
        Usa with_for_update() para garantir atomicidade:
        - Incrementa capacity_reserved
        - Valida: capacity_used + capacity_reserved <= capacity_total
        """
        pass

    @abstractmethod
    async def release_capacity(self, id: UUID, quantity: int) -> dict | None:
        """Liberar vagas reservadas com lock transacional pessimista.
        
        Usa with_for_update() para garantir atomicidade:
        - Decrementa capacity_reserved
        """
        pass

    @abstractmethod
    async def get_available(self, institution_id: UUID, grade: str, shift: str) -> int:
        """Calcular vagas disponíveis COM lock transacional pessimista.
        
        Retorna: capacity_total - capacity_used - capacity_reserved
        DEVE ser chamado dentro de with_for_update() lock.
        """
        pass

    @abstractmethod
    async def update_capacity_used(self, id: UUID, quantity: int) -> dict | None:
        """Incrementar capacity_used com lock pessimista (matrícula finalizada)."""
        pass
