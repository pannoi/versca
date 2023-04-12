from context import get_logger

logger = get_logger(__name__)

def test_info_log():
    logger.info("Test Message")

def test_error_log():
    logger.error("Test Error")
