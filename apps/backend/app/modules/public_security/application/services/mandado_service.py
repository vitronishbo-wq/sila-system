from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.public_security.application.ports.mandado_repository_port import MandadoRepositoryPort
from apps.backend.app.modules.public_security.application.ports.ocorrencia_repository_port import OcorrenciaRepositoryPort
from apps.backend.app.modules.public_security.application.ports.policial_repository_port import PolicialRepositoryPort
from apps.backend.app.modules.public_security.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.public_security.domain.enums import StatusMandado, TipoMandado
from apps.backend.app.modules.public_security.domain.models.mandado import Mandado

class MandadoService:

    def __init__(self, *, mandado_repo: MandadoRepositoryPort, ocorrencia_repo: OcorrenciaRepositoryPort, policial_repo: PolicialRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.mandado_repo = mandado_repo
        self.ocorrencia_repo = ocorrencia_repo
        self.policial_repo = policial_repo
        self.request_service = request_service

    async def expedir_mandado(self, *, ocorrencia_id: UUID, tipo: TipoMandado, autoridade_judicial: str, data_expedicao: date, data_validade: date, unidade_id: UUID | None=None, policial_responsavel_id: UUID | None=None, observacoes: str | None=None, citizen_id: UUID | None=None) -> Mandado:
        ocorrencia = await self.ocorrencia_repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise ValueError('Ocorrencia nao encontrada para expedicao de mandado')
        if policial_responsavel_id is not None:
            policial = await self.policial_repo.get_by_id(policial_responsavel_id)
            if policial is None:
                raise ValueError('Policial responsavel do mandado nao encontrado')
        numero_mandado = await self.mandado_repo.next_numero()
        mandado = Mandado.expedir(numero_mandado=numero_mandado, ocorrencia_id=ocorrencia_id, tipo=tipo, autoridade_judicial=autoridade_judicial, data_expedicao=data_expedicao, data_validade=data_validade, unidade_id=unidade_id, policial_responsavel_id=policial_responsavel_id, observacoes=observacoes)
        saved = await self.mandado_repo.save(mandado)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='EXPEDICAO_MANDADO', entity_id=saved.id, numero_processo=saved.numero_mandado, citizen_id=citizen_id, metadata={'numero_mandado': saved.numero_mandado, 'tipo': saved.tipo.value, 'ocorrencia_id': str(saved.ocorrencia_id)})
        return saved

    async def buscar_mandado(self, mandado_id: UUID) -> Mandado:
        mandado = await self.mandado_repo.get_by_id(mandado_id)
        if mandado is None:
            raise ValueError('Mandado nao encontrado')
        return mandado

    async def listar_mandados(self, *, ocorrencia_id: UUID | None=None, tipo: TipoMandado | None=None, status: StatusMandado | None=None) -> list[Mandado]:
        if ocorrencia_id is not None:
            return await self.mandado_repo.list_by_ocorrencia(ocorrencia_id)
        if tipo is not None:
            return await self.mandado_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.mandado_repo.list_by_status(status)
        return await self.mandado_repo.list_all()

    async def atualizar_status(self, *, mandado_id: UUID, status: StatusMandado, observacoes: str | None=None) -> Mandado:
        mandado = await self.buscar_mandado(mandado_id)
        mandado.atualizar_status(status, observacoes)
        return await self.mandado_repo.save(mandado)

    async def remover_mandado(self, mandado_id: UUID) -> None:
        deleted = await self.mandado_repo.delete(mandado_id)
        if not deleted:
            raise ValueError('Mandado nao encontrado')