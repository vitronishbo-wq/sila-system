"""
Configurações para os testes de performance do módulo Citizenship.
"""

import os

from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações gerais
BASE_URL = settings.API_BASE_URL
ADMIN_EMAIL = settings.ADMIN_EMAIL
ADMIN_PASSWORD = settings.ADMIN_PASSWORD

# Configurações de usuários simulados
USERS = {
    "citizen": {
        "count": 10,  # Número de usuários simultâneos
        "spawn_rate": 2,  # Usuários adicionados por segundo
        "class": "CitizenTestUser",
    },
    "atestado": {
        "count": 5,
        "spawn_rate": 1,
        "class": "AtestadoTestUser",
    },
    "report": {
        "count": 2,
        "spawn_rate": 0.5,
        "class": "ReportTestUser",
    },
}

# Duração dos testes (em segundos)
TEST_DURATION = 300  # 5 minutos

# Limites de desempenho aceitáveis (em milissegundos)
PERFORMANCE_THRESHOLDS = {
    "list_citizens": 500,
    "get_citizen": 300,
    "create_citizen": 800,
    "solicitar_atestado": 1000,
    "listar_atestados": 500,
    "get_summary": 2000,
    "generate_pdf": 3000,
}

# Taxa de erro aceitável (em %)
MAX_ERROR_RATE = 1.0

# Configurações de relatórios
REPORTS_DIR = "reports"
HTML_REPORT = os.path.join(REPORTS_DIR, "performance_report.html")
CSV_PREFIX = os.path.join(REPORTS_DIR, "stats")

# Cria o diretório de relatórios se não existir
os.makedirs(REPORTS_DIR, exist_ok=True)
