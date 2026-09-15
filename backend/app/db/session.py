from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

# pool_pre_ping=True: validates a pooled connection is still alive
# before handing it out. Without this, a connection that silently
# died (DB restart, idle timeout) surfaces as a confusing error on
# the NEXT query instead of being caught and replaced transparently.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a session, always closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()