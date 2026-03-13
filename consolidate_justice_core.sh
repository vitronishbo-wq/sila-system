#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

ROOT="apps/backend/app/modules/justice"
CORE="$ROOT/core"
DEPRECATED="$ROOT/_deprecated"
LEGACY="$CORE/infrastructure/legacy_adapters"
LOG="consolidate_justice_core.log"

if [ ! -d "$ROOT" ]; then
  echo "SKIP: $ROOT (root missing)"
  exit 0
fi

mkdir -p "$CORE/domain" "$CORE/application" "$CORE/infrastructure" "$DEPRECATED" "$LEGACY"
: > "$LOG"

log() {
  printf "%s\n" "$1" | tee -a "$LOG"
}

move_glob() {
  local src_glob="$1"
  local dest="$2"
  local matched=0
  local moved=0
  for path in $src_glob; do
    matched=1
    if mv -n "$path" "$dest/"; then
      moved=1
    else
      log "CONFLICT: $path -> $dest (exists)"
    fi
  done
  if [ "$matched" -eq 0 ]; then
    log "SKIP: $src_glob (no matches)"
  elif [ "$moved" -eq 1 ]; then
    log "MOVED: $src_glob -> $dest"
  else
    log "CONFLICT: $src_glob -> $dest (all existed)"
  fi
}

log "START: consolidate justice core"

# 1) Core hexagonal structure
log "STRUCTURE: $CORE/{domain,application,infrastructure}"

# 2) Domain extraction
move_glob "$ROOT/bounded_contexts/civil_registry_core/domain/entities/*" "$CORE/domain"
move_glob "$ROOT/bounded_contexts/identity_documents/domain/entities/*" "$CORE/domain"
move_glob "$ROOT/bounded_contexts/vital_events/domain/entities/*" "$CORE/domain"

# 3) Application extraction
move_glob "$ROOT/bounded_contexts/application/services/*.py" "$CORE/application"
move_glob "$ROOT/civil_registry/application/services/*.py" "$CORE/application"
move_glob "$ROOT/vital_events/application/services/*.py" "$CORE/application"

# 4) Legacy adapters isolation (no deletions)
move_glob "$ROOT/bounded_contexts/infrastructure/adapters/*" "$LEGACY"
move_glob "$ROOT/civil_registry/adapters/*" "$LEGACY"

# 5) Deprecate old contexts (no deletions)
for ctx in bounded_contexts civil_registry vital_events; do
  if [ -d "$ROOT/$ctx" ]; then
    mkdir -p "$DEPRECATED"
    mv "$ROOT/$ctx" "$DEPRECATED/"
    log "ARCHIVE: $ROOT/$ctx -> $DEPRECATED/$ctx"
  else
    log "SKIP: $ROOT/$ctx (missing)"
  fi
done

log "END: consolidate justice core"
