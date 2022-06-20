from typing import Any, Dict, List, Optional, Union

import fastapi
from fastapi import status
from pydantic import errors
from pydantic.error_wrappers import ErrorList, ErrorWrapper, flatten_errors
from pydantic.errors import PydanticErrorMixin

from . import error_code
from .schemas import CustomBaseModel

# DETAIL = "detail"
MSG = "msg"
TYPE = "type"
LOC = "loc"
CODE = "code"
CTX = "ctx"
DETAIL = "detail"


class Error(errors.PydanticValueError):
    ...


class HTTPException(fastapi.HTTPException):
    def __init__(
            self,
            detail: List[Dict[str, str]] = tuple(),
            status_code: int = status.HTTP_400_BAD_REQUEST,
            headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code, detail, headers)

    def get_detail(self) -> List[Dict]:
        return self.errors_pipeline(self.detail)

    @staticmethod
    def errors_pipeline(errors: List[Dict[str, Any]]) -> List[Dict]:
        return [{
            LOC: error.get(LOC),
            MSG: error.get(CTX).get(CODE) if error.get(CTX) and error.get(CTX).get(CODE) else error.get(TYPE),
            DETAIL: error.get(MSG),
            # TYPE: error.get(TYPE),
            # CTX: error.get(CTX)
        } for error in errors]

    @staticmethod
    def arrow_error_pipeline(errors: List[Dict[str, Any]]) -> List[Dict]:
        return [{
            LOC: " -> ".join(map(lambda l: str(l), error.get(LOC))),
            MSG: error.get(MSG),
            DETAIL: error.get(DETAIL)
        } for error in errors]

    def set_error(self, loc: List[Union[str, int]], error: PydanticErrorMixin, model=None) -> None:
        raw_errors: List[ErrorList] = [ErrorWrapper(exc=error, loc=tuple(loc))]
        model = model
        try:
            config = model.__config__  # type: ignore
        except AttributeError:
            config = model.__pydantic_model__.__config__  # type: ignore
        self.detail = list(flatten_errors(raw_errors, config))

    @classmethod
    def single_error(cls, error: PydanticErrorMixin, loc: List[Union[str, int]] = (), model=CustomBaseModel, status_code=status.HTTP_400_BAD_REQUEST,
                     headers: Dict[str, Any] = None) -> 'HTTPException':
        los_exception = cls(status_code=status_code, headers=headers)
        los_exception.set_error(loc, error, model)
        return los_exception

    @classmethod
    def with_error(
            cls, code, msg_template=None, loc: List[Union[str, int]] = (), model=CustomBaseModel, status_code=status.HTTP_400_BAD_REQUEST, headers: Dict[str, Any] = None, **kwargs
    ) -> 'HTTPException':
        los_exception = cls(status_code=status_code, headers=headers)
        if not msg_template:
            msg_template = error_code.msg_templates.get(code)
        los_exception.set_error(loc, Error(code=code, msg_template=msg_template, **kwargs), model)
        return los_exception

    @classmethod
    def from_los_arrow_exception(cls, errors: List[Dict], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        return cls(detail=[{LOC: error.get(LOC), TYPE: error.get(MSG), MSG: error.get(DETAIL)} for error in errors], status_code=status_code)
