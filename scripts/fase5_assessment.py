#!/usr/bin/env python3
"""
FASE 5 Assessment Script
Scans the system for ports/adapters, routers, health checks, and domain logic.
Provides baseline metrics for integration testing.
"""

import subprocess
import json
from pathlib import Path
from collections import defaultdict
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)


class FASE5Assessor:
    """Assess system readiness for FASE 5: Integration Tests."""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.modules_dir = self.workspace_root / "apps" / "backend" / "app" / "modules"
        self.results = defaultdict(dict)
    
    def run_assessment(self):
        """Run complete FASE 5 assessment."""
        logger.info("\n" + "="*80)
        logger.info("🔍 FASE 5: INTEGRATION TESTS — SYSTEM ASSESSMENT")
        logger.info("="*80 + "\n")
        
        self._assess_routers()
        self._assess_ports_adapters()
        self._assess_health_checks()
        self._assess_domain_entities()
        self._assess_events()
        
        self._print_summary()
    
    def _assess_routers(self):
        """Check for routers in all modules."""
        logger.info("📡 SCANNING ROUTERS...")
        
        routers = self._find_files("**/api/router.py")
        logger.info(f"   Found: {len(routers)} routers\n")
        
        for router in sorted(routers):
            module_name = router.parent.parent.parent.name
            with open(router) as f:
                content = f.read()
                has_prefix = "prefix=" in content
                has_tags = "tags=" in content
                has_health = "/health" in content
                
                self.results[module_name]["router"] = {
                    "exists": True,
                    "has_prefix": has_prefix,
                    "has_tags": has_tags,
                    "has_health": has_health,
                    "status": "✅" if all([has_prefix, has_tags, has_health]) else "⚠️"
                }
    
    def _assess_ports_adapters(self):
        """Check for ports and adapters."""
        logger.info("🔌 SCANNING PORTS & ADAPTERS...")
        
        ports = self._find_files("**/application/*_port.py")
        adapters = self._find_files("**/infrastructure/*_adapter.py")
        
        logger.info(f"   Found: {len(ports)} ports, {len(adapters)} adapters\n")
        
        for module_dir in sorted(self.modules_dir.iterdir()):
            if not module_dir.is_dir():
                continue
            
            module_name = module_dir.name
            module_ports = len([p for p in ports if module_name in str(p)])
            module_adapters = len([a for a in adapters if module_name in str(a)])
            
            self.results[module_name]["ports"] = {
                "count": module_ports,
                "status": "✅" if module_ports > 0 else "❌"
            }
            
            self.results[module_name]["adapters"] = {
                "count": module_adapters,
                "status": "✅" if module_adapters >= module_ports else "⚠️"
            }
    
    def _assess_health_checks(self):
        """Check for health check endpoints."""
        logger.info("❤️  SCANNING HEALTH CHECKS...")
        
        health_files = self._find_files("**/api/health.py")
        logger.info(f"   Found: {len(health_files)} health modules\n")
        
        for module_dir in sorted(self.modules_dir.iterdir()):
            if not module_dir.is_dir():
                continue
            
            module_name = module_dir.name
            has_health = any(module_name in str(h) for h in health_files)
            
            # Also check in router
            router_file = module_dir / "api" / "router.py"
            has_health_endpoint = False
            if router_file.exists():
                with open(router_file) as f:
                    content = f.read()
                    has_health_endpoint = "/health" in content
            
            self.results[module_name]["health"] = {
                "has_health_module": has_health,
                "has_health_endpoint": has_health_endpoint,
                "status": "✅" if has_health_endpoint else "⚠️"
            }
    
    def _assess_domain_entities(self):
        """Check domain entities and aggregates."""
        logger.info("📦 SCANNING DOMAIN ENTITIES...")
        
        entities = self._find_files("**/domain/entities/*.py")
        domain_files = self._find_files("**/domain/*.py")
        
        logger.info(f"   Found: {len(entities)} entity files, {len(domain_files)} domain files\n")
        
        for module_dir in sorted(self.modules_dir.iterdir()):
            if not module_dir.is_dir():
                continue
            
            module_name = module_dir.name
            domain_dir = module_dir / "domain"
            
            file_count = 0
            if domain_dir.exists():
                file_count = len(list(domain_dir.rglob("*.py"))) - 1  # -1 for __init__
            
            self.results[module_name]["domain"] = {
                "file_count": file_count,
                "has_entities": file_count > 0,
                "status": "✅" if file_count > 0 else "❌"
            }
    
    def _assess_events(self):
        """Check domain events."""
        logger.info("⚡ SCANNING DOMAIN EVENTS...")
        
        events_files = self._find_files("**/domain/events/__init__.py")
        logger.info(f"   Found: {len(events_files)} event definitions\n")
        
        for module_dir in sorted(self.modules_dir.iterdir()):
            if not module_dir.is_dir():
                continue
            
            module_name = module_dir.name
            events_file = module_dir / "domain" / "events" / "__init__.py"
            
            has_events = events_file.exists()
            event_count = 0
            
            if has_events:
                with open(events_file) as f:
                    content = f.read()
                    event_count = content.count("class ") - content.count("(ABC)")
            
            self.results[module_name]["events"] = {
                "has_events": has_events,
                "event_count": event_count,
                "status": "✅" if has_events else "❌"
            }
    
    def _find_files(self, pattern: str):
        """Find files matching pattern."""
        try:
            result = subprocess.run(
                ["find", str(self.modules_dir), "-name", pattern.split("/")[-1]],
                capture_output=True,
                text=True,
                timeout=5
            )
            return [Path(p) for p in result.stdout.strip().split("\n") if p]
        except Exception as e:
            logger.warning(f"Error finding files: {e}")
            return []
    
    def _print_summary(self):
        """Print summary report."""
        logger.info("\n" + "="*80)
        logger.info("📊 FASE 5 BASELINE METRICS")
        logger.info("="*80 + "\n")
        
        # Module-by-module summary
        logger.info("✅ MODULE COMPLIANCE STATUS\n")
        
        module_count = 0
        compliant = 0
        
        for module_name in sorted(self.results.keys()):
            module_count += 1
            checks = self.results[module_name]
            
            # Calculate module score
            status_icons = [v.get("status", "❌") for v in checks.values()]
            all_good = all(s == "✅" for s in status_icons)
            
            if all_good:
                compliant += 1
            
            logger.info(f"  {module_name:20} | " + " ".join(status_icons))
        
        logger.info("\n" + "-"*80)
        logger.info(f"TOTAL MODULES: {module_count} | FULLY COMPLIANT: {compliant}/{module_count}\n")
        
        # Category summary
        logger.info("📈 COMPONENT COVERAGE\n")
        
        categories = ["router", "ports", "adapters", "health", "domain", "events"]
        
        for category in categories:
            count = 0
            compliant_count = 0
            
            for module_data in self.results.values():
                if category in module_data:
                    count += 1
                    if module_data[category].get("status") == "✅":
                        compliant_count += 1
            
            if count > 0:
                pct = (compliant_count / count * 100)
                bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
                logger.info(f"  {category:10} | {bar} {pct:.0f}% ({compliant_count}/{count})")
        
        logger.info("\n" + "="*80)
        logger.info("🎯 NEXT STEPS FOR FASE 5\n")
        
        logger.info("1. Create test_ports_and_adapters.py")
        logger.info("   - Validate port/adapter pairs")
        logger.info("   - Check circular dependencies")
        logger.info("")
        logger.info("2. Create test_domain_logic.py")
        logger.info("   - Test aggregate invariants")
        logger.info("   - Test value object immutability")
        logger.info("")
        logger.info("3. Create test_router_validation.py")
        logger.info("   - Verify health endpoints")
        logger.info("   - Check OpenAPI contracts")
        logger.info("")
        logger.info("4. Create test_module_boundaries.py")
        logger.info("   - Build dependency graph")
        logger.info("   - Detect circular dependencies")
        logger.info("")
        logger.info("5. Create Docker E2E tests")
        logger.info("   - Full workflow testing")
        logger.info("   - RabbitMQ integration")
        logger.info("   - Event replay validation")
        logger.info("")
        logger.info("="*80 + "\n")
        
        logger.info(f"💾 Compliance Baseline: {(compliant/module_count*100):.0f}%")
        logger.info(f"📦 Ready for BATCH 1: Port/Adapter Validation\n")


def main():
    import sys
    
    workspace = sys.argv[1] if len(sys.argv) > 1 else "/home/dev03wsl/sila-system/apps/backend"
    
    assessor = FASE5Assessor(workspace)
    assessor.run_assessment()


if __name__ == "__main__":
    main()
