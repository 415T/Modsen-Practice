import logging

def return_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        log_formatter = logging.Formatter('%(asctime)-s: %(levelname)-s %(message)s')
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)
    return logger
