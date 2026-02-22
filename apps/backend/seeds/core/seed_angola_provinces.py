"""
Seed das 21 Províncias de Angola + Estrutura Territorial Hierárquica

Hierarquia:
- Províncias (21)
  └─ Municípios (2+ por província)
     └─ Comunas (2+ por município)

Estrutura de código territorial:
- Províncias: 3 letras (ex: LUA, HUA, BEN)
- Municípios: PROV-MUN (ex: LUA-MUN1, HUA-BAL)
- Comunas: PROV-MUN-COM (ex: LUA-MUN1-COM1)
"""

import asyncio
import logging
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.territory.models.territory import Territory

logger = logging.getLogger(__name__)

# ==================== ANGOLA PROVINCES DATA ====================
ANGOLA_PROVINCES = [
    # Províncias com capitais e código ISO
    {
        "code": "LUA",
        "name": "Luanda",
        "type": "province",
        "municipalities": [
            {
                "code": "LUA-IC",
                "name": "Icolo e Bengo",
                "communes": ["Icolo Campus", "Bengo"]
            },
            {
                "code": "LUA-MAT",
                "name": "Mato Grosso",
                "communes": ["Mato Grosso"]
            },
        ]
    },
    {
        "code": "BEN",
        "name": "Benguela",
        "type": "province",
        "municipalities": [
            {
                "code": "BEN-BAI",
                "name": "Baía Farta",
                "communes": ["Baía Farta"]
            },
            {
                "code": "BEN-BOL",
                "name": "Bolan0s",
                "communes": ["Bolanos"]
            },
        ]
    },
    {
        "code": "HUA",
        "name": "Huambo",
        "type": "province",
        "municipalities": [
            {
                "code": "HUA-HUA",
                "name": "Huambo",
                "communes": ["Huambo Centro", "Bailundo", "Ekunha"]
            },
            {
                "code": "HUA-ECU",
                "name": "Ecunha",
                "communes": ["Ecunha Sede"]
            },
        ]
    },
    {
        "code": "HUI",
        "name": "Huíla",
        "type": "province",
        "municipalities": [
            {
                "code": "HUI-MO",
                "name": "Moçamedes",
                "communes": ["Moçamedes"]
            },
            {
                "code": "HUI-LU",
                "name": "Lubango",
                "communes": ["Lubango"]
            },
        ]
    },
    {
        "code": "NAM",
        "name": "Namibe",
        "type": "province",
        "municipalities": [
            {
                "code": "NAM-NAM",
                "name": "Namibe",
                "communes": ["Namibe Sede"]
            },
        ]
    },
    {
        "code": "ZAI",
        "name": "Zaire",
        "type": "province",
        "municipalities": [
            {
                "code": "ZAI-ZAI",
                "name": "Zaire",
                "communes": ["Zaire Sede"]
            },
        ]
    },
    {
        "code": "UIG",
        "name": "Uíge",
        "type": "province",
        "municipalities": [
            {
                "code": "UIG-UIG",
                "name": "Uíge",
                "communes": ["Uíge Sede"]
            },
            {
                "code": "UIG-BUI",
                "name": "Buila",
                "communes": ["Buila Sede"]
            },
        ]
    },
    {
        "code": "KAS",
        "name": "Kasai",
        "type": "province",
        "municipalities": [
            {
                "code": "KAS-KAS",
                "name": "Kasai",
                "communes": ["Kasai Sede"]
            },
        ]
    },
    {
        "code": "KUW",
        "name": "Kuanza Sul",
        "type": "province",
        "municipalities": [
            {
                "code": "KUW-SUL",
                "name": "Sumbe",
                "communes": ["Sumbe"]
            },
        ]
    },
    {
        "code": "KUN",
        "name": "Kuanza Norte",
        "type": "province",
        "municipalities": [
            {
                "code": "KUN-NOR",
                "name": "N'dalatando",
                "communes": ["N'dalatando"]
            },
        ]
    },
    {
        "code": "MAL",
        "name": "Malange",
        "type": "province",
        "municipalities": [
            {
                "code": "MAL-MAL",
                "name": "Malange",
                "communes": ["Malange Sede"]
            },
        ]
    },
    {
        "code": "MOX",
        "name": "Moxico",
        "type": "province",
        "municipalities": [
            {
                "code": "MOX-MOX",
                "name": "Moxico",
                "communes": ["Moxico Sede"]
            },
        ]
    },
    {
        "code": "NAK",
        "name": "Nakonde",
        "type": "province",
        "municipalities": [
            {
                "code": "NAK-NAK",
                "name": "Nakonde",
                "communes": ["Nakonde Sede"]
            },
        ]
    },
    {
        "code": "BIE",
        "name": "Bié",
        "type": "province",
        "municipalities": [
            {
                "code": "BIE-BIE",
                "name": "Kuito",
                "communes": ["Kuito"]
            },
        ]
    },
    {
        "code": "CAB",
        "name": "Cabinda",
        "type": "province",
        "municipalities": [
            {
                "code": "CAB-CAB",
                "name": "Cabinda",
                "communes": ["Cabinda Sede"]
            },
        ]
    },
    {
        "code": "CUE",
        "name": "Cuene",
        "type": "province",
        "municipalities": [
            {
                "code": "CUE-CUE",
                "name": "Cuene",
                "communes": ["Cuene Sede"]
            },
        ]
    },
    {
        "code": "LUN",
        "name": "Lunda Norte",
        "type": "province",
        "municipalities": [
            {
                "code": "LUN-LUN",
                "name": "Dundo",
                "communes": ["Dundo"]
            },
        ]
    },
    {
        "code": "LUS",
        "name": "Lunda Sul",
        "type": "province",
        "municipalities": [
            {
                "code": "LUS-LUS",
                "name": "Saurimo",
                "communes": ["Saurimo"]
            },
        ]
    },
    {
        "code": "CUA",
        "name": "Cuanza",
        "type": "province",
        "municipalities": [
            {
                "code": "CUA-CUA",
                "name": "Cuanza",
                "communes": ["Cuanza Sede"]
            },
        ]
    },
    {
        "code": "CON",
        "name": "Congo",
        "type": "province",
        "municipalities": [
            {
                "code": "CON-CON",
                "name": "Congo",
                "communes": ["Congo Sede"]
            },
        ]
    },
]


async def seed_angola_provinces():
    """Seed da hierarquia territorial de Angola"""
    
    async with AsyncSessionLocal() as db:
        logger.info("🌱 Iniciando seed das províncias de Angola...")
        logger.info(f"📊 {len(ANGOLA_PROVINCES)} províncias a inserir")
        
        for prov_data in ANGOLA_PROVINCES:
            try:
                # Verificar se província já existe
                query = select(Territory).where(Territory.code == prov_data["code"])
                existing = await db.execute(query)
                if existing.scalar():
                    logger.info(f"⏭️  Província {prov_data['name']} ({prov_data['code']}) já existe")
                    continue
                
                # Criar província
                province = Territory(
                    id=uuid4(),
                    name=prov_data["name"],
                    code=prov_data["code"],
                    type="province",
                    parent_id=None,  # Províncias são nível superior
                )
                db.add(province)
                await db.flush()  # Garantir ID gerado
                
                logger.info(f"✅ Província {prov_data['name']} criada")
                
                # Criar municípios
                for mun_data in prov_data.get("municipalities", []):
                    municipality = Territory(
                        id=uuid4(),
                        name=mun_data["name"],
                        code=mun_data["code"],
                        type="municipality",
                        parent_id=province.id,  # Filho da província
                    )
                    db.add(municipality)
                    await db.flush()
                    
                    logger.debug(f"  └─ Município {mun_data['name']} criado")
                    
                    # Criar comunas
                    for commune_name in mun_data.get("communes", []):
                        commune_code = f"{mun_data['code']}-{commune_name[:3].upper()}"
                        commune = Territory(
                            id=uuid4(),
                            name=commune_name,
                            code=commune_code,
                            type="commune",
                            parent_id=municipality.id,  # Filho do município
                        )
                        db.add(commune)
                        
                        logger.debug(f"      └─ Comuna {commune_name} criada")
            
            except Exception as e:
                logger.error(f"❌ Erro ao processar {prov_data['name']}: {e}")
                await db.rollback()
                return False
        
        try:
            await db.commit()
            logger.info("✅ Seed Angola completo! Todas as províncias, municípios e comunas criados.")
            return True
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ Erro ao fazer commit: {e}")
            return False


async def main():
    """Entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    success = await seed_angola_provinces()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
