from enum import auto
from fastapi_utils.enums import StrEnum
class ETransition(StrEnum):
	approving_approve_disbursement = auto()
	
	approving_close_closed = auto()
	
	approving_return_init_pre_modify = auto()
	
	controlling_apply_approve_approving = auto()
	
	controlling_close_closed = auto()
	
	modifying_apply_control_controlling = auto()
	
	modifying_close_closed = auto()
	
	pre_modify_freeze_freezed = auto()
	
	pre_modify_process_modifying = auto()
	
	start_event_save_modifying = auto()
	