# VALIDACAO_RUNTIME_EDUCACAO

Data: 2026-06-10T21:23:22.172304Z

## Resumo Phase 1 — APIs
- **escolas_huambo**: status=200 time=0.199s count=4 
- **escolas_benguela**: status=200 time=0.235s count=4 
- **turmas_huambo**: status=200 time=0.211s count=7 
- **turmas_benguela**: status=200 time=0.3s count=7 
- **matriculas_citizen**: status=500 time=0.31s count=N/A 
- **fuc_citizen**: status=200 time=0.538s count=N/A 

## Resumo Phase 2 — Cadeia Educacional
- Matricula presente: False
- Boletim presente: False
- Certificado presente: False

### Matriculas sample
[]

### FUC summary
{}

## Resumo Phase 3 — Territorial checks
- **huambo_user_list_huambo**: status=200 time=0.159s count=1
- **huambo_user_list_benguela**: status=200 time=0.135s count=1
- **benguela_user_list_benguela**: status=200 time=0.147s count=1
- **benguela_user_list_huambo**: status=200 time=0.168s count=1
- **matricula_citizen_read**: status=500 time=0.31s count=N/A
- **boletins_citizen**: status=404 time=0.041s count={'detail': None}