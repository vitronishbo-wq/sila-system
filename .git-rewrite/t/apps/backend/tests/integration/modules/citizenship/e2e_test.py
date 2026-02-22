"""
Testes de ponta a ponta (E2E) para o módulo de cidadania.

Este script testa o fluxo completo da API de cidadania, incluindo:
1. Autenticação
2. CRUD de cidadãos
3. Validações e mensagens de erro
4. Permissões de acesso
"""

import json
import os
import sys
import uuid
from datetime import date, datetime
from typing import Any, Dict, Optional

import pytest
import requests  # Keep only one requests import
from fastapi import status
from fastapi.testclient import TestClient

# Adiciona o diretório raiz ao path para importações
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
)

# Configuração
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1/citizenship"

# Dados de teste
TEST_USER = {"username": "admin_test", "password": "testpassword123"}


class CitizenshipTestClient:
    """Cliente de teste para a API de cidadania."""

    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.headers = {}

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Realiza uma requisição HTTP."""
        from requests.exceptions import RequestException

        url = f"{self.base_url}{endpoint}"

        # Adiciona headers de autenticação se disponível
        if self.token:
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = f"Bearer {self.token}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=kwargs.get("headers", {}),
                **{k: v for k, v in kwargs.items() if k != "headers"},
            )

            # Tenta fazer o parse da resposta como JSON
            try:
                response_data = response.json()
            except ValueError:
                response_data = {"detail": response.text}

            # Log da requisição e resposta
            print(f"\n{'='*80}")
            print(f"[TEST] {method.upper()} {url}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response_data}")
            print("=" * 80)

            return {"status_code": response.status_code, "data": response_data}

        except RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            return {"status_code": 500, "data": {"detail": f"Request failed: {str(e)}"}}

    def login(self, username: str, password: str) -> bool:
        """Realiza login e armazena o token."""
        endpoint = "/api/v1/auth/login"
        data = {"username": username, "password": password}

        response = self._make_request("POST", endpoint, json=data)

        if response["status_code"] == 200 and "access_token" in response["data"]:
            self.token = response["data"]["access_token"]
            self.headers["Authorization"] = f"Bearer {self.token}"
            return True
        return False

    def create_citizen(self, citizen_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo cidadão."""
        endpoint = f"{API_PREFIX}/citizens/"
        return self._make_request("POST", endpoint, json=citizen_data)

    def get_citizen(self, citizen_id: str) -> Dict[str, Any]:
        """Obtém os dados de um cidadão pelo ID."""
        endpoint = f"{API_PREFIX}/citizens/{citizen_id}"
        return self._make_request("GET", endpoint)

    def update_citizen(
        self, citizen_id: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Atualiza os dados de um cidadão."""
        endpoint = f"{API_PREFIX}/citizens/{citizen_id}"
        return self._make_request("PUT", endpoint, json=update_data)

    def delete_citizen(self, citizen_id: str) -> Dict[str, Any]:
        """Remove um cidadão."""
        endpoint = f"{API_PREFIX}/citizens/{citizen_id}"
        return self._make_request("DELETE", endpoint)

    def search_citizens(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Busca cidadãos com base em critérios."""
        endpoint = f"{API_PREFIX}/citizens/search/"
        return self._make_request("POST", endpoint, json=query)


def run_e2e_tests():
    """Executa os testes de ponta a ponta."""
    print("🚀 Iniciando testes de ponta a ponta para o módulo de cidadania...\n")

    # Cria uma instância do cliente de teste
    client = CitizenshipTestClient()

    # 1. Teste de autenticação
    print("🔐 Testando autenticação...")
    if not client.login(TEST_USER["username"], TEST_USER["password"]):
        print("❌ Falha na autenticação. Verifique as credenciais de teste.")
        return False

    print("✅ Autenticação bem-sucedida!")

    # 2. Teste de criação de cidadão
    print("\n📝 Testando criação de cidadão...")
    citizen_data = {
        "bi_numero": f"TEST-{uuid.uuid4().hex[:8].upper()}",
        "nome_completo": "João da Silva Teste",
        "data_nascimento": "1990-01-15",
        "sexo": "M",
        "estado_civil": "SOLTEIRO",
        "nome_mae": "Maria da Silva",
        "nome_pai": "José da Silva",
        "naturalidade": "Luanda",
        "provincia_nascimento": "Luanda",
        "municipio_nascimento": "Luanda",
        "comuna_nascimento": "Ingombota",
        "pais_nascimento": "Angola",
        "data_emissao": "2020-01-01",
        "data_validade": "2030-01-01",
        "local_emissao": "Luanda",
        "provincia_residencia": "Luanda",
        "municipio_residencia": "Luanda",
        "comuna_residencia": "Ingombota",
        "bairro_residencia": "Maianga",
        "rua_residencia": "Rua da Samba",
        "casa_residencia": "123",
        "telefone_principal": "912345678",
        "telefone_alternativo": "923456789",
        "email": f"teste.{uuid.uuid4().hex[:8]}@exemplo.com",
        "estado": "ATIVO",
    }

    create_response = client.create_citizen(citizen_data)

    if create_response["status_code"] != 201:
        print(f"❌ Falha ao criar cidadão: {create_response['data']}")
        return False

    citizen_id = create_response["data"].get("id")
    if not citizen_id:
        print("❌ ID do cidadão não retornado na criação")
        return False

    print(f"✅ Cidadão criado com sucesso! ID: {citizen_id}")

    # 3. Teste de leitura de cidadão
    print("\n📖 Testando leitura de cidadão...")
    get_response = client.get_citizen(citizen_id)

    if get_response["status_code"] != 200:
        print(f"❌ Falha ao obter cidadão: {get_response['data']}")
        return False

    print(f"✅ Dados do cidadão obtidos com sucesso!")
    print(f"   Nome: {get_response['data']['nome_completo']}")
    print(f"   BI: {get_response['data']['bi_numero']}")

    # 4. Teste de atualização de cidadão
    print("\n✏️ Testando atualização de cidadão...")
    update_data = {
        "nome_completo": "João da Silva Teste Atualizado",
        "telefone_principal": "912345679",
        "email": f"atualizado.{uuid.uuid4().hex[:8]}@exemplo.com",
    }

    update_response = client.update_citizen(citizen_id, update_data)

    if update_response["status_code"] != 200:
        print(f"❌ Falha ao atualizar cidadão: {update_response['data']}")
        return False

    # Verifica se os dados foram atualizados
    get_updated = client.get_citizen(citizen_id)
    if (
        get_updated["status_code"] != 200
        or get_updated["data"]["nome_completo"] != update_data["nome_completo"]
    ):
        print("❌ Dados do cidadão não foram atualizados corretamente")
        return False

    print(f"✅ Cidadão atualizado com sucesso!")
    print(f"   Novo nome: {get_updated['data']['nome_completo']}")

    # 5. Teste de busca de cidadãos
    print("\n🔍 Testando busca de cidadãos...")
    search_query = {"nome_completo": "João", "page": 1, "page_size": 10}

    search_response = client.search_citizens(search_query)

    if search_response["status_code"] != 200 or "items" not in search_response["data"]:
        print(f"❌ Falha na busca de cidadãos: {search_response['data']}")
        return False

    print(f"✅ Busca de cidadãos realizada com sucesso!")
    print(f"   Total de itens encontrados: {search_response['data'].get('total', 0)}")

    # 6. Teste de exclusão de cidadão
    print("\n🗑️ Testando exclusão de cidadão...")
    delete_response = client.delete_citizen(citizen_id)

    if delete_response["status_code"] != 200:
        print(f"❌ Falha ao excluir cidadão: {delete_response['data']}")
        return False

    # Verifica se o cidadão foi realmente excluído
    get_deleted = client.get_citizen(citizen_id)
    if get_deleted["status_code"] != 404:
        print("❌ Cidadão não foi excluído corretamente")
        return False

    print("✅ Cidadão excluído com sucesso!")

    # 7. Teste de validação de dados inválidos
    print("\n⚠️ Testando validação de dados inválidos...")
    invalid_data = {
        "bi_numero": "",  # BI vazio
        "nome_completo": "",  # Nome vazio
        "data_nascimento": "data-invalida",
    }

    invalid_response = client.create_citizen(invalid_data)

    if invalid_response["status_code"] != 422:  # 422 Unprocessable Entity
        print(f"❌ Validação de dados inválidos falhou: {invalid_response['data']}")
        return False

    print("✅ Validação de dados inválidos funcionando corretamente!")

    # 8. Teste de permissões
    print("\n🔒 Testando controle de acesso não autorizado...")
    # Cria um novo cliente sem autenticação
    unauthorized_client = CitizenshipTestClient()

    # Tenta acessar um recurso protegido sem autenticação
    protected_response = unauthorized_client.get_citizen("123")

    if protected_response["status_code"] != 401:  # 401 Unauthorized
        print(
            f"❌ Controle de acesso não autorizado falhou: {protected_response['data']}"
        )
        return False

    print("✅ Controle de acesso não autorizado funcionando corretamente!")

    print("\n🎉 Todos os testes de ponta a ponta foram concluídos com sucesso!")
    return True


if __name__ == "__main__":
    # Instala as dependências necessárias se não estiverem disponíveis
    try:
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    except ImportError:
        print("Instalando dependências necessárias...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

    # Executa os testes
    success = run_e2e_tests()

    # Retorna código de saída apropriado
    sys.exit(0 if success else 1)
