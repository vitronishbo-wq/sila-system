# Locations Name Audit (2026-03-18)

## Duplicidades por Nome entre Tipos (amostra)
```
Alto Zaza   | {COMUNA,MUNICIPIO}    | 2
Ambriz      | {COMUNA,MUNICIPIO}    | 2
Bailundo    | {COMUNA,MUNICIPIO}    | 2
Balombo     | {COMUNA,MUNICIPIO}    | 2
Banga       | {COMUNA,MUNICIPIO}    | 2
Belize      | {COMUNA,MUNICIPIO}    | 2
Bembe       | {COMUNA,MUNICIPIO}    | 2
Bengo       | {COMUNA,PROVINCIA}    | 2
Benguela    | {MUNICIPIO,PROVINCIA} | 2
Bibala      | {COMUNA,MUNICIPIO}    | 2
Bimbe       | {COMUNA,MUNICIPIO}    | 2
Bocoio      | {COMUNA,MUNICIPIO}    | 2
Bula Atumba | {COMUNA,MUNICIPIO}    | 2
Cabinda     | {MUNICIPIO,PROVINCIA} | 2
Cachiungo   | {COMUNA,MUNICIPIO}    | 2
Caconda     | {COMUNA,MUNICIPIO}    | 2
Cacuaco     | {COMUNA,MUNICIPIO}    | 2
Cacula      | {COMUNA,MUNICIPIO}    | 2
Caculama    | {COMUNA,MUNICIPIO}    | 2
Cahama      | {COMUNA,MUNICIPIO}    | 2
```

## Conflitos de Grafia (acentos, hífen, maiúsculas)
```
andulo         | {ANDULO,Andulo}                         | {COMUNA,MUNICIPIO} | 2
camacupa       | {CAMACUPA,Camacupa}                     | {COMUNA,MUNICIPIO} | 2
catabola       | {CATABOLA,Catabola}                     | {COMUNA,MUNICIPIO} | 2
chinguar       | {CHINGUAR,Chinguar}                     | {COMUNA,MUNICIPIO} | 2
chipeta        | {CHIPETA,Chipeta}                       | {COMUNA,MUNICIPIO} | 2
chitembo       | {CHITEMBO,Chitembo}                     | {COMUNA,MUNICIPIO} | 2
cuemba         | {CUEMBA,Cuemba}                         | {COMUNA,MUNICIPIO} | 2
cutato         | {CUTATO,Cutato}                         | {COMUNA,MUNICIPIO} | 3
kundadyabaze   | {Kunda Dya Baze,Kunda dya Baze}         | {COMUNA,MUNICIPIO} | 2
lubia          | {LÚBIA,Lúbia}                           | {COMUNA,MUNICIPIO} | 2
maqueladozombo | {Maquela Do Zombo,Maquela do Zombo}     | {COMUNA,MUNICIPIO} | 2
mbanjiyangola  | {Mbanji Ya Ngola,Mbanji ya Ngola}       | {COMUNA,MUNICIPIO} | 2
mumbue         | {MUMBUÉ,Mumbué}                         | {COMUNA,MUNICIPIO} | 2
nharea         | {NHARÊA,Nharêa}                         | {COMUNA,MUNICIPIO} | 2
sambacaju      | {Samba Cajú,Samba caju}                 | {COMUNA,MUNICIPIO} | 2
```

## Duplicidades Indevidas (mesmo type + mesmo parent)
```
duplicates_same_parent = 0
```

## Correções Sugeridas (padronização futura)
Regras sugeridas:
- Title Case para cada palavra.
- Conectores em minúsculo: e, de, da, do, dos, das.
- Preservar hífens e acentuação oficial.

Exemplos:
- ANDULO → Andulo
- MAQUELA DO ZOMBO → Maquela do Zombo
- ICOLO E BENGO → Icolo e Bengo

