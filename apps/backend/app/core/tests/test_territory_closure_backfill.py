
import uuid
import pytest
from sqlalchemy import create_engine, Column, Uuid, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from app.core.models.territory_closure import TerritoryClosure

# --- Definição de Modelos Mock para o Teste ---
Base = declarative_base()

class Location(Base):
    __tablename__ = "locations"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    parent_id = Column(Uuid, ForeignKey("locations.id"), nullable=True)
    children = relationship("Location", backref="parent", remote_side=[id])

# --- Lógica de Backfill ---
def backfill_territory_closure(session):
    session.query(TerritoryClosure).delete()
    locations = session.query(Location).all()

    for loc in locations:
        # Cada local é descendente de si mesmo com profundidade 0
        session.add(TerritoryClosure(ancestor_id=loc.id, descendant_id=loc.id, depth=0))

        # Navega para cima na hierarquia
        depth = 1
        parent = loc.parent
        while parent:
            session.add(
                TerritoryClosure(
                    ancestor_id=parent.id, descendant_id=loc.id, depth=depth
                )
            )
            parent = parent.parent
            depth += 1
    session.commit()

# --- Teste Pytest ---
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TerritoryClosure.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_territory_closure_backfill(db_session):
    # 1. Setup da Hierarquia (Província > Município > Comuna)
    provincia = Location(id=uuid.uuid4())
    municipio = Location(id=uuid.uuid4(), parent_id=provincia.id)
    comuna = Location(id=uuid.uuid4(), parent_id=municipio.id)
    
    db_session.add_all([provincia, municipio, comuna])
    db_session.commit()

    # 2. Execução da Lógica de Backfill
    backfill_territory_closure(db_session)

    # 3. Validação dos Resultados
    closures = db_session.query(TerritoryClosure).all()
    closure_map = {(c.ancestor_id, c.descendant_id): c.depth for c in closures}

    # Asserções de auto-referência
    assert closure_map[(provincia.id, provincia.id)] == 0
    assert closure_map[(municipio.id, municipio.id)] == 0
    assert closure_map[(comuna.id, comuna.id)] == 0

    # Asserções de ancestralidade
    assert closure_map[(provincia.id, municipio.id)] == 1
    assert closure_map[(provincia.id, comuna.id)] == 2
    assert closure_map[(municipio.id, comuna.id)] == 1

    # Valida o número total de registros esperados
    assert len(closures) == 6 # 3 auto-referências + 3 hierárquicas
