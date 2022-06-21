import typing

from fast_boot.schemas import AbstractUser
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection

from apps.security.schemas import User as AuthUser, RoleHierarchyExtends
from database.base import session_factory
from database.models.sensor_record import User


class AuthenticationFilter(AuthenticationBackend):

    async def authenticate(self, conn: HTTPConnection) -> typing.Tuple[AuthCredentials, typing.Optional[AbstractUser]]:
        if "login" in conn.url.path:
            return None
        credentials: HTTPBasicCredentials = await HTTPBasic(auto_error=False)(conn)
        if not credentials:
            return None
        session = session_factory()
        user = session.query(User).filter(User.username == credentials.username).first()
        user = AuthUser(**user.__dict__, my_role_hierarchy=user.role_hierarchy)
        return AuthCredentials(scopes=[]), user
