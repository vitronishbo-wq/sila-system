"""
Pytest fixtures para testes de autenticação consolidados.
Elimina duplicação de 28+ testes "requires_auth" em múltiplos arquivos.
"""

import pytest
from uuid import uuid4
from typing import List, Tuple


@pytest.fixture
def protected_endpoints() -> List[Tuple[str, str, dict]]:
    """
    Fixture com TODOS os endpoints que requerem autenticação.
    
    Formato: (method, endpoint, json_payload)
    - method: "GET", "POST", "PATCH", "DELETE"
    - endpoint: URL do endpoint
    - json_payload: dados para POST/PATCH (vazio para GET/DELETE)
    
    Elimina 28+ testes duplicados em:
    - tests/test_citizen_documents.py
    - app/modules/identidade_civil/tests/test_*.py
    - app/modules/service_requests/tests/test_*.py
    """
    return [
        # ===== CITIZEN API =====
        # Certificados
        ("GET", "/api/citizen/certidoes", {}),
        ("POST", "/api/citizen/certidoes/solicitar", {
            "certificate_type": "nascimento",
            "quantity": 1
        }),
        
        # Atestados
        ("GET", "/api/citizen/atestados", {}),
        ("POST", "/api/citizen/atestados/solicitar", {
            "attestation_type": "residencia"
        }),
        
        # Faturas e Pagamentos
        ("GET", "/api/citizen/faturas", {}),
        ("GET", "/api/citizen/pagamentos", {}),
        
        # Rastreamento de Solicitações
        ("GET", "/api/citizen/solicitacoes", {}),
        ("GET", f"/api/citizen/solicitacoes/{uuid4()}", {}),
        
        # Notificações
        ("GET", "/api/citizen/notificacoes", {}),
        ("POST", f"/api/citizen/notificacoes/{uuid4()}/lido", {}),
        
        # ===== IDENTIDADE CIVIL =====
        ("GET", "/api/v1/identidade/bi/tipos-evento", {}),
        ("POST", "/api/v1/identidade/bi/emit", {
            "citizen_fuc_id": "CITIZEN-001"
        }),
        ("POST", "/api/v1/identidade/bi/renovar", {
            "citizen_fuc_id": "CITIZEN-001"
        }),
        ("POST", "/api/v1/identidade/bi/cancelar", {
            "citizen_fuc_id": "CITIZEN-001"
        }),
        ("POST", "/api/v1/identidade/sincronia/fuc", {}),
        ("GET", "/api/v1/identidade/cidadaos", {}),
        ("GET", "/api/v1/identidade/documentos", {}),
        
        # Atestados (identidade_civil)
        ("GET", f"/api/v1/identidade/atestados/{uuid4()}/status", {}),
        ("POST", "/api/v1/identidade/atestados/residencia", {
            "citizen_fuc_id": "CITIZEN-001"
        }),
        ("POST", "/api/v1/identidade/atestados/vida-e-identidade", {
            "citizen_fuc_id": "CITIZEN-001"
        }),
        
        # ===== SERVICE REQUESTS =====
        ("POST", "/api/v1/service-requests/", {
            "service_type": "IDENTIDADE_BI",
            "title": "Test",
            "description": "Test"
        }),
        ("GET", "/api/v1/service-requests/me", {}),
        ("GET", "/api/v1/service-requests/assigned", {}),
        ("GET", "/api/v1/service-requests/pending", {}),
        ("GET", f"/api/v1/service-requests/{uuid4()}", {}),
        ("POST", f"/api/v1/service-requests/{uuid4()}/submit", {}),
        ("POST", f"/api/v1/service-requests/{uuid4()}/assign", {
            "assigned_to_user_id": str(uuid4())
        }),
        ("PATCH", f"/api/v1/service-requests/{uuid4()}/status", {
            "status": "EM_ANALISE"
        }),
        ("POST", "/api/v1/service-requests/search", {
            "query": "test",
            "skip": 0,
            "limit": 10
        }),
        ("GET", "/api/v1/service-requests/stats", {}),
    ]


@pytest.fixture
def auth_test_summary(protected_endpoints) -> str:
    """Gera resumo dos testes de autenticação para logging/debug."""
    by_method = {}
    for method, endpoint, _ in protected_endpoints:
        by_method.setdefault(method, 0)
        by_method[method] += 1
    
    summary = "Protected Endpoints Summary:\n"
    for method, count in sorted(by_method.items()):
        summary += f"  {method}: {count} endpoints\n"
    summary += f"  TOTAL: {len(protected_endpoints)} endpoints"
    
    return summary
