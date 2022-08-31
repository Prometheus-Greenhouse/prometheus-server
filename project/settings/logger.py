
import logging
import sys
from pprint import pformat
from types import FrameType
from typing import cast

from loguru import logger
from loguru._defaults import LOGURU_FORMAT

from project.configs import ApplicationConfigs


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
    """
    Example:
    >>> payload = {'age': 87, 'is_active': True, 'name': 'Nick'}
    >>> logger.bind(payload=payload).debug("users payload")
    >>> [   {   'count': 2,
    >>> }]
    """

    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=2, compact=True, width=200
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


def init_logging():
    """
    Replaces logging handlers with a handler for using the custom handler.

    WARNING!
    if you call the init_logging in startup event function,
    then the first logs before the application start will be in the old format
    >>> app.add_event_handler("startup", init_logging)
    stdout:
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [11528] using statreload
    INFO:     Started server process [6036]
    INFO:     Waiting for application startup.
    2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.

    """
    logging.getLogger().level = logging.DEBUG if ApplicationConfigs().debug else logging.INFO
    loggers = [logging.getLogger("uvicorn.asgi")]
    loggers += [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    ]
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = [InterceptHandler()]

    logging.getLogger("uvicorn").handlers = []

    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )
