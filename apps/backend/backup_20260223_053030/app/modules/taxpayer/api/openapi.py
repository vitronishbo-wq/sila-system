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
    },
    "DeclarationResponse": {
        "value": {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "taxpayer_id": "123e4567-e89b-12d3-a456-426614174000",
            "declaration_number": "DEC/2024/000001",
            "tax_type": "IVA",
            "tax_period": "2024-01",
            "gross_amount": 1000000.00,
            "deductions": 150000.00,
            "net_amount": 850000.00,
            "declaration_date": "2024-02-15",
            "due_date": "2024-02-28",
            "status": "APPROVED",
            "protocol": "PROT-2024-0001",
            "submitted_by": "123e4567-e89b-12d3-a456-426614174001",
            "submitted_at": "2024-02-15T14:30:00Z",
            "processed_by": "123e4567-e89b-12d3-a456-426614174003",
            "processed_at": "2024-02-16T09:15:00Z"
        }
    },
    "DebtResponse": {
        "value": {
            "id": "123e4567-e89b-12d3-a456-426614174004",
            "taxpayer_id": "123e4567-e89b-12d3-a456-426614174000",
            "debt_number": "DEBT/2024/000001",
            "tax_type": "IVA",
            "original_amount": 850000.00,
            "current_amount": 892500.00,
            "interest": 42500.00,
            "fines": 0.00,
            "created_date": "2024-03-01",
            "due_date": "2024-03-31",
            "status": "PENDING"
        }
    },
    "PaymentResponse": {
        "value": {
            "id": "123e4567-e89b-12d3-a456-426614174005",
            "taxpayer_id": "123e4567-e89b-12d3-a456-426614174000",
            "debt_id": "123e4567-e89b-12d3-a456-426614174004",
            "payment_number": "PAY/2024/000001",
            "amount": 892500.00,
            "payment_method": "TRANSFER",
            "payment_date": "2024-03-15T10:30:00Z",
            "status": "COMPLETED",
            "reference": "REF-2024-0001",
            "paid_by": "123e4567-e89b-12d3-a456-426614174001"
        }
    },
    "CertificateResponse": {
        "value": {
            "id": "123e4567-e89b-12d3-a456-426614174006",
            "taxpayer_id": "123e4567-e89b-12d3-a456-426614174000",
            "certificate_number": "CERT/NIF/2024/000001",
            "certificate_type": "NIF",
            "year": 2024,
            "status": "ISSUED",
            "requested_at": "2024-03-01T09:00:00Z",
            "requested_by": "123e4567-e89b-12d3-a456-426614174001",
            "issued_at": "2024-03-02T14:30:00Z",
            "issued_by": "123e4567-e89b-12d3-a456-426614174003",
            "expires_at": "2024-06-01",
            "file_url": "/certificates/123e4567/download"
        }
    }
}
