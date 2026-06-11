## ACCESS_MODEL_IMPLEMENTATION_PLAN

### Estado atual

- ItemEstado

- Login✅
- JWT✅
- Roles✅
- Permissões✅
- Territorialidade⚠️ Parcial
- Especialização por módulo❌
- Ocultação de módulos por perfil❌
- Integrações externas⚠️ Homologação

---

### Estado desejado

- Hierarquia completa:

**Nacional → Provincial → Municipal → Escola → Operador**

- Especialização por vertical: Educação, Saúde, Ação Social, Agricultura, Turismo, Justiça…

- Ocultação dinâmica de módulos conforme perfil/território.

- Integrações externas visíveis mas com selo **AMBIENTE DE HOMOLOGAÇÃO**.

---

### Gap

- Territorialidade incompleta (falta escopo provincial/municipal/escola).

- Perfis não ocultam módulos fora do seu domínio.

- Especialização por vertical ainda não implementada.

- Integrações externas em mock, sem selo explícito.

---

### Mudanças mínimas necessárias

1. **Territorialidade**

Implementar `TerritoryScope` com níveis hierárquicos.

2. Associar cada utilizador a `User + Role + Territory + Institution + Module`.

3. **Especialização por módulo**

Criar `ModuleProfile` para Educação, Saúde, Justiça etc.

4. Mapear permissões específicas por vertical.

5. **Ocultação de módulos**

No portal administrativo, aplicar filtro por perfil/território.

6. Exibir apenas módulos autorizados.

7. **Integrações externas**

Marcar todas como `STATUS: HOMOLOGAÇÃO INTERNA`.

8. Exibir selo visível:

```
AMBIENTE DE HOMOLOGAÇÃO
Integrações simuladas para demonstração institucional
```

---

### Prioridade imediata

- Territorialidade

- Especialização por perfil

- Ocultação de módulos

👉 Isto garante impacto direto na apresentação governamental: cada nível vê apenas o que lhe compete, e o cidadão vê apenas o seu portal.

As integrações externas ficam em segundo plano, mas transparentes com selo de homologação.
