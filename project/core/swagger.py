from typing import Dict, List, Set, Union

from fastapi import status

from .schemas import ExceptionRes

response_status_codes = {
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    # status.HTTP_401_UNAUTHORIZED: "Unauthorized",
    # status.HTTP_402_PAYMENT_REQUIRED: "Payment Required ",
    # status.HTTP_403_FORBIDDEN: "Forbidden",
    # status.HTTP_404_NOT_FOUND: "Not Found",
    # status.HTTP_405_METHOD_NOT_ALLOWED: "Method Not Allowed",
    # status.HTTP_406_NOT_ACCEPTABLE: "Not Acceptable",
    # status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED: "Proxy Authentication Required",
    # status.HTTP_408_REQUEST_TIMEOUT: "Request Timeout",
    # status.HTTP_409_CONFLICT: "Conflict",
    status.HTTP_422_UNPROCESSABLE_ENTITY: "Unprocessable Entity",
    # status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    # status.HTTP_501_NOT_IMPLEMENTED: "Not Implemented",
    # status.HTTP_503_SERVICE_UNAVAILABLE: "Bad Gateway",

}


def swagger_response(
        response_model,
        success_status_code=status.HTTP_200_OK,
        success_description=None,
        fail_status_code: Union[int, List[int], Set[int]] = status.HTTP_400_BAD_REQUEST,
        fail_description: Dict[int, str] = None,
):
    result = {}
    # default response status
    if fail_description is None:
        fail_description = {}
    res_description = response_status_codes.copy()
    res_description.update(
        fail_description
    )
    if isinstance(fail_status_code, int):
        fail_status_code = {*res_description.keys(), fail_status_code}
    elif isinstance(fail_status_code, (set, list)):
        fail_status_code = {*res_description.keys(), *fail_status_code}

    # success
    result.update(
        {
            success_status_code: {
                "model": response_model,
                "description": success_description,
            }
        }
    )
    for fail_status in fail_status_code:
        result.update(
            {
                fail_status: {"model": ExceptionRes, "description": res_description.get(fail_status)}
            }
        )

    return result
