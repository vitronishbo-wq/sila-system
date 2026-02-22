"""
Inicialização do pacote 'modules'.
Este arquivo contém a função de descoberta de routers (get_module_routers)
que é importada e utilizada no backend/main.py.
"""

import os
import importlib
import logging
from typing import List, Tuple

logger = logging.getLogger("sila-backend.modules")


def get_module_routers() -> List[Tuple[str, "APIRouter"]]:
    """
    Descobre e importa automaticamente todos os routers definidos em subdiretórios
    do pacote 'modules'. Assume que cada subdiretório (módulo) tem um arquivo
    'router.py' que expõe uma variável 'router' do tipo APIRouter.

    Retorna:
        Uma lista de tuplas contendo (nome_do_modulo, APIRouter).
    """
    # Import APIRouter only when this function is called
    try:
        from fastapi import APIRouter
    except ImportError:
        logger.warning("FastAPI not available, returning empty routers list")
        return []

    routers: List[Tuple[str, APIRouter]] = []

    # O diretório atual é /opt/sila-system/backend/modules
    # A variável __file__ é o caminho para este __init__.py
    current_dir = os.path.dirname(__file__)

    # Itera sobre todos os itens no diretório 'modules'
    for item_name in os.listdir(current_dir):
        module_path = os.path.join(current_dir, item_name)

        # 1. Verifica se é um diretório e não é 'cache' ou '__pycache__'
        if os.path.isdir(module_path) and not item_name.startswith("__"):

            # Tenta encontrar router.py primeiro, depois endpoints.py
            router_file_path = os.path.join(module_path, "router.py")
            endpoints_file_path = os.path.join(module_path, "endpoints.py")

            router_file = None
            import_path = None

            if os.path.exists(router_file_path):
                router_file = "router"
                import_path = f"modules.{item_name}.router"
            elif os.path.exists(endpoints_file_path):
                router_file = "endpoints"
                import_path = f"modules.{item_name}.endpoints"

            # 2. Verifica se encontrou algum arquivo de router
            if router_file and import_path:
                module_name = item_name

                try:
                    # Importa o módulo dinamicamente
                    module = importlib.import_module(import_path)

                    # 3. Verifica se o router está presente
                    if hasattr(module, "router") and isinstance(
                        module.router, APIRouter
                    ):
                        routers.append((module_name, module.router))
                        logger.info(
                            f"Router encontrado e registrado: {module_name} (via {router_file}.py)"
                        )
                    else:
                        logger.warning(
                            f"O módulo '{module_name}' foi encontrado, mas '{router_file}.py' não expõe uma variável 'router' válida."
                        )

                except ImportError as e:
                    logger.error(
                        f"Erro ao importar router para o módulo '{module_name}' em '{import_path}': {e}"
                    )
                except Exception as e:
                    logger.error(
                        f"Erro desconhecido ao processar o módulo '{module_name}': {e}"
                    )
            else:
                logger.debug(
                    f"Módulo '{item_name}' não possui router.py nem endpoints.py"
                )

    # Debugging: Print discovered routers
    print("Discovered routers:", routers)
    logger.info(f"Discovered routers: {routers}")

    return routers


# Adiciona um router de exemplo, pois o sistema precisa de pelo menos um
# para registrar no main.py (e para confirmar que a descoberta funciona).
try:
    from fastapi import APIRouter

    example_router = APIRouter()

    @example_router.get(
        "/status", tags=["Example"], summary="Status do Módulo de Exemplo"
    )
    async def module_status():
        return {"module": "modules/__init__", "status": "operational"}

except ImportError:
    example_router = None


# Esta função é exportada e utilizada em backend.main
__all__ = ["get_module_routers"]
