from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database.base import get_session
from database.models import User as UserModel

router = APIRouter()


@cbv(router)
class SecurityApis:
    @router.get(
        path="/"
    )
    async def get_users(self, session: Session = Depends(get_session)):
        return session.query(UserModel).all()
