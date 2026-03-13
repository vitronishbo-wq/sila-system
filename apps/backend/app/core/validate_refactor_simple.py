"""
Teste simplificado: valida consolidação de exceções e remoção de core/iam
"""
from pathlib import Path


def test_exception_exports():
    """Valida estaticamente que exceções estão exportadas no core."""
    print('🧪 TESTE ESTÁTICO: Export de exceções do core')
    exc_path = Path(__file__).resolve().parent / 'exceptions' / '__init__.py'
    if not exc_path.exists():
        raise AssertionError('❌ core/exceptions/__init__.py não encontrado')
    content = exc_path.read_text()

    expected = [
        'SilaException',
        'ValidationException',
        'NotFoundException',
        'UnauthorizedException',
        'ForbiddenException',
        'ConflictException',
    ]
    missing = [name for name in expected if name not in content]
    if missing:
        raise AssertionError(f'❌ Exceções não exportadas: {missing}')
    print(f'✅ {len(expected)} exceções exportadas corretamente')


def test_core_iam_removed():
    """Valida remoção definitiva de core/iam."""
    print('🧪 TESTE ESTÁTICO: Remoção de core/iam')
    core_iam_path = Path(__file__).resolve().parent / 'iam'
    assert not core_iam_path.exists(), '❌ core/iam ainda existe'
    print('✅ core/iam removido')


def main():
    """Executa validações"""
    print('\n' + '=' * 80)
    print('DETALHES')
    print('=' * 80)
    test_exception_exports()
    test_core_iam_removed()
    print('\n' + '=' * 80)
    print('RESULTADO')
    print('=' * 80)
    print('✅ REFACTOR VALIDADO! Nenhum problema detectado.')


if __name__ == '__main__':
    try:
        main()
    except AssertionError as exc:
        print(str(exc))
        raise SystemExit(1)
