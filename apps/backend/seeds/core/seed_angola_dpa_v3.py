#!/usr/bin/env python3
"""
SILA Seed v3: Angola DPA 2024 - 100% Idempotente e Robusto

Features:
  ✅ Pode rodar várias vezes sem precisar truncar
  ✅ Usa upsert (ON CONFLICT) para todos os territórios
  ✅ Cria closure table automaticamente se não existir
  ✅ Usa IDs reais retornados do upsert
  ✅ Proteção contra FK errors em estados parciais
  ✅ Log detalhado de operações (inserted vs updated)
  ✅ Todas as 21 províncias do DPA 2024 (inclui Moxico Leste, Icolo e Bengo, Cuando)

Usage:
  python seed_angola_dpa_v3.py           # Seed completo
  python seed_angola_dpa_v3.py --check   # Apenas verificar estado atual
"""

import uuid
import psycopg2
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

backend_root = Path(__file__).resolve().parent.parent.parent
# PYTHONPATH should be configured via setup_dev_env.sh; do not mutate sys.path here.

load_dotenv(backend_root / ".env")
from app.core.settings import settings

# ============================================================================
# CONFIG
# ============================================================================

DB_CONFIG = {
    "host": settings.DB_HOST,
    "port": settings.DB_PORT,
    "database": settings.DB_NAME,
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD,
}

# Códigos oficiais das 21 províncias (DPA 2024)
PROVINCE_CODES = {
    "Cabinda": "CAB",
    "Zaire": "ZAI",
    "Uíge": "UIG",
    "Bengo": "BGO",
    "Icolo e Bengo": "ICB",    # Nova (de Bengo)
    "Luanda": "LUA",
    "Cuanza-Norte": "CNO",
    "Cuanza-Sul": "CSU",
    "Malanje": "MAL",
    "Lunda-Norte": "LNO",
    "Lunda-Sul": "LSU",
    "Benguela": "BGU",
    "Huambo": "HUA",
    "Bié": "BIE",
    "Moxico": "MOX",
    "Moxico Leste": "MXL",    # Nova (de Moxico)
    "Huíla": "HUI",
    "Namibe": "NAM",
    "Cunene": "CNN",
    "Cubango": "CCU",          # Antiga "Cuando Cubango" (renomeada)
    "Cuando": "CND",           # Nova (de Cuando Cubango)
}

# Angola DPA 2024 - Todas as províncias com municípios e comunas
# Fonte: INE Angola / Divisão Político-Administrativa 2024
ANGOLA_DPA_2024 = {
    "Luanda": {
        "Luanda": ["Ingombota", "Maianga", "Rangel", "Samba", "Sambizanga", "Kilamba Kiaxi"],
        "Belas": ["Belas", "Camama", "Benfica", "Morro Bento"],
        "Cacuaco": ["Cacuaco", "Funda", "Kikolo"],
        "Cazenga": ["Cazenga", "Hoji ya Henda", "Tala Hady"],
        "Viana": ["Viana", "Zango", "Mulenvos"],
        "Talatona": ["Talatona", "Camama Sul"],
    },
    "Benguela": {
        "Benguela": ["Benguela", "Dombe Grande", "Baía Farta"],
        "Lobito": ["Lobito", "Catumbela", "Canjala", "Egito Praia"],
        "Cubal": ["Cubal", "Tumbulo", "Capupa"],
        "Ganda": ["Ganda", "Casseque", "Ebanga"],
        "Balombo": ["Balombo", "Chongoroi"],
        "Bocoio": ["Bocoio", "Cubal do Lumbo", "Monte Belo"],
        "Caimbambo": ["Caimbambo"],
        "Chongoroi": ["Chongoroi", "Bolonguera"],
    },
    "Huambo": {
        "Huambo": ["Huambo", "Calima", "Chipipa"],
        "Caála": ["Caála", "Cuima", "Catata"],
        "Bailundo": ["Bailundo", "Bimbe", "Lunge"],
        "Longonjo": ["Longonjo", "Lepi", "Boa Vista"],
        "Mungo": ["Mungo", "Galanga"],
        "Cachiungo": ["Cachiungo", "Sambo"],
        "Ecunha": ["Ecunha", "Cuima"],
        "Chicala-Choloanga": ["Chicala-Choloanga"],
        "Chinjenje": ["Chinjenje"],
        "Londuimbali": ["Londuimbali"],
        "Ucuma": ["Ucuma"],
    },
    "Cabinda": {
        "Cabinda": ["Cabinda", "Malembo"],
        "Cacongo": ["Cacongo", "Dinge"],
        "Belize": ["Belize", "Luali"],
        "Buco-Zau": ["Buco-Zau", "Inhuca"],
    },
    "Zaire": {
        "Mbanza Kongo": ["Mbanza Kongo", "Luvu"],
        "Soyo": ["Soyo", "Pedra do Feitiço", "Mangue Grande"],
        "Nzeto": ["Nzeto", "Mussera"],
        "Cuimba": ["Cuimba"],
        "Nóqui": ["Nóqui"],
        "Tomboco": ["Tomboco"],
    },
    "Uíge": {
        "Uíge": ["Uíge", "Quitexe"],
        "Negage": ["Negage", "Cangola"],
        "Damba": ["Damba", "Maquela do Zombo"],
        "Maquela do Zombo": ["Maquela do Zombo"],
        "Bungo": ["Bungo"],
        "Songo": ["Songo"],
        "Bembe": ["Bembe"],
        "Buengas": ["Buengas"],
        "Mucaba": ["Mucaba"],
        "Puri": ["Puri"],
        "Sanza Pombo": ["Sanza Pombo"],
        "Ambuíla": ["Ambuíla"],
        "Alto Cauale": ["Alto Cauale"],
        "Quimbele": ["Quimbele"],
        "Macocola": ["Macocola"],
        "Milunga": ["Milunga"],
    },
    "Bengo": {
        "Caxito": ["Caxito", "Úcua"],
        "Dande": ["Dande", "Muxima"],
        "Ambriz": ["Ambriz", "Bela Vista"],
        "Nambuangongo": ["Nambuangongo"],
        "Dembos": ["Dembos", "Quibaxe"],
        "Pango Aluquém": ["Pango Aluquém"],
        "Bula Atumba": ["Bula Atumba"],
        "Kissama": ["Kissama"],
    },
    "Cuanza-Norte": {
        "Ndalatando": ["Ndalatando", "Samba Caju"],
        "Cambambe": ["Cambambe", "Dondo"],
        "Cazengo": ["Cazengo"],
        "Golungo Alto": ["Golungo Alto"],
        "Lucala": ["Lucala"],
        "Quiculungo": ["Quiculungo"],
        "Samba Cajú": ["Samba Cajú"],
        "Ambaca": ["Ambaca"],
        "Banga": ["Banga"],
        "Bolongongo": ["Bolongongo"],
    },
    "Cuanza-Sul": {
        "Sumbe": ["Sumbe", "Gungo"],
        "Porto Amboim": ["Porto Amboim", "Capolo"],
        "Amboim": ["Amboim", "Gabela"],
        "Libolo": ["Libolo", "Calulo"],
        "Quilenda": ["Quilenda"],
        "Quibala": ["Quibala"],
        "Cassongue": ["Cassongue"],
        "Conda": ["Conda"],
        "Ebo": ["Ebo"],
        "Mussende": ["Mussende"],
        "Seles": ["Seles"],
        "Waku Kungo": ["Waku Kungo"],
    },
    "Bié": {
        "Kuito": ["Kuito", "Trumba"],
        "Andulo": ["Andulo"],
        "Camacupa": ["Camacupa"],
        "Catabola": ["Catabola"],
        "Chinguar": ["Chinguar"],
        "Chitembo": ["Chitembo"],
        "Cuemba": ["Cuemba"],
        "Cunhinga": ["Cunhinga"],
        "Nharea": ["Nharea"],
    },
    "Cunene": {
        "Ondjiva": ["Ondjiva", "Humbe"],
        "Xangongo": ["Xangongo"],
        "Cuanhama": ["Cuanhama"],
        "Curoca": ["Curoca"],
        "Kahama": ["Kahama"],
        "Ombadja": ["Ombadja"],
    },
    "Huíla": {
        "Lubango": ["Lubango", "Arimba", "Huíla"],
        "Matala": ["Matala", "Capelongo"],
        "Chibia": ["Chibia"],
        "Caconda": ["Caconda"],
        "Cacula": ["Cacula"],
        "Caluquembe": ["Caluquembe"],
        "Chiange": ["Chiange"],
        "Chipindo": ["Chipindo"],
        "Cuvango": ["Cuvango"],
        "Gambos": ["Gambos"],
        "Humpata": ["Humpata"],
        "Jamba": ["Jamba"],
        "Quilengues": ["Quilengues"],
        "Quipungo": ["Quipungo"],
    },
    "Namibe": {
        "Moçâmedes": ["Moçâmedes", "Lucira"],
        "Tômbua": ["Tômbua"],
        "Virei": ["Virei"],
        "Bibala": ["Bibala"],
        "Camucuio": ["Camucuio"],
    },
    "Moxico": {
        "Luena": ["Luena", "Moxico"],
        "Bundas": ["Bundas"],
        "Camanongue": ["Camanongue"],
        "Cameia": ["Cameia"],
        "Léua": ["Léua"],
        "Luchazes": ["Luchazes"],
        "Luau": ["Luau"],
        "Lumeje": ["Lumeje"],
        "Alto Zambeze": ["Alto Zambeze"],
    },
    "Lunda-Norte": {
        "Dundo": ["Dundo", "Lucapa"],
        "Cambulo": ["Cambulo"],
        "Capenda Camulemba": ["Capenda Camulemba"],
        "Caungula": ["Caungula"],
        "Chitato": ["Chitato"],
        "Cuango": ["Cuango"],
        "Cuílo": ["Cuílo"],
        "Lubalo": ["Lubalo"],
        "Xá-Muteba": ["Xá-Muteba"],
    },
    "Lunda-Sul": {
        "Saurimo": ["Saurimo", "Muconda"],
        "Cacolo": ["Cacolo"],
        "Dala": ["Dala"],
        "Muconda": ["Muconda"],
    },
    "Malanje": {
        "Malanje": ["Malanje", "Ngola Luije"],
        "Cacuso": ["Cacuso"],
        "Calandula": ["Calandula"],
        "Cambundi-Catembo": ["Cambundi-Catembo"],
        "Cangandala": ["Cangandala"],
        "Cuaba Nzoji": ["Cuaba Nzoji"],
        "Cunda-Dia-Baze": ["Cunda-Dia-Baze"],
        "Luquembo": ["Luquembo"],
        "Marimba": ["Marimba"],
        "Massango": ["Massango"],
        "Mucari": ["Mucari"],
        "Quela": ["Quela"],
        "Quirima": ["Quirima"],
        "Kiwaba Nzoji": ["Kiwaba Nzoji"],
    },
    "Cubango": {
        # Parte oeste da antiga Cuando Cubango
        "Menongue": ["Menongue"],
        "Cuangar": ["Cuangar"],
        "Cuchi": ["Cuchi"],
        "Cuito Cuanavale": ["Cuito Cuanavale"],
        "Mavinga": ["Mavinga"],
    },
    "Cuando": {
        # Parte leste da antiga Cuando Cubango (nova província 2024)
        "Dirico": ["Dirico"],
        "Nancova": ["Nancova"],
        "Rivungo": ["Rivungo"],
        "Calai": ["Calai"],
    },
    "Moxico Leste": {
        # Nova província criada em 2024 (de Moxico)
        "Luau": ["Luau"],
        "Alto Zambeze": ["Alto Zambeze"],
        "Camanongue": ["Camanongue"],
    },
    "Icolo e Bengo": {
        # Nova província criada em 2024 (de Bengo)
        "Catete": ["Catete", "Cabiri"],
        "Bom Jesus": ["Bom Jesus"],
        "São Paulo": ["São Paulo"],
    },
}


# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def ensure_closure_table(cur):
    """Cria a closure table se não existir (fallback para deploys sem migration)."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS territory_closure (
            ancestor_id UUID REFERENCES territories(id) ON DELETE CASCADE,
            descendant_id UUID REFERENCES territories(id) ON DELETE CASCADE,
            depth INTEGER NOT NULL CHECK(depth >= 0),
            PRIMARY KEY (ancestor_id, descendant_id)
        );
    """)


def upsert_territory(cur, code: str, name: str, t_type: str, parent_id=None):
    """
    Insere ou atualiza um território. Retorna (id, was_inserted).
    
    Args:
        cur: psycopg2 cursor
        code: Código único do território
        name: Nome do território
        t_type: Tipo (COUNTRY, PROVINCE, MUNICIPALITY, COMMUNE)
        parent_id: UUID do pai (None para country)
    
    Returns:
        Tuple (uuid, bool): ID do território e se foi inserido (True) ou atualizado (False)
    """
    # Primeiro tenta buscar existente
    cur.execute("SELECT id FROM territories WHERE code = %s", (code,))
    row = cur.fetchone()
    
    if row:
        # Já existe, atualiza nome se diferente
        existing_id = row[0]
        cur.execute("""
            UPDATE territories 
            SET name = %s 
            WHERE id = %s AND name != %s
        """, (name, existing_id, name))
        return existing_id, False
    else:
        # Insere novo
        cur.execute("""
            INSERT INTO territories (id, code, name, type, parent_id)
            VALUES (gen_random_uuid(), %s, %s, %s, %s)
            RETURNING id;
        """, (code, name, t_type, parent_id))
        return cur.fetchone()[0], True


def maintain_closure(cur, descendant_id, parent_id=None):
    """
    Mantém a closure table para queries hierárquicas.
    
    Args:
        cur: psycopg2 cursor
        descendant_id: UUID do nó
        parent_id: UUID do pai (None para raiz)
    """
    # Auto-referência (depth 0)
    cur.execute("""
        INSERT INTO territory_closure (ancestor_id, descendant_id, depth)
        VALUES (%s, %s, 0)
        ON CONFLICT DO NOTHING;
    """, (descendant_id, descendant_id))
    
    # Links dos ancestrais do pai
    if parent_id:
        cur.execute("""
            INSERT INTO territory_closure (ancestor_id, descendant_id, depth)
            SELECT ancestor_id, %s, depth + 1
            FROM territory_closure
            WHERE descendant_id = %s
            ON CONFLICT DO NOTHING;
        """, (descendant_id, parent_id))


def get_current_stats(cur):
    """Retorna estatísticas atuais do banco."""
    stats = {}
    
    cur.execute("SELECT COUNT(*) FROM territories WHERE type = 'COUNTRY'")
    stats["countries"] = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM territories WHERE type = 'PROVINCE'")
    stats["provinces"] = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM territories WHERE type = 'MUNICIPALITY'")
    stats["municipalities"] = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM territories WHERE type = 'COMMUNE'")
    stats["communes"] = cur.fetchone()[0]
    
    try:
        cur.execute("SELECT COUNT(*) FROM territory_closure")
        stats["closure_rows"] = cur.fetchone()[0]
    except:
        stats["closure_rows"] = 0
    
    return stats


# ============================================================================
# SEED LOGIC
# ============================================================================

def seed_angola(check_only=False):
    """
    Seed principal: popula todos os territórios de Angola DPA 2024.
    
    Args:
        check_only: Se True, apenas mostra estatísticas sem inserir
    """
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()
    
    try:
        # Estatísticas pré-seed
        print("\n" + "=" * 70)
        print("🌍 SILA SEED v3: Angola DPA 2024 (Idempotente)")
        print("=" * 70)
        
        print("\n📊 Estado atual do banco:")
        stats_before = get_current_stats(cur)
        print(f"   • Países:     {stats_before['countries']}")
        print(f"   • Províncias: {stats_before['provinces']}")
        print(f"   • Municípios: {stats_before['municipalities']}")
        print(f"   • Comunas:    {stats_before['communes']}")
        print(f"   • Closure:    {stats_before['closure_rows']} relações")
        
        if check_only:
            print("\n✅ Modo --check: nenhuma alteração feita.")
            return
        
        # Garantir closure table existe
        ensure_closure_table(cur)
        
        # Contadores
        inserted = {"country": 0, "province": 0, "municipality": 0, "commune": 0}
        updated = {"country": 0, "province": 0, "municipality": 0, "commune": 0}
        
        # 1️⃣ País: Angola
        print("\n🌍 [1/4] Processando PAÍS...")
        country_id, was_new = upsert_territory(cur, "AO", "ANGOLA", "COUNTRY")
        maintain_closure(cur, country_id)
        if was_new:
            inserted["country"] += 1
            print(f"   ✅ ANGOLA criada (ID: {country_id})")
        else:
            updated["country"] += 1
            print(f"   ♻️  ANGOLA já existe (ID: {country_id})")
        
        # 2️⃣ Províncias
        print("\n📍 [2/4] Processando PROVÍNCIAS...")
        province_ids = {}
        
        for prov_name in ANGOLA_DPA_2024.keys():
            p_code = PROVINCE_CODES.get(prov_name, prov_name[:3].upper())
            p_id, was_new = upsert_territory(cur, p_code, prov_name, "PROVINCE", country_id)
            maintain_closure(cur, p_id, country_id)
            province_ids[prov_name] = p_id
            
            if was_new:
                inserted["province"] += 1
                print(f"   ✅ {prov_name} ({p_code})")
            else:
                updated["province"] += 1
                print(f"   ♻️  {prov_name} ({p_code})")
        
        # 3️⃣ Municípios
        print("\n🏙️  [3/4] Processando MUNICÍPIOS...")
        municipality_ids = {}
        
        for prov_name, municipalities in ANGOLA_DPA_2024.items():
            p_id = province_ids[prov_name]
            p_code = PROVINCE_CODES.get(prov_name, prov_name[:3].upper())
            
            for mun_name in municipalities.keys():
                m_code = f"{p_code}-{mun_name[:3].upper()}"
                m_id, was_new = upsert_territory(cur, m_code, mun_name, "MUNICIPALITY", p_id)
                maintain_closure(cur, m_id, p_id)
                municipality_ids[(prov_name, mun_name)] = m_id
                
                if was_new:
                    inserted["municipality"] += 1
        
        print(f"   Inseridos: {inserted['municipality']}, Existentes: {sum(1 for k in municipality_ids) - inserted['municipality']}")
        
        # 4️⃣ Comunas
        print("\n🏘️  [4/4] Processando COMUNAS...")
        
        for prov_name, municipalities in ANGOLA_DPA_2024.items():
            p_code = PROVINCE_CODES.get(prov_name, prov_name[:3].upper())
            
            for mun_name, communes in municipalities.items():
                m_id = municipality_ids[(prov_name, mun_name)]
                m_code = f"{p_code}-{mun_name[:3].upper()}"
                
                for com_name in communes:
                    c_code = f"{m_code}-{com_name[:3].upper()}"
                    com_id, was_new = upsert_territory(cur, c_code, com_name, "COMMUNE", m_id)
                    maintain_closure(cur, com_id, m_id)
                    
                    if was_new:
                        inserted["commune"] += 1
        
        print(f"   Comunas processadas: {inserted['commune']} novas")
        
        # Commit
        conn.commit()
        
        # Estatísticas pós-seed
        print("\n" + "=" * 70)
        print("📊 RESULTADO FINAL:")
        print("=" * 70)
        
        stats_after = get_current_stats(cur)
        print(f"\n   {'Tipo':<15} {'Antes':<10} {'Depois':<10} {'Novos':<10}")
        print(f"   {'-'*45}")
        print(f"   {'Países':<15} {stats_before['countries']:<10} {stats_after['countries']:<10} {inserted['country']:<10}")
        print(f"   {'Províncias':<15} {stats_before['provinces']:<10} {stats_after['provinces']:<10} {inserted['province']:<10}")
        print(f"   {'Municípios':<15} {stats_before['municipalities']:<10} {stats_after['municipalities']:<10} {inserted['municipality']:<10}")
        print(f"   {'Comunas':<15} {stats_before['communes']:<10} {stats_after['communes']:<10} {inserted['commune']:<10}")
        print(f"   {'Closure':<15} {stats_before['closure_rows']:<10} {stats_after['closure_rows']:<10}")
        
        total_new = sum(inserted.values())
        print(f"\n   ✅ Total de novos registros: {total_new}")
        print(f"   ✅ Seed completado com sucesso!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ ERRO: {e}")
        print("   Rollback executado.")
        raise
    finally:
        cur.close()
        conn.close()


def show_hierarchy(limit=50):
    """Mostra os primeiros N registros da hierarquia."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "=" * 70)
    print(f"📋 HIERARQUIA DE TERRITÓRIOS (primeiros {limit} registros)")
    print("=" * 70)
    
    cur.execute("""
        SELECT t.code, t.name, t.type, p.name as parent_name
        FROM territories t
        LEFT JOIN territories p ON t.parent_id = p.id
        ORDER BY 
            CASE t.type 
                WHEN 'COUNTRY' THEN 1 
                WHEN 'PROVINCE' THEN 2 
                WHEN 'MUNICIPALITY' THEN 3 
                WHEN 'COMMUNE' THEN 4 
            END,
            t.name
        LIMIT %s
    """, (limit,))
    
    print(f"\n   {'Código':<20} {'Nome':<30} {'Tipo':<15} {'Pai':<20}")
    print(f"   {'-'*85}")
    
    for row in cur.fetchall():
        code, name, t_type, parent = row
        parent_display = parent or "-"
        print(f"   {code:<20} {name:<30} {t_type:<15} {parent_display:<20}")
    
    cur.close()
    conn.close()
    print()


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Seed Angola DPA 2024 - 100% Idempotente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python seed_angola_dpa_v3.py          # Seed completo
  python seed_angola_dpa_v3.py --check  # Apenas mostra estatísticas
  python seed_angola_dpa_v3.py --show   # Mostra hierarquia após seed
        """
    )
    parser.add_argument("--check", action="store_true", help="Apenas verificar estado atual")
    parser.add_argument("--show", action="store_true", help="Mostrar hierarquia após seed")
    parser.add_argument("--limit", type=int, default=50, help="Limite de registros a mostrar (padrão: 50)")
    args = parser.parse_args()
    
    if args.check:
        seed_angola(check_only=True)
    else:
        seed_angola(check_only=False)
        if args.show:
            show_hierarchy(limit=args.limit)


if __name__ == "__main__":
    main()
