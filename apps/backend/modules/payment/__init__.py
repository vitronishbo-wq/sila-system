"""
Payment Module

Responsável por:
- Processamento de pagamentos
- Gestão de transações
- Integração com múltiplos provedores
- Serviços, repositórios, schemas e endpoints FastAPI

Nota:
Este __init__.py não importa automaticamente routers, models ou services.
Isso evita:
    - importações circulares
    - carregamento precoce de dependências pesadas
    - falhas em testes (ex.: psycopg2)
    - problemas em ambientes sem FastAPI/Pydantic

Para usar componentes específicos, importe diretamente:
    from modules.payment.endpoints import router
    from modules.payment.models.payment import Payment
    from modules.payment.services.payment_service import PaymentService
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
