#!/usr/bin/env python3
"""Full event reconciliation: Registry vs Runtime."""
from pathlib import Path
import re, json

modules_path = Path('apps/backend/app/modules')

# ---- STEP 1: Extract Registry Events from bootstrap.py ----
bootstrap = Path('sila_platform/governance/bootstrap.py').read_text(encoding='utf-8')

# Parse all ModuleRegistry registrations
registry_events = {}  # module -> {exposes: [], consumes: []}
for m in re.finditer(r'module="([^"]+)".*?exposed_events=\[(.*?)\].*?consumed_events=\[(.*?)\]', bootstrap, re.DOTALL):
    mod = m.group(1)
    exposes = re.findall(r'"([^"]+)"', m.group(2))
    consumes = re.findall(r'"([^"]+)"', m.group(3))
    registry_events[mod] = {'exposes': exposes, 'consumes': consumes}

print(f"Registry modules with events: {len(registry_events)}")
for mod, ev in sorted(registry_events.items()):
    print(f"  {mod}: exposes={ev['exposes']}, consumes={ev['consumes']}")

# ---- STEP 2: Extract Runtime Events ----
# 2a. Domain event classes (from domain/events/__init__.py)
runtime_events = {}  # module -> [class names]
for f in sorted(modules_path.rglob('domain/events/__init__.py')):
    rel = f.relative_to(modules_path)
    parts = rel.parts
    # The module name is typically the first part
    if len(parts) >= 4:
        # e.g., economy/domain/events/__init__.py -> mod="economy"
        # or economy/core/domain/events/__init__.py -> mod="economy"
        mod = parts[0]
        # Handle deeper paths like economy/core/domain/events/__init__.py
        idx = list(parts).index('domain')
        if idx >= 1:
            if idx == 1:
                mod = parts[0]
            else:
                mod = '/'.join(parts[:idx])
    
    content = f.read_text(encoding='utf-8')
    # Find class definitions that inherit from DomainEvent
    classes = re.findall(r'^class\s+(\w+)\s*\(', content, re.MULTILINE)
    event_types = re.findall(r'self\.event_type\s*=\s*"([^"]+)"', content)
    
    if mod not in runtime_events:
        runtime_events[mod] = {'classes': [], 'event_types': []}
    runtime_events[mod]['classes'].extend(classes)
    runtime_events[mod]['event_types'].extend(event_types)

# 2b. Event handler registrations (from application/event_handlers.py)
handler_events = {}  # module -> {handles: [event names]}
for f in sorted(modules_path.rglob('application/event_handlers.py')):
    rel = f.relative_to(modules_path)
    mod = rel.parts[0]
    content = f.read_text(encoding='utf-8')
    # Find handler dict entries: "EventName": handle_func
    handled = re.findall(r'"(\w+)"\s*:\s*handle_', content)
    if mod not in handler_events:
        handler_events[mod] = []
    handler_events[mod].extend(handled)

print(f"\nRuntime modules with domain events: {len(runtime_events)}")
for mod, ev in sorted(runtime_events.items()):
    print(f"  {mod}: classes={ev['classes']}, event_types={ev['event_types']}")

print(f"\nRuntime modules with event handlers: {len(handler_events)}")
for mod, ev in sorted(handler_events.items()):
    print(f"  {mod}: handles={ev}")

# ---- STEP 3: Build Reconciliation Table ----
# Collect all unique event names from both sides
all_registry_events = set()
all_runtime_events = set()
registry_event_map = {}  # event_name -> [modules that expose/consume it]
runtime_event_map = {}   # event_name -> [modules that define/handle it]

for mod, ev in registry_events.items():
    for e in ev['exposes']:
        all_registry_events.add(e)
        registry_event_map.setdefault(e, []).append(f"{mod}(exposes)")
    for e in ev['consumes']:
        all_registry_events.add(e)
        registry_event_map.setdefault(e, []).append(f"{mod}(consumes)")

for mod, ev in runtime_events.items():
    for e in ev['event_types']:
        all_runtime_events.add(e)
        runtime_event_map.setdefault(e, []).append(f"{mod}(defines)")
    for e in ev['classes']:
        all_runtime_events.add(e)
        runtime_event_map.setdefault(e, []).append(f"{mod}(class)")

for mod, ev in handler_events.items():
    for e in ev:
        all_runtime_events.add(e)
        runtime_event_map.setdefault(e, []).append(f"{mod}(handles)")

all_events = sorted(all_registry_events | all_runtime_events)

# ---- STEP 4: Classify each event ----
results = []
for event in all_events:
    in_registry = event in all_registry_events
    in_runtime = event in all_runtime_events
    registry_refs = registry_event_map.get(event, [])
    runtime_refs = runtime_event_map.get(event, [])
    
    # Determine status
    if in_registry and in_runtime:
        # Check if names match semantically
        status = "VALID"
    elif in_registry and not in_runtime:
        status = "REGISTRY_ONLY"
    elif not in_registry and in_runtime:
        status = "RUNTIME_ONLY"
    else:
        status = "GHOST_EVENT"
    
    # Check for name mismatch (registry uses snake_case, runtime uses PascalCase)
    registry_snake = event  # e.g., "citizen_updated"
    runtime_pascal = ''.join(w.capitalize() for w in event.split('_'))  # e.g., "CitizenUpdated"
    
    if status == "REGISTRY_ONLY":
        # Check if PascalCase version exists in runtime
        if runtime_pascal in all_runtime_events:
            status = "NAME_MISMATCH"
    
    results.append({
        'event': event,
        'registry_name': event,
        'runtime_name': runtime_pascal if in_runtime else (runtime_pascal if status == "NAME_MISMATCH" else 'N/A'),
        'registry_refs': registry_refs,
        'runtime_refs': runtime_refs,
        'in_registry': in_registry,
        'in_runtime': in_runtime,
        'status': status
    })

# Print summary
print(f"\n=== Reconciliation Summary ===")
status_counts = {}
for r in results:
    status_counts[r['status']] = status_counts.get(r['status'], 0) + 1
    print(f"  {r['status']:20s} {r['event']:40s} registry={r['registry_refs']} runtime={r['runtime_refs']}")

print(f"\nStatus counts: {status_counts}")

# ---- STEP 5: Write Report ----
r1 = f"""# EVENT TRUTH RECONCILIATION REPORT

> Gerado em: 2026-06-08
> Proposito: Reconciliar eventos entre RegistryCatalog e Runtime real

---

## Resumo

| Metrica | Valor |
|---|---|
| Total eventos Registry | {len(all_registry_events)} |
| Total eventos Runtime | {len(all_runtime_events)} |
| Total eventos reconciliados | {len(all_events)} |
| VALID | {status_counts.get('VALID', 0)} |
| REGISTRY_ONLY (Ghost) | {status_counts.get('REGISTRY_ONLY', 0)} |
| RUNTIME_ONLY | {status_counts.get('RUNTIME_ONLY', 0)} |
| NAME_MISMATCH | {status_counts.get('NAME_MISMATCH', 0)} |

## Tabela de Reconciliacao

| Evento | Registry Name | Runtime Name | Registry | Runtime | Status |
|---|---|---|---|---|---|
"""
for r in results:
    reg_refs = ', '.join(r['registry_refs']) if r['registry_refs'] else '-'
    rt_refs = ', '.join(r['runtime_refs']) if r['runtime_refs'] else '-'
    r1 += f"| {r['event']} | {r['registry_name']} | {r['runtime_name']} | {reg_refs} | {rt_refs} | {r['status']} |\n"

r1 += f"""
## Eventos REGISTRY_ONLY (Ghost Events)

Estes eventos existem no RegistryCatalog mas NAO existem no codigo runtime:

| Evento | Publisher (Registry) | Subscribers (Registry) | Acao |
|---|---|---|---|
"""
for r in results:
    if r['status'] == 'REGISTRY_ONLY':
        publishers = [x for x in r['registry_refs'] if '(exposes)' in x]
        consumers = [x for x in r['registry_refs'] if '(consumes)' in x]
        r1 += f"| {r['event']} | {', '.join(publishers) if publishers else '-'} | {', '.join(consumers) if consumers else '-'} | CORRIGIR alias ou REMOVER |\n"

r1 += f"""
## Eventos NAME_MISMATCH

Estes eventos tem nomes diferentes entre Registry (snake_case) e Runtime (PascalCase):

| Registry Name | Runtime Name | Modulos Afetados | Acao |
|---|---|---|---|
"""
for r in results:
    if r['status'] == 'NAME_MISMATCH':
        r1 += f"| {r['registry_name']} | {r['runtime_name']} | {', '.join(r['registry_refs'])} | Alias registry_name -> runtime_name |\n"

r1 += f"""
## Eventos RUNTIME_ONLY

Estes eventos existem no codigo runtime mas NAO estao no RegistryCatalog:

| Evento | Modulo | Acao |
|---|---|---|
"""
for r in results:
    if r['status'] == 'RUNTIME_ONLY':
        r1 += f"| {r['event']} | {', '.join(r['runtime_refs'])} | Adicionar ao RegistryCatalog |\n"

r1 += """
## Plano de Correcacao

### Acao 1: Corrigir `citizen_updated`
- Registry: `identity` expoe `citizen_updated` (consumido por 11 modulos)
- Runtime: NAO EXISTE. Identity module define `IdentityDocumentVerified`, `IdentityDocumentStatusChanged`, etc.
- Solucao: 
  - Renomear no RegistryCatalog: `citizen_updated` -> `IdentityDocumentVerified`
  - Ou adicionar alias: registry guarda ambos os nomes

### Acao 2: Corrigir `identity_verified`
- Registry: `identity` expoe `identity_verified` (consumido por 11 modulos)
- Runtime: NAO EXISTE como string. A classe `IdentityDocumentVerified` existe.
- Solucao:
  - Renomear: `identity_verified` -> `IdentityDocumentVerified`

### Acao 3: RegistryCatalog sync
- Adicionar todos os eventos RUNTIME_ONLY ao RegistryCatalog
- Remover ou criar alias para eventos REGISTRY_ONLY

### Acao 4: Automacao
- Criar script `scripts/sync_events.py` que valida registry vs runtime
- Integrar no `make daily-audit`
"""

Path('reports/EVENT_TRUTH_REPORT.md').write_text(r1, encoding='utf-8')
print("\n[OK] EVENT_TRUTH_REPORT.md")

# ---- STEP 6: Write JSON ----
json_output = {
    'timestamp': '2026-06-08',
    'summary': {
        'total_registry_events': len(all_registry_events),
        'total_runtime_events': len(all_runtime_events),
        'total_reconciled': len(all_events),
        'valid': status_counts.get('VALID', 0),
        'registry_only': status_counts.get('REGISTRY_ONLY', 0),
        'runtime_only': status_counts.get('RUNTIME_ONLY', 0),
        'name_mismatch': status_counts.get('NAME_MISMATCH', 0),
    },
    'events': results
}

Path('reports/EVENT_RECONCILIATION.json').write_text(json.dumps(json_output, indent=2, ensure_ascii=False), encoding='utf-8')
print("[OK] EVENT_RECONCILIATION.json")

# ---- STEP 7: Generate bootstrap.py patch ----
# Build the corrected events mapping
corrected_events = {}
for mod, ev in registry_events.items():
    new_exposes = []
    for e in ev['exposes']:
        runtime_pascal = ''.join(w.capitalize() for w in e.split('_'))
        if runtime_pascal in all_runtime_events:
            new_exposes.append(runtime_pascal)
        else:
            new_exposes.append(e)
    new_consumes = []
    for e in ev['consumes']:
        runtime_pascal = ''.join(w.capitalize() for w in e.split('_'))
        if runtime_pascal in all_runtime_events:
            new_consumes.append(runtime_pascal)
        else:
            new_consumes.append(e)
    corrected_events[mod] = {'exposes': new_exposes, 'consumes': new_consumes}

print(f"\n=== Suggested bootstrap.py corrections ===")
for mod, ev in sorted(corrected_events.items()):
    orig = registry_events[mod]
    if ev['exposes'] != orig['exposes'] or ev['consumes'] != orig['consumes']:
        print(f"{mod}:")
        if ev['exposes'] != orig['exposes']:
            print(f"  exposes: {orig['exposes']} -> {ev['exposes']}")
        if ev['consumes'] != orig['consumes']:
            print(f"  consumes: {orig['consumes']} -> {ev['consumes']}")
