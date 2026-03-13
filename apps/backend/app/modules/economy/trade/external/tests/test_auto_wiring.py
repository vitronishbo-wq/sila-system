from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.endpoints import get_endpoint_routers, iter_endpoint_modules
from apps.backend.app.modules.economy.trade.external.api.router import router

def test_auto_wiring_discovery_consistency():
    modules = list(iter_endpoint_modules())
    routers = get_endpoint_routers()
    assert len(modules) == len(routers)
    assert 'agente_carga' in modules
    assert 'cancelamento_radar' in modules
    assert 'despachante' in modules
    assert 'drawback' in modules
    assert 'drawback_externo' in modules
    assert 'drawback_integrado' in modules
    assert 'drawback_interno' in modules
    assert 'drawback_isencao' in modules
    assert 'drawback_restituicao' in modules
    assert 'drawback_substituicao' in modules
    assert 'drawback_suspensao' in modules
    assert 'drawback_verde_amarelo' in modules
    assert 'habilitacao_exportador' in modules
    assert 'habilitacao_importador' in modules
    assert 'habilitacao_radar' in modules
    assert 'radar' in modules
    assert 'siscomex_drawback' in modules
    assert 'suspensao_radar' in modules
    assert 'transportador_internacional' in modules
    assert 'exportadores' in modules
    assert 'importador' in modules

def test_auto_wiring_router_contains_core_routes():
    paths = {item.path for item in router.routes}
    assert any(('/agentes-carga' in path for path in paths))
    assert any(('/cancelamento_radar' in path for path in paths))
    assert any(('/despachantes' in path for path in paths))
    assert any(('/drawback/' in path for path in paths))
    assert any(('/drawback_externo' in path for path in paths))
    assert any(('/drawback_integrado' in path for path in paths))
    assert any(('/drawback_interno' in path for path in paths))
    assert any(('/drawback_isencao' in path for path in paths))
    assert any(('/drawback_restituicao' in path for path in paths))
    assert any(('/drawback_substituicao' in path for path in paths))
    assert any(('/drawback_suspensao' in path for path in paths))
    assert any(('/drawback_verde_amarelo' in path for path in paths))
    assert any(('/habilitacoes-exportador' in path for path in paths))
    assert any(('/habilitacoes-importador' in path for path in paths))
    assert any(('/habilitacao_radar' in path for path in paths))
    assert any(('/radar/' in path for path in paths))
    assert any(('/siscomex_drawback' in path for path in paths))
    assert any(('/suspensao_radar' in path for path in paths))
    assert any(('/transportadores-internacionais' in path for path in paths))
    assert any(('/exportadores' in path for path in paths))
    assert any(('/importadores' in path for path in paths))