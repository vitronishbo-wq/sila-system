#!/bin/bash

{
  echo '🔄 Starting parallel cleanup batches...'
  echo ''
  
  # Backup
  echo '[1/6] Creating backup...'
  tar -czf /tmp/sila_before_cleanup.tar.gz apps/backend/app/modules/resources/ambiente 2>/dev/null
  echo '✅ Backup created'
  echo ''
  
  # Batch 1: Ambiente schemas
  echo '[2/6] Cleaning Ambiente schemas...'
  COUNT1=$(find apps/backend/app/modules/resources/ambiente/api/schemas -name '*.py' -type f -empty 2>/dev/null | wc -l)
  find apps/backend/app/modules/resources/ambiente/api/schemas -name '*.py' -type f -empty -delete 2>/dev/null
  echo "✅ Deleted $COUNT1 schema stubs"
  
  # Batch 2: Ambiente endpoints
  echo '[3/6] Cleaning Ambiente endpoints...'
  COUNT2=$(find apps/backend/app/modules/resources/ambiente/api/endpoints -name '*.py' -type f -empty 2>/dev/null | wc -l)
  find apps/backend/app/modules/resources/ambiente/api/endpoints -name '*.py' -type f -empty -delete 2>/dev/null
  echo "✅ Deleted $COUNT2 endpoint stubs"
  
  # Batch 3: Ambiente models
  echo '[4/6] Cleaning Ambiente models...'
  COUNT3=$(find apps/backend/app/modules/resources/ambiente/domain/models -name '*.py' -type f -empty 2>/dev/null | wc -l)
  find apps/backend/app/modules/resources/ambiente/domain/models -name '*.py' -type f -empty -delete 2>/dev/null
  echo "✅ Deleted $COUNT3 model stubs"
  
  # Batch 4: Ambiente tests
  echo '[5/6] Cleaning Ambiente tests...'
  COUNT4=$(find apps/backend/app/modules/resources/ambiente/tests -name '*.py' -type f -empty 2>/dev/null | wc -l)
  find apps/backend/app/modules/resources/ambiente/tests -name '*.py' -type f -empty -delete 2>/dev/null
  echo "✅ Deleted $COUNT4 test stubs"
  
  echo ''
  echo '[6/6] Verifying cleanup...'
  TOTAL_BEFORE=726
  TOTAL_AFTER=$(find apps/backend/app -name '*.py' -type f -empty ! -name '__init__*' 2>/dev/null | wc -l)
  REMOVED=$((TOTAL_BEFORE - TOTAL_AFTER))
  
  echo "📊 Results:"
  echo "   Before: $TOTAL_BEFORE empty files"
  echo "   After:  $TOTAL_AFTER empty files"
  echo "   Removed: $REMOVED files"
  echo "   Reduction: $((REMOVED * 100 / TOTAL_BEFORE))%"
} 2>&1
