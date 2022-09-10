from functools import wraps

from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from project.configs import DatabaseConfigs
from project.core.base import SessionFactory

engine = create_engine(DatabaseConfigs().oracle.url, poolclass=QueuePool)
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


SessionFactory.session_factory = get_session


def scoped_session(func):
    @wraps(func)
    def wrapper(*args, **kw):
        with Session_.begin() as session:
            kw.update({"session": session})
            res = func(*args, **kw)
            return res

    return wrapper
