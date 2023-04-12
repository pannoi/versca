import sys, time
import logging, coloredlogs, logging.config

logging.Formatter.converter = time.gmtime
FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s — %(name)s:%(funcName)s:%(lineno)d — %(message)s")

def get_console_handler():
    """ Console handler. """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)

    return console_handler

def get_logger(logger_name):
    """ Init logger. """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    coloredlogs.install(level='DEBUG', logger=logger)

    if not logger.handlers:
        logger.addHandler(get_console_handler())

    logger.propagate = False

    return logger
