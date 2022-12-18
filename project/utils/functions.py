import logging

from loguru import logger


def debug(msg):
    if logging.getLogger().level == logging.DEBUG:
        return logger.opt(depth=1).debug(msg)


def info(msg):
    if logging.getLogger().level == logging.DEBUG:
        return logger.opt(depth=1).info(msg)


def success(msg):
    if logging.getLogger().level == logging.DEBUG:
        return logger.opt(depth=1).success(msg)


def emp_str(v) -> str:
    return str(v) if v is not None else ""


def to_pascal_case(s: str):
    return "".join([part[0:1].upper() + part[1:] for part in s.split("_")])


def op(file, mode='r', encoding="utf8"):
    return open(file, mode, encoding=encoding)


def log_file(data, file):
    with open(file, "w") as f:
        f.write(str(data))
