from typing import Dict

from fastapi import APIRouter, status, Path, Body, Depends, Security
from fastapi.security import HTTPBasic
from fastapi_utils.cbv import cbv

from apps.workflow.constants.action import EAction
from apps.workflow.examples.commit import COMMIT_EXAMPLE
from apps.workflow.services import WorkflowService
from project.core import DataResponse
from project.core.swagger import swagger_response

router = APIRouter(dependencies=[Security(HTTPBasic())])


@cbv(router)
class WorkFlowAPI:
    service: WorkflowService = Depends(WorkflowService)

    @router.post(
        path="/{los_id}/states/interpreters",
        status_code=status.HTTP_200_OK,
        responses=swagger_response(
            response_model=DataResponse[Dict],
            success_status_code=status.HTTP_200_OK
        )
    )
    async def state_interpreter(self, action: EAction, los_id: str = Path(...)):
        next_state_package = await self.service.state_interpreter(action=action, los_id=los_id)
        return DataResponse(data=next_state_package)

    @router.post(
        path="/{los_id}/states/commit",
        status_code=status.HTTP_200_OK,
        responses=swagger_response(
            response_model=DataResponse[Dict],
            success_status_code=status.HTTP_200_OK
        )
    )
    async def commit_interpreter(self, los_id: str, next_state_package: Dict = Body(..., example=COMMIT_EXAMPLE)):
        data = await self.service.commit(los_id, next_state_package)
        return DataResponse(data=data)

    @router.get(
        path="/{los_id}/state-guide",
        description="Hướng dẫn hành động cho document ở trạng thái hiện tại",
        responses=swagger_response(
            response_model=Dict,
            success_status_code=status.HTTP_200_OK
        )
    )
    async def get_guild_of_document(self, los_id: str = Path(...)):
        data = await self.service.get_document_state_guide(los_id)
        return DataResponse(data=data)
