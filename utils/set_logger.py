import logging


def set_logger(file_name: str) -> logging.getLogger():
    """
    A function to set the logger.
    Args:
        file_name: (str) -> The name of the log file.
    Returns:
        logger: (logging.Logger) -> The logger.
    """
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.NOTSET)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - line %(lineno)d - %(message)s")
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger