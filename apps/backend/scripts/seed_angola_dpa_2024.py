import asyncio
import logging
from sqlalchemy import select
from config.database import AsyncSessionLocal
from modules.location.models.region import Region

logging.basicConfig(level=logging.INFO, format="%(asctime)s [INFO] %(message)s")
logger = logging.getLogger("seed_dpa")

# Dados da DPA 2024 conforme Lei 15/24
# (Exemplo reduzido - expanda com a lista completa de províncias e municípios)
ANGOLA_DPA = {
    "ANGOLA": {
        "Cabinda": {
            "BELIZE": ["Luali", "Belize"],
            "BUCO-ZAU": [],
            "CABINDA": [],
            "CACONGO": ["Dinge", "Lândana"],
            "MICONJE": [],
            "MASSABI": [],
            "NECUTO": ["Necuto", "Inhuca"],
            "TANDO ZINZE": ["Tando Zinze", "Malembo"],
            "LIAMBO": [],
            "NGOIO": [],
        },
        "Zaire": {
            "MBANZA KONGO": ["Mbanza Kongo", "Caluca", "Madimba", "Quiende"],
            "SOYO": ["Soyo", "Pedra de Feitiço"],
            "NZETO": ["Nzeto", "Musserra", "Quibala Norte"],
            "CUIMBA": ["Cuimba", "Buela", "Luvaca"],
            "NÓQUI": ["Mpala"],
            "TOMBOCO": ["Tomboco", "Quinsimba", "Quinzau"],
            "LUVO": [],
            "LUFICO": ["Lufico"],
            "QUÊLO": [],
            "SERRA DE CANDA": [],
            "QUINDEJE": ["Quibala-Norte", "Quindeje"],
        },
        "Uíge": {
            "UÍGE": ["Uíge", "Luanga", "Casseche", "Cancungo"],
            "CANGOLA": ["Cangola", "Bengo", "Caiongo"],
            "AMBUÍLA": [],
            "BEMBE": ["Bembe", "Mabaia"],
            "NOVA ESPERANÇA": ["Nova Esperança", "Buenga-Sul", "Cuilo Camboso"],
            "BUNGO": [],
            "MILUNGA": ["Milunga", "Macocola"],
            "DAMBA": ["Damba", "Petecusso", "Camatambo", "Lêmboa"],
            "MAQUELA DO ZOMBO": ["Maquela do Zombo", "Quibocolo"],
            "MUCABA": ["Mucaba", "Uando Mucaba"],
            "NEGAGE": ["Negage", "Dimuca", "Quisseque"],
            "PURI": [],
            "QUIMBELE": ["Quimbele", "Icoca"],
            "DANGE QUITEXE": ["Quitexe", "Aldeia Viçosa"],
            "SANZA POMBO": ["Sanza Pombo", "Cuilo Pombo", "Uamba", "Alfândega"],
            "SONGO": ["Songo", "Quivuenga"],
            "SACANDICA": ["Sacandica", "Cuilo Futa", "Béu"],
            "NSOSSO": [],
            "LUCUNG": [],
            "QUIPEDRO": [],
            "MASSAU": ["Massau", "Macolo"],
            "VISTA ALEGRE": ["Vista Alegre", "Cambamba"],
            "ALTO ZAZA": ["Alto Zaza", "Cuango Calumbo"],
        },
        "Bengo": {
            "BULA ATUMBA": ["Bula Atumba", "Quiage"],
            "DANDE": ["Caxito", "Mabubas", "Quicabo"],
            "QUIBAXE": ["Coxe", "Paredes", "Quibaxe"],
            "NAMBUANGONGO": ["Canacassala", "Gombe", "Zala"],
            "PANGO ALUQUÉM": ["Pango Aluquém", "Cazuangongo"],
            "AMBRIZ": ["Ambriz", "Bela Vista", "Tabi"],
            "MUXALUANDO": ["Muxaluando", "Quixico", "Cage Mazumbo"],
            "PIRI": [],
            "QUICUNZO": [],
            "ÚCUA": [],
            "PANGUILA": [],
            "BARRA DO DANDE": [],
        },
        "Cuanza-Norte": {
            "AMBACA": ["Camabatela", "Máua", "Bindo"],
            "BANGA": ["Banga", "Cariamba"],
            "BOLONGONGO": [],
            "CAMBAMBE": ["Dondo", "Dange ya Menha", "São Pedro da Quilemba"],
            "CAZENGO": ["Caculo Camuiza", "Ndalatando"],
            "GOLUNGO ALTO": ["Golungo Alto", "Cambondo", "Quilombo quía Puto"],
            "LUCALA": ["Lucala", "Quiangombe"],
            "NGONGUEMBO": ["Quilombo dos Dembos", "Camame", "Cavunga"],
            "QUICULUNGO": [],
            "SAMBA CAJÚ": ["Samba Caju", "Samba Lucala"],
            "MASSANGANO": ["Massangano", "Zenza do Itombe"],
            "CÊRCA": [],
            "TANGO": [],
            "TERREIRO": ["Terreiro", "Quiquiemba"],
            "ALDEIA NOVA": [],
            "CACULO CABAÇA": [],
            "LUINGA": [],
        },
        "Cuanza-Sul": {
            "GABELA": ["Gabela", "Assango"],
            "CASSONGUE": ["Cassongue", "Atóme", "Dumbi"],
            "WAKU KUNGO": [],
            "CONDA": ["Cunjo", "Conda"],
            "EBO": ["Ebo", "Cassanje"],
            "CALULO": ["Calulo", "Cabuta"],
            "MUSSENDE": ["Mussende", "Quipaxi"],
            "PORTO AMBOIM": ["Porto Amboim", "Capolo"],
            "QUIBALA": ["Quibala", "Dala Cachibo"],
            "QUILENDA": [],
            "SELES": ["Seles", "Botera"],
            "SUMBE": ["Sumbe", "Quicombo"],
            "QUIRIMBO": [],
            "MUNENGA": [],
            "QUISSONGO": [],
            "GUNGO": [],
            "SANGA": [],
            "GANGULA": [],
            "PAMBANGALA": [],
            "CONDÉ": [],
            "AMBOIVA": [],
            "LONHE": ["Lonhe", "Cariango"],
            "QUENHA": [],
            "BOA ENTRADA": [],
        },
        "Huambo": {
            "BAILUNDO": ["Bailundo", "Lunge", "Luvemba"],
            "CAÁLA": [],
            "CACHIUNGO": ["Chinhama", "Cachiungo"],
            "CHICALA CHOLOANGA": ["Mbave", "Chicala"],
            "CHINJENJE": ["Chinjenje", "Chiaca"],
            "ECUNHA": ["Ecunha", "Quipeio"],
            "HUAMBO": ["Huambo", "Calima"],
            "LONDUIMBALI": ["Londuimbali", "Ussoque"],
            "LONGONJO": ["Longonjo", "Lépi"],
            "MUNGO": ["Mungo", "Cambuengo"],
            "UCUMA": ["Ucuma", "Cacoma", "Mundundo"],
            "BIMBE": ["Bimbe", "Hengue"],
            "SAMBO": ["Sambo", "Samboto"],
            "GALANGA": ["Galanga", "Cumbira"],
            "ALTO HAMA": [],
            "CHILATA": [],
            "CUIMA": ["Cuima", "Catata"],
        },
        "Benguela": {
            "BAÍA FARTA": [],
            "BALOMBO": ["Balombo", "Maca Mombolo"],
            "BOCOIO": ["Bocoio", "Cubal do Lumbo", "Monte Belo"],
            "CAIMBAMBO": ["Caimbambo", "Caiave", "Viangombe"],
            "CATUMBELA": [],
            "CHONGORÓI": ["Chongorói", "Camuine"],
            "CUBAL": [],
            "GANDA": [],
            "LOBITO": [],
            "BENGUELA": [],
            "EGITO PRAIA": ["Egito Praia", "Canjala"],
            "CHINDUMBO": [],
            "DOMBE GRANDE": [],
            "CAPUPA": [],
            "BIÓPIO": [],
            "CHILA": [],
            "CHICUMA": [],
            "BABAERA": [],
            "IAMBALA": [],
            "CATENGUE": [],
            "BOLONGUERA": [],
            "CANHAMELA": [],
            "NAVEGANTES": [],
        },
        "Huíla": {
            "CACONDA": ["Caconda", "Gungue", "Uaba", "Cusse"],
            "CACULA": ["Cacula", "Tchicuaqueia"],
            "CALUQUEMBE": ["Caluquembe", "Calepi", "Negola"],
            "CHIBIA": ["Chibia", "Jau"],
            "CHICOMBA": ["Chicomba", "Cutenda"],
            "CHIPINDO": ["Chipindo", "Bambi"],
            "CUVANGO": [],
            "GAMBOS": ["Chiange", "Chimbemba"],
            "HUMPATA": [],
            "JAMBA MINEIRA": ["Cassinga", "Jamba Mineira"],
            "LUBANGO": ["Lubango", "Huíla"],
            "MATALA": [],
            "QUILENGUES": ["Quilengues", "Impulo", "Dinde"],
            "QUIPUNGO": [],
            "DONGO": [],
            "HOQUE": [],
            "CAPELONGO": ["Capelongo", "Mulondo"],
            "CHITUTO": [],
            "CAPUNDA CAVILONGO": ["Capunda Cavilongo", "Quihita"],
            "VITI VIVALI": [],
            "GALANGUE": [],
            "PALANCA": [],
            "CHICUNGO": [],
        },
        "Namibe": {
            "MOÇÂMEDES": [],
            "CAMUCUIO": ["Camucuio", "Mamué", "Chingo"],
            "BIBALA": ["Bibala", "Capangombe", "Caitou", "Lola"],
            "VIREI": ["Virei", "Cainde"],
            "TÔMBUA": [],
            "LUCIRA": ["Lucira", "Bentiaba"],
            "IONA": [],
            "SACOMAR": [],
            "CACIMBAS": [],
        },
        "Cunene": {
            "CAHAMA": ["Cahama", "Otchinjau"],
            "CUANHAMA": ["Ondjiva", "Môngua"],
            "CUROCA": [],
            "CUVELAI": [],
            "NAMACUNDE": [],
            "OMBANDJA": ["Xangongo", "Ombala yo Mungu"],
            "CHIÉDE": [],
            "NEHONE": ["Nehone", "Evale"],
            "HUMBE": ["Mucope", "Humbe"],
            "MUPA": [],
            "NAULILA": [],
            "CHITADO": [],
            "CAFIMA": [],
            "CHISSUATA": [],
        },
        "Cubango": {
            "CALAI": [],
            "CUANGAR": [],
            "CUCHI": [],
            "CUTATO": ["Cutato", "Vissati"],
            "CAIUNDO": ["Caiundo", "Jamba Cueio"],
            "LONGA": ["Longa", "Baixo Longa"],
            "MENONGUE": [],
            "NANCOVA": ["Nancova", "Rito"],
            "SAVATE": ["Savate", "Bondo Caíla"],
            "CHINGUANJA": [],
            "MAVENGUE": ["Mavengue", "Maué"],
        },
        "Cuando": {
            "CUITO CUANAVALE": ["Cuito Cuanavale", "Lupire"],
            "DIRICO": ["Dirico", "Xamavera"],
            "MAVINGA": [],
            "RIVUNGO": [],
            "XIPUNDO": [],
            "DIMA": ["Cunjamba", "Cutuile"],
            "LUIANA": [],
            "MUCUSSO": [],
            "LUENGUE": [],
        },
        "Moxico": {
            "CHIÚME": [],
            "LUMBALA NGUIMBO": ["Lumbala Nguimbo", "Mussuma Mitete", "Sessa"],
            "CAMANONGUE": [],
            "LÉUA": ["Léua", "Liangongo"],
            "ALTO CUITO": [],
            "LUTEMBO": ["Lutembo", "Luvuei"],
            "CANGUMBE": [],
            "LUENA": ["Luena", "Cassongo"],
            "CANGAMBA": ["Cangombe", "Cassamba", "Cangamba", "Muié"],
            "LUCUSSE": [],
            "NINDA": [],
            "LUTUAI": [],
        },
        "Moxico Leste": {
            "CAZOMBO": ["Cazombo", "Lumbala Caquengue"],
            "LUACANO": [],
            "CAMEIA": [],
            "LUAU": [],
            "NANA CANDUNDO": [],
            "MACONDO": ["Macondo", "Calunda"],
            "CAIANDA": [],
            "LÓVUA DO ZAMBEZE": [],
            "LAGO DILOLO": [],
        },
        "Malanje": {
            "CACUSO": ["Cacuso", "Soqueco"],
            "CAHOMBO": ["Micanda", "Cahombo"],
            "CALANDULA": ["Calandula", "Cota"],
            "CAMBUNDI CATEMBO": ["Cambundi Catembo", "Dumba Cambango"],
            "CANGANDALA": ["Cangandala", "Caribo", "Culamagia"],
            "KIWABA NZOJI": ["Kiwaba Nzoji", "Mufuma"],
            "KUNDA DYA BAZE": ["Kunda dya Baze", "Lemba"],
            "LUQUEMBO": ["Luquembo", "Dombo wa Zanga"],
            "MALANJE": ["Malanje", "Lombe"],
            "MARIMBA": ["Marimba", "Mangando"],
            "MASSANGO": [],
            "QUELA": ["Quela", "Bângalas"],
            "QUIRIMA": ["Quirima", "Sautar"],
            "CATECO CANGOLA": [],
            "CUALE": [],
            "PUNGO A NDONGO": [],
            "NGOLA LUIJI": ["Ngola Luiji", "Cambaxe"],
            "QUIHUHU": ["Quihuhu", "Quinguengue"],
            "XANDEL": ["Xandel", "Moma"],
            "CAMBO SUINGINGE": [],
            "MILANDO": [],
            "QUITAPA": [],
            "CAPUNDA": ["Capunda", "Quimbango", "Cunga Palanga"],
            "MUQUIXE": [],
            "QUÊSSUA": [],
            "CACULAMA": ["Caculama", "Caxinga"],
            "MBANJI YA NGOLA": ["Mbanji ya Ngola", "Cabombo"],
        },
        "Luanda": {
            "BELAS": [],
            "CACUACO": [],
            "CAMAMA": [],
            "CAZENGA": [],
            "HOJI-YA-HENDA": [],
            "INGOMBOTA": [],
            "KILAMBA": [],
            "KILAMBA KIAXI": [],
            "MAIANGA": [],
            "MULENVOS": [],
            "MUSSULO": [],
            "RANGEL": [],
            "SAMBA": [],
            "SAMBIZANGA": [],
            "TALATONA": [],
            "VIANA": [],
        },
        "Icolo e Bengo": {
            "CATETE": ["Catete", "Caculo Cahango", "Cassoneca", "Caxicane"],
            "QUIÇAMA": ["Demba Chio", "Mumbondo", "Muxima", "Quixinge"],
            "CALUMBO": [],
            "CABIRI": [],
            "CABO LEDO": [],
            "BOM JESUS": [],
            "SEQUELE": ["Funda", "Quifangondo", "Sequele"],
        },
        "Lunda-Norte": {
            "DUNDO": ["Dundo", "Luachimo"],
            "CAMBULO": ["Cachimo", "Nzage"],
            "CAPENDA CAMULEMBA": ["Capenda Camulemba", "Xinge"],
            "CUANGO": [],
            "CUÍLO": ["Caluango", "Cuílo"],
            "LUBALO": ["Muvuluege", "Lubalo"],
            "LUCAPA": ["Camissombo", "Lucapa"],
            "LÓVUA": [],
            "XÁ-MUTEBA": [],
            "XÁ CASSAU": ["Xá Cassau", "Capaia"],
            "CAMAXILO": [],
            "LUANGUE": [],
            "LUREMO": [],
            "CANZAR": ["Canzar", "Luia"],
            "CASSANJE CALUCALA": ["Cassanje Calucala", "Iongo"],
            "MUSSUNGUE": ["Mussungue", "Caíta"],
            "CAFUNFU": [],
        },
        "Lunda-Sul": {
            "CACOLO": [],
            "DALA": [],
            "MUCONDA": [],
            "SAURIMO": ["Mona Quimbundo", "Saurimo"],
            "CHILUAGE": [],
            "CASSAI-SUL": [],
            "XASSENGUE": ["Xassengue", "Cucumbi"],
            "ALTO CHICAPA": [],
            "SOMBO": [],
            "MURIEGE": [],
            "LUMA CASSAI": [],
            "CAZAGE": [],
            "MUANGUEJI": [],
            "CASSENGO": [],
        },
        "Bié": {
            "ANDULO": ["Andulo", "Cassumbe", "Chivaúlo"],
            "CAMACUPA": ["Camacupa", "Cuanza", "Muinha"],
            "CATABOLA": ["Catabola", "Caiuera", "Sande"],
            "CHINGUAR": ["Chinguar", "Cutato", "Cangote"],
            "CHITEMBO": ["Chitembo", "Cachingues", "Malengue"],
            "CUEMBA": ["Cuemba", "Munhango", "Sachinemuna"],
            "CUITO": ["Cuito", "Cunje"],
            "CUNHINGA": [],
            "NHARÊA": ["Nharêa", "Gamba", "Caieie"],
            "LUANDO": [],
            "RINGOMA": [],
            "MUMBUÉ": ["Mumbué", "Mutumbo", "Soma Cuanza"],
            "CALUCINGA": [],
            "CHICALA": [],
            "CHIPETA": ["Chipeta", "Chiuca"],
            "UMPULO": [],
            "LÚBIA": ["Lúbia", "Dando"],
            "CAMBÂNDUA": [],
            "BELO HORIZONTE": [],
        },  # Fecha Bié
    }  # Fecha ANGOLA
}  # Fecha o dicionário principal


async def seed_dpa():
    async with AsyncSessionLocal() as session:
        try:
            logger.info("🇦🇴 Iniciando Seeder da DPA 2024 (Lei 15/24) com Comunas...")

            # 1. Criar Nível Central (País)
            res = await session.execute(select(Region).where(Region.name == "ANGOLA"))
            country = res.scalar_one_or_none()

            if not country:
                country = Region(name="ANGOLA", type="PAIS", parent_id=None)
                session.add(country)
                await session.flush()
                logger.info("✓ Criado nível Central: ANGOLA")

            batch_count = 0
            # 2. Iterar Províncias, Municípios e Comunas
            for prov_name, municipalities in ANGOLA_DPA["ANGOLA"].items():
                # Gerenciar Transação por Província para segurança
                try:
                    # Verificar/Criar Província
                    res_p = await session.execute(
                        select(Region).where(Region.name == prov_name,
                                             Region.parent_id == country.id)
                    )
                    province = res_p.scalar_one_or_none()

                    if not province:
                        province = Region(name=prov_name, type="PROVINCIA", parent_id=country.id)
                        session.add(province)
                        await session.flush()
                        logger.info(f"  ↳ Província: {prov_name}")

                    # Criar Municípios
                    for mun_name, communes in municipalities.items():
                        res_m = await session.execute(
                            select(Region).where(Region.name == mun_name,
                                                 Region.parent_id == province.id)
                        )
                        municipality = res_m.scalar_one_or_none()

                        if not municipality:
                            municipality = Region(
                                name=mun_name, type="MUNICIPIO", parent_id=province.id)
                            session.add(municipality)
                            await session.flush()
                            logger.info(f"    • Município: {mun_name}")

                        # Criar Comunas (O "Pulo do Gato": busca combinada com parent_id)
                        for com_name in communes:
                            res_c = await session.execute(
                                select(Region).where(Region.name == com_name,
                                                     Region.parent_id == municipality.id)
                            )
                            if not res_c.scalar_one_or_none():
                                commune = Region(name=com_name, type="COMUNA",
                                                 parent_id=municipality.id)
                                session.add(commune)
                                logger.info(f"      - Comuna: {com_name}")
                                batch_count += 1

                                # Batch commit a cada 50 novas regiões para economia de memória
                                if batch_count % 50 == 0:
                                    await session.commit()
                                    # Reboot session context after commit if needed, or just continue

                    await session.commit()  # Commit ao final de cada província
                except Exception as prov_err:
                    await session.rollback()
                    logger.error(f"❌ Erro na província {prov_name}: {prov_err}")
                    continue

            logger.info("✅ DPA 2024 (Províncias, Municípios e Comunas) populada com sucesso!")

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Erro fatal ao popular DPA: {e}")

if __name__ == "__main__":
    asyncio.run(seed_dpa())
