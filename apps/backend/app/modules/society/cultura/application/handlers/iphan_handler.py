from __future__ import annotations
from app.modules.society.cultura.application.events import BemTombadoEvent

def build_iphan_handler(iphan_adapter):

    async def _handler(event: BemTombadoEvent) -> None:
        await iphan_adapter.registrar_bem_tombado({'bem_id': str(event.bem_id), 'nome': event.nome, 'tipo': event.tipo, 'nivel_tombamento': event.nivel_tombamento})
    return _handler