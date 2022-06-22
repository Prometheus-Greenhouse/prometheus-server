from fastapi import APIRouter

from apps.document import apis as document_apis
from apps.security import apis as security_apis
from apps.workflow import apis as wf_apis

router = APIRouter()
router.include_router(router=wf_apis.router)
router.include_router(router=document_apis.router, prefix="/documents")
router.include_router(router=security_apis.router, prefix="/security")
