import typing

from fast_boot.schemas import AbstractUser, UnAuthenticatedUser
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection

from apps.security.schemas import User as AuthUser
from database.base import Session_
from database.models import User


class AuthenticationFilter(AuthenticationBackend):

    async def authenticate(self, conn: HTTPConnection) -> typing.Tuple[AuthCredentials, typing.Optional[AbstractUser]]:
        un_auth = AuthCredentials(scopes=[]), UnAuthenticatedUser()
        if "login" in conn.url.path:
            return un_auth
        credentials: HTTPBasicCredentials = await HTTPBasic(auto_error=False)(conn)
        if not credentials:
            return un_auth
        session = Session_()
        user = session.query(User).filter(User.username == credentials.username).first()
        if user:
            user = AuthUser(**user.__dict__, my_role_hierarchy=user.role_hierarchy)
        else:
            return un_auth
        return AuthCredentials(scopes=[]), user
