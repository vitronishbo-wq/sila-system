# VALIDACAO_RUNTIME_EDUCACAO

Data: 2026-06-10T21:55:32.559597Z

## Resumo Phase 1 — APIs
- **escolas_huambo**: status=200 time=15.2s count=4 
- **escolas_benguela**: status=200 time=0.241s count=4 
- **turmas_huambo**: status=200 time=0.571s count=7 
- **turmas_benguela**: status=200 time=0.267s count=7 
- **matriculas_citizen**: status=200 time=1.032s count=1 
- **fuc_citizen**: status=200 time=0.524s count=N/A 

## Resumo Phase 2 — Cadeia Educacional
- Matricula presente: False
- Boletim presente: False
- Certificado presente: False

### Matriculas sample
[]

### FUC summary
{}

## Resumo Phase 3 — Territorial checks
- **huambo_user_list_huambo**: status=200 time=0.252s count=1
- **huambo_user_list_benguela**: status=200 time=0.255s count=1
- **benguela_user_list_benguela**: status=200 time=0.229s count=1
- **benguela_user_list_huambo**: status=200 time=0.183s count=1
- **matricula_citizen_read**: status=200 time=1.032s count=1
- **boletins_citizen**: status=404 time=2.165s count={'detail': None}
 
## Baseline Updates
- **BUG-MAT-001**: Status legado "confirmada" — **RESOLVIDO** — Data: 2026-06-10

## Freeze Notice
- **Domínio**: Educação
- **Status**: FROZEN FOR DEMO
- **Entrada em vigor**: 2026-06-10
- **Regra**: Nenhuma migration; Nenhum refactor; Nenhuma alteração estrutural até a demonstração.