import logging

from loguru import logger


def debug(msg):
    if logging.getLogger().level == logging.DEBUG:
        return logger.opt(depth=1).debug(msg)
