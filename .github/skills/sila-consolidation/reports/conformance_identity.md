# Consolidation Conformance Report: identity

**Generated**: 2026-03-12 14:48:48
**Module Path**: `apps\backend\app\modules\identity\core`
**Overall Status**: PASSED
**Conformance Score**: 30.8%

---

## Hexagonal Directory Structure

PASS domain/
PASS application/
PASS infrastructure/

**Score**: 3/3 items

## Required Boundary Files

WARN domain/__init__.py (Domain exports)
WARN application/__init__.py (Application exports)
WARN infrastructure/__init__.py (Infrastructure exports)

**Score**: 0/3 items

## Circular Dependency Detection


**Status**: PASS

## Entity Consolidation

PASS Entities in domain/entities/
  - Count: 0
PASS Orphaned entities outside domain/entities
  - Count: 0

**Score**: 1/2 items

## Service Unification

WARN Application services
  - Count: 0

**Score**: 0/1 items

## Infrastructure Isolation

WARN Unknown

**Score**: 0/1 items

## Port Definitions

WARN Ports directory

**Score**: 0/1 items

## Test Coverage

WARN Test directories found
  - Count: 0
WARN Test files found
  - Count: 0

**Score**: 0/2 items

---

## Sign-Off

Module consolidated and audit passed
