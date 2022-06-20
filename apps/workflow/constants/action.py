from enum import auto
from fastapi_utils.enums import StrEnum
class EAction(StrEnum):
	apply_approve = auto()

	apply_control = auto()

	approve = auto()

	close = auto()

	freeze = auto()

	process = auto()

	return_init = auto()

	save = auto()
