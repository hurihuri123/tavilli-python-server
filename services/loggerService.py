import logging

logging.basicConfig(level=logging.DEBUG)  # TODO: set level acocrding to ENV

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
