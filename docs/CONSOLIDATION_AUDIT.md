# 🔴 AUDITORIA DE CONSOLIDAÇÃO - SILA SYSTEM
## Data: 18 de Março de 2026

---

## 1️⃣ FRONTEND (React/Vite)

### Diagnóstico
| Métrica | apps/frontend | interfaces/frontend |
|---------|--------|---------|
| **Status Docker** | ✅ ATIVO (infra/docker-compose.yml) | ❌ Orphaned |
| **Estrutura** | Completa (auth/, components/, pages/) | Parcial |
| **Último componente criado** | IdentityPage.tsx, BiometricEnrollmentPage.tsx | Desatualizado |
| **Assets Format** | PNG/JPEG (legado) | WebP (otimizado) |

### Diferenças Críticas
**Apenas em apps/frontend:**
- `auth/` - Sistema de autenticação
- `AdminObservability.tsx` - Observabilidade
- `Toast.tsx`, `useToast.tsx` - Sistema de notificações
- `index.tsx` - Entry point

**Apenas em interfaces/frontend:**
- Imagens em WebP (mais otimizadas)
  - `auth-bg-admin.webp`
  - `auth-bg-citizen.webp`
  - `brand-logo-sila.webp`
  - `dashboard-citizen-hero.webp`
  - Etc (georeferenciação otimizada)

### ⚠️ Risco de Manutenção
- **Mudanças precisam ser feitas em dobro**
- **Nova lógica (Identity/Biometria) só está em apps/frontend**
- **interfaces/frontend vai ficar obsoleto rapidamente**

---

## 2️⃣ ALEMBIC (Migrações Database)

### Diagnóstico
| Localização | Status | Migrações | Tamanho |
|---------|--------|---------|---------|
| `./alembic/` (raiz) | ❌ OBSOLETO | 9 | 21.8 KB |
| `./apps/backend/alembic/` | ✅ ATIVO | 85 | ~19 MB |

### Encontrados
```
- alembic/env.py (configuração raiz - DESCONECTADA)
- alembic/versions/ (9 migrações antigas)
- apps/backend/alembic/env.py (ATIVO)
- apps/backend/alembic/versions/ (85 migrações - A VERDADE)
```

### 🚨 Problema Crítico
- **Raiz do projeto aponta para `/alembic/` (confuso para novos devs)**
- **85 migrações estão em `apps/backend/alembic/` (correto)**
- **Alguém pode acidentalmente rodar a raiz e quebrar tudo**

---

## 3️⃣ BASE REPOSITORY (DDD Pattern)

### Duplicatas Encontradas
```
❌ apps/backend/core/repositories/base_repository.py
✅ apps/backend/app/core/database/repositories/base_repository.py (PRINCIPAL)
⚠️ apps/backend/app/modules/governance/statistics/infrastructure/repositories/base_named_repository.py
⚠️ apps/backend/app/modules/payment/infrastructure/base_repository.py
```

### Impacto
- Alterações no contrato de repositório precisam ser feitas **3-4 vezes**
- Inconsistência em tipo de query, paginação, filtros
- Desacoplamento quebrado entre módulos

---

## 📋 RECOMENDAÇÕES PRIORITÁRIAS

### 🥇 PRIORITÁRIO 1: Frontend Consolidation
**Ação:** Absorver `interfaces/frontend` → `apps/frontend`
**Risco:** LOW (interfaces/frontend não está em uso)
**Benefício:** Elimina 1 duplicação, unifica hooks de Identity/Biometria

```bash
# Safety: Backup antes
mv interfaces/frontend interfaces/.frontend.backup-2026-03-18

# Depois: Cu-paste WebP assets se forem mais otimizados
# cp interfaces/.frontend.backup-2026-03-18/src/assets/images/*.webp apps/frontend/src/assets/images/
```

### 🥈 PRIORITÁRIO 2: Alembic Cleanup
**Ação:** Remover `/alembic` da raiz (apenas guardar)
**Risco:** MEDIUM (configurações podem estar ligadas)
**Verificar:** Qual é referenciado em venv, pytest.ini, setup.py?

```bash
# Safety: Backup
mkdir -p reports/alembic-backups
cp -r alembic reports/alembic-backups/alembic-raiz-2026-03-18

# Depois:
rm -rf alembic/
```

### 🥉 PRIORITÁRIO 3: BaseRepository Deduplication
**Ação:** Definir `apps/backend/app/core/database/repositories/base_repository.py` como single source of truth
**Risco:** HIGH (afeta 900+ módulos)
**Estratégia:** Batch normalization (paralelismo disciplinado)

---

## 🔍 COMANDO ATÓMICO DE AUDITORIA (Executado)
```bash
✅ Frontend diff: Completado
✅ Alembic count: 9 vs 85 migrações
✅ BaseRepository scan: 4 duplicatas encontradas
```

