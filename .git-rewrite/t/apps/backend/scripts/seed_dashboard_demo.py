#!/usr/bin/env python3
"""
Seed Dashboard Script - SILA System
Demonstração com dados simulados

Este script popula o dashboard com dados realistas.
Para usar em produção, configure o banco de dados em .env
"""

import asyncio
import random
from datetime import datetime, timedelta, UTC
import json

# ===========================
# Data Pools (Angola 2025)
# ===========================

NOMES = [
    "Ana", "João", "Maria", "Pedro", "Luísa", "Carlos", "Beatriz", "António",
    "Sofia", "Miguel", "Margarida", "Gonçalo", "Filipa", "Nuno", "Joana"
]

SOBRENOMES = [
    "da Silva", "dos Santos", "Pereira", "Costa", "Lopes", "Ferreira",
    "Gomes", "Rodrigues", "Almeida", "Marques", "Oliveira", "Sousa",
    "Martins", "Correia", "Vieira"
]

# ===========================
# Funções Auxiliares
# ===========================

def gerar_nome() -> str:
    """Gera nome aleatório realista"""
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"

def gerar_email(nome: str, idx: int) -> str:
    """Gera email corporativo .gov.ao"""
    primeiro = nome.split()[0].lower()
    return f"{primeiro}{idx}@sila.gov.ao"

def gerar_bi() -> str:
    """Gera número de Bilhete de Identidade realista (Angola)"""
    return f"{random.randint(1000000, 9999999)}LA{random.randint(10,99)}"

def gerar_data_aleatoria(dias_atras: int = 365) -> str:
    """Gera data aleatória nos últimos N dias (ISO format)"""
    data = datetime.now(UTC) - timedelta(days=random.randint(0, dias_atras))
    return data.isoformat()

# ===========================
# Seed Data Generators
# ===========================

def gerar_usuarios(quantidade: int = 89) -> list:
    """Gera lista de usuários realistas"""
    print(f"  ➕ Gerando {quantidade} usuários...")
    
    usuarios = []
    
    # Admin
    usuarios.append({
        "id": 1,
        "email": "admin@sila.gov.ao",
        "name": "Admin SILA",
        "is_active": True,
        "created_at": (datetime.now(UTC) - timedelta(days=365)).isoformat()
    })
    
    # Outros usuários
    for i in range(2, quantidade + 1):
        nome = gerar_nome()
        usuarios.append({
            "id": i,
            "email": gerar_email(nome, i),
            "name": nome,
            "is_active": random.choice([True, True, True, False]),
            "created_at": gerar_data_aleatoria(180)
        })
    
    return usuarios

def gerar_documentos(quantidade: int = 1247) -> list:
    """Gera lista de documentos realistas"""
    print(f"  ➕ Gerando {quantidade} documentos...")
    
    documentos = []
    
    for i in range(1, quantidade + 1):
        nome_beneficiario = gerar_nome()
        documentos.append({
            "id": i,
            "filename": f"doc_{datetime.now(UTC).strftime('%Y%m%d')}_{i+1000}.pdf",
            "original_name": f"Certidão_{nome_beneficiario.replace(' ', '_')}_{random.randint(1970,2005)}.pdf",
            "file_size": random.randint(80000, 5000000),
            "uploaded_by_id": random.randint(1, 89),
            "created_at": gerar_data_aleatoria(365)
        })
    
    return documentos

def gerar_citizenship_requests(quantidade: int = 42) -> list:
    """Gera lista de citizenship requests"""
    print(f"  ➕ Gerando {quantidade} atividades (citizenship requests)...")
    
    statuses = ["approved", "pending", "processing", "rejected"]
    atividades = []
    
    for i in range(1, quantidade + 1):
        nome = gerar_nome()
        atividades.append({
            "id": i,
            "full_name": nome,
            "bi_number": gerar_bi(),
            "status": random.choice(statuses),
            "created_at": gerar_data_aleatoria(30)
        })
    
    return atividades

def gerar_complaints(quantidade: int = 17) -> list:
    """Gera lista de reclamações"""
    print(f"  ➕ Gerando {quantidade} reclamações...")
    
    statuses = ["pending", "open", "in_progress", "closed"]
    complaints = []
    
    for i in range(1, quantidade + 1):
        complaints.append({
            "id": i,
            "title": f"Reclamação #{i:03d}",
            "description": f"Problema com serviço - Descrição detalhada #{i}",
            "status": random.choice(statuses),
            "created_at": gerar_data_aleatoria(30)
        })
    
    return complaints

# ===========================
# Main Execution
# ===========================

def main():
    """Executa seed e salva em arquivo JSON"""
    
    print("\n" + "="*70)
    print("🌱 SEED DASHBOARD - SILA SYSTEM (Angola 2025)")
    print("="*70 + "\n")
    
    print("📊 Gerando dados seed...\n")
    
    # Gerar dados
    usuarios = gerar_usuarios(89)
    documentos = gerar_documentos(1247)
    citizenship_requests = gerar_citizenship_requests(42)
    complaints = gerar_complaints(17)
    
    # Preparar dados para salvamento
    dados_completos = {
        "timestamp": datetime.now(UTC).isoformat(),
        "statistics": {
            "usuarios": len(usuarios),
            "documentos": len(documentos),
            "citizenship_requests": len(citizenship_requests),
            "complaints": len(complaints),
            "total": len(usuarios) + len(documentos) + len(citizenship_requests) + len(complaints)
        },
        "data": {
            "usuarios": usuarios,
            "documentos": documentos,
            "citizenship_requests": citizenship_requests,
            "complaints": complaints
        }
    }
    
    # Salvar em arquivo JSON
    output_file = "seed_data_dashboard.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("✅ SEED DATA GERADO COM SUCESSO!")
    print("="*70)
    print(f"\n📊 Dados Populados:")
    print(f"   • {len(usuarios):>6} Usuários")
    print(f"   • {len(documentos):>6} Documentos")
    print(f"   • {len(citizenship_requests):>6} Atividades (Citizenship Requests)")
    print(f"   • {len(complaints):>6} Reclamações (Complaints)")
    print(f"   {'─' * 45}")
    print(f"   • {dados_completos['statistics']['total']:>6} TOTAL DE REGISTROS")
    
    print(f"\n💾 Dados salvos em: {output_file}")
    print(f"\n🔧 Próximos Passos:")
    print(f"   1. Certifique-se que o PostgreSQL está rodando")
    print(f"   2. Configure o .env com DATABASE_URL válido")
    print(f"   3. Execute as migrações: alembic upgrade head")
    print(f"   4. Execute o script com banco ativo: python scripts/seed_dashboard_db.py")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
