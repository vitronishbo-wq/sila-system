from apps.backend.app.modules.society.cultura.application.events import event_bus
from apps.backend.app.modules.society.cultura.application.handlers.ecad_handler import build_ecad_handler
from apps.backend.app.modules.society.cultura.application.handlers.iphan_handler import build_iphan_handler
from apps.backend.app.modules.society.cultura.application.handlers.minc_handler import build_minc_edital_handler, build_minc_projeto_handler
from apps.backend.app.modules.society.cultura.application.handlers.turismo_handler import build_turismo_handler

def register_handlers(*, iphan_adapter=None, minc_adapter=None, ecad_adapter=None, turismo_adapter=None) -> None:
    if iphan_adapter is not None:
        event_bus.subscribe('BemTombadoEvent', build_iphan_handler(iphan_adapter))
    if minc_adapter is not None:
        event_bus.subscribe('EditalPublicadoEvent', build_minc_edital_handler(minc_adapter))
        event_bus.subscribe('ProjetoAprovadoEvent', build_minc_projeto_handler(minc_adapter))
    if ecad_adapter is not None:
        event_bus.subscribe('EventoProgramadoEvent', build_ecad_handler(ecad_adapter))
    if turismo_adapter is not None:
        event_bus.subscribe('EventoProgramadoEvent', build_turismo_handler(turismo_adapter))
__all__ = ['register_handlers', 'build_iphan_handler', 'build_minc_edital_handler', 'build_minc_projeto_handler', 'build_ecad_handler', 'build_turismo_handler']