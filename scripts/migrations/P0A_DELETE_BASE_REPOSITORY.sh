#!/bin/bash
# P0-A: BATCH DELETE base_repository.py phantom files
# Generated: March 16, 2026

echo "🔥 FASE 0-A: Deleting 26 base_repository.py phantom files..."
echo ""

FILES=(
  "apps/backend/app/modules/energy/domain/repositories/base_repository.py"
  "apps/backend/app/modules/tourism/domain/repositories/base_repository.py"
  "apps/backend/app/modules/payment/domain/repositories/base_repository.py"
  "apps/backend/app/modules/documents/domain/repositories/base_repository.py"
  "apps/backend/app/modules/api/domain/repositories/base_repository.py"
  "apps/backend/app/modules/civil_protection/domain/repositories/base_repository.py"
  "apps/backend/app/modules/logistics/domain/repositories/base_repository.py"
  "apps/backend/app/modules/infrastructure_sector/domain/repositories/base_repository.py"
  "apps/backend/app/modules/migration_service/domain/repositories/base_repository.py"
  "apps/backend/app/modules/industry/domain/repositories/base_repository.py"
  "apps/backend/app/modules/saude/domain/repositories/base_repository.py"
  "apps/backend/app/modules/procurement/domain/repositories/base_repository.py"
  "apps/backend/app/modules/compliance/domain/repositories/base_repository.py"
  "apps/backend/app/modules/educacao/domain/repositories/base_repository.py"
  "apps/backend/app/modules/justice/domain/repositories/base_repository.py"
  "apps/backend/app/modules/public_security/domain/repositories/base_repository.py"
  "apps/backend/app/modules/governance/domain/repositories/base_repository.py"
  "apps/backend/app/modules/intelligence/domain/repositories/base_repository.py"
  "apps/backend/app/modules/operations/domain/repositories/base_repository.py"
  "apps/backend/app/modules/xroad/domain/repositories/base_repository.py"
  "apps/backend/app/modules/identity/domain/repositories/base_repository.py"
  "apps/backend/app/modules/resources/domain/repositories/base_repository.py"
  "apps/backend/app/modules/audit/domain/repositories/base_repository.py"
  "apps/backend/app/modules/society/domain/repositories/base_repository.py"
  "apps/backend/app/modules/infrastructure/domain/repositories/base_repository.py"
  "apps/backend/app/modules/economy/domain/repositories/base_repository.py"
)

DELETED=0
FAILED=0

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    rm "$file"
    echo "✅ Deleted: $file"
    ((DELETED++))
  else
    echo "⚠️  Not found: $file"
    ((FAILED++))
  fi
done

echo ""
echo "🎉 RESULT: $DELETED files deleted, $FAILED not found"
echo "📊 NET EFFECT: 26 phantom files removed from codebase"
echo ""
echo "✅ P0-A COMPLETE: base_repository.py consolidation successful"
