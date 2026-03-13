# Consolidation Conformance Report: justice

**Generated**: 2026-03-12 15:51:42
**Module Path**: `apps\backend\app\modules\justice\core`
**Overall Status**: PASSED
**Conformance Score**: 96.0%

---

## Hexagonal Directory Structure

PASS domain/
PASS application/
PASS infrastructure/

**Score**: 3/3 items

## Required Boundary Files

PASS domain/__init__.py (Domain exports)
PASS application/__init__.py (Application exports)
PASS infrastructure/__init__.py (Infrastructure exports)

**Score**: 3/3 items

## Circular Dependency Detection


**Status**: PASS

## Entity Consolidation

PASS Entities in domain/entities/
  - Count: 0
PASS Orphaned entities outside domain/entities
  - Count: 0

**Score**: 1/2 items

## Service Unification

PASS Application services
  - Count: 1

**Score**: 1/1 items

## Infrastructure Isolation

PASS finances_service_adapter.py
PASS educacao_service_adapter.py
PASS assistencia_social_service_adapter.py
PASS saude_service_adapter.py
PASS juventude_service_adapter.py
PASS request_tracking_service_adapter.py
PASS notification_service_adapter.py
PASS attestation_service_adapter.py
PASS civil_registry_adapter.py
PASS emprego_service_adapter.py
PASS certificate_service_adapter.py
PASS civil_registry_port.py

**Score**: 12/12 items

## Port Definitions

PASS Ports directory exists
  - Count: 2
PASS Ports using ABC/abstractmethod
  - Count: 1

**Score**: 2/2 items

## Test Coverage

PASS Test directories found
  - Count: 1
PASS Test files found
  - Count: 1

**Score**: 2/2 items

---

## Sign-Off

Module consolidated and audit passed
