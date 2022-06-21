from typing import Dict, Any

from fast_boot.schemas import AbstractUser
from pydantic import Field

from apps.security.schemas import User
from apps.workflow.states.base import Context
from project.core import CustomBaseModel


class Document(CustomBaseModel, Context):
    los_id: str = Field(None)
    state_id: str = Field(None)
    content: Dict = Field({})
    _user: User = Field(None)

    def __init__(self, user: User, **data: Any):
        super().__init__(**data)
        object.__setattr__(self, "_user", user)

    @property
    def id(self):
        return self.los_id

    @property
    def user(self) -> AbstractUser:
        return self._user

    @classmethod
    def from_dict(cls, d):
        # functions.debug(d)
        d["user"] = d["_user"]
        return cls(**d)
