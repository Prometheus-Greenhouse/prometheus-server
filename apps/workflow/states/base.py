import abc
import inspect
from typing import TypeVar, Dict, Optional, Type, List, Any

from fast_boot.schemas import AbstractUser, CustomBaseModel
from pydantic import Field

from apps.workflow import states
from apps.workflow.constants.action import EAction
from apps.workflow.possible_state_filter import PossibleStateFilter


class Context(metaclass=abc.ABCMeta):
    _state: 'State'

    @property
    def state(self):
        return self._state

    def set_state(self, state: 'State') -> None:
        object.__setattr__(self, "_state", state)

    @property
    @abc.abstractmethod
    def id(self):
        ...

    @property
    @abc.abstractmethod
    def user(self) -> AbstractUser:
        ...

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, d):
        ...

    @abc.abstractmethod
    def dict(self):
        ...

    def __str__(self):
        return {self.id, self.user}


C = TypeVar("C", bound=Context)


class NextStateRequest(CustomBaseModel):
    action: EAction = Field(None)
    content: Dict = Field({})

    def __init__(self, action: EAction, *args, **kwargs):
        super().__init__(**kwargs)
        self.action = action


class State(metaclass=abc.ABCMeta):
    _state_id: str
    _state_name: str

    def __init__(
            self,
            ctx: Context,
            pre_transition_id: str = None,
            state_filter=PossibleStateFilter()
    ):
        self.ctx = ctx
        self.prev_transition_id = pre_transition_id
        self.state_filter = state_filter
        state_filter.state = self

    @property
    @abc.abstractmethod
    def accessible_permissions(self) -> 'PermissionSchema':
        ...

    def role_interceptor(self, ):
        ...

    async def next_state(self, request: NextStateRequest) -> 'State':
        ...

    @abc.abstractmethod
    async def possible_states(self, **kwargs) -> Dict:
        """Tùy vào điều kiện của hồ sơ mà có thể xử lý để trả về các state khả kiến khác nhau"""
        ...

    @property
    def state_id(self) -> str:
        return self._state_id

    @property
    def state_name(self) -> str:
        return self._state_name

    @staticmethod
    def get_class_from_state_id(state_id: Optional['EState']) -> Type['State']:
        rs = set(filter(
            lambda class_tup:
            issubclass(class_tup[1], State) and class_tup[1]._state_id == state_id,
            inspect.getmembers(states, inspect.isclass)
        ))
        clazz_name, clazz = rs.pop()
        return clazz

    def dict(self) -> Dict:
        self.ctx.set_state(None)
        return {"_state_id": self._state_id, "ctx": self.ctx.dict(), "pre_transition_id": self.prev_transition_id}

    @classmethod
    def from_dict(cls, d, context_type: Type[C]) -> 'State':
        ctx = context_type.from_dict(d.get("ctx"))
        print("--->", ctx)
        state = cls(ctx, d.get("pre_transition_id"))
        ctx.set_state(state)
        return state


class PermissionSchema(CustomBaseModel):
    write: List[Any] = Field([])
    read: List[Any] = Field([])
