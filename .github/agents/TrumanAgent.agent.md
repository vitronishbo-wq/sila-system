# SILA CORE v3 — AGENT EXECUTION PROTOCOL

## WORKSPACE IDENTITY

## MANDATORY STARTUP SEQUENCE

Antes de responder a qualquer pedido técnico:

Resolver o módulo alvo.

Ler docs/tree.json.

Ler docs/modules/tree.modules.json.

Usar tree.md e tree.modules.txt apenas como fallback.

## HARD CONSTRAINTS

PROIBIDO

Recursively scan the repository.

Infer file paths.

Open entire directories.

Read more than 200 lines per file chunk.

Read more than 5 files per cycle.

Modify files that were not explicitly read.

Break hexagonal architecture boundaries.

Introduce circular dependencies.

Modify generated audit reports.

## REQUIRED WORKFLOW

BEFORE EDITING

Return exactly:

AFTER EDITING

Execute exactly:

## BLOCKING CONDITIONS

Stop immediately and return:

If any of these are missing:

resolved paths

entrypoints

workflows

tests

## SUCCESS CRITERIA

Only return STATUS: OK if all are true:

imports valid

tests passed

daily-audit passed

indexes updated

## MANDATORY OUTPUT FORMAT