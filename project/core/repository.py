import abc
from typing import Generic, Iterable, List, Optional, TypeVar, Union

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count
from starlette import status

from . import error_code
from .base import Base
from .exception import HTTPException
from .schemas import Page, Pageable, Sort

T = TypeVar("T")
ID = TypeVar("ID")


class IRepository(Generic[T, ID]):

    @abc.abstractmethod
    def count(self, *args, **kwargs) -> int:
        ...

    @abc.abstractmethod
    def delete(self, entity: T) -> int:
        ...

    @abc.abstractmethod
    def delete_all(self, entities: Iterable[T]) -> None:
        ...

    @abc.abstractmethod
    def delete_all_by_id_in_batch(self, integers: Iterable[ID]) -> None:
        ...

    @abc.abstractmethod
    def delete_all_in_batch(self, entities: Iterable[T]) -> None:
        ...

    @abc.abstractmethod
    def delete_by_id(self, integer: ID) -> bool:
        ...

    @abc.abstractmethod
    def exists(self, *args, **kwargs) -> bool:
        ...

    @abc.abstractmethod
    def exists_by_id(self, integer: ID) -> bool:
        ...

    @abc.abstractmethod
    def find_all(self, pageable: Optional[Pageable], sort: Optional[Sort]) -> Union[List[T], Page[T]]:
        ...

    @abc.abstractmethod
    def find_all_by_id(self, integers: Iterable[ID]) -> List[T]:
        ...

    @abc.abstractmethod
    def find_by_id(self, integer: ID) -> Optional[T]:
        ...

    @abc.abstractmethod
    def find_one(self, *args, **kwargs) -> Optional[T]:
        ...

    @abc.abstractmethod
    def get_by_id(self, integer: ID) -> T:
        ...

    @abc.abstractmethod
    def insert(self, entity: T) -> T:
        ...

    @abc.abstractmethod
    def insert_all(self, entities: Iterable[T]) -> List[T]:
        ...

    @abc.abstractmethod
    def save_and_flush(self, entity: T) -> T:
        ...

    @abc.abstractmethod
    def save_all_and_flush(self, entities: Iterable[T]) -> List[T]:
        ...


class Repository(IRepository[T, ID], Base):
    type_ = T
    id_ = ID

    def delete(self, entity: T) -> int:
        rs = self.session.delete(entity)
        logger.info(f"sqlalchemy delete: {rs}")
        return rs

    def delete_all(self, entities: Iterable[T]) -> None:
        self.session.delete(entities)

    def delete_all_by_id_in_batch(self, integers: Iterable[ID]) -> None:
        self.session.query(self.type_.id.in_(integers)).delete()

    def delete_all_in_batch(self, entities: Iterable[T]) -> None:
        self.session.delete(entities)

    def delete_by_id(self, id: ID) -> bool:
        self.session.query(self.type_.id == id).delete()

    def exists(self, *args, **kwargs) -> bool:
        ...

    def exists_by_id(self, integer: ID) -> bool:
        return bool(self.session.query(1).where(self.type_.id == integer).first())

    def find_all(self, pageable: Pageable = None, sort: Sort = None, *args, **kwargs) -> Union[List[T], Page[T]]:
        if pageable:
            entities = self.session.query(self.type_).offset(pageable.page - 1).size(pageable.size).all()
            total_entities = self.session.query(count(self.type_.id))
            return Page(content=entities, total_elements=total_entities, size=pageable.size, number=pageable.page, sort=pageable.sort)
        if sort:
            orders = [f"{sort.order_by}, {order.direction}" for order in sort.direction]
            return self.session.query(self.type_).order_by(sa.text(str(orders))).all()
        return self.session.query(self.type_).all()

    def find_all_by_id(self, integers: Iterable[ID]) -> List[T]:
        return self.session.query(self.type_).where(self.type_.id.in_(integers))

    def find_by_id(self, integer: ID) -> T:
        return self.session.query(self.type_).filter(self.type_.id == integer).one()

    def get_by_id(self, integer: ID) -> T:
        return self.session.get(self.type_, integer)

    def insert(self, entity: T) -> T:
        try:
            self.session.add(entity)
            self.session.flush()
        except IntegrityError as e:
            logger.exception(e)
            raise HTTPException.with_error(code=error_code.UPDATE_ERROR, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return entity

    def insert_all(self, entities: Iterable[T]) -> List[T]:
        try:
            self.session.bulk_save_objects(entities, return_defaults=True)
        except Exception as ex:
            logger.exception(ex)
        return list(entities)
