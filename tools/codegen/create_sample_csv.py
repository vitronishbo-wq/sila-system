#!/usr/bin/env python3
"""
Sample CSV file for SILA service generation.

This file demonstrates the CSV format expected by the generate_module.py batch command.
Copy this file and modify it for your specific needs.

CSV Format:
- module: The target module name (must exist)
- service_key: Unique identifier for the service (PascalCase)
- service_name_pt: Portuguese display name
- service_name_en: English display name
- service_type: 'citizen' or 'internal' (optional, defaults to 'citizen')

Usage:
    python tools/codegen/generate_module.py batch --csv sample_services.csv
"""

import csv
from pathlib import Path


def create_sample_csv():
    """Create a sample CSV file with common SILA services."""

    sample_services = [
        # Health Module Services
        [
            "health",
            "AgendamentoConsulta",
            "Agendamento de Consulta",
            "Medical Appointment Booking",
            "citizen",
        ],
        [
            "health",
            "SolicitacaoExame",
            "Solicitação de Exame",
            "Lab Test Request",
            "citizen",
        ],
        [
            "health",
            "AgendamentoVacinacao",
            "Agendamento de Vacinação",
            "Vaccination Appointment",
            "citizen",
        ],
        [
            "health",
            "ConsultaTelemedicina",
            "Consulta de Telemedicina",
            "Telemedicine Consultation",
            "citizen",
        ],
        [
            "health",
            "EmergenciaMedica",
            "Emergência Médica",
            "Medical Emergency",
            "citizen",
        ],
        [
            "health",
            "RenovacaoReceita",
            "Renovação de Receita",
            "Prescription Renewal",
            "citizen",
        ],
        # Citizenship Module Services
        [
            "citizenship",
            "EmissaoBI",
            "Emissão de Bilhete de Identidade",
            "ID Card Issuance",
            "citizen",
        ],
        [
            "citizenship",
            "AtualizacaoEndereco",
            "Atualização de Endereço",
            "Address Update",
            "citizen",
        ],
        [
            "citizenship",
            "CertidaoNascimento",
            "Certidão de Nascimento",
            "Birth Certificate",
            "citizen",
        ],
        [
            "citizenship",
            "RegistroCivil",
            "Registro Civil",
            "Civil Registration",
            "citizen",
        ],
        ["citizenship", "AlteracaoNome", "Alteração de Nome", "Name Change", "citizen"],
        # Education Module Services
        [
            "education",
            "MatriculaEscolar",
            "Matrícula Escolar",
            "School Enrollment",
            "citizen",
        ],
        [
            "education",
            "TransferenciaEscolar",
            "Transferência Escolar",
            "School Transfer",
            "citizen",
        ],
        [
            "education",
            "HistoricoEscolar",
            "Histórico Escolar",
            "Academic Record",
            "citizen",
        ],
        [
            "education",
            "CertificadoConclusao",
            "Certificado de Conclusão",
            "Completion Certificate",
            "citizen",
        ],
        [
            "education",
            "BolsaEstudo",
            "Bolsa de Estudo",
            "Scholarship Application",
            "citizen",
        ],
        # Commercial Module Services (Internal)
        [
            "commercial",
            "AberturaProcesso",
            "Abertura de Processo",
            "Process Opening",
            "internal",
        ],
        [
            "commercial",
            "LicencaFuncionamento",
            "Licença de Funcionamento",
            "Operating License",
            "internal",
        ],
        [
            "commercial",
            "RegistroEmpresa",
            "Registro de Empresa",
            "Company Registration",
            "internal",
        ],
        [
            "commercial",
            "AlvaraFuncionamento",
            "Alvará de Funcionamento",
            "Operating Permit",
            "internal",
        ],
        [
            "commercial",
            "TaxaInspecao",
            "Taxa de Inspeção",
            "Inspection Fee",
            "internal",
        ],
        # Urbanism Module Services (Internal)
        [
            "urbanism",
            "LicencaConstrucao",
            "Licença de Construção",
            "Building Permit",
            "internal",
        ],
        [
            "urbanism",
            "AprovacaoProjeto",
            "Aprovação de Projeto",
            "Project Approval",
            "internal",
        ],
        ["urbanism", "HabiteSe", "Habite-se", "Occupancy Permit", "internal"],
        [
            "urbanism",
            "ParcelamentoSolo",
            "Parcelamento do Solo",
            "Land Division",
            "internal",
        ],
        [
            "urbanism",
            "ZoneamentoUso",
            "Zoneamento e Uso do Solo",
            "Zoning and Land Use",
            "internal",
        ],
        # Finance Module Services
        ["finance", "PagamentoTaxa", "Pagamento de Taxa", "Fee Payment", "citizen"],
        [
            "finance",
            "EmissaoGuia",
            "Emissão de Guia",
            "Payment Guide Issuance",
            "citizen",
        ],
        ["finance", "ConsultaDebito", "Consulta de Débito", "Debt Inquiry", "citizen"],
        [
            "finance",
            "ParcelamentoDivida",
            "Parcelamento de Dívida",
            "Debt Installment",
            "citizen",
        ],
        ["finance", "IsencaoTaxa", "Isenção de Taxa", "Fee Exemption", "citizen"],
    ]

    # Create CSV file
    csv_path = Path(__file__).parent / "sample_services.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_services)

    print(f"✅ Sample CSV created: {csv_path}")
    print(f"   Total services: {len(sample_services)}")
    print(f"   Modules covered: {len(set(row[0] for row in sample_services))}")
    print()
    print("Usage examples:")
    print("   # Generate all services")
    print(f"   python tools/codegen/generate_module.py batch --csv {csv_path}")
    print()
    print("   # Generate only citizen services")
    print(f"   python tools/codegen/generate_module.py batch --csv {csv_path} --type citizen")
    print()
    print("   # Generate only internal services")
    print(f"   python tools/codegen/generate_module.py batch --csv {csv_path} --type internal")
    print()
    print("Note: Make sure target modules exist before running generation.")


if __name__ == "__main__":
    create_sample_csv()
