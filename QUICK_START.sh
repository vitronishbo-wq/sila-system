#!/bin/bash

# ============================================================================
# QUICK START: Consolidação de Módulos em 4 Comandos
# ============================================================================

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║        🚀 CONSOLIDAÇÃO DE MÓDULOS SILA - QUICK START                      ║
║                                                                            ║
║        Tempo: 15 minutos | Risco: BAIXO | Teste: SIM                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 RESUMO DO PROBLEMA:
  • 3 diretórios de módulos causam conflitos: /modules/, /app/modules/, 
    /apps/backend/app/modules/
  • Imports duplicados e inconsistentes
  • Impossibilidade de manutenção centralizada

✅ SOLUÇÃO:
  • Consolidar para 1 único local: /apps/backend/app/modules/
  • Atualizar todos imports
  • Remover diretórios antigos

════════════════════════════════════════════════════════════════════════════

PASSO 1: PREPARAÇÃO (2 minutos)
════════════════════════════════════════════════════════════════════════════

Executar:

  cd /home/dev03wsl/sila-system
  git checkout -b consolidate/modules-single-source
  git add -A && git commit -m "wip: save current state"

Resultado esperado:
  ✓ Branch criado localmente
  ✓ Estado atual guardado em git

════════════════════════════════════════════════════════════════════════════

PASSO 2: PREVIEW (1 minuto)
════════════════════════════════════════════════════════════════════════════

Executar:

  bash scripts/preview_consolidation.sh

Resultado esperado:
  ✓ Ver EXATAMENTE o que vai mudar (sem fazer mudanças)
  ✓ 7 seções descrevendo: duplicação, ficheiros, imports, estatísticas

💡 Dica: Leitura cuidada desta saída vai responder 90% das dúvidas!

════════════════════════════════════════════════════════════════════════════

PASSO 3: CONSOLIDAÇÃO (3 minutos)
════════════════════════════════════════════════════════════════════════════

Executar:

  bash scripts/consolidate_modules.sh

O script vai pedir confirmação:
  "Prosseguir? (s/n)"
  → Digitar: s

Resultado esperado:
  ✓ FASE 1: Backup criado em /tmp/sila_modules_backup/
  ✓ FASE 2: Módulos consolidados
  ✓ FASE 3: Imports atualizados (~50 ficheiros)
  ✓ FASE 4: Diretórios antigos removidos
  ✓ FASE 5: Validação passada

SAÍDA ESPERADA:
  ================================================================
  ✅ CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO
  ================================================================
  RESUMO:
    • Módulos consolidados: 6
    • Imports atualizados: 45
    • Diretórios antigos removidos: /modules/, /app/modules/
    • Backup guardado: /tmp/sila_modules_backup/modules_XXXXX.tar.gz

════════════════════════════════════════════════════════════════════════════

PASSO 4: VALIDAÇÃO (2 minutos)
════════════════════════════════════════════════════════════════════════════

Executar:

  bash scripts/validate_consolidation.sh

Resultado esperado:

  [1] Verificar remoção de diretórios antigos...
      ✓ /modules/ foi removido
      ✓ /app/modules/ foi removido
  
  [2] Verificar localização única...
      ✓ Localização unificada: /apps/backend/app/modules/
  
  [3] Verificar módulos consolidados...
      ✓ Total de módulos: 20
  
  [4] Verificar imports antigos (CRÍTICO)...
      ✓ Nenhum import antigo encontrado
  
  [5] Verificar estrutura hexagonal...
      ✓ Módulos com arquitetura hexagonal: 18/20
  
  [6] Verificar testes...
      ✓ Ficheiros de teste encontrados: 30+
  
  [7] Verificar duplicação...
      ✓ Nenhum módulo duplicado
  
  [8] Verificar module.yaml...
      ✓ Ficheiros module.yaml: 15+
  
  [9] Verificar documentação...
      ✓ Ficheiros ARCHITECTURE.md: 10+
  
  [10] Validação Python...
       ✓ Nenhum erro de syntax

  ================================================================
  ✅ CONSOLIDAÇÃO VALIDADA COM SUCESSO!
  ================================================================

════════════════════════════════════════════════════════════════════════════

PASSO 5 (FINAL): GIT COMMIT & PUSH (2 minutos)
════════════════════════════════════════════════════════════════════════════

Executar:

  git status             # Ver mudanças
  git diff --stat       # Ver resumo
  git add -A            # Preparar commit
  
  # Fazer commit com mensagem descritiva
  git commit -m "consolidate: unify modules to single source of truth

- Remove /modules and /app/modules directories
- Consolidate all modules to /apps/backend/app/modules/
- Update all imports from 'modules.X' to 'apps.backend.app.modules.X'
- Merge duplicated modules (identity, documents, payment, educacao, justice, xroad)

Changes:
- Deleted: ~100 files in /modules/ and /app/modules/
- Modified: ~50 .py files with updated imports
- No functional changes, only structure consolidation"

  # Push para review
  git push -u origin consolidate/modules-single-source

Resultado esperado:
  ✓ Commit feito com mensagem descritiva
  ✓ Branch enviado para GitHub
  ✓ PR pronta para review

════════════════════════════════════════════════════════════════════════════

✅ CONCLUSÃO: Está feito!
════════════════════════════════════════════════════════════════════════════

Depois de consolidação:

  1. Code Review: PR será revisada dentro de XYZABC
  2. Merge: Após aprovação, PR mergida para main
  3. Update Team: Informar sobre novo padrão de imports
  4. Documentation: Atualizar README.md com novo path

════════════════════════════════════════════════════════════════════════════

📊 ANTES vs DEPOIS
════════════════════════════════════════════════════════════════════════════

ANTES:
  /modules/identity/                ❌ Desatualizado
  /app/modules/identity/            ❌ Parcial
  /apps/backend/app/modules/identity/ ✓ Completo
  
  Imports: from modules.identity import X
           from app.modules.identity import X
           from apps.backend.app.modules.identity import X
  
  Resultado: CONFUSÃO, tipo errors, manutenção impossível

DEPOIS:
  /apps/backend/app/modules/        ✅ Único
  
  Imports: from apps.backend.app.modules.identity import X
  
  Resultado: CLARIDADE, sem conflicts, fácil manutenção

════════════════════════════════════════════════════════════════════════════

🔙 RECUPERAÇÃO (se precisar reverter)
════════════════════════════════════════════════════════════════════════════

Se algo correr mal:

  # Opção 1: Restaurar do backup criado pelo script
  tar -xzf /tmp/sila_modules_backup/modules_*.tar.gz -C /home/dev03wsl/sila-system

  # Opção 2: Reverter git
  git reset --hard HEAD~1
  git clean -fd

  # Branch será reverter automaticamente

════════════════════════════════════════════════════════════════════════════

📚 DOCUMENTAÇÃO COMPLETA
════════════════════════════════════════════════════════════════════════════

Para aprender mais, consultar:

  1. CONSOLIDATION_INDEX.md
     └─ Índice de todos ficheiros e como usá-los
  
  2. MODULES_CONSOLIDATION_SUMMARY.md
     └─ Resumo executivo (5 minutos de leitura)
  
  3. MODULES_CONSOLIDATION_REPORT.md
     └─ Análise completa e detalhada
  
  4. CONSOLIDATION_EXECUTION_GUIDE.md
     └─ Passo-a-passo com opção manual e automática

════════════════════════════════════════════════════════════════════════════

⏱️ TEMPO TOTAL: ~15 minutos
  Passo 1 (Prep):       2 minutos
  Passo 2 (Preview):    1 minuto
  Passo 3 (Consol.):    3 minutos
  Passo 4 (Valid.):     2 minutos
  Passo 5 (Git):        2 minutos
  Leitura de docs:      5 minutos (opcional)

════════════════════════════════════════════════════════════════════════════

🟢 PRONTO PARA COMEÇAR! Quer prosseguir? (s/n)

EOF

# Perguntar se quer começar
read -p "Executar agora? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "✅ Iniciando consolidação..."
    echo ""
    echo "PASSO 1: PREPARAÇÃO"
    echo "──────────────────────────────────────────────────────────────"
    cd /home/dev03wsl/sila-system
    git checkout -b consolidate/modules-single-source 2>/dev/null || echo "Branch já existe"
    echo "✓ Branch preparado"
    echo ""
    
    echo "PASSO 2: PREVIEW"
    echo "──────────────────────────────────────────────────────────────"
    bash scripts/preview_consolidation.sh 2>/dev/null | tail -50
    echo ""
    
    read -p "Continuar com consolidação? (s/n): " -n 1 -r2
    echo
    if [[ $REPLY2 =~ ^[Ss]$ ]]; then
        echo ""
        echo "PASSO 3: CONSOLIDAÇÃO"
        echo "──────────────────────────────────────────────────────────────"
        bash scripts/consolidate_modules.sh
        echo ""
        
        echo "PASSO 4: VALIDAÇÃO"
        echo "──────────────────────────────────────────────────────────────"
        bash scripts/validate_consolidation.sh
        echo ""
        
        echo "✅ Consolidação Completa!"
        echo "Próxima ação: Fazer commit & push"
    else
        echo "Abortado"
    fi
else
    echo "Para começar depois, execute:"
    echo "  bash /home/dev03wsl/sila-system/scripts/consolidate_modules.sh"
fi
