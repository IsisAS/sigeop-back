from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET search_path TO sigeop, public")
    cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)