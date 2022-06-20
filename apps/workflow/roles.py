from enum import auto

from fastapi_utils.enums import StrEnum


class ERole(StrEnum):
    STAFF = auto()
    CONTROLLER = auto()
    APPROVER = auto()
    ANY = auto()
