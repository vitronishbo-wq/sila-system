"""Configurações OpenAPI para o módulo taxpayer"""

from typing import Dict, Any

taxpayer_tags = [
    {
        "name": "Contribuintes",
        "description": "Operações de gestão de contribuintes"
    },
    {
        "name": "Declarações",
        "description": "Submissão e consulta de declarações fiscais"
    },
    {
        "name": "Dívidas",
        "description": "Gestão de dívidas fiscais"
    },
    {
        "name": "Pagamentos",
        "description": "Processamento de pagamentos"
    },
    {
        "name": "Certidões",
        "description": "Solicitação de certidões fiscais"
    },
    {
        "name": "Sincronização",
        "description": "Sincronização com AGT"
    }
]

taxpayer_examples: Dict[str, Any] = {
    "TaxpayerCreate": {
        "value": {
            "nif": "123456789",
            "name": "João Silva",
            "email": "joao.silva@email.com",
            "phone": "+244923456789",
            "address": "Rua Principal, 123, Luanda",
            "tax_regime": "GERAL"
        }
    },
    "TaxpayerResponse": {
        "value": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "nif": "123456789",
            "name": "João Silva",
            "email": "joao.silva@email.com",
            "phone": "+244923456789",
            "address": "Rua Principal, 123, Luanda",
            "tax_regime": "GERAL",
            "status": "ACTIVE",
            "registered_by": "123e4567-e89b-12d3-a456-426614174001",
            "registered_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T10:00:00Z",
            "agt_status": "ACTIVE",
            "agt_last_sync": "2024-01-01T09:00:00Z"
        }
    },
    "DeclarationCreate": {
        "value": {
            "tax_type": "IVA",
            "tax_period": "2024-01",
            "gross_amount": 1000000.00,
            "deductions": 150000.00
        }
    }
}
