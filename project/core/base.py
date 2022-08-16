import abc
import inspect
from typing import (
    Any, Callable, Dict, List, Optional, Type, TypeVar, Union, get_type_hints
)

from fastapi import Request, Depends
from loguru import logger
from pydantic.error_wrappers import ErrorList, ErrorWrapper, flatten_errors
from pydantic.errors import PydanticErrorMixin
from pydantic.typing import is_classvar
from sqlalchemy.orm import Session

from . import error_code
from .exception import Error
from .schemas import CustomBaseModel

T = TypeVar("T")
CBV_CLASS_KEY = "__cbv_class__"


class Base(metaclass=abc.ABCMeta):

    def __init__(self, request: Request = None):
        self.raw_errors: List[ErrorList] = []
        self.model = CustomBaseModel
        self._error_cache: Optional[List[Dict[str, Any]]] = None
        self.request = request
        self.session = None

    def errors(self) -> List[Dict[str, Any]]:
        if self._error_cache is None:
            try:
                config = self.model.__config__  # type: ignore
            except AttributeError:
                config = self.model.__pydantic_model__.__config__  # type: ignore
            self._error_cache = list(flatten_errors(self.raw_errors, config))
        return self._error_cache

    def append_error(self, loc: List[Union[str, float]], code: str = None, msg_template: str = None, error: PydanticErrorMixin = None, **kwargs) -> None:
        """
        mặc định sử dụng LOSError phải có code vs msg_template tương ứng
        :param loc: vị trí của field lỗi
        :param code: error_code
        :param msg_template:
        :param error: sử dụng error có sẵn trong package errors của pydantic
        :return:
        """
        # assert hasattr(message, error.), "Không tìm thấy msg error"
        assert (code or error), "Required code or error"
        if code:
            if msg_template is None:
                msg_template = error_code.msg_templates.get(code)
            assert msg_template, f"Required msg_template for code: {code}"
            self.raw_errors.append(ErrorWrapper(exc=Error(code=code, msg_template=str(msg_template), **kwargs), loc=tuple(loc)))
        elif error:
            self.raw_errors.append(ErrorWrapper(exc=error, loc=tuple(loc)))

    def has_error(self) -> bool:
        return bool(self.raw_errors)

    def count_errors(self) -> int:
        return len(self.raw_errors)

    def nested(
            self,
            objects: Union[dict, list],
            map_with_key: str,
            children_fields: dict,
            children_list: list = None,
            key_child_map_parent=None
    ):
        """
        thay kiểu dũ liệu trong childfields sẽ ra data như mong muốn
        - children_fields={"detail": {'t1', 't2'}}: data child la dict
        - children_fields={"detail": ['t1', 't2']}: data child la list
        - Có thể nest con vào cha theo trường hợp trên:
            + tách key mapping
        re = ctr.nested(objects=data, map_with_key='the_luong_id', children_fields={"detail": ['t1', 't2']})

        re = ctr.nested(objects=re, map_with_key='id', children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']})

        re = ctr.nested(
            objects=NEST_PARENT_FD,
            map_with_key='id',
            children_fields={"detail": ['the_luong_id', 'the_luong_name', 'detail']},
            children_list=NEST_CHILDREN_FD
        )
        """
        objects_cp = objects.copy()

        if isinstance(objects, dict):
            object_list = [objects_cp]
        else:
            object_list = objects_cp

        if not isinstance(children_fields, dict):
            raise Exception('fields type is dict')

        if len(children_fields) < 1:
            return objects_cp

        if not objects_cp:
            return objects_cp

        for key in children_fields:
            assert isinstance(children_fields[key], (list, set)), 'children is type list'
            assert len(children_fields[key]) > 0, 'children is not null'
            # assert children_fields[key][0][-2:] == "id", "First field of child  must be primary key ID"

        if children_list:
            data_result = self.__nest_child_to_parent(
                parent_list=object_list,
                map_with_key=map_with_key,
                children_fields=children_fields,
                children_list=children_list,
                key_child_map_parent=key_child_map_parent
            )
        else:
            data_result = self.__nest_me(
                objects=object_list,
                map_with_key=map_with_key,
                fields=children_fields
            )
        if isinstance(objects, dict):
            return data_result[0] if data_result else {}
        else:
            return data_result

    def __nest_me(
            self,
            objects: list,
            map_with_key: str,
            fields: dict
    ):

        all_key_child = []
        for key_child, value_child in fields.items():
            all_key_child += list(value_child)

        nest_level_data = list(
            map(
                lambda x: self.__nest_level(data_item=x, all_key_child=all_key_child, fields=fields),
                objects
            )
        )

        key_in_parent = set()
        data_parent = dict()

        for temp in list(nest_level_data):
            if temp[map_with_key] not in key_in_parent:
                key_in_parent.add(temp[map_with_key])
                data_parent.update({
                    temp[map_with_key]: temp
                })
            else:
                for key_field, value_field in fields.items():
                    if not temp[key_field]:
                        continue

                    if isinstance(value_field, list):
                        if temp[key_field][0] not in data_parent[temp[map_with_key]][key_field]:
                            data_parent[temp[map_with_key]][key_field].append(temp[key_field][0])
        return list(data_parent.values())

    def __nest_child_to_parent(self, parent_list, map_with_key: str,
                               children_fields: dict, children_list: list = None,
                               key_child_map_parent=None):

        all_key_child = []
        for key_child, value_child in children_fields.items():
            all_key_child += list(value_child)

        nest_level_data = list(
            map(
                lambda x: self.__nest_level(data_item=x, all_key_child=all_key_child, fields=children_fields),
                children_list
            )
        )

        for parent in parent_list:
            for child in nest_level_data:
                if key_child_map_parent:
                    if parent[map_with_key] == child[key_child_map_parent]:
                        self.__nest_type(parent=parent, child=child, children_fields=children_fields)
                else:
                    if parent[map_with_key] == child[map_with_key]:
                        self.__nest_type(parent=parent, child=child, children_fields=children_fields)
        return parent_list

    @staticmethod
    def __nest_type(parent, child, children_fields):
        for key_field, value_field in children_fields.items():
            if not child[key_field]:
                continue
            if isinstance(value_field, list):
                if key_field not in parent:
                    parent.update({
                        key_field: [child[key_field][0]]
                    })
                elif child[key_field][0] not in parent[key_field]:
                    parent[key_field].append(child[key_field][0])
            else:
                parent.update({
                    key_field: child[key_field][0]
                })

    @staticmethod
    def __nest_level(data_item: dict, all_key_child: list, fields: dict):
        child_temp = {}
        parent_temp = {}
        for key_temp, value_temp in data_item.items():
            if key_temp in all_key_child:
                for key_field, value_field in fields.items():
                    if key_temp in value_field:
                        if key_field not in child_temp:
                            child_temp.update({
                                key_field: {}
                            })
                        child_temp[key_field].update({
                            key_temp: value_temp
                        })
            else:
                parent_temp.update({
                    key_temp: value_temp
                })

        for key_field, value_field in fields.items():
            if isinstance(value_field, list):
                parent_temp.update({
                    key_field: [child_temp[key_field]]
                })
            else:
                parent_temp.update({
                    key_field: child_temp[key_field]
                })

        return parent_temp


def service(cls: Type[T]) -> Type[T]:
    _init_base(cls)
    return cls


def insert_func(self, entity):
    logger.info("insert func")
    self.session.add(entity)
    self.session.flush()


class SessionFactory:
    session_factory = None

    @staticmethod
    def set_session_factory(session_factory):
        SessionFactory.session_factory = session_factory


def repos(type_, id_):
    def set_session(cls):
        old_signature = inspect.signature(cls.__init__)
        new_parameters = [
            x for x in list(old_signature.parameters.values())[1:] if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]
        parameter_kwargs = {"default": Depends(SessionFactory.session_factory)}
        new_parameters.append(
            inspect.Parameter(name="session", kind=inspect.Parameter.KEYWORD_ONLY, annotation=Session, **parameter_kwargs)
        )
        return old_signature.replace(parameters=new_parameters)

    def inner(cls):
        setattr(cls, "type_", type_)
        setattr(cls, "id_", id_)

        setattr(cls, "insert", insert_func)
        _init_repos_base(cls)
        return cls

    return inner


def _init_repos_base(cls: Type[Any]) -> None:
    """
    Idempotently modifies the provided `cls`, performing the following modifications:
    * The `__init__` function is updated to set any class-annotated dependencies as instance attributes
    * The `__signature__` attribute is updated to indicate to FastAPI what arguments should be passed to the initializer
    """
    if getattr(cls, CBV_CLASS_KEY, False):  # pragma: no cover
        return  # Already initialized
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x for x in old_parameters if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = ["session"]
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=hint, **parameter_kwargs)
        )
    new_parameters.append(
        inspect.Parameter(name="session", kind=inspect.Parameter.KEYWORD_ONLY, annotation=Session, default=Depends(SessionFactory.session_factory))
    )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, CBV_CLASS_KEY, True)


def _init_base(cls: Type[Any]) -> None:
    """
    Idempotently modifies the provided `cls`, performing the following modifications:
    * The `__init__` function is updated to set any class-annotated dependencies as instance attributes
    * The `__signature__` attribute is updated to indicate to FastAPI what arguments should be passed to the initializer
    """
    if getattr(cls, CBV_CLASS_KEY, False):  # pragma: no cover
        return  # Already initialized
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x for x in old_parameters if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=hint, **parameter_kwargs)
        )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, CBV_CLASS_KEY, True)


def singleton(clazz: Type[T]) -> Type[T]:
    @staticmethod
    def instance(*args, **kwargs) -> T:
        try:
            return getattr(clazz, "__instance__")
        except AttributeError:
            setattr(clazz, "__instance__", clazz(*args, **kwargs))
            return getattr(clazz, "__instance__")

    setattr(clazz, "instance", instance)
    return clazz
