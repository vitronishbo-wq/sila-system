"""
PASSO 6 — LOCK CONCORRENTE REAL

Serviço de matrícula com transação ACID e lock pessimista.

REGRA CRÍTICA:
    SELECT ... FOR UPDATE é OBRIGATÓRIO em TODAS as operações de reserva.
    Sem isso: race condition → overbooking → corrupção acadêmica

Padrão Seguro:
    async with session.begin():
        # 1. Lock pessimista na capacidade
        capacity = await reserve_with_lock(...)
        
        # 2. Criar matrícula dentro da mesma transação
        enrollment = await create_enrollment(...)
        
        # 3. Commit automático ou rollback em erro
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.repositories import (
    SQLAlchemyAcademicIdentityRepository,
    SQLAlchemyCapacityRepository,
    SQLAlchemyEnrollmentRepository,
)


class EnrollmentTransactionService:
    """Serviço de matrícula com garantias ACID e lock transacional."""

    def __init__(
        self,
        session: AsyncSession,
        identity_repo: SQLAlchemyAcademicIdentityRepository,
        capacity_repo: SQLAlchemyCapacityRepository,
        enrollment_repo: SQLAlchemyEnrollmentRepository,
    ):
        self.session = session
        self.identity_repo = identity_repo
        self.capacity_repo = capacity_repo
        self.enrollment_repo = enrollment_repo

    async def enroll_student_with_lock(
        self,
        student_id: UUID,
        institution_id: UUID,
        grade: str,
        shift: str,
        academic_year: str,
        quantity: int = 1,
    ) -> dict:
        """
        Matricular estudante com lock pessimista na capacidade.

        Fluxo Atômico:
        1. Verificar identidade acadêmica (sem lock)
        2. SELECT capacity FOR UPDATE (lock pessimista) ← CRÍTICO
        3. Validar disponibilidade
        4. Incrementar capacity_reserved
        5. Criar registro de enrollment
        6. Commit transação completa
        
        Se qualquer passo falhar, tudo é rolled back.
        
        Protege contra:
        - ✅ Race condition: 2 processes vendo mesma vaga
        - ✅ Overbooking: Matriz com mais alunos que capacidade
        - ✅ Corrupção: Dados inconsistentes entre capacity e enrollment
        """

        # Iniciar transação explícita
        async with self.session.begin():
            # PASSO 1: Verificar identidade (leitura sem lock)
            identity = await self.identity_repo.get_by_id(student_id)
            if not identity:
                raise ValueError(f"Identidade {student_id} não encontrada")

            # PASSO 2: LOCK PESSIMISTA na capacidade
            # ⚠️  SEM WITH_FOR_UPDATE = VULNERABILITY
            capacity = await self.capacity_repo.reserve_capacity(
                institution_id=institution_id,
                grade=grade,
                shift=shift,
                quantity=quantity,
            )

            if capacity is None:
                raise ValueError(
                    f"Sem vagas disponíveis: {institution_id}/{grade}/{shift}"
                )

            # PASSO 3: Criar matrícula dentro da mesma transação
            enrollment_data = {
                "id": uuid4(),
                "student_id": student_id,
                "institution_id": institution_id,
                "academic_year": academic_year,
                "grade": grade,
                "status": "ACTIVE",
                "started_at": datetime.utcnow(),
                "ended_at": None,
                "transfer_origin_id": None,
                "transfer_destination_id": None,
            }

            enrollment = await self.enrollment_repo.save(enrollment_data)

            # PASSO 4: Commit automático ao sair do bloco 'async with'
            # Se houver erro, rollback automático

            return {
                "enrollment": enrollment,
                "capacity_after_reserve": capacity,
                "lock_status": "LOCKED_PESSIMISTIC_FOR_UPDATE",
            }

    async def enroll_batch_with_distributed_locks(
        self,
        student_enrollments: list[dict],
    ) -> dict:
        """
        Matricular lote de estudantes com locks distribuídos.

        Cada instituição/grade/shift é locked independentemente.
        Múltiplas matrículas podem proceder em paralelo se forem
        em capacidades diferentes.

        Exemplo entrada:
        [
            {
                "student_id": UUID,
                "institution_id": UUID,
                "grade": "5A",
                "shift": "MORNING",
                "academic_year": "2026",
            },
            ...
        ]
        """
        results = []
        errors = []

        async with self.session.begin():
            for enroll in student_enrollments:
                try:
                    result = await self.enroll_student_with_lock(
                        student_id=enroll["student_id"],
                        institution_id=enroll["institution_id"],
                        grade=enroll["grade"],
                        shift=enroll["shift"],
                        academic_year=enroll["academic_year"],
                    )
                    results.append(result)
                except Exception as e:
                    errors.append({"enrollment": enroll, "error": str(e)})
                    # Rollback toda a transação se um item falhar
                    raise

        return {
            "enrolled": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors,
        }

    async def check_capacity_availability(
        self,
        institution_id: UUID,
        grade: str,
        shift: str,
    ) -> dict:
        """
        Consultar disponibilidade de vagas COM lock pessimista.

        ⚠️ IMPORTANTE:
        Este método também usa FOR UPDATE para garantir que
        o resultado é valido para operações subsequentes.
        Sem lock, o valor pode estar obsoleto antes de usar.
        """
        async with self.session.begin():
            available = await self.capacity_repo.get_available(
                institution_id=institution_id,
                grade=grade,
                shift=shift,
            )

            return {
                "institution_id": institution_id,
                "grade": grade,
                "shift": shift,
                "available_spots": available,
                "query_locked": True,  # Com FOR UPDATE
                "safe_for_enrollment": available > 0,
            }

    async def release_reserved_capacity(
        self,
        capacity_id: UUID,
        quantity: int = 1,
    ) -> dict:
        """Liberar vagas reservadas (cancelamento de matrícula)."""
        async with self.session.begin():
            result = await self.capacity_repo.release_capacity(
                id=capacity_id,
                quantity=quantity,
            )

            if result is None:
                raise ValueError(f"Capacidade {capacity_id} não encontrada")

            return {
                "capacity_id": capacity_id,
                "released": quantity,
                "capacity_after_release": result,
            }


# ============================================================================
# EXEMPLO DE USO SEGURO
# ============================================================================

async def exemplo_matricula_segura():
    """
    Exemplo: Como usar corretamente o padrão de lock pessimista.
    
    Este exemplo FUNCIONA porque usa:
    1. async with session.begin() - transação explícita
    2. reserve_capacity() - que usa with_for_update()
    3. Tudo é atômico: sucesso completo ou falha completa
    """
    # Pseudocódigo (não executável)
    # service = EnrollmentTransactionService(session, repos...)
    # 
    # try:
    #     result = await service.enroll_student_with_lock(
    #         student_id=uuid.uuid4(),
    #         institution_id=uuid.uuid4(),
    #         grade="5A",
    #         shift="MORNING",
    #         academic_year="2026",
    #     )
    #     print(f"✅ Matriculado com sucesso: {result['enrollment']}")
    # except ValueError as e:
    #     print(f"❌ Erro: {e}")  # Sem vagas, identidade inválida, etc.
    pass


# ============================================================================
# EXPLICAÇÃO DA REGRA CRÍTICA
# ============================================================================

"""
SEM FOR UPDATE (❌ ERRADO):
    1. Process A: SELECT capacity WHERE id=123
       → Result: capacity_total=30, capacity_used=28, capacity_reserved=0
    2. Process B: SELECT capacity WHERE id=123
       → Result: capacity_total=30, capacity_used=28, capacity_reserved=0
    3. Process A: available = 30 - 28 - 0 = 2 ✓ UPDATE capacity_reserved = 1
    4. Process B: available = 30 - 28 - 0 = 2 ✓ UPDATE capacity_reserved = 1
    5. RESULTADO: capacity_reserved = 1 (ERRADO! Deveria ser 2)
       → Overbooking: 30 vagas, mas 29+1+1 = 31 alocadas!

COM FOR UPDATE (✅ CORRETO):
    1. Process A: SELECT capacity WHERE id=123 FOR UPDATE
       → Lock adquirido, wait time = ~0ms
    2. Process B: SELECT capacity WHERE id=123 FOR UPDATE
       → Lock aguardando Process A (bloqueado)
    3. Process A: available = 30 - 28 - 0 = 2 ✓ UPDATE capacity_reserved = 1
       → COMMIT, lock liberado
    4. Process B: SELECT capacity WHERE id=123 FOR UPDATE (agora desbloqueado)
       → Result: capacity_total=30, capacity_used=28, capacity_reserved=1
    5. Process B: available = 30 - 28 - 1 = 1 ✓ UPDATE capacity_reserved = 2
    6. RESULTADO: capacity_reserved = 2 ✓ CORRETO!
       → Nenhum overbooking, dados consistentes
"""
