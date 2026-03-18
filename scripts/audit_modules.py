#!/usr/bin/env python3
"""
FASE 5: Real Module Audit
Scans all 28 modules for actual problems and missing implementations.
"""

from pathlib import Path
from collections import defaultdict
import sys

class ModuleAuditor:
    def __init__(self, modules_path):
        self.modules_path = Path(modules_path)
        self.results = defaultdict(list)
        
    def audit(self):
        """Audit all modules for real issues."""
        modules = sorted([d for d in self.modules_path.iterdir() if d.is_dir() and not d.name.startswith('_')])
        
        print(f"\n{'='*80}")
        print(f"🔍 AUDITING {len(modules)} MODULES")
        print(f"{'='*80}\n")
        
        for module in modules:
            self._audit_module(module)
        
        self._print_report()
    
    def _audit_module(self, module_path):
        """Audit a single module."""
        module_name = module_path.name
        issues = []
        
        # Check api/routers.py
        router_file = module_path / "api" / "routers.py"
        if not router_file.exists():
            issues.append("❌ Missing api/routers.py")
        else:
            content = router_file.read_text(errors='ignore')
            if "@router.get" not in content and "@app.get" not in content:
                issues.append("⚠️  api/routers.py exists but no GET endpoints")
            if "/health" not in content:
                issues.append("⚠️  No /health endpoints")
        
        # Check domain/models.py
        models_file = module_path / "domain" / "models.py"
        if not models_file.exists():
            issues.append("❌ Missing domain/models.py")
        
        # Check domain/exceptions.py
        exc_file = module_path / "domain" / "exceptions.py"
        if not exc_file.exists():
            issues.append("❌ Missing domain/exceptions.py")
        
        # Check application/commands.py
        cmd_file = module_path / "application" / "commands.py"
        if not cmd_file.exists():
            issues.append("❌ Missing application/commands.py")
        
        # Check infrastructure/adapters.py
        adapter_file = module_path / "infrastructure" / "adapters.py"
        if not adapter_file.exists():
            issues.append("⚠️  Missing infrastructure/adapters.py")
        
        # Check infrastructure/repositories.py
        repo_file = module_path / "infrastructure" / "repositories.py"
        if not repo_file.exists():
            issues.append("⚠️  Missing infrastructure/repositories.py")
        
        # Check for event handlers
        handlers_file = module_path / "application" / "event_handlers.py"
        if not handlers_file.exists():
            issues.append("⚠️  Missing application/event_handlers.py")
        
        self.results[module_name] = issues
    
    def _print_report(self):
        """Print detailed audit report."""
        total_modules = len(self.results)
        modules_with_issues = sum(1 for issues in self.results.values() if issues)
        
        print(f"\n📊 SUMMARY")
        print(f"   Total Modules: {total_modules}")
        print(f"   Modules with Issues: {modules_with_issues}")
        print(f"   Health Score: {100 * (total_modules - modules_with_issues) // total_modules}%\n")
        
        # Group by issue type
        issue_counts = defaultdict(int)
        for module_issues in self.results.values():
            for issue in module_issues:
                issue_counts[issue] += 1
        
        print("🔴 TOP ISSUES")
        for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"   {issue} ({count} modules)")
        
        print("\n📋 DETAILED REPORT\n")
        for module_name in sorted(self.results.keys()):
            issues = self.results[module_name]
            if issues:
                print(f"   {module_name}")
                for issue in issues:
                    print(f"      {issue}")
                print()
    
if __name__ == "__main__":
    modules_path = Path(__file__).parent.parent / "apps" / "backend" / "app" / "modules"
    
    if not modules_path.exists():
        print(f"❌ Modules path not found: {modules_path}")
        sys.exit(1)
    
    auditor = ModuleAuditor(modules_path)
    auditor.audit()
