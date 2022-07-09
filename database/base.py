from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from project.configs import DATABASES

engine = create_engine(DATABASES.oracle.url, poolclass=NullPool)
Session_ = sessionmaker(engine, expire_on_commit=False)


def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = Session_()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.commit()
        session.close()
