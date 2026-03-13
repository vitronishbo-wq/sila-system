#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

ROOT="apps/backend/app/modules/identity"
CORE="$ROOT/core"
DEPRECATED="$ROOT/_deprecated"
LEGACY="$CORE/infrastructure/legacy_adapters"
LOG="consolidate_identity_core.log"

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

log "START: consolidate identity core"
log "STRUCTURE: $CORE/{domain,application,infrastructure}"

process_ctx() {
  local ctx="$1"
  local candidates=(
    "$ROOT/$ctx"
    "$ROOT/bounded_contexts/$ctx"
    "$DEPRECATED/$ctx"
    "$DEPRECATED/bounded_contexts/$ctx"
  )
  local src=""
  for path in "${candidates[@]}"; do
    if [ -d "$path" ]; then
      src="$path"
      break
    fi
  done
  if [ -z "$src" ]; then
    log "SKIP: $ROOT/$ctx (missing)"
    return
  fi

  move_glob "$src/domain/*" "$CORE/domain"
  move_glob "$src/application/*" "$CORE/application"
  move_glob "$src/infrastructure/*" "$CORE/infrastructure"
  move_glob "$src/adapters/*" "$LEGACY"

  if [ "$src" = "$ROOT/$ctx" ] || [ "$src" = "$ROOT/bounded_contexts/$ctx" ]; then
    mkdir -p "$DEPRECATED"
    mv "$src" "$DEPRECATED/"
    log "ARCHIVE: $ROOT/$ctx -> $DEPRECATED/$ctx"
  else
    log "ARCHIVE: $src (already deprecated)"
  fi
}

for ctx in sovereign_identity_wallet credential_management; do
  process_ctx "$ctx"
done

log "END: consolidate identity core"
