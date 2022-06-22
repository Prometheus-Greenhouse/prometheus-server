from typing import Dict

from fastapi import Depends
from pydantic.error_wrappers import ValidationError
from starlette.requests import Request

from apps.workflow.constants.action import EAction
from apps.workflow.constants.state import EState
from apps.workflow.schemas import Document
from apps.workflow.states.base import NextStateRequest, State
from database.repositories.document import DocumentRepos
from project.core import service, HTTPException, error_code


@service
class WorkflowService:
    document_repos: DocumentRepos = Depends(DocumentRepos)
    request: Request

    async def state_interpreter(self, los_id: str, action: EAction = None, request: NextStateRequest = None, *args, **kwargs) -> Dict:
        if not request:
            try:
                request = NextStateRequest(action=action)
            except ValidationError as e:
                raise HTTPException(detail=e.errors())

        current_state = await self._get_current_state(los_id, request)
        target_state = await current_state.next_state(request)

        return {
            "los_id": los_id,
            "state_request": request.dict(),
            "target_state": target_state.dict()
        }

    async def commit(self, los_id, next_state_package: Dict = None):
        target_state_dict = next_state_package["target_state"]
        #
        # if next_state_package.get("new_document"):
        #     ctx = target_state_dict["ctx"]
        #     target_state_dict["ctx"] = next_state_package["new_document"]
        #     target_state_dict["ctx"]["_user"] = ctx["_user"]
        #

        target_state_id = target_state_dict["_state_id"]
        clazz = State.get_class_from_state_id(target_state_id)
        target_state = clazz.from_dict(target_state_dict, Document)

        self.document_repos.update(
            los_id=los_id,
            state_id=target_state.state_id,
            state_name=target_state.state_name
        )

    async def get_document_state_guide(self, los_id: str) -> Dict:
        current_state = await self._get_current_state(los_id)
        button_map = await current_state.possible_states()
        state_guide = {
            "state_id": current_state.state_id,
            "state_name": current_state.state_name,
            "guide": button_map,
        }
        return state_guide

    async def _get_current_state(self, los_id: str, request: NextStateRequest = None) -> State:
        """
        - Lấy current state trong workflow logger \n
        - Từ current state lấy được parse ra class state tuong ứng \n
        - Cuối cùng ta được current state và context của state đó là hồ sơ đã khởi tạo \n
        :param los_uuid:
        :return: current_state
        """
        doc = self.document_repos.get_by_los_id(los_id)

        doc = Document(user=self.request.user, **doc.__dict__ if doc else {})
        if doc.state_id:
            state_id = doc.state_id
        elif not doc.state_id and (request and request.action == EAction.save):
            state_id = EState.start_event
        else:
            raise HTTPException.with_error(loc=["path", "los_id"], code=error_code.ID_NOT_FOUND, id=los_id)

        clazz = State.get_class_from_state_id(state_id)
        # functions.debug("class: {}".format(clazz))
        doc.set_state(clazz(doc))
        return doc.state
