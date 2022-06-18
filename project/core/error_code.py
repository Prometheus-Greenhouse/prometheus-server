# datetime error
DATE_NOT_GT = "DATE_NOT_GT"
DATE_NOT_GE = "DATE_NOT_GE"
DATE_NOT_LT = "DATE_NOT_LT"
DATE_NOT_LE = "DATE_NOT_LE"
# database
DATABASE_INSERT_FAILED = "DATABASE_INSERT_FAILED"
QUERY_DATA_ERROR = "QUERY_DATA_ERROR"
CREATE_ERROR = "CREATE_ERROR"
UPDATE_ERROR = "UPDATE_ERROR"
NOT_FOUND = "NOT_FOUND"
ID_NOT_FOUND = "ID_NOT_FOUND "
MULTIPLE_RESULT_FOUND_WITH_FILTER = "MULTIPLE_RESULT_FOUND_WITH_FILTER"

NOT_IMPLEMENTED_ERROR = "NOT_IMPLEMENTED_ERROR"

# auth
USERNAME_PASSWORD_INVALID = "USERNAME_PASSWORD_INVALID"
TOKEN_EXPIRED = "TOKEN_EXPIRED"
ERROR_INVALID_TOKEN = "ERROR_INVALID_TOKEN"
UN_AUTHORIZE = "UN_AUTHORIZE"
# cic
VALUES_NOT_MATCH = "VALUES_NOT_MATCH"
DOCUMENT_NOT_EXISTS = "DOCUMENT_NOT_EXISTS"
SERVICE_ERROR = "SERVICE_ERROR"
KEY_ERROR = "KEY_ERROR"
BAD_REQUEST = "BAD_REQUEST"
ID_ALREADY_EXIST_ERROR = "ID_ALREADY_EXIST_ERROR"
# workflow
CANNOT_CHANGE_STATE = "CANNOT_CHANGE_STATE"
WORKFLOW_LOGGER_SERVICE_ERROR = "WORKFLOW_LOGGER_SERVICE_ERROR"
WORKFLOW_LOG_FAILED = "WORKFLOW_LOG_FAILED"
# idm
IDM_SERVICE_ERROR = "IDM_SERVICE_ERROR"
# DWH
ERROR_CALL_SERVICE_DWH = "ERROR_CALL_SERVICE_DWH"
# LOS
LOS_SERVICE_ERROR = "LOS_SERVICE_ERROR"
msg_templates = {
    NOT_IMPLEMENTED_ERROR: "not implemented error",
    # datetime error
    DATE_NOT_GT: "ensure this value is greater then {limit_value}",
    DATE_NOT_GE: "ensure this value is greater or equal to {limit_value}",
    DATE_NOT_LT: "ensure this value is less than {limit_value}",
    DATE_NOT_LE: "ensure this value is less than or equal to {limit_value}",
    # database
    DATABASE_INSERT_FAILED: "database insert failed",
    QUERY_DATA_ERROR: "query data error",
    CREATE_ERROR: "create error",
    UPDATE_ERROR: "update error",
    NOT_FOUND: "not found",
    ID_NOT_FOUND: "id {id} not found",
    MULTIPLE_RESULT_FOUND_WITH_FILTER: "'{filter}' multiple result found. Expected one",
    # auth
    USERNAME_PASSWORD_INVALID: "Username or password invalid",
    TOKEN_EXPIRED: "token_expired",
    ERROR_INVALID_TOKEN: "error_invalid_token",
    UN_AUTHORIZE: "un authorize",

    DOCUMENT_NOT_EXISTS: "document not exists!",
    SERVICE_ERROR: "service error",
    KEY_ERROR: "key error",
    BAD_REQUEST: "bad request",
    ID_ALREADY_EXIST_ERROR: "id already exist",

    # workflow
    CANNOT_CHANGE_STATE: "cannot change state",
    WORKFLOW_LOGGER_SERVICE_ERROR: "workflow logger service error",
    WORKFLOW_LOG_FAILED: "workflow log failed - loan_type: {loan_type}, los_id: {los_id}, action: {action}, position: {position}, transition_id: {transition_id}",
    # cic
    VALUES_NOT_MATCH: "values not match; expected: '{expected}', actual: '{actual}' ",
    # idm
    IDM_SERVICE_ERROR: "idm service error",
    # dwh
    ERROR_CALL_SERVICE_DWH: "Call service DWH error",
    # los
    LOS_SERVICE_ERROR: "Los service error"
}
