from __future__ import annotations
from app.modules.society.cultura.application.events import EditalPublicadoEvent, ProjetoAprovadoEvent

def build_minc_edital_handler(minc_adapter):

    async def _handler(event: EditalPublicadoEvent) -> None:
        await minc_adapter.publicar_edital({'edital_id': str(event.edital_id), 'numero': event.numero, 'titulo': event.titulo, 'tipo': event.tipo, 'valor_total': event.valor_total})
    return _handler

def build_minc_projeto_handler(minc_adapter):

    async def _handler(event: ProjetoAprovadoEvent) -> None:
        await minc_adapter.reportar_execucao_projeto({'projeto_id': str(event.projeto_id), 'codigo_projeto': event.codigo_projeto, 'titulo': event.titulo, 'proponente': event.proponente, 'valor_aprovado': event.valor_aprovado})
    return _handler