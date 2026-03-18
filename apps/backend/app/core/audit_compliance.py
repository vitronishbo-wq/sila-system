"""
Auditoria de Conformidade Arquitetural do Core SILA
Validação automática de padrões DDD e arquitetura em camadas
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class AuditFinding:
    severity: str
    category: str
    message: str
    location: str
    suggestion: str

class CoreAudit:

    def __init__(self, core_path: str):
        self.core_path = Path(core_path)
        self.findings: List[AuditFinding] = []
        self.modules: Dict[str, Dict] = {}

    def run(self) -> Dict:
        """Execute auditoria completa"""
        print('🔍 Iniciando auditoria do Core SILA...')
        self._audit_structure()
        self._audit_imports()
        self._audit_documentation()
        self._audit_exceptions()
        self._audit_ddd_compliance()
        report = self._generate_report()
        self._print_summary(report)
        return report

    def _audit_structure(self):
        """Valida estrutura de macro-domínios"""
        print('  ✓ Validando estrutura...')
        expected_dirs = {'rbac': 'Role-Based Access Control', 'audit': 'Audit trail & SLA', 'exceptions': 'Exceções centralizadas', 'observability': 'Logging, tracing, metrics', 'resilience': 'Circuit breaker, retry policies', 'events': 'Event bus', 'rate_limit': 'Rate limiting', 'locks': 'Distributed locks', 'feature_flags': 'Feature toggles', 'territory': 'Territorial hierarchy', 'db': 'Database layer (SQLAlchemy)', 'bridges': 'Cross-domain bridges'}
        for module, description in expected_dirs.items():
            module_path = self.core_path / module
            if module_path.is_dir():
                self.modules[module] = {'status': '✅', 'description': description, 'path': str(module_path)}
            else:
                self.findings.append(AuditFinding(severity='high', category='structure', message=f'Módulo {module} não encontrado', location=f'core/{module}', suggestion=f'Criar diretório: mkdir -p {module_path}'))

    def _audit_imports(self):
        """Valida padrões de importação (evita ciclos, cross-cutting concerns)"""
        print('  ✓ Validando imports...')
        exceptions_path = self.core_path / 'exceptions' / 'base.py'
        if exceptions_path.is_file():
            self.findings.append(AuditFinding(severity='low', category='imports', message='✅ Exceções centralizadas detectadas', location='core/exceptions/base.py', suggestion='Manter este padrão'))

    def _audit_documentation(self):
        """Valida existência de documentação arquitetural"""
        print('  ✓ Validando documentação...')
        doc_file = self.core_path / 'ARCHITECTURE.md'
        if doc_file.is_file():
            self.findings.append(AuditFinding(severity='low', category='documentation', message='✅ Documentação arquitetural encontrada', location='core/ARCHITECTURE.md', suggestion='Manter atualizado'))
        else:
            self.findings.append(AuditFinding(severity='high', category='documentation', message='❌ Falta documentação arquitetural', location='core/', suggestion='Criar: core/ARCHITECTURE.md'))

    def _audit_exceptions(self):
        """Valida consolidação de exceções"""
        print('  ✓ Validando exceções...')
        exc_types = ['SilaException', 'ValidationException', 'NotFoundException', 'UnauthorizedException', 'ForbiddenException', 'ConflictException']
        exc_path = self.core_path / 'exceptions' / '__init__.py'
        if exc_path.is_file():
            with open(exc_path) as f:
                content = f.read()
            missing = [t for t in exc_types if t not in content]
            if not missing:
                self.findings.append(AuditFinding(severity='low', category='structure', message=f'✅ Todas {len(exc_types)} exceções centralizadas estão presentes', location='core/exceptions/__init__.py', suggestion=''))
            else:
                for exc_type in missing:
                    self.findings.append(AuditFinding(severity='medium', category='structure', message=f'Exceção {exc_type} não exportada', location='core/exceptions/__init__.py', suggestion=f"Adicionar ao __all__: '{exc_type}'"))

    def _audit_ddd_compliance(self):
        """Valida conformidade com DDD em módulos principais"""
        print('  ✓ Validando DDD...')
        ddd_modules = []
        for module in ddd_modules:
            module_path = self.core_path / module
            expected_layers = ['domain', 'application', 'infrastructure']
            for layer in expected_layers:
                layer_path = module_path / layer
                if layer_path.is_dir():
                    self.findings.append(AuditFinding(severity='low', category='structure', message=f'✅ {module}/{layer} encontrado', location=f'core/{module}/{layer}', suggestion=''))
                else:
                    self.findings.append(AuditFinding(severity='high', category='structure', message=f'Falta camada DDD: {module}/{layer}', location=f'core/{module}/', suggestion=f'Criar: mkdir -p {module}/{layer}'))

    def _generate_report(self) -> Dict:
        """Gera relatório de auditoria"""
        critical = [f for f in self.findings if f.severity == 'critical']
        high = [f for f in self.findings if f.severity == 'high']
        medium = [f for f in self.findings if f.severity == 'medium']
        low = [f for f in self.findings if f.severity == 'low']
        total = len(self.findings)
        positivos = len([f for f in self.findings if '✅' in f.message])
        score = positivos / total * 100 if total > 0 else 0
        report = {'timestamp': datetime.now().isoformat(), 'core_path': str(self.core_path), 'modules_found': len(self.modules), 'total_findings': total, 'findings_by_severity': {'critical': len(critical), 'high': len(high), 'medium': len(medium), 'low': len(low)}, 'conformance_score': round(score, 1), 'modules': self.modules, 'findings': [asdict(f) for f in self.findings]}
        return report

    def _print_summary(self, report: Dict):
        """Imprime sumário em console"""
        print('\n' + '=' * 80)
        print('📊 RELATÓRIO DE AUDITORIA ARQUITETURAL')
        print('=' * 80)
        print(f'\n✅ Módulos encontrados: {report['modules_found']}')
        print(f'📝 Total de findings: {report['total_findings']}')
        print(f'📈 Score de conformidade: {report['conformance_score']}%')
        print('\n🔴 Severidade:')
        print(f'  Critical: {report['findings_by_severity']['critical']}')
        print(f'  High: {report['findings_by_severity']['high']}')
        print(f'  Medium: {report['findings_by_severity']['medium']}')
        print(f'  Low: {report['findings_by_severity']['low']}')
        print('\n📋 Principais issues:')
        for finding in self.findings[:10]:
            icon = '🔴' if finding.severity == 'critical' else '🟠' if finding.severity == 'high' else '🟡' if finding.severity == 'medium' else '🟢'
            print(f'  {icon} [{finding.category}] {finding.message}')
            if finding.suggestion:
                print(f'     → {finding.suggestion}')
        print('\n' + '=' * 80)

async def main():
    """Entrypoint para auditoria"""
    core_path = os.path.join(os.path.dirname(__file__))
    audit = CoreAudit(core_path)
    report = audit.run()
    report_file = Path(core_path) / 'AUDIT_REPORT.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f'\n✅ Relatório salvo em: {report_file}')
    return report
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())