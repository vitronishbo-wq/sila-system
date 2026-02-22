import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from contextlib import contextmanager

# Logger para rastreabilidade de transações de base de dados
logger = logging.getLogger(__name__)

# Configuração de conexão via ambiente (12-Factor App)
# O fallback é mantido para ambiente de desenvolvimento local
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://sila_admin:sila_pass_2024@localhost:5432/sila_financas"
)

# Engine com parâmetros de resiliência e performance enterprise
# pool_size: número de conexões mantidas abertas
# max_overflow: conexões extras permitidas em picos de carga
# pool_pre_ping: verifica se a conexão é válida antes de cada uso (evita 500s por timeout de socket)
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False
)

# Fábrica de sessões configurada para controlo manual de transações
# autocommit=False: EXIGE commit() explícito, permitindo transações atómicas
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency Provider para injeção de dependência em rotas FastAPI.
    Utiliza o padrão unit-of-work por requisição HTTP.
    """
    db = SessionLocal()
    try:
        yield db
        # Nota: O commit deve ser feito no serviço ou repositório.
        # Caso queira commit automático por request, poderia ser adicionado aqui.
    finally:
        db.close()

@contextmanager
def transactional_session() -> Generator[Session, None, None]:
    """
    Context Manager Enterprise para execução de transações atómicas robustas.
    Implementa o padrão explícito de Commit/Rollback/Close para máxima segurança.
    
    Este padrão é ideal para operações em segundo plano (background tasks), 
    processamento de webhooks e lógica de serviço complexa que envolve múltiplas tabelas.
    
    Exemplo de uso:
    with transactional_session() as session:
        # Operações de base de dados...
        # Se sair do bloco sem erro, executa COMMIT.
        # Se ocorrer qualquer exceção, executa ROLLBACK.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
        logger.debug("Transação consolidada (COMMIT) com sucesso.")
    except Exception as e:
        db.rollback()
        logger.error(f"Falha na transação de base de dados. Executado ROLLBACK. Detalhes: {str(e)}")
        raise e
    finally:
        db.close()
