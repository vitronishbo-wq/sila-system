"""
Dados de exemplo para o módulo Sanitation
Demonstra o uso dos novos campos responsible_entity e technical_manager
"""

from datetime import datetime

from modules.sanitation.models.sanitation import SanitationRecord, SanitationType
from modules.sanitation.schemas.sanitation import SanitationCreate

# Dados de exemplo para diferentes municípios angolanos
SAMPLE_SANITATION_DATA = [
    {
        "municipality_id": 1,  # Luanda
        "sanitation_type": SanitationType.WATER,
        "coverage_percentage": 85.0,
        "responsible_entity": "EPAL - Empresa Pública de Águas de Luanda",
        "technical_manager": "Eng. João Manuel Silva",
    },
    {
        "municipality_id": 1,  # Luanda
        "sanitation_type": SanitationType.SEWAGE,
        "coverage_percentage": 45.0,
        "responsible_entity": "EPAL - Empresa Pública de Águas de Luanda",
        "technical_manager": "Eng. Maria Fernanda Costa",
    },
    {
        "municipality_id": 1,  # Luanda
        "sanitation_type": SanitationType.WASTE,
        "coverage_percentage": 70.0,
        "responsible_entity": "ELISAL - Empresa de Limpeza de Luanda",
        "technical_manager": "Eng. Pedro António Mendes",
    },
    {
        "municipality_id": 2,  # Benguela
        "sanitation_type": SanitationType.WATER,
        "coverage_percentage": 65.0,
        "responsible_entity": "EPAL Benguela",
        "technical_manager": "Eng. Ana Cristina Rodrigues",
    },
    {
        "municipality_id": 2,  # Benguela
        "sanitation_type": SanitationType.WASTE,
        "coverage_percentage": 55.0,
        "responsible_entity": "Serviços Municipais de Benguela",
        "technical_manager": "Téc. Carlos Eduardo Santos",
    },
    {
        "municipality_id": 3,  # Huambo
        "sanitation_type": SanitationType.WATER,
        "coverage_percentage": 50.0,
        "responsible_entity": "Direção Provincial das Águas do Huambo",
        "technical_manager": "Eng. Isabel Maria Fernandes",
    },
    {
        "municipality_id": 3,  # Huambo
        "sanitation_type": SanitationType.HYGIENE,
        "coverage_percentage": 30.0,
        "responsible_entity": "Direção Provincial da Saúde do Huambo",
        "technical_manager": "Dr. Manuel José Pereira",
    },
    {
        "municipality_id": 4,  # Lobito
        "sanitation_type": SanitationType.WATER,
        "coverage_percentage": 75.0,
        "responsible_entity": "EPAL Benguela - Extensão Lobito",
        "technical_manager": "Eng. Francisco Domingos",
    },
    {
        "municipality_id": 4,  # Lobito
        "sanitation_type": SanitationType.SEWAGE,
        "coverage_percentage": 40.0,
        "responsible_entity": "Administração Municipal do Lobito",
        "technical_manager": "Eng. Teresa Alves",
    },
]


def create_sample_records(db_session):
    """
    Cria registros de exemplo na base de dados
    """
    records = []
    for data in SAMPLE_SANITATION_DATA:
        record = SanitationRecord(
            municipality_id=data["municipality_id"],
            sanitation_type=data["sanitation_type"],
            coverage_percentage=data["coverage_percentage"],
            responsible_entity=data["responsible_entity"],
            technical_manager=data["technical_manager"],
            last_updated=datetime.utcnow(),
        )
        records.append(record)

    db_session.add_all(records)
    db_session.commit()
    return records


def get_sample_create_schemas():
    """
    Retorna schemas de criação para testes
    """
    schemas = []
    for data in SAMPLE_SANITATION_DATA:
        schema = SanitationCreate(
            municipality_id=data["municipality_id"],
            sanitation_type=data["sanitation_type"],
            coverage_percentage=data["coverage_percentage"],
            responsible_entity=data["responsible_entity"],
            technical_manager=data["technical_manager"],
        )
        schemas.append(schema)
    return schemas


# Exemplos de estatísticas esperadas
EXPECTED_STATISTICS = {
    1: {  # Luanda
        "total_records": 3,
        "avg_coverage": 66.67,  # (85 + 45 + 70) / 3
        "by_type": {"water": 85.0, "sewage": 45.0, "waste": 70.0},
    },
    2: {  # Benguela
        "total_records": 2,
        "avg_coverage": 60.0,  # (65 + 55) / 2
        "by_type": {"water": 65.0, "waste": 55.0},
    },
    3: {  # Huambo
        "total_records": 2,
        "avg_coverage": 40.0,  # (50 + 30) / 2
        "by_type": {"water": 50.0, "hygiene": 30.0},
    },
}

# Exemplos de atualizações
SAMPLE_UPDATES = [
    {
        "coverage_percentage": 90.0,
        "technical_manager": "Eng. João Manuel Silva (Atualizado)",
    },
    {
        "coverage_percentage": 55.0,
        "responsible_entity": "EPAL - Empresa Pública de Águas de Luanda (Reformulada)",
    },
    {
        "sanitation_type": SanitationType.WASTE,
        "coverage_percentage": 80.0,
        "responsible_entity": "ELISAL - Nova Gestão",
        "technical_manager": "Eng. Pedro António Mendes (Promovido)",
    },
]
