from fastapi import APIRouter

from apps.sensor import apis as sensor_apis

router = APIRouter()
# router.include_router(router=wf_apis.router)
router.include_router(router=sensor_apis.router)
# router.include_router(router=document_apis.router, prefix="/documents")
# router.include_router(router=security_apis.router, prefix="/security")
