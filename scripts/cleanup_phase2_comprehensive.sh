#!/bin/bash

{
  echo '🔄 Phase 2: COMPREHENSIVE CLEANUP - All Remaining Sectors'
  echo ''
  
  # Pre-cleanup stats
  TOTAL_BEFORE=$(find apps/backend/app -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  echo "📊 Pre-cleanup: $TOTAL_BEFORE empty files"
  echo ''
  
  # Backup
  echo '[0/4] Creating comprehensive backup...'
  tar -czf /tmp/sila_phase2_comprehensive_backup.tar.gz \
    apps/backend/app/modules/resources \
    apps/backend/app/modules/governance \
    apps/backend/app/modules/operations \
    2>/dev/null
  echo '✅ Backup created'
  echo ''
  
  # Batch 1: Resources (non-ambiente)
  echo '[1/4] Cleaning Resources modules (pescas, petroleo, etc)...'
  COUNT1=$(find apps/backend/app/modules/resources -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  find apps/backend/app/modules/resources -name '*.py' -type f -empty ! -name '__init__*' -delete 2>/dev/null
  echo "✅ Deleted $COUNT1 resource schema/endpoint/model stubs"
  
  # Batch 2: Governance
  echo '[2/4] Cleaning Governance modules...'
  COUNT2=$(find apps/backend/app/modules/governance -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  find apps/backend/app/modules/governance -name '*.py' -type f -empty ! -name '__init__*' -delete 2>/dev/null
  echo "✅ Deleted $COUNT2 governance stubs"
  
  # Batch 3: Operations & Documents
  echo '[3/4] Cleaning Operations & Documents modules...'
  COUNT3=$(find apps/backend/app/modules/operations -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  COUNT4=$(find apps/backend/app/modules/documents -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  find apps/backend/app/modules/operations -name '*.py' -type f -empty ! -name '__init__*' -delete 2>/dev/null
  find apps/backend/app/modules/documents -name '*.py' -type f -empty ! -name '__init__*' -delete 2>/dev/null
  echo "✅ Deleted $((COUNT3 + COUNT4)) ops/docs stubs"
  
  # Batch 4: Catch-all remaining
  echo '[4/4] Final cleanup pass (all modules)...'
  COUNT5=$(find apps/backend/app/modules -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  find apps/backend/app/modules -name '*.py' -type f -empty ! -name '__init__*' -delete 2>/dev/null
  echo "✅ Deleted $COUNT5 remaining stubs"
  
  echo ''
  echo '📈 Phase 2 Results:'
  TOTAL_AFTER=$(find apps/backend/app -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  TOTAL_DELETED=$((TOTAL_BEFORE - TOTAL_AFTER))
  echo "   Before:     $TOTAL_BEFORE empty files"
  echo "   After:      $TOTAL_AFTER empty files"
  echo "   Deleted:    $TOTAL_DELETED files"
  echo "   Reduction:  $(( TOTAL_DELETED * 100 / TOTAL_BEFORE ))%"
  
} 2>&1
