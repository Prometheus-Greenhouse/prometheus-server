from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBasic
from fastapi_utils.cbv import cbv

from apps.workflow.constants.action import EAction
from apps.workflow.services import WorkflowService

router = APIRouter(dependencies=[Security(HTTPBasic())])


@cbv(router)
class DocumentAPI:
    workflow: WorkflowService = Depends(WorkflowService)

    @router.post(
        path="/apply/approve"
    )
    async def apply_approve(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.apply_approve)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/apply/control"
    )
    async def apply_control(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.apply_control)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/approve"
    )
    async def approve(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.approve)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/close"
    )
    async def close(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.close)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/freeze"
    )
    async def freeze(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.freeze)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/process"
    )
    async def process(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.process)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/return/init"
    )
    async def return_init(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.return_init)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/save"
    )
    async def save(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.save)
        await self.workflow.commit(los_id, interpreter)
