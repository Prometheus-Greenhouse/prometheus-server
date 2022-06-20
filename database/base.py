from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from project.settings.configs import DATABASES

engine = create_engine(DATABASES.oracle.url, poolclass=NullPool)
session_factory = sessionmaker(engine, expire_on_commit=False)


def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.commit()
        session.close()
