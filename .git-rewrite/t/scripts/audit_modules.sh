#!/bin/bash
set -euo pipefail

echo "🔍 Auditoria completa do diretório 'apps/backend/modules'..."
echo "================================================================"

BASE="apps/backend/modules"

# 1. Listar todos os módulos
echo "[1/8] Estrutura de módulos:"
ls -1 $BASE
echo "----------------------------------------------------------------"

# 2. Procurar duplicações de tabelas (__tablename__)
echo "[2/8] Procurando tabelas duplicadas (__tablename__):"
grep -R "__tablename__" --include="*.py" $BASE | sort
echo "----------------------------------------------------------------"

# 3. Procurar classes duplicadas Payment/Transaction
echo "[3/8] Procurando classes Payment/PaymentTransaction:"
grep -R "class Payment\b" --include="*.py" $BASE || true
grep -R "class PaymentTransaction\b" --include="*.py" $BASE || true
echo "----------------------------------------------------------------"

# 4. Procurar uso de model_validate (Pydantic v2)
echo "[4/8] Procurando uso de model_validate:"
grep -R "model_validate" --include="*.py" $BASE || true
echo "----------------------------------------------------------------"

# 5. Procurar enums com .value
echo "[5/8] Procurando acesso a .value em status:"
grep -R "status.value" --include="*.py" $BASE || true
echo "----------------------------------------------------------------"

# 6. Procurar referências residuais a 'finance'
echo "[6/8] Procurando referências a 'finance':"
grep -R "finance" --include="*.py" $BASE || true
echo "----------------------------------------------------------------"

# 7. Procurar imports circulares (simplificado: módulos importando-se mutuamente)
echo "[7/8] Procurando imports entre módulos:"
grep -R "^from " --include="*.py" $BASE | sort | uniq | head -n 50
echo "----------------------------------------------------------------"

# 8. Resumo final
echo "[8/8] Auditoria concluída."
echo "✅ Revise os resultados acima para duplicações, conflitos ou referências inválidas."
