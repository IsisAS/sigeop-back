import pytest
from typing import Generator
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, event
from sqlalchemy.orm import sessionmaker, Session

from src.main import app
from src.db.base import Base
from src.core.deps import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("ATTACH DATABASE ':memory:' AS sigeop")
    cursor.execute("PRAGMA foreign_keys=OFF")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def _reset_factories():
    """Reset factory counters before each test to ensure consistent state."""
    from tests.helpers import (
        StatusFactory, TipoFactory, PPIFactory, PedidoFactory,
        TematicaFactory, UnidadeFactory, TematicaVinculoFactory,
        AnalistaFactory, AgenteFactory, CasoStatusFactory, CasoFactory,
        OperacaoTipoFactory, OperacaoStatusFactory, OperacaoFactory,
        MissaoTipoFactory, MissaoStatusFactory, MissaoFactory,
        PlanoStatusFactory, PlanoTipoFactory, PlanoFactory, PlanoMissaoFactory
    )
    
    for factory in [
        StatusFactory, TipoFactory, PPIFactory, PedidoFactory,
        TematicaFactory, UnidadeFactory, TematicaVinculoFactory,
        AnalistaFactory, AgenteFactory, CasoStatusFactory, CasoFactory,
        OperacaoTipoFactory, OperacaoStatusFactory, OperacaoFactory,
        MissaoTipoFactory, MissaoStatusFactory, MissaoFactory,
        PlanoStatusFactory, PlanoTipoFactory, PlanoFactory, PlanoMissaoFactory
    ]:
        factory.reset()
    yield

@pytest.fixture(autouse=True)
def _mock_ciclo_client():
    """Prevents real HTTP calls to the Ciclo API during all tests."""
    with patch("src.integrations.ciclo.ciclo_client.CicloClient._get") as mock_get:
        mock_get.return_value = {"_embedded": {"unidades": [], "servidores": []}}
        yield


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Fixture que fornece um session de banco de dados limpo para cada teste."""
    # Drop all tables from previous test
    Base.metadata.drop_all(bind=engine)
    # Create fresh schema
    Base.metadata.create_all(bind=engine)
    
    # Get all table names and truncate them (SQLite needs DELETE FROM)
    from sqlalchemy import inspect, text
    
    session = TestingSessionLocal()
    
    # Delete all rows from all tables
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        try:
            session.execute(text(f"DELETE FROM {table_name}"))
        except:
            pass
    session.commit()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(autouse=True)
def _cleanup_before_each_test(db: Session):
    """Cleanup fixture que executa ANTES de cada teste."""
    from sqlalchemy import text, inspect
    
    # Delete all data from all tables before the test
    inspector = inspect(db.get_bind())
    table_names = inspector.get_table_names()
    
    # Reverse order to respect foreign keys
    for table_name in reversed(table_names):
        try:
            db.execute(text(f"DELETE FROM {table_name}"))
        except:
            pass
    db.commit()
    
    yield


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
