Title: TECH-DEBT: remove domain enums shim & migrate imports

Description: Remove temporary shim at `apps/backend/app/domain/enums.py` and migrate imports to canonical module enums.

Checklist:
- Replace imports `from apps.backend.app.domain.enums` with module-specific imports
- Remove `apps/backend/app/domain/enums.py`
- Run `make clean-audit && make daily-audit` and `pytest` to validate

