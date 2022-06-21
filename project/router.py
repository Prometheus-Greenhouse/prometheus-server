from fastapi import APIRouter

from apps.workflow import apis

router = APIRouter()
router.include_router(router=apis.router)
