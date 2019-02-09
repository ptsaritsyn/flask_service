import logging


class Configuration:
    DEBUG = False
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'logs/errors.log'
    LOGGING_LEVEL = logging.DEBUG
