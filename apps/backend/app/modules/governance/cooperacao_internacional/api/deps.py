from __future__ import annotations
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.acordo_service import AcordoService
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.projeto_cooperacao_service import ProjetoCooperacaoService
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.visto_service import VistoService
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.adapters.mre_adapter import MREAdapter
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.adapters.onu_adapter import ONUAdapter
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.persistence.outbox import InMemoryOutbox
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.repositories.inmemory_acordo_repository import InMemoryAcordoRepository
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.repositories.inmemory_projeto_repository import InMemoryProjetoCooperacaoRepository
from apps.backend.app.modules.governance.cooperacao_internacional.infrastructure.repositories.inmemory_visto_repository import InMemoryVistoRepository
_acordo_repo = InMemoryAcordoRepository()
_projeto_repo = InMemoryProjetoCooperacaoRepository()
_visto_repo = InMemoryVistoRepository()
_outbox = InMemoryOutbox()
_mre_adapter = MREAdapter()
_onu_adapter = ONUAdapter()
_acordo_service = AcordoService(acordo_repo=_acordo_repo, outbox=_outbox, mre_adapter=_mre_adapter, onu_adapter=_onu_adapter)
_projeto_service = ProjetoCooperacaoService(projeto_repo=_projeto_repo, outbox=_outbox)
_visto_service = VistoService(visto_repo=_visto_repo, outbox=_outbox)

def get_acordo_service() -> AcordoService:
    return _acordo_service

def get_projeto_service() -> ProjetoCooperacaoService:
    return _projeto_service

def get_visto_service() -> VistoService:
    return _visto_service

def get_outbox() -> InMemoryOutbox:
    return _outbox

async def reset_state_for_tests() -> None:
    _acordo_repo._items.clear()
    _projeto_repo._items.clear()
    _visto_repo._items.clear()
    await _outbox.clear()