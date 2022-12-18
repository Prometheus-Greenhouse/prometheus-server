import decimal
from typing import Dict, List, Union

import orjson
from pydantic import UUID4
from sqlalchemy import VARCHAR, TypeDecorator, String, CLOB
from sqlalchemy.dialects.oracle.cx_oracle import OracleDialect_cx_oracle


class JSONLob(TypeDecorator):

    @property
    def python_type(self):
        return Union[List, Dict]

    impl = CLOB
    cache_ok = True

    def process_bind_param(self, value, dialect: OracleDialect_cx_oracle):
        if value is None:
            return None

        def default(obj):
            if isinstance(obj, decimal.Decimal):
                return str(obj)
            raise TypeError

        return orjson.dumps(value, default=default)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return orjson.loads(value)


class UUIDSql(TypeDecorator):

    @property
    def python_type(self):
        return UUID4

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return UUID4(value)


class Boolean(TypeDecorator):

    @property
    def python_type(self):
        return bool

    impl = VARCHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return {True: 1, False: 0}.get(value)

    def process_result_value(self, value, dialect):
        return {1: True, 0: False}.get(value)
