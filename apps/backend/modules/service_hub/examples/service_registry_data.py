"""
Dados de exemplo para o Service Registry

Demonstra o registro de serviços de diferentes módulos do sistema SILA
e exemplos de integração entre módulos.
"""

from datetime import datetime
from typing import Any, Dict, List

from modules.service_hub.models.service_registry import ServiceRegistry
from modules.service_hub.schemas.service_registry import ServiceCreate

# Dados de exemplo para diferentes módulos do sistema SILA
SAMPLE_SERVICES_DATA = [
    # Módulo Citizenship - Serviços de Cidadania
    {
        "module_name": "citizenship",
        "service_name": "apply_passport",
        "description": "Solicitação de passaporte angolano",
        "category": "identity",
    },
    {
        "module_name": "citizenship",
        "service_name": "request_id_card",
        "description": "Solicitação de cartão de identidade (BI)",
        "category": "identity",
    },
    {
        "module_name": "citizenship",
        "service_name": "verify_document",
        "description": "Verificação de autenticidade de documentos",
        "category": "identity",
    },
    {
        "module_name": "citizenship",
        "service_name": "update_personal_data",
        "description": "Atualização de dados pessoais",
        "category": "identity",
    },
    # Módulo Education - Serviços de Educação
    {
        "module_name": "education",
        "service_name": "enroll_student",
        "description": "Matrícula de estudante em instituição de ensino",
        "category": "education",
    },
    {
        "module_name": "education",
        "service_name": "request_certificate",
        "description": "Solicitação de certificados e diplomas",
        "category": "education",
    },
    {
        "module_name": "education",
        "service_name": "transfer_school",
        "description": "Transferência entre instituições de ensino",
        "category": "education",
    },
    {
        "module_name": "education",
        "service_name": "scholarship_application",
        "description": "Candidatura a bolsas de estudo",
        "category": "education",
    },
    # Módulo Health - Serviços de Saúde
    {
        "module_name": "health",
        "service_name": "book_appointment",
        "description": "Marcação de consultas médicas",
        "category": "health",
    },
    {
        "module_name": "health",
        "service_name": "get_medical_record",
        "description": "Acesso a registros médicos",
        "category": "health",
    },
    {
        "module_name": "health",
        "service_name": "vaccination_schedule",
        "description": "Agendamento de vacinas",
        "category": "health",
    },
    {
        "module_name": "health",
        "service_name": "emergency_contact",
        "description": "Contato de emergência médica",
        "category": "health",
    },
    {
        "module_name": "health",
        "service_name": "prescription_renewal",
        "description": "Renovação de prescrições médicas",
        "category": "health",
    },
    # Módulo Social - Serviços Sociais
    {
        "module_name": "social",
        "service_name": "apply_benefit",
        "description": "Solicitação de benefícios sociais",
        "category": "social_security",
    },
    {
        "module_name": "social",
        "service_name": "pension_request",
        "description": "Solicitação de pensão",
        "category": "social_security",
    },
    {
        "module_name": "social",
        "service_name": "disability_support",
        "description": "Apoio para pessoas com deficiência",
        "category": "social_security",
    },
    # Módulo Finance - Serviços Financeiros
    {
        "module_name": "finance",
        "service_name": "pay_taxes",
        "description": "Pagamento de impostos",
        "category": "taxes",
    },
    {
        "module_name": "finance",
        "service_name": "tax_declaration",
        "description": "Declaração de impostos",
        "category": "taxes",
    },
    {
        "module_name": "finance",
        "service_name": "business_license",
        "description": "Licenciamento de negócios",
        "category": "business",
    },
    # Módulo Transport - Serviços de Transporte
    {
        "module_name": "transport",
        "service_name": "renew_license",
        "description": "Renovação de carta de condução",
        "category": "transport",
    },
    {
        "module_name": "transport",
        "service_name": "vehicle_registration",
        "description": "Registo de veículos",
        "category": "transport",
    },
    {
        "module_name": "transport",
        "service_name": "driving_test",
        "description": "Marcação de exame de condução",
        "category": "transport",
    },
    # Módulo Housing - Serviços de Habitação
    {
        "module_name": "housing",
        "service_name": "apply_housing",
        "description": "Candidatura a habitação social",
        "category": "housing",
    },
    {
        "module_name": "housing",
        "service_name": "property_registration",
        "description": "Registo de propriedades",
        "category": "housing",
    },
    # Módulo Sanitation - Serviços de Saneamento
    {
        "module_name": "sanitation",
        "service_name": "water_connection",
        "description": "Ligação de água",
        "category": "utilities",
    },
    {
        "module_name": "sanitation",
        "service_name": "waste_collection",
        "description": "Coleta de resíduos",
        "category": "utilities",
    },
    # Módulo Governance - Serviços de Governança
    {
        "module_name": "governance",
        "service_name": "public_consultation",
        "description": "Participação em consultas públicas",
        "category": "governance",
    },
    {
        "module_name": "governance",
        "service_name": "complaint_submission",
        "description": "Submissão de reclamações",
        "category": "governance",
    },
]


def create_sample_services(db_session) -> List[ServiceRegistry]:
    """
    Cria registros de exemplo na base de dados.

    Args:
        db_session: Sessão do banco de dados

    Returns:
        List[ServiceRegistry]: Lista de serviços criados
    """
    services = []
    for data in SAMPLE_SERVICES_DATA:
        service = ServiceRegistry(
            module_name=data["module_name"],
            service_name=data["service_name"],
            description=data["description"],
            category=data["category"],
            is_active=True,
            created_at=datetime.utcnow(),
        )
        services.append(service)

    db_session.add_all(services)
    db_session.commit()
    return services


def get_sample_create_schemas() -> List[ServiceCreate]:
    """
    Retorna schemas de criação para testes.

    Returns:
        List[ServiceCreate]: Lista de schemas para criação
    """
    schemas = []
    for data in SAMPLE_SERVICES_DATA:
        schema = ServiceCreate(
            module_name=data["module_name"],
            service_name=data["service_name"],
            description=data["description"],
            category=data["category"],
        )
        schemas.append(schema)
    return schemas


# Exemplos de payloads para encaminhamento
SAMPLE_FORWARD_PAYLOADS = {
    "citizenship": {
        "apply_passport": {
            "citizen_id": "123456789",
            "passport_type": "ordinary",
            "urgency": "normal",
            "contact_info": {
                "phone": "+244 900 123 456",
                "email": "citizen@example.com",
            },
        },
        "request_id_card": {
            "citizen_id": "123456789",
            "document_type": "first_time",
            "pickup_location": "Luanda",
        },
        "verify_document": {
            "document_id": "BI123456789",
            "document_type": "id_card",
            "verification_type": "authenticity",
        },
    },
    "education": {
        "enroll_student": {
            "student_id": "STU001",
            "school_id": "ESC001",
            "grade": "10",
            "academic_year": "2024/2025",
        },
        "request_certificate": {
            "student_id": "STU001",
            "certificate_type": "completion",
            "academic_year": "2023/2024",
        },
    },
    "health": {
        "book_appointment": {
            "patient_id": "PAT001",
            "doctor_id": "DOC001",
            "appointment_type": "consultation",
            "preferred_date": "2024-09-20",
            "preferred_time": "14:00",
        },
        "vaccination_schedule": {
            "patient_id": "PAT001",
            "vaccine_type": "covid19",
            "dose_number": 1,
        },
    },
    "social": {
        "apply_benefit": {
            "citizen_id": "123456789",
            "benefit_type": "unemployment",
            "family_size": 4,
            "monthly_income": 50000,
        }
    },
    "finance": {
        "pay_taxes": {
            "taxpayer_id": "TAX123456",
            "tax_type": "income",
            "amount": 150000,
            "payment_method": "bank_transfer",
        }
    },
}


# Estatísticas esperadas após carregar dados de exemplo
EXPECTED_STATISTICS = {
    "total_services": len(SAMPLE_SERVICES_DATA),
    "by_category": {
        "identity": 4,
        "education": 4,
        "health": 5,
        "social_security": 3,
        "taxes": 2,
        "business": 1,
        "transport": 3,
        "housing": 2,
        "utilities": 2,
        "governance": 2,
    },
    "by_module": {
        "citizenship": 4,
        "education": 4,
        "health": 5,
        "social": 3,
        "finance": 2,
        "transport": 3,
        "housing": 2,
        "sanitation": 2,
        "governance": 2,
    },
}


# Exemplos de integração entre módulos
INTEGRATION_EXAMPLES = [
    {
        "scenario": "Matrícula Escolar com Verificação de Identidade",
        "description": "Ao matricular um estudante, o módulo education verifica a identidade no módulo citizenship",
        "flow": [
            {
                "step": 1,
                "module": "education",
                "action": "Recebe solicitação de matrícula",
            },
            {
                "step": 2,
                "module": "education",
                "action": "Encaminha verificação para citizenship via service_hub",
                "payload": {
                    "service": "verify_document",
                    "data": {"document_id": "BI123456789"},
                },
            },
            {
                "step": 3,
                "module": "citizenship",
                "action": "Verifica autenticidade do documento",
            },
            {
                "step": 4,
                "module": "education",
                "action": "Processa matrícula com documento verificado",
            },
        ],
    },
    {
        "scenario": "Consulta Médica com Histórico Social",
        "description": "Ao marcar consulta, o módulo health consulta benefícios sociais para determinar isenções",
        "flow": [
            {"step": 1, "module": "health", "action": "Recebe solicitação de consulta"},
            {
                "step": 2,
                "module": "health",
                "action": "Consulta benefícios sociais via service_hub",
                "payload": {
                    "service": "check_benefits",
                    "data": {"citizen_id": "123456789"},
                },
            },
            {"step": 3, "module": "social", "action": "Retorna status de benefícios"},
            {
                "step": 4,
                "module": "health",
                "action": "Aplica isenções se aplicável e agenda consulta",
            },
        ],
    },
]


def get_integration_example(scenario_name: str) -> Dict[str, Any]:
    """
    Obtém exemplo de integração por nome do cenário.

    Args:
        scenario_name: Nome do cenário

    Returns:
        Dict: Exemplo de integração ou None se não encontrado
    """
    for example in INTEGRATION_EXAMPLES:
        if scenario_name.lower() in example["scenario"].lower():
            return example
    return None


def get_services_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Filtra serviços por categoria.

    Args:
        category: Categoria desejada

    Returns:
        List: Serviços da categoria
    """
    return [s for s in SAMPLE_SERVICES_DATA if s["category"] == category]


def get_services_by_module(module_name: str) -> List[Dict[str, Any]]:
    """
    Filtra serviços por módulo.

    Args:
        module_name: Nome do módulo

    Returns:
        List: Serviços do módulo
    """
    return [s for s in SAMPLE_SERVICES_DATA if s["module_name"] == module_name]
