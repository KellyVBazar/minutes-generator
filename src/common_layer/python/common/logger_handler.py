import logging
import os
import sys


def create_logger() -> logging.Logger:
    app_name = os.environ.get("APP_NAME", "default_app")
    new_logger = logging.getLogger(app_name)

    logger = logging.getLogger(app_name)
    level = os.environ.get("LOG_LEVEL", logging.INFO)

    logger.setLevel(level)
    logger.propagate = False

    log_formatter = logging.Formatter(
        "[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(module)s:%(lineno)d] - %(message)s"
    )

    if not new_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        new_logger.addHandler(console_handler)

    return logger


logger = create_logger()
