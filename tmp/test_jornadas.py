import json, subprocess, sys

BASE = 'http://localhost:8000'

def test(label, method='GET', path='/', body=None, expected=None):
    url = BASE + path
    try:
        if method == 'GET':
            r = subprocess.run(['curl', '-s', '-w', '\n%{http_code}', '-o', '/dev/stderr', url],
                             capture_output=True, text=True, timeout=5)
        elif method == 'POST':
            r = subprocess.run(['curl', '-s', '-w', '\n%{http_code}', '-X', 'POST', url,
                             '-H', 'Content-Type: application/json', '-d', json.dumps(body or {})],
                             capture_output=True, text=True, timeout=5)
        out = r.stdout.strip()
        code = r.stderr.strip().split('\n')[-1] if r.stderr else '???'
        ok = code.startswith('2') if expected is None else code == str(expected)
        status = 'OK' if ok else 'FAIL'
        print(f'  [{status}] {label}  ({code})')
        return ok
    except subprocess.TimeoutExpired:
        print(f'  [FAIL] {label}  (timeout)')
        return False
    except Exception as e:
        print(f'  [FAIL] {label}  ({e})')
        return False

results = []

print('=== JORNADA 1 — Identidade / FUC ===')
results.append(test('Health - live', 'GET', '/api/health/live'))
results.append(test('Health - ready', 'GET', '/api/health/ready'))
results.append(test('Auth - whoami (no auth)', 'GET', '/api/auth/whoami'))
results.append(test('Auth - me (no auth)', 'GET', '/api/auth/me'))
results.append(test('Citizen - profile (no auth)', 'GET', '/api/citizen/profile'))
results.append(test('Citizen - events (no auth)', 'GET', '/api/citizen/events'))
results.append(test('Identity - subdomains', 'GET', '/api/v1/identidade'))

print()
print('=== JORNADA 2 — Educação ===')
results.append(test('Educacao - marketplace discovery', 'GET', '/educacao/marketplace/discovery'))
results.append(test('Educacao - marketplace search', 'GET', '/educacao/marketplace/search'))
results.append(test('Marketplace - search health', 'GET', '/marketplace/search/health'))
results.append(test('Service catalog', 'GET', '/api/v1/service-catalog'))
results.append(test('Portal', 'GET', '/api/v1/portal'))

print()
print('=== JORNADA 3 — Saúde ===')
results.append(test('Society - assistencia social', 'GET', '/society/assistencia_social/assistencia-social'))
results.append(test('Society - seguranca social', 'GET', '/society/seguranca_social/seguranca-social'))
results.append(test('Society - familia', 'GET', '/society/familia/familia'))
results.append(test('Society - tests', 'GET', '/society/tests/society-test'))

print()
print('=== JORNADA 4 — Governança / Workflow ===')
results.append(test('Workflow', 'GET', '/governance/workflow/workflow'))
results.append(test('Goverance - admin local', 'GET', '/governance/administracao_local/administracao_local'))
results.append(test('Service requests', 'GET', '/governance/service_requests/service-requests'))
results.append(test('Admin - dashboard', 'GET', '/api/admin/dashboard'))
results.append(test('Admin - citizens', 'GET', '/api/admin/citizens'))

print()
print('=== INFRA ===')
results.append(test('Providers - health', 'GET', '/api/providers/health'))
results.append(test('Providers - metrics', 'GET', '/api/providers/metrics'))

print(f'\nRESULTADO: {sum(results)}/{len(results)} OK')
