"""
🚀 Teste de Bootstrap da Aplicação FastAPI

Verifica se a aplicação FastAPI inicializa completamente, carregando todas as
rotas, dependências e middlewares sem erros.
"""

import os
import sys

import pytest
from fastapi.testclient import TestClient

# Adiciona o diretório backend ao sys.path para que `app.main` possa ser encontrado
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
)


def test_app_bootstrap():
    """
    Tenta inicializar a aplicação FastAPI e criar um cliente de teste.
    Uma falha aqui indica um problema na inicialização da aplicação, como
    dependências ausentes, erros de sintaxe ou problemas na configuração de rotas.
    """
    try:
        from app.main import (  # Importação tardia para capturar erros de inicialização
            app,
        )

        client = TestClient(app)
        assert client is not None
        print("\n✅ Aplicação FastAPI inicializada com sucesso!")

        # Opcional: Fazer uma requisição a um endpoint básico para garantir que está respondendo
        # A maioria das apps FastAPI tem /docs (Swagger UI)
        response = client.get("/docs")
        assert (
            response.status_code == 200
        ), f"Endpoint /docs retornou {response.status_code}"
        print("✅ Endpoint /docs acessível e respondendo corretamente.")

    except ImportError as e:
        pytest.fail(
            f"❌ Falha de importação ao inicializar a aplicação FastAPI. Verifique se o arquivo 'backend/app/main.py' e a variável 'app' existem. Erro: {e}",
            pytrace=True,
        )
    except Exception as e:
        pytest.fail(
            f"❌ Falha geral ao inicializar a aplicação FastAPI: {e}", pytrace=True
        )
