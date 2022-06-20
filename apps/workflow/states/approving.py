from typing import Dict
from loguru import logger
from starlette import status
from apps.workflow.constants.action import EAction
from apps.workflow.constants.state import EState
from apps.workflow.constants.transition import ETransition
from apps.workflow.roles import ERole
from apps.workflow.states.base import State, PermissionSchema, NextStateRequest
from project.core import error_code, HTTPException
class Approving(State):
    _state_id = EState.approving
    @property
    def accessible_permissions(self) -> PermissionSchema:
        return PermissionSchema(
            write=[ERole.APPROVER]
        )
        
    async def next_state(self, request:NextStateRequest) -> 'State':
        next_state = (await self.possible_states()).get(request.action)
        if not next_state:
            raise HTTPException.with_error(loc=["next_state"], code=error_code.CANNOT_CHANGE_STATE, status_code=status.HTTP_412_PRECONDITION_FAILED)
        clazz = self.get_class_from_state_id(next_state["id"])
        ctx = self.ctx
        ctx.set_state(clazz(ctx, pre_transition_id=next_state["transition_id"]))
        return ctx.state
    async def possible_states(self, **kwargs) -> Dict:
        write_permission = self.accessible_permissions.write
        possible_states = {
            EAction.return_init: { 
"id": EState.pre_modify, 
"transition_id": ETransition.approving_return_init_pre_modify,}
,
EAction.approve: { 
"id": EState.disbursement, 
"transition_id": ETransition.approving_approve_disbursement,}
,
EAction.close: { 
"id": EState.closed, 
"transition_id": ETransition.approving_close_closed,}

            }
        return await self.state_filter.do_filter(
            possible_states,
            permissions=write_permission,
            **kwargs
        )
        