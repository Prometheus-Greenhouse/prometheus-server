from typing import Dict

from starlette import status

from apps.workflow.constants.action import EAction
from apps.workflow.constants.state import EState
from apps.workflow.constants.transition import ETransition
from apps.workflow.roles import ERole
from apps.workflow.states.base import State, PermissionSchema, NextStateRequest
from project.core import error_code, HTTPException


class StartEvent(State):
    _state_id = EState.start_event
    _state_name = "tart_event"

    @property
    def accessible_permissions(self) -> PermissionSchema:
        return PermissionSchema(
            write=[ERole.STAFF]
        )

    async def next_state(self, request: NextStateRequest) -> 'State':
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
            EAction.save: {
                "id": EState.modifying,
                "transition_id": ETransition.start_event_save_modifying, }

        }
        return await self.state_filter.do_filter(
            possible_states,
            permissions=write_permission,
            **kwargs
        )
