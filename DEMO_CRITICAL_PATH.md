# DEMO_CRITICAL_PATH

Data: 2026-06-10
Alvo: demonstracao ministerial de sexta-feira, 2026-06-12.

## Regra Executiva

Objetivo nao e completar o sistema.

Objetivo e demonstracao impecavel.

Pergunta obrigatoria antes de qualquer tarefa:

```text
Isto impacta diretamente a demonstracao?
```

Se nao impacta:

```text
POSTERGAR
```

## Congelamento

Nao mexer ate a demo, exceto correcao critica:

```text
RBAC base
Governanca
FUC
Estrutura territorial
Dominio Educacao
Alembic autogenerate
Marketplace
Transferencias instantaneas
Capacity Engine
```

Meta:

```text
ZERO regressoes
```

## Fluxo Principal

Ordem obrigatoria do ensaio:

```text
Login
Dashboard Educacao
Escola
Turma
Aluno
Matricula
Boletim
Certificado
FUC
```

Tempo alvo:

```text
8 a 10 minutos
```

Tempo maximo:

```text
12 minutos
```

## Matriz de Validacao

| Fluxo | Validacao | Resultado esperado | Status |
| --- | --- | --- | --- |
| 1. Escola | `GET escolas` | 200 e lista nao vazia | PENDENTE ENSAIO |
| 1. Escola | `POST escola` | 200/201 dentro do territorio | PENDENTE ENSAIO |
| 1. Escola | `GET escola/{id}` | 200 | PENDENTE ENSAIO |
| 2. Turma | `POST turma` | 200/201 | PENDENTE ENSAIO |
| 2. Turma | `GET turma` | 200 e lista nao vazia | PENDENTE ENSAIO |
| 3. Aluno | `AcademicIdentity` | criar/consultar aluno | PENDENTE ENSAIO |
| 4. Matricula | `Aluno -> Turma -> Matricula` | matricula criada/consultada | PENDENTE ENSAIO |
| 5. Boletim | criar | 200/201 | PENDENTE ENSAIO |
| 5. Boletim | consultar | 200 | PENDENTE ENSAIO |
| 6. Certificado | emitir | 200/201 | PENDENTE ENSAIO |
| 6. Certificado | consultar | 200 | PENDENTE ENSAIO |
| 7. FUC | `GET /fuc/{citizen_id}/educacao` | 200 com educacao consolidada | PENDENTE ENSAIO |

## FUC Prioritario

Endpoint mais importante da reuniao:

```text
GET /fuc/11111111-1111-4111-8111-111111111111/educacao
```

Dados esperados:

```text
identidades >= 1
matriculas >= 1
boletins >= 1
certificados >= 1
```

## Autorizacao Territorial

Executar apenas estes cenarios.

| Cenario | Acao | Resultado esperado | Status |
| --- | --- | --- | --- |
| Governador Huambo | Criar escola Huambo | 200/201 | PENDENTE ENSAIO |
| Governador Huambo | Criar escola Benguela | 403 | PENDENTE ENSAIO |
| Administrador Municipal | Criar escola fora do municipio | 403 | PENDENTE ENSAIO |

Se os tres passarem:

```text
territorialidade considerada aprovada para demo
```

## Critério de Pronto

So considerar pronto quando todos estiverem verdes:

```text
Backend sobe sem erro
Login funciona
Escola funciona
Turma funciona
Aluno funciona
Matricula funciona
Boletim funciona
Certificado funciona
FUC funciona
Territorialidade devolve 403 corretamente
Um unico head Alembic valido
Demonstracao completa em menos de 10 minutos
```

## Postergado

Nao entra no escopo da demo:

```text
educacao_institution_capacities
Marketplace
Transferencias instantaneas
Capacity Engine
Novas migrations
Refactors de RBAC
Refactors de governanca
Refactors de dominio Educacao
```
