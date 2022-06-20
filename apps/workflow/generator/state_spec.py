import json
from typing import Dict, List

from pydantic import Field

from project.core import CustomBaseModel
from project.utils import functions
from transition_spec import TransitionSpec


class StateSpec(CustomBaseModel):
    id: str = Field(None)
    name: str = Field(None)
    documentation: Dict = Field(None)
    possible_states: List[TransitionSpec] = Field([])

    def to_node(self) -> str:
        return json.dumps({
            "name": self.name,
            "code": self.id,
            "is_start_node": self.documentation.get("is_start_node"),
            "state_group": self.documentation.get("state_group"),
        }, ensure_ascii=False)

    def to_state(self) -> str:
        possible_states_str = ",\n".join(map(lambda t: t.to_possible_state(), self.possible_states))
        roles = self.documentation.get("roles", [])
        write = ", ".join([f"ERole.{r}" for r in roles])
        permission_str = f"""PermissionSchema(
            write=[{write}]
        )
        """
        return f"""
class {functions.to_pascal_case(self.id)}(State):
    _state_id = EState.{self.id}
    @property
    def accessible_permissions(self) -> PermissionSchema:
        return {permission_str}
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
        possible_states = {chr(123)}
            {possible_states_str}
            {chr(125)}
        return await self.state_filter.do_filter(
            possible_states,
            permissions=write_permission,
            **kwargs
        )
        """
