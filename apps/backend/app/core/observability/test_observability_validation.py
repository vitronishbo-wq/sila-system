"""
Teste de Validação - Observabilidade de Nível Governamental

Valida:
1. ContextVars fluem corretamente
2. JSON Formatter produz output válido
3. Circuit Breaker funciona corretamente
4. Middleware injeta contexto
5. OTel está pronto (sem erros)
"""
import json
import logging
import sys
from pathlib import Path
BACKEND_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BACKEND_ROOT))

def test_context_vars():
    """Valida ContextVars e correlação."""
    print('🧪 Teste 1: ContextVars')
    try:
        from app.core.observability.context import set_request_context, get_request_id, get_user_id, get_context_dict
        request_id = set_request_context(user_id='user_123', territory_id='province_luanda')
        assert get_request_id() == request_id, 'Request ID não corresponde'
        assert get_user_id() == 'user_123', 'User ID não corresponde'
        context = get_context_dict()
        assert 'request_id' in context
        assert context['user_id'] == 'user_123'
        print('✅ ContextVars funcionando corretamente')
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
        assert False, f'Erro: {e}'

def test_json_formatter():
    """Valida formatação JSON estruturada."""
    print('🧪 Teste 2: JSON Formatter')
    try:
        from app.core.observability.enterprise_formatter import SilaEnterpriseJSONFormatter
        formatter = SilaEnterpriseJSONFormatter()
        record = logging.LogRecord(name='test.logger', level=logging.INFO, pathname='test.py', lineno=42, msg='Teste de log estruturado', args=(), exc_info=None)
        output = formatter.format(record)
        data = json.loads(output)
        assert 'timestamp' in data, 'Falta timestamp'
        assert 'level' in data, 'Falta level'
        assert 'message' in data, 'Falta message'
        assert 'request_id' in data, 'Falta request_id'
        assert data['level'] == 'INFO', f'Level incorreto: {data['level']}'
        print(f'✅ JSON Formatter produz output válido')
        print(f'   Sample: {json.dumps(data)[:100]}...')
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
        assert False, f'Erro: {e}'

def test_circuit_breaker():
    """Valida Circuit Breaker."""
    print('🧪 Teste 3: Circuit Breaker')
    try:
        from app.core.resilience.circuit_breaker_patterns import CircuitBreaker, CircuitBreakerOpen
        cb = CircuitBreaker(name='test-service', failure_threshold=3, recovery_timeout=60, expected_exception=ValueError)

        def failing_func():
            raise ValueError('Operação falhou')
        for i in range(3):
            try:
                cb.call(failing_func)
            except ValueError:
                pass
        from app.core.resilience.circuit_breaker_patterns import CircuitState
        assert cb.state == CircuitState.OPEN, 'Circuit não abriu após falhas'
        try:
            cb.call(failing_func)
            assert False, 'Deveria ter levantado CircuitBreakerOpen'
        except CircuitBreakerOpen:
            pass
        stats = cb.stats
        assert stats.failure_count >= 3, 'Contagem de falhas incorreta'
        print('✅ Circuit Breaker funcionando corretamente')
        print(f'   Stats: {stats.failure_count} falhas, état={stats.state.value}')
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
        assert False, f'Erro: {e}'

def test_otel_availability():
    """Valida disponibilidade de OTel (graceful degradation)."""
    print('🧪 Teste 4: OpenTelemetry Availability')
    try:
        from app.core.observability.otel_integration import OTEL_AVAILABLE
        if OTEL_AVAILABLE:
            print('✅ OpenTelemetry disponível (pacotes instalados)')
        else:
            print('⚠️ OpenTelemetry não instalado (graceful degradation)')
            print('   Install: pip install opentelemetry-api opentelemetry-sdk')
    except Exception as e:
        print(f'❌ Erro: {e}')
        assert False, f'Erro: {e}'

def main():
    """Executa todos os testes."""
    print('=' * 80)
    print('🔬 SUITE DE TESTES: OBSERVABILIDADE GOVERNAMENTAL')
    print('=' * 80)
    tests = [('ContextVars', test_context_vars), ('JSON Formatter', test_json_formatter), ('Circuit Breaker', test_circuit_breaker), ('OTel Availability', test_otel_availability)]
    failures = []
    for name, test_fn in tests:
        try:
            test_fn()
        except AssertionError as e:
            failures.append((name, str(e)))
        except Exception as e:
            failures.append((name, str(e)))
    print('\n' + '=' * 80)
    print('📊 RESULTADO')
    print('=' * 80)
    total = len(tests)
    passed = total - len(failures)
    for name, _ in tests:
        icon = '❌' if any((f[0] == name for f in failures)) else '✅'
        print(f'{icon} {name}')
    print(f'\n✅ PASSOU: {passed}/{total} testes')
    if passed == total:
        print('\n🎉 OBSERVABILIDADE GOVERNAMENTAL VALIDADA!')
        return
    print(f'\n⚠️ {total - passed} teste(s) falharam')
    assert not failures, f'{len(failures)} teste(s) falharam'
if __name__ == '__main__':
    import sys
    try:
        main()
    except AssertionError:
        sys.exit(1)