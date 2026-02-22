"""
Dados de exemplo para o módulo Training

Este arquivo contém dados realistas para demonstração e testes do sistema de treinamento.
Inclui programas de capacitação típicos do contexto angolano e exemplos de uso.
"""

from datetime import datetime, timedelta
from typing import Any, Dict

# Dados de exemplo para programas de treinamento
SAMPLE_TRAINING_PROGRAMS = [
    {
        "title": "Formação em Administração Pública",
        "description": "Capacitação de servidores públicos em gestão administrativa moderna, processos burocráticos e atendimento ao cidadão.",
        "category": "government",
        "start_date": datetime(2025, 10, 1, 9, 0),
        "end_date": datetime(2025, 11, 1, 17, 0),
        "location": "Centro de Formação Administrativa - Luanda",
        "instructor": "Dr. António Silva",
        "max_participants": 30,
        "requirements": "Ensino médio completo, experiência em serviço público",
        "objectives": "Melhorar eficiência administrativa e qualidade do atendimento público",
    },
    {
        "title": "Capacitação em Tecnologias de Informação",
        "description": "Treinamento em ferramentas digitais, sistemas de gestão e segurança da informação para funcionários públicos.",
        "category": "technical",
        "start_date": datetime(2025, 9, 15, 8, 30),
        "end_date": datetime(2025, 10, 15, 16, 30),
        "location": "Instituto Nacional de Tecnologia - Luanda",
        "instructor": "Eng. Maria Fernandes",
        "max_participants": 25,
        "requirements": "Conhecimentos básicos de informática",
        "objectives": "Digitalizar processos administrativos e melhorar eficiência tecnológica",
    },
    {
        "title": "Educação Cívica e Participação Cidadã",
        "description": "Programa de formação cívica para líderes comunitários e cidadãos interessados em participação democrática.",
        "category": "civic",
        "start_date": datetime(2025, 11, 1, 14, 0),
        "end_date": datetime(2025, 12, 1, 18, 0),
        "location": "Casa da Cultura - Benguela",
        "instructor": "Prof. João Mateus",
        "max_participants": 50,
        "requirements": "Liderança comunitária ou interesse em participação cívica",
        "objectives": "Fortalecer participação democrática e conhecimento dos direitos e deveres",
    },
    {
        "title": "Gestão de Recursos Humanos",
        "description": "Formação especializada em gestão de pessoas, liderança e desenvolvimento organizacional.",
        "category": "professional",
        "start_date": datetime(2025, 12, 1, 9, 0),
        "end_date": datetime(2026, 1, 15, 17, 0),
        "location": "Universidade Católica de Angola - Luanda",
        "instructor": "Dr. Isabel Santos",
        "max_participants": 20,
        "requirements": "Ensino superior, experiência em gestão",
        "objectives": "Desenvolver competências de liderança e gestão de equipes",
    },
    {
        "title": "Capacitação em Saúde Pública",
        "description": "Treinamento para profissionais de saúde em políticas públicas, epidemiologia e gestão sanitária.",
        "category": "professional",
        "start_date": datetime(2025, 10, 15, 8, 0),
        "end_date": datetime(2025, 11, 30, 16, 0),
        "location": "Instituto Superior de Ciências da Saúde - Luanda",
        "instructor": "Dr. Carlos Mendes",
        "max_participants": 35,
        "requirements": "Formação em área da saúde",
        "objectives": "Melhorar gestão de serviços de saúde pública",
    },
    {
        "title": "Formação em Agricultura Sustentável",
        "description": "Capacitação de técnicos agrícolas em práticas sustentáveis, irrigação e gestão de recursos naturais.",
        "category": "technical",
        "start_date": datetime(2025, 9, 1, 7, 30),
        "end_date": datetime(2025, 10, 1, 15, 30),
        "location": "Instituto de Desenvolvimento Agrário - Huambo",
        "instructor": "Eng. Agr. Pedro Costa",
        "max_participants": 40,
        "requirements": "Formação técnica em agricultura ou experiência rural",
        "objectives": "Promover agricultura sustentável e segurança alimentar",
    },
    {
        "title": "Capacitação em Educação Inclusiva",
        "description": "Formação de professores em metodologias inclusivas e atendimento a necessidades especiais.",
        "category": "professional",
        "start_date": datetime(2025, 11, 15, 8, 0),
        "end_date": datetime(2025, 12, 20, 16, 0),
        "location": "Instituto Superior de Ciências da Educação - Lubango",
        "instructor": "Prof. Ana Rodrigues",
        "max_participants": 30,
        "requirements": "Formação em pedagogia ou licenciatura em ensino",
        "objectives": "Promover educação inclusiva e acessível",
    },
    {
        "title": "Gestão Financeira Municipal",
        "description": "Capacitação de gestores municipais em orçamento público, controle financeiro e transparência fiscal.",
        "category": "government",
        "start_date": datetime(2025, 10, 1, 9, 0),
        "end_date": datetime(2025, 11, 15, 17, 0),
        "location": "Tribunal de Contas - Luanda",
        "instructor": "Dr. Fernando Oliveira",
        "max_participants": 25,
        "requirements": "Cargo de gestão municipal ou formação em economia/contabilidade",
        "objectives": "Melhorar gestão financeira e transparência municipal",
    },
]

# Dados de exemplo para inscrições
SAMPLE_ENROLLMENTS = [
    {
        "program_id": 1,
        "user_id": 101,
        "status": "completed",
        "enrollment_date": datetime(2025, 9, 15),
        "completion_date": datetime(2025, 11, 1),
        "grade": 16.5,
        "attendance_percentage": 92.0,
        "certificate_issued": True,
        "certificate_number": "CERT-ADM-2025-001",
        "feedback": "Excelente programa, muito útil para minha função administrativa",
    },
    {
        "program_id": 1,
        "user_id": 102,
        "status": "completed",
        "enrollment_date": datetime(2025, 9, 16),
        "completion_date": datetime(2025, 11, 1),
        "grade": 14.0,
        "attendance_percentage": 88.0,
        "certificate_issued": True,
        "certificate_number": "CERT-ADM-2025-002",
        "feedback": "Bom conteúdo, instrutor muito competente",
    },
    {
        "program_id": 2,
        "user_id": 103,
        "status": "in_progress",
        "enrollment_date": datetime(2025, 9, 10),
        "completion_date": None,
        "grade": None,
        "attendance_percentage": 75.0,
        "certificate_issued": False,
        "certificate_number": None,
        "feedback": None,
    },
    {
        "program_id": 3,
        "user_id": 104,
        "status": "confirmed",
        "enrollment_date": datetime(2025, 10, 20),
        "completion_date": None,
        "grade": None,
        "attendance_percentage": None,
        "certificate_issued": False,
        "certificate_number": None,
        "feedback": None,
    },
    {
        "program_id": 4,
        "user_id": 105,
        "status": "pending",
        "enrollment_date": datetime(2025, 11, 1),
        "completion_date": None,
        "grade": None,
        "attendance_percentage": None,
        "certificate_issued": False,
        "certificate_number": None,
        "feedback": None,
    },
]

# Exemplos de payloads para API
SAMPLE_API_REQUESTS = {
    "create_program": {
        "title": "Formação em Gestão de Projetos",
        "description": "Capacitação em metodologias ágeis e gestão de projetos públicos",
        "category": "professional",
        "start_date": "2025-12-01T09:00:00",
        "end_date": "2026-01-15T17:00:00",
        "location": "Centro de Formação - Luanda",
        "instructor": "Eng. Paulo Mendes",
        "max_participants": 25,
        "requirements": "Ensino superior, experiência em gestão",
        "objectives": "Desenvolver competências em gestão de projetos",
    },
    "enroll_user": {"program_id": 1, "user_id": 123},
    "complete_enrollment": {
        "grade": 17.5,
        "attendance_percentage": 95.0,
        "feedback": "Programa excepcional, superou expectativas",
    },
    "update_program": {
        "title": "Formação Avançada em Administração Pública",
        "location": "Centro de Formação - Benguela",
        "max_participants": 35,
    },
    "filter_programs": {
        "category": "government",
        "location": "Luanda",
        "start_date_from": "2025-10-01",
        "start_date_to": "2025-12-31",
    },
}

# Exemplos de respostas da API
SAMPLE_API_RESPONSES = {
    "program_created": {
        "id": 9,
        "title": "Formação em Gestão de Projetos",
        "description": "Capacitação em metodologias ágeis e gestão de projetos públicos",
        "category": "professional",
        "start_date": "2025-12-01T09:00:00",
        "end_date": "2026-01-15T17:00:00",
        "location": "Centro de Formação - Luanda",
        "instructor": "Eng. Paulo Mendes",
        "max_participants": 25,
        "current_participants": 0,
        "requirements": "Ensino superior, experiência em gestão",
        "objectives": "Desenvolver competências em gestão de projetos",
        "created_at": "2025-09-14T10:00:00",
        "updated_at": "2025-09-14T10:00:00",
    },
    "enrollment_completed": {
        "id": 15,
        "program_id": 1,
        "user_id": 123,
        "status": "completed",
        "enrollment_date": "2025-09-20T10:00:00",
        "completion_date": "2025-11-01T16:00:00",
        "grade": 17.5,
        "attendance_percentage": 95.0,
        "certificate_issued": True,
        "certificate_number": "CERT-ADM-2025-015",
        "feedback": "Programa excepcional, superou expectativas",
        "created_at": "2025-09-20T10:00:00",
        "updated_at": "2025-11-01T16:00:00",
    },
    "statistics": {
        "total_programs": 8,
        "active_programs": 5,
        "total_enrollments": 127,
        "completed_enrollments": 89,
        "certificates_issued": 76,
        "completion_rate": 70.1,
        "by_category": {
            "government": 25,
            "professional": 45,
            "technical": 32,
            "civic": 25,
        },
        "by_status": {
            "pending": 15,
            "confirmed": 23,
            "in_progress": 38,
            "completed": 89,
            "cancelled": 12,
        },
        "average_grade": 15.2,
        "average_attendance": 84.5,
    },
    "certificate_verification": {
        "valid": True,
        "certificate_number": "CERT-ADM-2025-001",
        "program_title": "Formação em Administração Pública",
        "user_name": "João Silva",
        "completion_date": "2025-11-01T16:00:00",
        "grade": 16.5,
        "attendance_percentage": 92.0,
        "issued_date": "2025-11-01T17:00:00",
    },
}

# Cenários de integração com outros módulos
INTEGRATION_SCENARIOS = {
    "with_governance": {
        "description": "Integração com módulo de governança para treinamentos obrigatórios",
        "example": {
            "mandatory_training": {
                "title": "Ética no Serviço Público",
                "category": "government",
                "required_for_roles": ["administrator", "manager", "public_servant"],
                "compliance_deadline": "2025-12-31",
                "governance_policy_id": "POL-ETH-2025-001",
            }
        },
    },
    "with_education": {
        "description": "Integração com sistema educacional para formação continuada",
        "example": {
            "continuing_education": {
                "title": "Metodologias de Ensino Modernas",
                "category": "professional",
                "target_audience": "teachers",
                "education_level": "higher_education",
                "credits": 30,
            }
        },
    },
    "with_citizens": {
        "description": "Programas de capacitação para cidadãos",
        "example": {
            "citizen_training": {
                "title": "Direitos e Deveres do Cidadão",
                "category": "civic",
                "target_audience": "general_public",
                "free_access": True,
                "community_impact": "high",
            }
        },
    },
    "with_service_hub": {
        "description": "Registro no hub de serviços para descoberta",
        "example": {
            "service_registration": {
                "module_name": "training",
                "service_name": "program_management",
                "description": "Gestão completa de programas de treinamento",
                "category": "education",
                "endpoints": [
                    "/training/programs",
                    "/training/enrollments",
                    "/training/certificates",
                ],
            }
        },
    },
}

# Dados para testes de carga e performance
LOAD_TEST_DATA = {
    "bulk_programs": [
        {
            "title": f"Programa de Teste {i}",
            "category": ["government", "professional", "technical", "civic"][i % 4],
            "start_date": datetime(2025, 10, 1) + timedelta(days=i * 7),
            "end_date": datetime(2025, 11, 1) + timedelta(days=i * 7),
            "max_participants": 20 + (i % 30),
        }
        for i in range(1, 101)  # 100 programas
    ],
    "bulk_enrollments": [
        {
            "program_id": (i % 10) + 1,
            "user_id": i + 1000,
            "status": ["pending", "confirmed", "in_progress"][i % 3],
        }
        for i in range(1, 501)  # 500 inscrições
    ],
}


def get_sample_program(category: str = None) -> Dict[str, Any]:
    """Retorna um programa de exemplo filtrado por categoria."""
    programs = SAMPLE_TRAINING_PROGRAMS
    if category:
        programs = [p for p in programs if p["category"] == category]
    return programs[0] if programs else SAMPLE_TRAINING_PROGRAMS[0]


def get_sample_enrollment(status: str = None) -> Dict[str, Any]:
    """Retorna uma inscrição de exemplo filtrada por status."""
    enrollments = SAMPLE_ENROLLMENTS
    if status:
        enrollments = [e for e in enrollments if e["status"] == status]
    return enrollments[0] if enrollments else SAMPLE_ENROLLMENTS[0]


def generate_certificate_number(program_id: int, sequence: int) -> str:
    """Gera número de certificado único."""
    categories = {1: "ADM", 2: "TEC", 3: "CIV", 4: "PRO"}
    category_code = categories.get(program_id, "GEN")
    year = datetime.now().year
    return f"CERT-{category_code}-{year}-{sequence:03d}"


# Configurações para demonstração
DEMO_CONFIG = {
    "auto_create_programs": True,
    "auto_enroll_users": True,
    "simulate_completions": True,
    "generate_certificates": True,
    "create_statistics": True,
}

if __name__ == "__main__":
    print("Dados de exemplo do módulo Training:")
    print(f"- {len(SAMPLE_TRAINING_PROGRAMS)} programas de exemplo")
    print(f"- {len(SAMPLE_ENROLLMENTS)} inscrições de exemplo")
    print(f"- {len(INTEGRATION_SCENARIOS)} cenários de integração")
    print(f"- {len(LOAD_TEST_DATA['bulk_programs'])} programas para teste de carga")
    print(f"- {len(LOAD_TEST_DATA['bulk_enrollments'])} inscrições para teste de carga")
