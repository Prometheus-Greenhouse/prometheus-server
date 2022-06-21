from typing import Dict

from apps.workflow.constants.action import EAction
from apps.workflow.roles import ERole


class PossibleStateFilter:
    def __init__(self, state=None):
        self.state = state

    async def do_filter(self, possible_states, **kwargs):
        for filter_attr in filter(lambda attr: attr.endswith("filter") and attr != "do_filter" and callable(getattr(self, attr)), dir(self)):
            filter_func = getattr(self, filter_attr)
            possible_states = await filter_func(possible_states, **kwargs)
        return possible_states

    async def permission_filter(self, possible_states: Dict, **kwargs) -> Dict:
        algorithm = {
            ERole.STAFF: {
                EAction.save, EAction.close, EAction.apply_control, EAction.process
            },
            ERole.CONTROLLER: {
                EAction.apply_approve, EAction.close
            },
            ERole.APPROVER: {
                EAction.approve, EAction.return_init, EAction.freeze
            }
        }
        roles = map(lambda r: r.code, self.state.ctx.user.role_hierarchy.roles)
        include_actions = set()
        for role in roles:
            include_actions.update(algorithm.get(role))
        return {action: value for action, value in possible_states.items() if action in include_actions}
