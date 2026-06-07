# SILA System Workspace

Root Path:
/home/dev03wsl/sila-system

Primary Backend Root:
/home/dev03wsl/sila-system/apps/backend/app/modules

Environment:
- WSL2 Ubuntu 24.04
- Windows 11 Host
- Python enterprise backend
- Hexagonal architecture
- X-Road interoperability strategy
- PostgreSQL
- Redis
- Celery

Repository Characteristics:
- Massive modular monolith / federated services architecture
- 900+ service domains consolidated into module structure
- Parallel infrastructure and domain segmentation
- Heavy compliance and audit requirements
- Multi-sector governmental architecture

Critical Index Files:
- docs/tree.md
- docs/modules/tree.modules.txt

Primary Architecture:
Hexagonal Architecture + X-Road interoperability

Core Module Location:
apps/backend/app/modules/

Workspace Rules:
- Use docs/tree.md and docs/modules/tree.modules.txt strictly as indexes
- Never recursively scan the entire repository
- Use grep/find/Select-String for targeted discovery
- Read only relevant files after path discovery
- Preserve context window efficiency
- Preserve architecture boundaries strictly
- Never collapse domain/infrastructure separation
- Never introduce circular dependencies
- Prefer root-cause fixes over superficial patches

Execution Strategy:
- Parallel batch normalization
- Compliance-first operations
- Audit-before-purge
- Infrastructure/domain isolation
- X-Road port-based interoperability
- Structured consolidation workflows

Important Commands:
cd ~/sila-system
make clean-audit
make daily-audit
cat reports/daily_audit.md

Validation Commands:
pytest
make clean-audit
make daily-audit

Expected Agent Behavior:
- Autonomous repository analysis
- Intelligent module discovery
- Runtime validation
- Dependency inspection
- Safe architectural refactoring
- Compliance reporting
- Batch-based normalization
- Infrastructure-safe execution

Never:
- recursively load the full repository
- purge before successful audit
- refactor blindly across modules
- break bounded contexts
- violate hexagonal architecture
- bypass X-Road interoperability boundaries
- modify unrelated modules during normalization