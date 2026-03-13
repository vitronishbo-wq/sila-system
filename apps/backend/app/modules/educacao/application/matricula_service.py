from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from app.modules.educacao.application.ports import EscolaRepositoryPort, MatriculaRepositoryPort, TurmaRepositoryPort
from app.modules.educacao.domain.models import CicloEnsino, Matricula, StatusMatricula
from app.modules.educacao.exceptions import CitizenNotFoundError, IdadeMinimaNaoAtendidaError, EscolaNotFoundError, InvalidMatriculaStateError, MatriculaAlreadyExistsError, TurmaNotFoundError, TurmaSemVagasError

class MatriculaService:
    """Service de matricula escolar integrando nucleo de identidade e tracking."""

    def __init__(self, matricula_repo: MatriculaRepositoryPort, turma_repo: TurmaRepositoryPort, escola_repo: EscolaRepositoryPort, citizen_repo: CitizenRepositoryPort, request_service: ServiceRequestLifecycleBridge):
        self.matricula_repo = matricula_repo
        self.turma_repo = turma_repo
        self.escola_repo = escola_repo
        self.citizen_repo = citizen_repo
        self.request_service = request_service

    async def criar_matricula(self, *, citizen_id: UUID, escola_id: UUID, turma_id: UUID, ano_letivo_id: UUID, observacoes: Optional[str]=None) -> Matricula:
        citizen = await self.citizen_repo.get_by_id(citizen_id)
        if not citizen:
            raise CitizenNotFoundError(f'Cidadao {citizen_id} nao encontrado')
        escola = await self.escola_repo.get_by_id(escola_id)
        if not escola:
            raise EscolaNotFoundError(f'Escola {escola_id} nao encontrada')
        turma = await self.turma_repo.get_by_id(turma_id)
        if not turma:
            raise TurmaNotFoundError(f'Turma {turma_id} nao encontrada')
        if not turma.ativa:
            raise InvalidMatriculaStateError('Turma informada esta inativa')
        if turma.escola_id != escola_id:
            raise InvalidMatriculaStateError('Turma nao pertence a escola informada')
        if turma.ano_letivo_id != ano_letivo_id:
            raise InvalidMatriculaStateError('Turma nao pertence ao ano letivo informado')
        ocupacao_turma = await self.turma_repo.count_matriculas_ativas(turma_id, ano_letivo_id)
        if ocupacao_turma >= turma.capacidade:
            raise TurmaSemVagasError('Turma sem vagas disponiveis')
        nascimento = getattr(citizen, 'birth_date', None)
        if nascimento is None:
            raise IdadeMinimaNaoAtendidaError('Cidadao sem data de nascimento para validacao de idade minima')
        idade_minima = self._idade_minima_para_contexto(classe=turma.classe, ciclos=escola.ciclos)
        idade_cidadao = self._calcular_idade(nascimento, date.today())
        if idade_cidadao < idade_minima:
            raise IdadeMinimaNaoAtendidaError(f'Idade minima nao atendida para a turma: minimo {idade_minima}, atual {idade_cidadao}')
        exists = await self.matricula_repo.exists_active_for_citizen(citizen_id, ano_letivo_id)
        if exists:
            raise MatriculaAlreadyExistsError('Cidadao ja possui matricula ativa/pendente no ano letivo informado')
        ano_atual = date.today().year
        numero_processo = await self.matricula_repo.next_numero_processo(ano_atual, escola_id)
        matricula = Matricula(id=uuid4(), numero_processo=numero_processo, citizen_id=citizen_id, escola_id=escola_id, turma_id=turma_id, ano_letivo_id=ano_letivo_id, data_matricula=date.today(), status=StatusMatricula.PENDENTE, observacoes=observacoes)
        saved = await self.matricula_repo.save(matricula)
        await self.request_service.create_education_request(entity_id=saved.id, citizen_id=citizen_id, numero_processo=numero_processo, escola_nome=escola.nome, ano_letivo=str(ano_letivo_id))
        return saved

    async def ativar_matricula(self, matricula_id: UUID) -> Matricula:
        matricula = await self.matricula_repo.get_by_id(matricula_id)
        if not matricula:
            raise InvalidMatriculaStateError('Matricula nao encontrada')
        try:
            matricula.ativar()
        except ValueError as exc:
            raise InvalidMatriculaStateError(str(exc)) from exc
        updated = await self.matricula_repo.save(matricula)
        await self.request_service.mark_education_request_completed(entity_id=matricula_id, actor_id=updated.citizen_id, metadata={'ativacao_data': date.today().isoformat()})
        return updated

    async def listar_por_cidadao(self, citizen_id: UUID, ano_letivo_id: Optional[UUID]=None) -> list[Matricula]:
        return await self.matricula_repo.get_by_citizen(citizen_id, ano_letivo_id)

    @staticmethod
    def _calcular_idade(nascimento: date, referencia: date) -> int:
        return referencia.year - nascimento.year - ((referencia.month, referencia.day) < (nascimento.month, nascimento.day))

    @staticmethod
    def _idade_minima_por_classe(classe: str) -> int | None:
        digitos = ''.join((ch for ch in classe or '' if ch.isdigit()))
        if not digitos:
            return None
        numero = int(digitos)
        if numero <= 6:
            return 6
        if numero <= 9:
            return 12
        return 15

    @staticmethod
    def _idade_minima_por_ciclo(ciclos: list[CicloEnsino]) -> int:
        base = {CicloEnsino.PRE_ESCOLAR: 4, CicloEnsino.PRIMARIO: 6, CicloEnsino.SECUNDARIO_1: 12, CicloEnsino.SECUNDARIO_2: 15, CicloEnsino.TECNICO: 15, CicloEnsino.FORMACAO: 15}
        if not ciclos:
            return 6
        return min((base.get(c, 6) for c in ciclos))

    def _idade_minima_para_contexto(self, *, classe: str, ciclos: list[CicloEnsino]) -> int:
        idade_por_classe = self._idade_minima_por_classe(classe)
        if idade_por_classe is not None:
            return idade_por_classe
        return self._idade_minima_por_ciclo(ciclos)
