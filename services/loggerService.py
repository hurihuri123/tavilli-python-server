import logging

from config.config import IS_PRODUCTION

logger_level = logging.INFO if IS_PRODUCTION else logging.DEBUG
logging.basicConfig(level=logger_level)

handle = "tavilli-python-server"
logger = logging.getLogger(handle)


class LoggerService(object):
    @staticmethod
    def debug(message):
        logger.debug(message)

    @staticmethod
    def info(message):
        logger.info(message)

    @staticmethod
    def error(message):
        logger.error(message)
