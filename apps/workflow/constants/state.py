from enum import auto
from fastapi_utils.enums import StrEnum
class EState(StrEnum):
	approving = auto()
	"Hồ sơ đang phê duyệt"
	closed = auto()
	"Hồ sơ đã đóng"
	controlling = auto()
	"Hồ sơ đang kiểm soát"
	disbursement = auto()
	"Hồ sơ được giải ngân"
	freezed = auto()
	"Hồ sơ bị phong tỏa"
	modifying = auto()
	"Hồ sơ đang nhập liệu"
	pre_modify = auto()
	"Hồ sơ chờ tiếp nhận"
	start_event = auto()
	"tart_event"