from typing import List

from fast_boot.schemas import AbstractUser, CustomBaseModel
from fast_boot.security.access.hierarchical_roles import RoleHierarchy
from pydantic import Field


class RoleHierarchyExtends(RoleHierarchy, CustomBaseModel):
    class Role(CustomBaseModel):
        code: str = Field(...)

    roles: List[Role] = Field([])


class User(AbstractUser):
    username: str = Field(...)
    fullname: str = Field(...)
    my_role_hierarchy: RoleHierarchyExtends = Field(...)

    @property
    def identity(self) -> str:
        return self.username

    @property
    def role_hierarchy(self) -> RoleHierarchy:
        return self.my_role_hierarchy

    @property
    def display_name(self) -> str:
        return self.fullname

    @property
    def is_authenticated(self) -> bool:
        return True

    def get_branch_code(self) -> str:
        return None

    def get_branch_parent_code(self) -> str:
        return None
