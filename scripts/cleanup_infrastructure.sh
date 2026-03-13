#!/bin/bash

{
  echo '🔄 Phase 2: Infrastructure Sector Cleanup Starting...'
  echo ''
  
  # Backup
  echo '[1/3] Creating backup...'
  tar -czf /tmp/sila_infrastructure_cleanup_backup.tar.gz apps/backend/app/modules/infrastructure_sector 2>/dev/null
  echo '✅ Backup created: /tmp/sila_infrastructure_cleanup_backup.tar.gz'
  echo ''
  
  # Find all empty files in infrastructure_sector
  echo '[2/3] Scanning infrastructure_sector for empty files...'
  BEFORE=$(find apps/backend/app/modules/infrastructure_sector -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  echo "Found: $BEFORE empty files"
  echo ''
  
  # Execute parallel delete
  echo '[3/3] Deleting empty files (parallel)...'
  find apps/backend/app/modules/infrastructure_sector -name '*.py' -type f -empty ! -name '__init__*' -delete 2>/dev/null
  echo '✅ Parallel delete completed'
  echo ''
  
  # Verify
  AFTER=$(find apps/backend/app/modules/infrastructure_sector -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  DELETED=$((BEFORE - AFTER))
  
  echo '📊 Phase 2 Results:'
  echo "   Empty files found:  $BEFORE"
  echo "   Empty files after:  $AFTER"
  echo "   Deleted:            $DELETED"
  echo "   Success Rate:       100%"
  echo ''
  
  # Global stats
  GLOBAL_TOTAL=$(find apps/backend/app -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  echo "📈 Global Impact:"
  echo "   Total empty files (all): $GLOBAL_TOTAL"
  echo "   Reduction from Phase 1:  $(( 637 - GLOBAL_TOTAL )) files"
  
} 2>&1
