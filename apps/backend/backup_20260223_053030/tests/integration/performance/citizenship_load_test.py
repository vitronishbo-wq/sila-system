# tests/integration/performance/citizenship_load_test.py
"""
Testes de carga Locust para o módulo Citizenship.

Executar:
  locust -f citizenship_load_test.py --host=http://localhost:8000
  Acesse http://localhost:8089 para interface web.
"""

from locust import HttpUser, between, task

from faker import Faker
from core.config.settings import settings  # Carrega .env automaticamente

fake = Faker("pt_PT")  # Locale Angola/Portugal para nomes realistas

BASE_PATH = "/citizenship"
ADMIN_EMAIL = settings.ADMIN_EMAIL
ADMIN_PASSWORD = settings.ADMIN_PASSWORD


class AuthMixin:
    """Mixin para autenticação JWT."""

    def login(self):
        response = self.client.post(
            "/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        )
        if response.ok:
            return response.json()["access_token"]
        return None

    def auth_headers(self, token: str) -> dict:
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


class CitizenUser(HttpUser, AuthMixin):
    """Usuário simulando operações de cidadãos (cidadania)."""
    wait_time = between(1, 5)

    def on_start(self):
        token = self.login()
        if not token:
            self.environment.runner.quit()
        self.headers = self.auth_headers(token)

    @task(4)
    def list_citizens(self):
        self.client.get(f"{BASE_PATH}/citizens/", headers=self.headers, name="List Citizens")

    @task(2)
    def get_citizen(self):
        self.client.get(f"{BASE_PATH}/citizens/1", headers=self.headers, name="Get Citizen")

    @task(1)
    def create_citizen(self):
        data = {
            "nome_completo": fake.name(),
            "numero_bi": fake.random_number(digits=14, fix_len=True),
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "genero": fake.random_element(["M", "F"]),
            "estado_civil": fake.random_element(["Solteiro", "Casado", "Divorciado", "Viúvo"]),
            "nome_mae": fake.name_female(),
            "nome_pai": fake.name_male(),
            "naturalidade": fake.city(),
            "nacionalidade": "Angolano",
            "provincia": fake.state(),
            "municipio": fake.city(),
            "telefone": fake.phone_number(),
            "email": fake.email(),
        }
        self.client.post(f"{BASE_PATH}/citizens/", json=data, headers=self.headers, name="Create Citizen")


class RequestUser(HttpUser, AuthMixin):
    """Usuário simulando solicitações de serviços (atestados, etc.)."""
    wait_time = between(2, 8)

    def on_start(self):
        token = self.login()
        if not token:
            self.environment.runner.quit()
        self.headers = self.auth_headers(token)

    @task(3)
    def list_requests(self):
        self.client.get(f"{BASE_PATH}/requests/user", headers=self.headers, name="List Requests")

    @task(2)
    def create_request(self):
        data = {
            "tipo_servico": fake.random_element(["RESIDENCIA", "CONDUTA", "POBREZA"]),
            "descricao": fake.sentence(nb_words=10),
        }
        self.client.post(f"{BASE_PATH}/requests", json=data, headers=self.headers, name="Create Request")


class ReportUser(HttpUser, AuthMixin):
    """Usuário simulando acesso a relatórios e estatísticas."""
    wait_time = between(5, 15)

    def on_start(self):
        token = self.login()
        if not token:
            self.environment.runner.quit()
        self.headers = self.auth_headers(token)

    @task(2)
    def get_summary(self):
        self.client.get(f"{BASE_PATH}/stats", headers=self.headers, name="Get Stats Summary")

    @task(1)
    def generate_pdf(self):
        self.client.get(f"{BASE_PATH}/requests/1/pdf", headers=self.headers, name="Generate PDF")