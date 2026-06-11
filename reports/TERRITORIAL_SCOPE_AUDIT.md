**ESTADO REAL**

- **Resumo**: o código contém definição clara da hierarquia territorial (Province → Municipality → Commune) e utilities para validação territorial em [apps/backend/app/core/constants.py](apps/backend/app/core/constants.py#L120-L140) e [apps/backend/app/core/rbac/territorial_access.py](apps/backend/app/core/rbac/territorial_access.py#L1-L183). Mapeamentos de roles por domínio existem em `governance.py` por módulo (ex.: [apps/backend/app/modules/educacao/rbac/roles.py](apps/backend/app/modules/educacao/rbac/roles.py#L1-L62)).

- **Validação de enforcement real por âmbito** (Nacional / Provincial / Municipal / Institucional): implementação registrada mas uso inconsistente. A tabela abaixo indica status _real_ observado no código (não intenções nem roadmap).

| Módulo | Territorialidade Implementada | Parcial | Ausente |
|---|---:|:---:|:---:|
| Educação | X | ✓ |  |
| Saúde | X | ✓ |  |
| Registo Civil | X | ✓ |  |
| Pagamentos / Multicaixa | X | ✓ |  |
| Justiça | X | ✓ |  |
| Segurança Social | X | ✓ |  |
| Turismo | X | ✓ |  |
| Comércio / Indústria | X | ✓ |  |

- **Motivo da classificação**: para todos os módulos acima existe _modelagem_ de papéis territoriais e/ou mapeamento (`Role* -> RoleGovernance`) (ver vários `governance.py` em `apps/backend/app/modules/*/governance.py`), e muitos repositórios/serviços aceitam filtros `municipio`/`provincia`. Porém, não foi identificado uso consistente em todos os endpoints de `Depends(require_territorial_access(...))` ou equivalente que aplique automaticamente o `territory_id` do usuário — logo: territorialidade implementada (estrutura SIM) mas enforcement nos endpoints é parcial.

**Casos reais (análise)**

- CASO A — Diretor Provincial de Educação do Huambo
  - Deve ver: apenas Huambo
  - Não deve ver: Benguela, Luanda
  - Resultado observado: NÃO IMPLEMENTADO
  - Justificativa: existe infra de verificação territorial ([apps/backend/app/core/rbac/territorial_access.py](apps/backend/app/core/rbac/territorial_access.py#L1-L183)) e seeds mostram utilizadores provinciais (ex.: [apps/backend/seeds/core/seed_founding_users_with_territories.py](apps/backend/seeds/core/seed_founding_users_with_territories.py#L1-L80)), mas não há garantias de que todas as rotas apliquem essa verificação automaticamente.

- CASO B — Escola Municipal
  - Deve ver: seus alunos
  - Não deve ver: alunos de outras escolas
  - Resultado observado: NÃO IMPLEMENTADO
  - Justificativa: relações de domínio (ex.: `GuardianStudentLink`) existem, mas não se encontra enforcement universal em endpoints.

- CASO C — Técnico Municipal Assistência Social
  - Deve ver: beneficiários do município
  - Não deve ver: beneficiários nacionais
  - Resultado observado: NÃO IMPLEMENTADO
  - Justificativa: módulos têm campos territoriais; porém ausência de uso consistente dos guards indica risco de exposição cruzada.

**Recomendação de curto prazo**
- Adotar `require_territorial_access(...)` como dependency padrão em endpoints que retornam/alteram dados com territorialidade; auditar rotas críticas e aplicar patches de verificação (sem alterar modelagem de roles).
