# GOVERNANCE_RULES.md

## Constituição do Motor de Governança Territorial do SILA

**Versão:** 1.0
**Status:** Canônico / Obrigatório
**Escopo:** Núcleo de Governança Territorial, Autorização, Hierarquia Administrativa e Gestão Institucional

---

# PREÂMBULO

O SILA é uma plataforma de governação territorial e administrativa.

Toda autoridade, entidade, instituição, processo, documento e utilizador existente no sistema deve estar subordinado a uma estrutura territorial formal e auditável.

Este documento define as regras fundamentais que governam o sistema e prevalece sobre implementações, seeds, configurações, workflows ou decisões operacionais que entrem em conflito com ele.

---

# PRINCÍPIO 0 — BOOTSTRAP OBRIGATÓRIO

## 0.1

O arquivo `AGENT_RULES.md` é a referência inicial obrigatória para qualquer agente, automação, processo CI/CD ou operação administrativa.

## 0.2

Antes de qualquer alteração estrutural, o sistema deve validar a conformidade com este documento.

## 0.3

Nenhuma funcionalidade pode ser implementada em desacordo com estas regras.

---

# PRINCÍPIO 1 — SUPERADMINISTRADOR NACIONAL

## 1.1

Existe apenas um utilizador bootstrap permanente:

```text
SUPER_ADMIN_NACIONAL
```

## 1.2

O Super Administrador Nacional é responsável por:

* Administração global
* Recuperação de emergência
* Nomeação inicial de Governadores Provinciais
* Correções estruturais extraordinárias
* Governança nacional

## 1.3

Nenhum outro utilizador administrativo pode ser criado por seed permanente.

## 1.4

Todos os demais utilizadores devem ser criados através de workflows administrativos do próprio sistema.

---

# PRINCÍPIO 2 — TERRITÓRIOS SÃO ENTIDADES DINÂMICAS

## 2.1

A hierarquia territorial oficial é:

```text
PAÍS
 └── PROVÍNCIA
      └── MUNICÍPIO
           └── COMUNA
                └── BAIRRO (opcional)
```

## 2.2

A entidade territorial Angola é fixa e pode ser pré-carregada.

## 2.3

As Províncias podem ser pré-carregadas com base na divisão administrativa oficial.

## 2.4

Municípios, Comunas e Bairros nunca devem ser hardcoded.

## 2.5

Toda expansão territorial deve ocorrer através dos mecanismos administrativos do sistema.

## 2.6

O código de negócio nunca deve assumir:

* Quantidade de províncias
* Quantidade de municípios
* Quantidade de comunas
* Quantidade de bairros

---

# PRINCÍPIO 3 — CADEIA DE AUTORIDADE TERRITORIAL

## 3.1

Nenhum utilizador pode criar entidades fora do seu território.

## 3.2

Nenhum utilizador pode atribuir a terceiros um escopo superior ao seu.

## 3.3

Nenhum utilizador pode nomear autoridades acima da sua hierarquia.

## 3.4

Toda criação territorial deve respeitar a cadeia administrativa.

Exemplo:

```text
Governador Huambo
 └── cria Município Caála

Administrador Caála
 └── cria Comunas de Caála
```

---

# PRINCÍPIO 4 — GOVERNADOR PROVINCIAL

Role:

```text
ROLE_GOVERNADOR_PROVINCIAL
```

Pode:

* Criar Municípios
* Editar Municípios
* Desativar Municípios
* Nomear Administradores Municipais

Somente dentro da sua província.

Exemplo:

```text
Governador Huambo
✓ Caála
✓ Longonjo
✗ Lobito
✗ Benguela
```

---

# PRINCÍPIO 5 — ADMINISTRADOR MUNICIPAL

Pode:

* Criar Comunas
* Gerir Comunas
* Criar Bairros
* Gerir Bairros
* Gerir instituições municipais

Somente dentro do seu município.

---

# PRINCÍPIO 6 — INSTITUIÇÕES SÃO DINÂMICAS

Instituições não são hardcoded.

O sistema deve permitir registrar tipos institucionais.

Exemplos:

* Escola
* Hospital
* Centro de Saúde
* Conservatória
* Tribunal
* Administração Municipal
* Biblioteca
* Universidade
* Delegação Ministerial

---

## Modelo mínimo

```text
Institution
- id
- type
- territory_id
- created_by
- managed_by
- status
- created_at
- updated_at
```

---

# PRINCÍPIO 7 — DIRETORES PROVINCIAIS

## Educação

Pode:

* Criar Escolas
* Editar Escolas
* Nomear Diretores Escolares

Somente na sua província.

## Saúde

Pode:

* Criar Hospitais
* Criar Centros de Saúde
* Nomear Diretores de Unidades de Saúde

Somente na sua província.

---

# PRINCÍPIO 8 — TERRITORY_ID OBRIGATÓRIO

Toda entidade operacional deve possuir:

```text
territory_id
created_by
managed_by
```

Obrigatoriamente.

---

## Aplicação mínima

* Citizen
* School
* Hospital
* Institution
* Process
* Workflow
* Document
* License
* Inspection
* Complaint
* Benefit
* Request

---

# PRINCÍPIO 9 — HERANÇA TERRITORIAL

Uma entidade referencia apenas um território.

Exemplo:

```text
School
 └── territory_id
```

Província, Município e Comuna devem ser inferidos pela árvore territorial.

Duplicação territorial é proibida.

---

# PRINCÍPIO 10 — ESCOPOS NUNCA VÊM DO FRONTEND

O frontend nunca é fonte de verdade para escopo territorial.

Proibido:

```json
{
  "province_id": "..."
}
```

como critério de autorização.

O escopo deve ser calculado pelo backend utilizando:

* JWT
* Base de dados
* Hierarquia territorial

---

# PRINCÍPIO 11 — AUTORIZAÇÃO OFICIAL

Toda autorização do SILA deve obedecer:

```text
ALLOW(action, actor, resource) =

RBAC(actor)
AND
TerritorialScope(actor, resource)
AND
Ownership(actor, resource)
AND
EntityStatus(resource)
```

Nenhum componente pode ignorar qualquer uma dessas verificações.

---

# PRINCÍPIO 12 — DELEGAÇÃO ADMINISTRATIVA

Permissões podem ser delegadas.

Toda delegação deve ser:

* Temporária ou permanente
* Auditável
* Revogável

---

## Modelo mínimo

```text
Delegation
- delegated_by
- delegated_to
- permissions
- territory_id
- valid_from
- valid_until
- revoked_at
```

---

# PRINCÍPIO 13 — AUDITORIA OBRIGATÓRIA

Toda operação administrativa crítica deve gerar registo auditável.

Exemplos:

* Criação de Município
* Criação de Escola
* Criação de Hospital
* Promoção de Utilizador
* Alteração Territorial
* Delegação
* Revogação de Permissões

---

## Modelo mínimo

```text
AuditEvent
- actor_id
- action
- entity_type
- entity_id
- territory_id
- before
- after
- created_at
```

---

# PRINCÍPIO 14 — SEPARAÇÃO ENTRE TERRITÓRIO E INSTITUIÇÃO

Territórios e Instituições são conceitos independentes.

```text
Território ≠ Instituição
```

Exemplo:

```text
Huambo
 ├── Escola A
 ├── Escola B
 ├── Hospital A
 └── Hospital B
```

Instituições pertencem a territórios.

Territórios nunca pertencem a instituições.

---

# PRINCÍPIO 15 — PROIBIÇÃO DE IDs MÁGICOS

Exceto o bootstrap nacional autorizado:

```text
SUPER_ADMIN_NACIONAL
```

é proibido depender de:

* UUIDs específicos
* Emails específicos
* Usernames específicos
* IDs específicos

na lógica de negócio.

---

# PRINCÍPIO 16 — SEEDS E DESENVOLVIMENTO

## Produção

O bootstrap oficial cria apenas:

```text
SUPER_ADMIN_NACIONAL
```

## Desenvolvimento

Utilizadores de desenvolvimento:

* Devem ser efémeros
* Devem ser regeneráveis
* Nunca são fonte de verdade

---

## DEV_CREDENTIALS

`docs/DEV_CREDENTIALS.md`

é apenas utilitário de desenvolvimento local.

Não possui valor normativo.

---

# PRINCÍPIO 17 — VALIDAÇÃO AUTOMÁTICA

O pipeline CI/CD deve falhar quando detectar:

* Utilizadores administrativos hardcoded
* Municípios hardcoded
* Comunas hardcoded
* Instituições hardcoded
* Bypass de escopo territorial
* Bypass de auditoria
* Entidades críticas sem territory_id
* Entidades críticas sem created_by
* Entidades críticas sem managed_by

---

# REGRA DE OURO

Nenhuma entidade operacional, instituição, utilizador, processo, documento ou unidade territorial abaixo do bootstrap nacional pode depender de dados hardcoded.

Toda expansão territorial, institucional e administrativa deve ocorrer através da cadeia de autoridade definida e governada pelo próprio SILA.

O sistema deve ser capaz de adaptar-se a alterações administrativas futuras sem necessidade de alterações no código de negócio.

---

# PRINCÍPIO FINAL

O território governa a autoridade.

A autoridade governa as instituições.

As instituições governam os processos.

Nenhuma operação pode quebrar esta cadeia.
