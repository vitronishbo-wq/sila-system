# SLA Provinces Snapshot (2026-03-18)

## Lista Oficial (DPA 2024)
- Cabinda
- Zaire
- Uíge
- Bengo
- Cuanza-Norte
- Cuanza-Sul
- Huambo
- Benguela
- Huíla
- Namibe
- Cunene
- Cubango
- Cuando
- Moxico
- Moxico Leste
- Malanje
- Lunda-Norte
- Lunda-Sul
- Bié
- Icolo e Bengo
- Luanda

## Enum Atual (app/core/sla_engine/models.py)
- CABINDA = cabinda
- ZAIRE = zaire
- UIGE = uige
- BENGO = bengo
- ICOLO_E_BENGO = icolo_e_bengo
- LUANDA = luanda
- KUANZA_NORTE = kuanza_norte
- KUANZA_SUL = kuanza_sul
- MALANJE = malanje
- LUNDA_NORTE = lunda_norte
- LUNDA_SUL = lunda_sul
- BENGUELA = benguela
- HUAMBO = huambo
- BIE = bie
- MOXICO = moxico
- MOXICO_LESTE = moxico_leste
- HUILA = huila
- NAMIBE = namibe
- CUNENE = cunene
- CUBANGO = cubango
- CUANDO = cuando

## Seeds Carregados
- seed_21_provinces_final.py atualizado para grafia DPA 2024.
- refactor_locations.py atualizado para grafia DPA 2024.
- seed_locations_dpa_2024.py executado (reset) usando docs/seed_angola_dpa_2024.cpython-312.pyc.
- run_master_seed.py já usa DPA 2024 (Cuanza-Norte, Cuanza-Sul, Lunda-Norte, Lunda-Sul, Cubango, Cuando).
- seed_angola_dpa_v3.py já usa DPA 2024 e contempla Cubango/Cuando.
- seed_sla_completo.sql ajustado para usar scope_id "cubango".

## Contagens de Territórios (locations)
- Províncias: 21
- Municípios: 326
- Comunas: 378

## Exemplos de Hierarquia (Província → Município → Comuna)
- Huambo → Bailundo → Bailundo
- Huambo → Bailundo → Lunge
- Huambo → Cachiungo → Cachiungo
- Huambo → Chicala Choloanga → Chicala
- Huambo → Chinjenje → Chiaca

## Testes Validados
- pytest apps/backend/app/core/sla_engine/tests: 10 passed.

## Auditoria e Rotina
- reports/locations_corrections_full.csv: inventário completo com nome original, canonical e chave normalizada.
- reports/locations_corrections_suggested.csv: apenas conflitos de grafia (acentos/hífen/maiúsculas).
- apps/backend/scripts/run_locations_maintenance.sh: normaliza Title Case + gera CSVs de auditoria.
- Cadência sugerida: após cada carga de locations e antes de cada release.

## Integração com SLA
- SLAContext normaliza nomes (acentos, hífen, espaços) e mapeia aliases como Cuanza/Kuanza e Kuando/Cubango.

## Agendamento (cron)
```
0 2 * * * /home/dev03wsl/sila-system/apps/backend/scripts/run_locations_maintenance.sh >> /home/dev03wsl/sila-system/reports/maintenance.log 2>&1
```

## Release Pipeline
- Executar `run_locations_maintenance.sh` antes de cada release.
- Anexar `locations_corrections_full.csv` e `locations_corrections_suggested.csv` ao snapshot da versão.

