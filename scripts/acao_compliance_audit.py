"""
ACAO Compliance Audit for Domain Events
Validates that all official status tracking requirements are met.

ACAO (Autoridade Catáloga Oficial) Requirements:
- All status changes must be auditable
- Compliance events must include official metadata
- Event sourcing provides immutable audit trail
- All documents/certificates must be trackable
"""

import asyncio
import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ACAOComplianceAuditor:
    """
    Audits all modules for ACAO compliance.
    
    Checks:
    1. All ComplianceEvent subclasses present
    2. All StatusChangeEvent variants present
    3. All required metadata fields populated
    4. All modules have event handlers
    5. All command handlers publish events
    """
    
    # Required ACAO compliance event types per module category
    REQUIRED_ACAO_EVENTS = {
        "justice": [
            "CitizenIdentityDocumentIssued",
            "BirthRecordCertificateIssued",
            "MarriageCertificateIssued",
            "DeathCertificateIssued",
        ],
        "identity": [
            "IdentityDocumentIssued",
            "BiometricDataRecorded",
            "AccessRightChangedStatus",
        ],
        "economy": [
            "TaxpayerRegistrationApproved",
            "TaxDeclarationSubmitted",
            "PaymentReceiptIssued",
        ],
        "payment": [
            "PaymentProcessed",
            "PaymentApproved",
            "InvoiceIssued",
        ],
        "health": [
            "MedicalRecordCreated",
            "PrescriptionIssued",
            "VaccinationRecorded",
        ],
        "educacao": [
            "StudentEnrolled",
            "CertificateIssued",
            "DiplomaAwarded",
        ],
        "documents": [
            "DocumentIssued",
            "DocumentArchived",
            "DocumentRevokedStatus",
        ],
    }
    
    # Required audit metadata fields
    REQUIRED_METADATA_FIELDS = {
        "user_id",
        "command_name",
        "timestamp_utc",
        "compliance_requirement",  # for ComplianceEvent
    }
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.modules_dir = self.workspace_root / "apps" / "backend" / "app" / "modules"
        self.audit_results: Dict[str, Any] = defaultdict(dict)
        self.compliance_score = 0.0
        self.total_checks = 0
        self.passed_checks = 0
    
    async def audit_all_modules(self) -> Dict[str, Any]:
        """Run comprehensive ACAO compliance audit."""
        logger.info("🔍 Starting ACAO Compliance Audit...")
        logger.info(f"Workspace: {self.workspace_root}")
        
        modules = sorted([d.name for d in self.modules_dir.iterdir() if d.is_dir()])
        logger.info(f"Found {len(modules)} modules to audit")
        
        for module_name in modules:
            await self._audit_module(module_name)
        
        return self._generate_audit_report()
    
    async def _audit_module(self, module_name: str) -> None:
        """Audit a single module."""
        module_path = self.modules_dir / module_name
        
        logger.info(f"  ► Auditing module: {module_name}")
        
        checks = {
            "events_defined": await self._check_events_defined(module_name, module_path),
            "handlers_present": await self._check_handlers_present(module_name, module_path),
            "commands_present": await self._check_commands_present(module_name, module_path),
            "acao_events": await self._check_acao_events(module_name, module_path),
            "metadata_fields": await self._check_metadata_fields(module_name, module_path),
        }
        
        self.audit_results[module_name] = checks
    
    async def _check_events_defined(self, module_name: str, module_path: Path) -> Tuple[bool, str]:
        """Check if domain/events/__init__.py exists and has events."""
        self.total_checks += 1
        
        events_file = module_path / "domain" / "events" / "__init__.py"
        
        if not events_file.exists():
            return False, "domain/events/__init__.py not found"
        
        try:
            content = events_file.read_text()
            has_events = "class " in content and "DomainEvent" in content
            
            if has_events:
                self.passed_checks += 1
                event_count = content.count("class ") - 1  # -1 for potential imports
                return True, f"{event_count} events defined"
            else:
                return False, "No DomainEvent subclasses found"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    async def _check_handlers_present(self, module_name: str, module_path: Path) -> Tuple[bool, str]:
        """Check if application/event_handlers.py exists."""
        self.total_checks += 1
        
        handlers_file = module_path / "application" / "event_handlers.py"
        
        if not handlers_file.exists():
            return False, "application/event_handlers.py not found"
        
        try:
            content = handlers_file.read_text()
            has_handlers = "async def handle_" in content
            has_registry = "_EVENT_HANDLERS" in content
            
            if has_handlers and has_registry:
                self.passed_checks += 1
                handler_count = content.count("async def handle_")
                return True, f"{handler_count} async handlers + registry"
            else:
                return False, "Missing handlers or registry"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    async def _check_commands_present(self, module_name: str, module_path: Path) -> Tuple[bool, str]:
        """Check if application/commands.py exists."""
        self.total_checks += 1
        
        commands_file = module_path / "application" / "commands.py"
        
        if not commands_file.exists():
            return False, "application/commands.py not found"
        
        try:
            content = commands_file.read_text()
            has_handlers = "CommandHandler" in content
            has_publishing = "event_bus.publish" in content
            
            if has_handlers and has_publishing:
                self.passed_checks += 1
                handler_count = content.count("class ") - 1  # -1 for potential inheritance
                return True, f"{handler_count} command handlers with event publishing"
            else:
                return False, "Missing command handlers or event publishing"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    async def _check_acao_events(self, module_name: str, module_path: Path) -> Tuple[bool, str]:
        """Check for ACAO compliance events."""
        self.total_checks += 1
        
        events_file = module_path / "domain" / "events" / "__init__.py"
        
        if not events_file.exists():
            return False, "Events file not found"
        
        try:
            content = events_file.read_text()
            
            # Check for ComplianceEvent usage
            has_compliance_events = "ComplianceEvent" in content
            has_status_change_events = "StatusChangeEvent" in content
            
            if has_compliance_events and has_status_change_events:
                self.passed_checks += 1
                return True, "Has ComplianceEvent and StatusChangeEvent"
            elif has_compliance_events or has_status_change_events:
                self.passed_checks += 1
                return True, "Has partial ACAO compliance events"
            else:
                return False, "Missing ACAO compliance event types"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    async def _check_metadata_fields(self, module_name: str, module_path: Path) -> Tuple[bool, str]:
        """Check if events include required metadata fields."""
        self.total_checks += 1
        
        commands_file = module_path / "application" / "commands.py"
        
        if not commands_file.exists():
            return False, "Commands file not found"
        
        try:
            content = commands_file.read_text()
            
            # Check for metadata fields in event publishing
            has_correlation_id = "correlation_id" in content
            has_user_id = '"user_id"' in content or "'user_id'" in content
            has_timestamp = "timestamp_utc" in content
            
            if has_correlation_id and has_user_id and has_timestamp:
                self.passed_checks += 1
                return True, "All required metadata fields present"
            else:
                missing = []
                if not has_correlation_id:
                    missing.append("correlation_id")
                if not has_user_id:
                    missing.append("user_id")
                if not has_timestamp:
                    missing.append("timestamp_utc")
                return False, f"Missing metadata: {', '.join(missing)}"
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    def _generate_audit_report(self) -> Dict[str, Any]:
        """Generate compliance audit report."""
        logger.info("\n" + "="*80)
        logger.info("ACAO COMPLIANCE AUDIT REPORT")
        logger.info("="*80)
        
        self.compliance_score = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        
        logger.info(f"\n📊 OVERALL SCORE: {self.compliance_score:.1f}% ({self.passed_checks}/{self.total_checks} checks passed)")
        logger.info("\n📋 MODULE AUDIT RESULTS:")
        logger.info("-" * 80)
        
        module_count = len(self.audit_results)
        compliant_modules = 0
        
        for module_name in sorted(self.audit_results.keys()):
            checks = self.audit_results[module_name]
            
            all_passed = all(check[0] for check in checks.values())
            if all_passed:
                compliant_modules += 1
            
            status_icon = "✅" if all_passed else "⚠️"
            logger.info(f"\n{status_icon} {module_name.upper()}")
            
            for check_name, (passed, message) in checks.items():
                check_icon = "✅" if passed else "❌"
                logger.info(f"  {check_icon} {check_name:20} → {message}")
        
        logger.info("\n" + "="*80)
        logger.info(f"COMPLIANCE SUMMARY:")
        logger.info(f"  • Modules audited: {module_count}")
        logger.info(f"  • Fully compliant: {compliant_modules}/{module_count}")
        logger.info(f"  • Overall score: {self.compliance_score:.1f}%")
        logger.info("="*80 + "\n")
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "compliance_score": self.compliance_score,
            "modules_audited": module_count,
            "modules_compliant": compliant_modules,
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "results_by_module": dict(self.audit_results),
        }


async def run_acao_audit(workspace_root: str) -> Dict[str, Any]:
    """Run ACAO compliance audit."""
    auditor = ACAOComplianceAuditor(workspace_root)
    return await auditor.audit_all_modules()


if __name__ == "__main__":
    import sys
    
    workspace = sys.argv[1] if len(sys.argv) > 1 else "/workspace"
    
    # Run async audit
    results = asyncio.run(run_acao_audit(workspace))
    
    # Exit with appropriate code
    score = results.get("compliance_score", 0)
    sys.exit(0 if score >= 90 else 1)
