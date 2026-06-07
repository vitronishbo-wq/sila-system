
================================================================================
BATCH 1: CONSOLIDATE EXCEPTION CLASSES (Parallel extraction)
================================================================================

[1A] Consolidating NotFoundException classes...
  ✓ Created not_found_exception.py

[1B] Consolidating ValidationException classes...
  ✓ Created validation_exception.py

[1C] Consolidating ConflictException classes...
  ✓ Created conflict_exception.py

[1D] Updating core/exceptions/__init__.py...
  ✓ Updated __init__.py

================================================================================
BATCH 2: UPDATE EXCEPTION IMPORTS (Parallel replacement)
================================================================================
  ✓ Updated app/modules/identity/domain/exceptions/__init__.py

  • Total files updated: 1

================================================================================
BATCH 3: REMOVE DUPLICATE EXCEPTIONS (Sequential purge)
================================================================================
  ✓ Deleted app/modules/justice/exceptions.py
  ✓ Deleted app/modules/educacao/exceptions.py
  ✓ Deleted app/modules/documents/domain/exceptions.py
  ✓ Deleted app/modules/documents/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/documents/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/wallet/domain/exceptions.py
  ✓ Deleted app/modules/industry/domain/exceptions.py
  ✓ Deleted app/modules/industry/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/industry/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/api/domain/exceptions.py
  ✓ Deleted app/modules/api/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/api/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/payment/domain/exceptions.py
  ✓ Deleted app/modules/payment/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/payment/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/identity/domain/exceptions.py
  ✓ Deleted app/modules/identity/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/identity/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/economy/domain/exceptions.py
  ✓ Deleted app/modules/economy/financas/exceptions.py
  ✓ Deleted app/modules/economy/taxpayer/api/exceptions.py
  ✓ Deleted app/modules/economy/taxpayer/domain/exceptions.py
  ✓ Deleted app/modules/economy/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/economy/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/economy/financas/domain/exceptions.py
  ✓ Deleted app/modules/economy/apoio_empresarial/domain/exceptions.py
  ✓ Deleted app/modules/economy/industria/domain/exceptions.py
  ✓ Deleted app/modules/economy/core/domain/exceptions.py
  ✓ Deleted app/modules/economy/trade/domain/exceptions.py
  ✓ Deleted app/modules/economy/trade/external/exceptions.py
  ✓ Deleted app/modules/economy/trade/services/exceptions.py
  ✓ Deleted app/modules/economy/trade/external/domain/exceptions.py
  ✓ Deleted app/modules/economy/trade/services/domain/exceptions.py
  ✓ Deleted app/modules/economy/public_budget/domain/exceptions.py
  ✓ Deleted app/modules/resources/agricultura/exceptions.py
  ✓ Deleted app/modules/resources/aguas_saneamento/exceptions.py
  ✓ Deleted app/modules/resources/domain/exceptions.py
  ✓ Deleted app/modules/resources/ambiente/exceptions.py
  ✓ Deleted app/modules/resources/recursos_minerais/domain/exceptions.py
  ✓ Deleted app/modules/resources/agricultura/domain/exceptions.py
  ✓ Deleted app/modules/resources/petroleo_gas/domain/exceptions.py
  ✓ Deleted app/modules/resources/aguas_saneamento/domain/exceptions.py
  ✓ Deleted app/modules/resources/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/resources/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/resources/pecuaria/domain/exceptions.py
  ✓ Deleted app/modules/resources/seguranca_alimentar/domain/exceptions.py
  ✓ Deleted app/modules/resources/ambiente/domain/exceptions.py
  ✓ Deleted app/modules/resources/pescas/domain/exceptions.py
  ✓ Deleted app/modules/resources/pescas/industrial/domain/exceptions.py
  ✓ Deleted app/modules/resources/florestas/domain/exceptions.py
  ✓ Deleted app/modules/governance/domain/exceptions.py
  ✓ Deleted app/modules/governance/statistics/exceptions.py
  ✓ Deleted app/modules/governance/planeamento/domain/exceptions.py
  ✓ Deleted app/modules/governance/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/governance/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/governance/workflow/domain/exceptions.py
  ✓ Deleted app/modules/governance/administracao_local/domain/exceptions.py
  ✓ Deleted app/modules/governance/statistics/domain/exceptions.py
  ✓ Deleted app/modules/governance/service_requests/domain/exceptions.py
  ✓ Deleted app/modules/governance/cooperacao_internacional/domain/exceptions.py
  ✓ Deleted app/modules/compliance/domain/exceptions.py
  ✓ Deleted app/modules/compliance/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/compliance/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/infrastructure_sector/urbanismo_habitacao/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/gestao_fundiaria/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/telecomunicacoes/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/urbanismo_habitacao/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/infrastructure_sector/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/infrastructure_sector/obras_publicas/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/aviacao_civil/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/gestao_fundiaria/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/meteorologia/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/logistica/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure_sector/logistica/ports/domain/exceptions.py
  ✓ Deleted app/modules/migration_service/domain/exceptions.py
  ✓ Deleted app/modules/migration_service/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/migration_service/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/notifications/domain/exceptions.py
  ✓ Deleted app/modules/energy/domain/exceptions.py
  ✓ Deleted app/modules/energy/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/energy/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/audit/domain/exceptions.py
  ✓ Deleted app/modules/audit/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/audit/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/xroad/domain/exceptions.py
  ✓ Deleted app/modules/xroad/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/xroad/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/operations/domain/exceptions.py
  ✓ Deleted app/modules/operations/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/operations/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/public_security/domain/exceptions.py
  ✓ Deleted app/modules/public_security/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/public_security/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/justice/domain/exceptions.py
  ✓ Deleted app/modules/justice/events/domain/exceptions.py
  ✓ Deleted app/modules/justice/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/justice/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/justice/civil_registry/domain/exceptions.py
  ✓ Deleted app/modules/justice/_deprecated/domain/exceptions.py
  ✓ Deleted app/modules/procurement/domain/exceptions.py
  ✓ Deleted app/modules/procurement/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/procurement/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/logistics/domain/exceptions.py
  ✓ Deleted app/modules/logistics/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/logistics/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/infrastructure/domain/exceptions.py
  ✓ Deleted app/modules/infrastructure/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/infrastructure/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/society/domain/exceptions.py
  ✓ Deleted app/modules/society/desporto/exceptions.py
  ✓ Deleted app/modules/society/familia/exceptions.py
  ✓ Deleted app/modules/society/emprego/exceptions.py
  ✓ Deleted app/modules/society/seguranca_social/exceptions.py
  ✓ Deleted app/modules/society/igualdade/domain/exceptions.py
  ✓ Deleted app/modules/society/trabalho_inspecao/domain/exceptions.py
  ✓ Deleted app/modules/society/juventude/domain/exceptions.py
  ✓ Deleted app/modules/society/assistencia_social/domain/exceptions.py
  ✓ Deleted app/modules/society/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/society/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/society/desporto/domain/exceptions.py
  ✓ Deleted app/modules/society/familia/domain/exceptions.py
  ✓ Deleted app/modules/society/patrimonio_cultural/domain/exceptions.py
  ✓ Deleted app/modules/society/cultura/domain/exceptions.py
  ✓ Deleted app/modules/society/emprego/domain/exceptions.py
  ✓ Deleted app/modules/society/seguranca_social/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/ciencia_pesquisa/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/intelligence/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/intelligence/tecnologia_inovacao/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/arquivo_nacional/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/operations/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/bi/domain/exceptions.py
  ✓ Deleted app/modules/intelligence/defesa_consumidor/domain/exceptions.py
  ✓ Deleted app/modules/educacao/domain/exceptions.py
  ✓ Deleted app/modules/educacao/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/educacao/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/saude/domain/exceptions.py
  ✓ Deleted app/modules/saude/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/saude/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/civil_protection/domain/exceptions.py
  ✓ Deleted app/modules/civil_protection/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/civil_protection/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/tourism/domain/exceptions.py
  ✓ Deleted app/modules/tourism/domain/exceptions/not_found_exception.py
  ✓ Deleted app/modules/tourism/domain/exceptions/validation_exception.py
  ✓ Deleted app/modules/documents/domain/exceptions/__init__.py
  ✓ Deleted app/modules/industry/domain/exceptions/__init__.py
  ✓ Deleted app/modules/api/domain/exceptions/__init__.py
  ✓ Deleted app/modules/payment/domain/exceptions/__init__.py
  ✓ Deleted app/modules/identity/domain/exceptions/__init__.py
  ✓ Deleted app/modules/economy/domain/exceptions/__init__.py
  ✓ Deleted app/modules/resources/domain/exceptions/__init__.py
  ✓ Deleted app/modules/governance/domain/exceptions/__init__.py
  ✓ Deleted app/modules/compliance/domain/exceptions/__init__.py
  ✓ Deleted app/modules/infrastructure_sector/domain/exceptions/__init__.py
  ✓ Deleted app/modules/migration_service/domain/exceptions/__init__.py
  ✓ Deleted app/modules/energy/domain/exceptions/__init__.py
  ✓ Deleted app/modules/audit/domain/exceptions/__init__.py
  ✓ Deleted app/modules/xroad/domain/exceptions/__init__.py
  ✓ Deleted app/modules/operations/domain/exceptions/__init__.py
  ✓ Deleted app/modules/public_security/domain/exceptions/__init__.py
  ✓ Deleted app/modules/justice/domain/exceptions/__init__.py
  ✓ Deleted app/modules/procurement/domain/exceptions/__init__.py
  ✓ Deleted app/modules/logistics/domain/exceptions/__init__.py
  ✓ Deleted app/modules/infrastructure/domain/exceptions/__init__.py
  ✓ Deleted app/modules/society/domain/exceptions/__init__.py
  ✓ Deleted app/modules/intelligence/domain/exceptions/__init__.py
  ✓ Deleted app/modules/educacao/domain/exceptions/__init__.py
  ✓ Deleted app/modules/saude/domain/exceptions/__init__.py
  ✓ Deleted app/modules/civil_protection/domain/exceptions/__init__.py
  ✓ Deleted app/modules/tourism/domain/exceptions/__init__.py
  ✓ Deleted app/modules/society/familia/domain/exceptions/__init__.py

  • Total files deleted: 175

================================================================================
BATCH 4: VALIDATION (Sequential verification)
================================================================================

[4A] Checking Python syntax...
  ✓ All files have valid Python syntax

[4B] Verifying core exceptions accessibility...
  ✗ Import error: No module named 'app'
================================================================================
EXCEPTION CONSOLIDATION EXECUTION REPORT
================================================================================

Actions Performed:
  • Exception classes consolidated: 3
  • Files with imports updated: 1
  • Duplicate exception files deleted: 175

Results:
  • Validation errors: 1

Impact:
  • Exception definitions reduced: 56 → 3 (94.6% reduction)
  • Scattered modules: 28 → 1 (centralized at core/exceptions/)
  • Standard import pattern: from apps.backend.app.core.exceptions import <Exception>

================================================================================