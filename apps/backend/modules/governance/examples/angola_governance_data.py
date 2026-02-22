"""
Exemplos de dados para demonstrar o módulo governance adaptado ao contexto angolano.

Este arquivo contém exemplos realistas de:
- Estrutura administrativa angolana (provincial, municipal, comunal)
- Nomeações conforme legislação de Angola
- Reuniões de CMAS e órgãos administrativos
- Decisões administrativas (despachos, portarias, regulamentos)
"""

from datetime import date
from typing import Any, Dict, List

# Estrutura de Instituições - Hierarquia Administrativa Angolana
INSTITUTIONS_EXAMPLES = [
    # Governo Provincial de Luanda
    {
        "name": "Governo Provincial de Luanda",
        "type": "provincial_government",
        "code": "GPL",
        "description": "Órgão superior da administração provincial de Luanda",
        "level": 1,
        "province": "Luanda",
        "address": "Largo do Palácio, Luanda",
        "phone": "+244 222 334 455",
        "email": "geral@governoluanda.gov.ao",
        "status": "active",
        "established_date": date(1975, 11, 11),
    },
    # Administração Municipal de Luanda
    {
        "name": "Administração Municipal de Luanda",
        "type": "municipal_admin",
        "code": "AML",
        "description": "Administração do Município de Luanda",
        "parent_id": 1,  # Filho do Governo Provincial
        "level": 2,
        "province": "Luanda",
        "municipality": "Luanda",
        "address": "Rua Major Kanhangulo, Luanda",
        "phone": "+244 222 445 566",
        "email": "geral@admluanda.gov.ao",
        "status": "active",
    },
    # Administração Comunal da Ingombota
    {
        "name": "Administração Comunal da Ingombota",
        "type": "communal_admin",
        "code": "ACI",
        "description": "Administração da Comuna da Ingombota",
        "parent_id": 2,  # Filho da Administração Municipal
        "level": 3,
        "province": "Luanda",
        "municipality": "Luanda",
        "commune": "Ingombota",
        "address": "Rua Rainha Ginga, Ingombota",
        "phone": "+244 222 556 677",
        "status": "active",
    },
    # Direção Provincial de Educação de Luanda
    {
        "name": "Direção Provincial de Educação de Luanda",
        "type": "provincial_directorate",
        "code": "DPEL",
        "description": "Direção responsável pela educação na província de Luanda",
        "parent_id": 1,
        "level": 2,
        "province": "Luanda",
        "address": "Rua Ndunduma, Luanda",
        "phone": "+244 222 667 788",
        "email": "geral@educacaoluanda.gov.ao",
        "status": "active",
    },
    # CMAS de Luanda
    {
        "name": "Conselho Municipal de Auscultação Social de Luanda",
        "type": "cmas",
        "code": "CMAS-LDA",
        "description": "Órgão de consulta e participação social do município de Luanda",
        "parent_id": 2,
        "level": 3,
        "province": "Luanda",
        "municipality": "Luanda",
        "address": "Rua Major Kanhangulo, Luanda",
        "phone": "+244 222 445 566",
        "status": "active",
    },
]

# Exemplos de Mandatos/Nomeações
MANDATES_EXAMPLES = [
    # Governador Provincial de Luanda
    {
        "person_id": 1,  # Assumindo que existe um cidadão com ID 1
        "institution_id": 1,  # Governo Provincial de Luanda
        "role": "Governador Provincial",
        "role_code": "GOV-PROV",
        "appointment_type": "decreto_presidencial",
        "appointment_authority": "Presidente da República",
        "appointment_document": "Decreto Presidencial nº 45/2024",
        "start_date": date(2024, 3, 15),
        "responsibilities": "Dirigir a administração provincial, coordenar as políticas do Executivo na província",
        "salary_grade": "Escalão Superior",
        "status": "active",
    },
    # Administrador Municipal de Luanda
    {
        "person_id": 2,
        "institution_id": 2,  # Administração Municipal de Luanda
        "role": "Administrador Municipal",
        "role_code": "ADM-MUN",
        "appointment_type": "despacho_governador",
        "appointment_authority": "Governador Provincial de Luanda",
        "appointment_document": "Despacho nº 12/GPL/2024",
        "start_date": date(2024, 4, 1),
        "responsibilities": "Administrar o município, executar políticas locais",
        "salary_grade": "Escalão A",
        "status": "active",
    },
    # Diretor Provincial de Educação
    {
        "person_id": 3,
        "institution_id": 4,  # Direção Provincial de Educação
        "role": "Diretor Provincial de Educação",
        "role_code": "DIR-PROV-EDU",
        "department": "Educação",
        "appointment_type": "portaria_ministerial",
        "appointment_authority": "Ministro da Educação",
        "appointment_document": "Portaria nº 234/MED/2024",
        "start_date": date(2024, 2, 1),
        "responsibilities": "Dirigir e coordenar o sistema educativo provincial",
        "salary_grade": "Escalão A",
        "status": "active",
    },
]

# Exemplos de Reuniões de Conselhos
COUNCIL_MEETINGS_EXAMPLES = [
    # Reunião Ordinária do CMAS
    {
        "institution_id": 5,  # CMAS de Luanda
        "meeting_type": "cmas_ordinaria",
        "title": "1ª Reunião Ordinária do CMAS de Luanda - 2024",
        "meeting_number": "001/CMAS-LDA/2024",
        "meeting_date": date(2024, 3, 15),
        "start_time": "09:00",
        "end_time": "12:30",
        "venue": "Sala de Reuniões da Administração Municipal",
        "agenda": """
        1. Abertura e verificação do quórum
        2. Aprovação da ata da reunião anterior
        3. Apresentação do plano de desenvolvimento municipal 2024
        4. Discussão sobre projetos de saneamento básico
        5. Propostas da sociedade civil
        6. Diversos
        """,
        "chairperson": "Administrador Municipal de Luanda",
        "secretary": "Secretário do CMAS",
        "quorum_required": 15,
        "quorum_present": 18,
        "status": "completed",
        "is_public": True,
        "minutes_approved": True,
        "decisions_summary": "Aprovado plano de desenvolvimento municipal, priorizados 3 projetos de saneamento",
        "resolutions": "Resolução nº 01/CMAS-LDA/2024 - Aprovação do plano municipal",
    },
    # Reunião de Coordenação Provincial
    {
        "institution_id": 1,  # Governo Provincial
        "meeting_type": "conselho_provincial",
        "title": "Conselho de Coordenação Provincial - Março 2024",
        "meeting_number": "003/CCP-LDA/2024",
        "meeting_date": date(2024, 3, 20),
        "start_time": "14:00",
        "end_time": "17:00",
        "venue": "Sala do Conselho do Governo Provincial",
        "agenda": """
        1. Balanço da execução orçamental do 1º trimestre
        2. Coordenação entre direções provinciais
        3. Preparação da época chuvosa
        4. Projetos de infraestrutura prioritários
        """,
        "chairperson": "Governador Provincial",
        "secretary": "Chefe de Gabinete",
        "status": "completed",
        "is_public": False,
        "minutes_approved": True,
    },
]

# Exemplos de Decisões Administrativas
DECISIONS_EXAMPLES = [
    # Despacho do Governador
    {
        "institution_id": 1,  # Governo Provincial
        "decision_type": "despacho",
        "number": "001/GP-LDA/2024",
        "title": "Criação da Comissão Provincial de Emergência",
        "decision_date": date(2024, 1, 15),
        "publication_date": date(2024, 1, 20),
        "effective_date": date(2024, 1, 20),
        "issuing_authority": "Governador Provincial de Luanda",
        "authority_title": "Governador Provincial",
        "summary": "Cria comissão para coordenar ações de emergência na província durante a época chuvosa",
        "legal_basis": "Lei nº 17/16 - Lei da Organização e Funcionamento da Administração Local do Estado",
        "subject_area": "protecao_civil",
        "keywords": "emergência, época chuvosa, proteção civil, coordenação",
        "status": "published",
        "is_public": True,
        "requires_publication": True,
        "publication_medium": "Boletim Oficial da Província de Luanda",
        "publication_reference": "BO nº 03/2024",
        "target_audience": "Administrações municipais, direções provinciais, sociedade civil",
    },
    # Portaria Municipal
    {
        "institution_id": 2,  # Administração Municipal
        "decision_type": "portaria",
        "number": "002/AML/2024",
        "title": "Regulamento de Funcionamento dos Mercados Municipais",
        "decision_date": date(2024, 2, 10),
        "publication_date": date(2024, 2, 15),
        "effective_date": date(2024, 3, 1),
        "issuing_authority": "Administrador Municipal de Luanda",
        "authority_title": "Administrador Municipal",
        "summary": "Estabelece normas para funcionamento, higiene e segurança nos mercados municipais",
        "legal_basis": "Lei nº 17/16 - LOFALE, Regulamento Geral dos Mercados",
        "subject_area": "comercio",
        "keywords": "mercados, comércio, higiene, segurança, regulamento",
        "status": "published",
        "is_public": True,
        "requires_publication": True,
        "publication_medium": "Jornal de Angola",
        "implementation_deadline": date(2024, 4, 1),
        "responsible_for_implementation": "Direção Municipal de Comércio",
    },
    # Deliberação do CMAS
    {
        "institution_id": 5,  # CMAS
        "council_meeting_id": 1,  # Da reunião ordinária
        "decision_type": "deliberacao_cmas",
        "number": "001/CMAS-LDA/2024",
        "title": "Parecer sobre Projeto de Requalificação Urbana da Baixa de Luanda",
        "decision_date": date(2024, 3, 15),
        "issuing_authority": "Conselho Municipal de Auscultação Social",
        "authority_title": "CMAS de Luanda",
        "summary": "Parecer favorável ao projeto com recomendações sobre reassentamento de famílias",
        "subject_area": "urbanismo",
        "keywords": "requalificação urbana, baixa de luanda, reassentamento, participação social",
        "status": "approved",
        "is_public": True,
        "target_audience": "Administração Municipal, Governo Provincial, população afetada",
        "recommendations": """
        1. Garantir reassentamento digno das famílias afetadas
        2. Preservar patrimônio histórico e cultural
        3. Assegurar participação comunitária em todas as fases
        4. Criar programa de apoio aos comerciantes locais
        """,
    },
    # Ordem de Serviço
    {
        "institution_id": 4,  # Direção Provincial de Educação
        "decision_type": "ordem_servico",
        "number": "005/DPEL/2024",
        "title": "Início do Ano Letivo 2024 - Orientações Gerais",
        "decision_date": date(2024, 1, 30),
        "effective_date": date(2024, 2, 5),
        "issuing_authority": "Diretor Provincial de Educação",
        "authority_title": "Diretor Provincial",
        "summary": "Orientações para início do ano letivo, calendário escolar e procedimentos administrativos",
        "subject_area": "educacao",
        "keywords": "ano letivo, calendário escolar, matrículas, professores",
        "status": "published",
        "is_public": True,
        "target_audience": "Diretores escolares, professores, encarregados de educação",
        "implementation_deadline": date(2024, 2, 12),
        "responsible_for_implementation": "Direções Municipais de Educação",
    },
]


def get_sample_data() -> Dict[str, List[Dict[str, Any]]]:
    """Retorna todos os dados de exemplo organizados."""
    return {
        "institutions": INSTITUTIONS_EXAMPLES,
        "mandates": MANDATES_EXAMPLES,
        "council_meetings": COUNCIL_MEETINGS_EXAMPLES,
        "decisions": DECISIONS_EXAMPLES,
    }


def print_governance_structure():
    """Imprime a estrutura hierárquica de governance angolana."""
    print("🏛️  ESTRUTURA DE GOVERNANCE - ANGOLA")
    print("=" * 50)
    print()

    print("📍 HIERARQUIA ADMINISTRATIVA:")
    print("1️⃣  Governo Provincial (Nível 1)")
    print("   ├── Administração Municipal (Nível 2)")
    print("   │   ├── Administração Comunal (Nível 3)")
    print("   │   └── CMAS - Conselho Municipal de Auscultação Social (Nível 3)")
    print("   └── Direções Provinciais (Nível 2)")
    print("       └── Direções Municipais (Nível 3)")
    print()

    print("👥 TIPOS DE NOMEAÇÃO:")
    print("• Decreto Presidencial → Governadores Provinciais")
    print("• Despacho do Governador → Administradores Municipais")
    print("• Portaria Ministerial → Diretores Provinciais")
    print("• Despacho do Administrador → Administradores Comunais")
    print("• Designação Interna → Cargos técnicos")
    print("• Nomeação CMAS → Membros dos conselhos")
    print()

    print("📋 TIPOS DE DECISÕES:")
    print("• Despacho → Decisões administrativas gerais")
    print("• Portaria → Regulamentos e normas")
    print("• Deliberação CMAS → Pareceres e recomendações")
    print("• Ordem de Serviço → Instruções operacionais")
    print("• Circular → Comunicações internas")
    print("• Resolução → Decisões de conselhos")
    print()

    print("🏢 TIPOS DE REUNIÕES:")
    print("• CMAS Ordinária/Extraordinária → Participação social")
    print("• Conselho Provincial → Coordenação entre direções")
    print("• Gabinete do Governador → Decisões executivas")
    print("• Reunião Técnica → Coordenação operacional")


if __name__ == "__main__":
    print_governance_structure()

    sample_data = get_sample_data()
    print(f"\n📊 DADOS DE EXEMPLO DISPONÍVEIS:")
    print(f"• {len(sample_data['institutions'])} Instituições")
    print(f"• {len(sample_data['mandates'])} Mandatos")
    print(f"• {len(sample_data['council_meetings'])} Reuniões")
    print(f"• {len(sample_data['decisions'])} Decisões")
