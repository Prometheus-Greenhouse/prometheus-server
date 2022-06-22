from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBasic
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from apps.workflow.constants.action import EAction
from apps.workflow.services import WorkflowService
from database.base import get_session
from database.models.sensor_record import DocumentModel

router = APIRouter(dependencies=[Security(HTTPBasic())])


@cbv(router)
class DocumentAPI:
    workflow: WorkflowService = Depends(WorkflowService)

    @router.post(
        path="/{los_id}/apply/approve"
    )
    async def apply_approve(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.apply_approve)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/apply/control"
    )
    async def apply_control(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.apply_control)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/approve"
    )
    async def approve(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.approve)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/close"
    )
    async def close(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.close)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/freeze"
    )
    async def freeze(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.freeze)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/process"
    )
    async def process(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.process)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/return/init"
    )
    async def return_init(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.return_init)
        await self.workflow.commit(los_id, interpreter)

    @router.post(
        path="/{los_id}/save"
    )
    async def save(self, los_id: str):
        interpreter = await self.workflow.state_interpreter(los_id, action=EAction.save)
        await self.workflow.commit(los_id, interpreter)

    @router.get(
        path="/"
    )
    async def get_documents(self, session: Session = Depends(get_session)):
        return session.query(DocumentModel).all()
