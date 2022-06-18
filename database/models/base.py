from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import (
    DateTime, MetaData, String, func
)
from sqlalchemy.orm import declared_attr, as_declarative

from database.types import UUIDSql


@as_declarative(metadata=MetaData())
class Base:
    __name__: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __str__(self):
        return str(self.__dict__)


class BaseModel(Base):
    __abstract__ = True

    created_at = Column("CREATED_AT", DateTime, default=datetime.now, server_default=func.now())

    created_by = Column("CREATED_BY", String(20), default=None)

    modified_at = Column("MODIFIED_AT", DateTime, default=datetime.now, onupdate=datetime.now, server_default=func.now())

    modified_by = Column("MODIFIED_BY", String(20), default=None)

    uuid = Column("UUID", UUIDSql(40))
