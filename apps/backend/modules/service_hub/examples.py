"""
Service Hub Examples

Exemplos de uso do módulo Service Hub para demonstrar
como criar e gerenciar serviços públicos digitais.
"""

from modules.service_hub.models.service_hub import ServiceCategory, ServiceScope
from modules.service_hub.schemas.service_hub import (
    ServiceCreate,
    ServiceLocationCreate,
)


def get_sample_services():
    """
    Retorna uma lista de serviços de exemplo para demonstração.

    Returns:
        List[ServiceCreate]: Lista de serviços de exemplo
    """
    return [
        ServiceCreate(
            name="Emissão de Bilhete de Identidade",
            category=ServiceCategory.IDENTITY,
            description="Emissão de bilhete de identidade para cidadãos angolanos",
            scope=ServiceScope.NATIONAL,
            estimated_time=20,
            requirements={
                "documents": [
                    "Certidão de nascimento",
                    "2 fotografias 3x4",
                    "Comprovativo de residência",
                ],
                "age_requirement": 16,
                "fees": 5000,
                "validity_period": "10 anos",
            },
        ),
        ServiceCreate(
            name="Emissão de Passaporte",
            category=ServiceCategory.IDENTITY,
            description="Emissão de passaporte para cidadãos angolanos",
            scope=ServiceScope.NATIONAL,
            estimated_time=30,
            requirements={
                "documents": [
                    "Bilhete de Identidade",
                    "Certidão de nascimento",
                    "2 fotografias 3x4",
                    "Comprovativo de residência",
                ],
                "age_requirement": 18,
                "fees": 15000,
                "validity_period": "5 anos",
            },
        ),
        ServiceCreate(
            name="Certidão de Nascimento",
            category=ServiceCategory.CIVIL_REGISTRY,
            description="Emissão de certidão de nascimento",
            scope=ServiceScope.NATIONAL,
            estimated_time=15,
            requirements={
                "documents": [
                    "Declaração de nascimento",
                    "Documento de identidade dos pais",
                    "Comprovativo de residência",
                ],
                "age_requirement": 0,
                "fees": 2000,
                "validity_period": "Vitalícia",
            },
        ),
        ServiceCreate(
            name="Certidão de Casamento",
            category=ServiceCategory.CIVIL_REGISTRY,
            description="Emissão de certidão de casamento civil",
            scope=ServiceScope.NATIONAL,
            estimated_time=25,
            requirements={
                "documents": [
                    "Bilhete de Identidade de ambos os cônjuges",
                    "Certidão de nascimento de ambos",
                    "Comprovativo de residência",
                    "Testemunhas",
                ],
                "age_requirement": 18,
                "fees": 8000,
                "validity_period": "Vitalícia",
            },
        ),
        ServiceCreate(
            name="Visto de Permanência",
            category=ServiceCategory.IMMIGRATION,
            description="Emissão de visto de permanência para estrangeiros",
            scope=ServiceScope.NATIONAL,
            estimated_time=45,
            requirements={
                "documents": [
                    "Passaporte válido",
                    "Certificado de antecedentes criminais",
                    "Comprovativo de meios de subsistência",
                    "Exame médico",
                ],
                "age_requirement": 18,
                "fees": 25000,
                "validity_period": "1 ano",
            },
        ),
        ServiceCreate(
            name="Registo de Empresa",
            category=ServiceCategory.BUSINESS,
            description="Registo de empresa no sistema comercial",
            scope=ServiceScope.NATIONAL,
            estimated_time=60,
            requirements={
                "documents": [
                    "Estatutos da empresa",
                    "Documentos dos sócios",
                    "Comprovativo de capital social",
                    "Alvará de localização",
                ],
                "age_requirement": 18,
                "fees": 30000,
                "validity_period": "Indefinido",
            },
        ),
    ]


def get_sample_locations():
    """
    Retorna uma lista de locais de atendimento de exemplo.

    Returns:
        List[ServiceLocationCreate]: Lista de locais de exemplo
    """
    return [
        ServiceLocationCreate(
            province="Luanda",
            municipality="Luanda",
            address="Rua Amílcar Cabral, 123 - Luanda",
            contact_info={
                "phone": "+244 923 456 789",
                "email": "atendimento.luanda@mint.gov.ao",
                "working_hours": {
                    "monday": "08:00-17:00",
                    "tuesday": "08:00-17:00",
                    "wednesday": "08:00-17:00",
                    "thursday": "08:00-17:00",
                    "friday": "08:00-15:00",
                },
            },
        ),
        ServiceLocationCreate(
            province="Benguela",
            municipality="Benguela",
            address="Avenida Marginal, 456 - Benguela",
            contact_info={
                "phone": "+244 923 456 790",
                "email": "atendimento.benguela@mint.gov.ao",
                "working_hours": {
                    "monday": "08:00-17:00",
                    "tuesday": "08:00-17:00",
                    "wednesday": "08:00-17:00",
                    "thursday": "08:00-17:00",
                    "friday": "08:00-15:00",
                },
            },
        ),
        ServiceLocationCreate(
            province="Huíla",
            municipality="Lubango",
            address="Rua da República, 789 - Lubango",
            contact_info={
                "phone": "+244 923 456 791",
                "email": "atendimento.lubango@mint.gov.ao",
                "working_hours": {
                    "monday": "08:00-17:00",
                    "tuesday": "08:00-17:00",
                    "wednesday": "08:00-17:00",
                    "thursday": "08:00-17:00",
                    "friday": "08:00-15:00",
                },
            },
        ),
        ServiceLocationCreate(
            province="Cabinda",
            municipality="Cabinda",
            address="Avenida 4 de Fevereiro, 321 - Cabinda",
            contact_info={
                "phone": "+244 923 456 792",
                "email": "atendimento.cabinda@mint.gov.ao",
                "working_hours": {
                    "monday": "08:00-17:00",
                    "tuesday": "08:00-17:00",
                    "wednesday": "08:00-17:00",
                    "thursday": "08:00-17:00",
                    "friday": "08:00-15:00",
                },
            },
        ),
    ]


def get_service_categories_info():
    """
    Retorna informações sobre as categorias de serviços disponíveis.

    Returns:
        dict: Informações sobre cada categoria
    """
    return {
        ServiceCategory.IDENTITY: {
            "name": "Documentos de Identidade",
            "description": "Serviços relacionados à emissão de documentos de identidade",
            "examples": ["BI", "Passaporte", "Carta de Condução"],
        },
        ServiceCategory.CIVIL_REGISTRY: {
            "name": "Registo Civil",
            "description": "Serviços de registo civil e certidões",
            "examples": [
                "Certidão de Nascimento",
                "Certidão de Casamento",
                "Certidão de Óbito",
            ],
        },
        ServiceCategory.IMMIGRATION: {
            "name": "Imigração",
            "description": "Serviços de imigração e vistos",
            "examples": [
                "Visto de Permanência",
                "Visto de Trabalho",
                "Visto de Estudo",
            ],
        },
        ServiceCategory.EDUCATION: {
            "name": "Educação",
            "description": "Serviços educacionais e académicos",
            "examples": [
                "Reconhecimento de Diplomas",
                "Equivalências",
                "Bolsas de Estudo",
            ],
        },
        ServiceCategory.HEALTH: {
            "name": "Saúde",
            "description": "Serviços de saúde pública",
            "examples": ["Cartão de Saúde", "Certificados Médicos", "Vacinação"],
        },
        ServiceCategory.SOCIAL_SECURITY: {
            "name": "Segurança Social",
            "description": "Serviços de segurança social e previdência",
            "examples": ["Registo de Contribuinte", "Pensões", "Subsídios"],
        },
        ServiceCategory.TAXES: {
            "name": "Impostos",
            "description": "Serviços fiscais e tributários",
            "examples": ["Declaração de IRS", "Certidão de Dívidas", "Isenções"],
        },
        ServiceCategory.BUSINESS: {
            "name": "Negócios",
            "description": "Serviços para empresas e negócios",
            "examples": ["Registo de Empresa", "Licenças Comerciais", "Alvarás"],
        },
        ServiceCategory.TRANSPORT: {
            "name": "Transporte",
            "description": "Serviços de transporte e mobilidade",
            "examples": [
                "Carta de Condução",
                "Licença de Condução",
                "Registo de Veículos",
            ],
        },
        ServiceCategory.HOUSING: {
            "name": "Habitação",
            "description": "Serviços relacionados à habitação",
            "examples": [
                "Licença de Construção",
                "Registo Predial",
                "Certidão de Habitação",
            ],
        },
        ServiceCategory.OTHER: {
            "name": "Outros",
            "description": "Outros serviços não categorizados",
            "examples": ["Certidões Diversas", "Autenticações", "Reconhecimentos"],
        },
    }


def get_service_scopes_info():
    """
    Retorna informações sobre os escopos de serviços disponíveis.

    Returns:
        dict: Informações sobre cada escopo
    """
    return {
        ServiceScope.NATIONAL: {
            "name": "Nacional",
            "description": "Serviço disponível em todo o território nacional",
            "coverage": "Todas as províncias e municípios",
        },
        ServiceScope.PROVINCE: {
            "name": "Provincial",
            "description": "Serviço disponível apenas em uma província específica",
            "coverage": "Uma província e seus municípios",
        },
        ServiceScope.MUNICIPALITY: {
            "name": "Municipal",
            "description": "Serviço disponível apenas em um município específico",
            "coverage": "Um município específico",
        },
    }


# Exemplo de uso programático
async def create_sample_services(service_hub_service):
    """
    Cria serviços de exemplo no sistema.

    Args:
        service_hub_service: Instância do ServiceHubService
    """
    services = get_sample_services()
    created_services = []

    for service_data in services:
        try:
            service = await service_hub_service.create_service(service_data)
            created_services.append(service)
            print(f"✅ Serviço criado: {service.name}")
        except Exception as e:
            print(f"❌ Erro ao criar serviço {service_data.name}: {str(e)}")

    return created_services


async def add_sample_locations(service_hub_service, service_id: int):
    """
    Adiciona locais de atendimento de exemplo para um serviço.

    Args:
        service_hub_service: Instância do ServiceHubService
        service_id: ID do serviço
    """
    locations = get_sample_locations()
    created_locations = []

    for location_data in locations:
        try:
            location = await service_hub_service.create_service_location(
                service_id, location_data
            )
            created_locations.append(location)
            print(f"✅ Local criado: {location.province}/{location.municipality}")
        except Exception as e:
            print(
                f"❌ Erro ao criar local {location_data.province}/{location_data.municipality}: {str(e)}"
            )

    return created_locations


# Exemplo de consultas
async def demonstrate_queries(service_hub_service):
    """
    Demonstra diferentes tipos de consultas ao service hub.

    Args:
        service_hub_service: Instância do ServiceHubService
    """
    print("\n🔍 Demonstração de Consultas:")

    # Listar todos os serviços
    services, total = await service_hub_service.list_services(
        ServiceFilters(is_active=True), skip=0, limit=10
    )
    print(f"📊 Total de serviços ativos: {total}")

    # Buscar por categoria
    identity_services = await service_hub_service.get_services_by_category(
        ServiceCategory.IDENTITY
    )
    print(f"🆔 Serviços de identidade: {len(identity_services)}")

    # Buscar por escopo
    national_services = await service_hub_service.get_services_by_scope(
        ServiceScope.NATIONAL
    )
    print(f"🌍 Serviços nacionais: {len(national_services)}")

    # Estatísticas
    stats = await service_hub_service.get_service_statistics()
    print(f"📈 Estatísticas: {stats}")


if __name__ == "__main__":
    print("🚀 Service Hub - Exemplos de Uso")
    print("=" * 50)

    print("\n📋 Serviços de Exemplo:")
    for service in get_sample_services():
        print(f"  • {service.name} ({service.category.value})")

    print("\n📍 Locais de Exemplo:")
    for location in get_sample_locations():
        print(f"  • {location.province}/{location.municipality}")

    print("\n🏷️ Categorias Disponíveis:")
    for category, info in get_service_categories_info().items():
        print(f"  • {category.value}: {info['name']}")

    print("\n🌍 Escopos Disponíveis:")
    for scope, info in get_service_scopes_info().items():
        print(f"  • {scope.value}: {info['name']}")
