import logging
import os.path
import logging.handlers # Import for RotatingFileHandler
import logging.config
from src.paths import LOGS_DIR


class CustomFormatter(logging.Formatter):
    grey = "\u001b[37;1m"
    cyan = "\u001b[36;1m"
    green = "\u001b[32;1m"
    yellow = "\u001b[33;1m"
    red = "\u001b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"

    FORMATS = {
        logging.DEBUG: cyan + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset,
    }

    def get_header_length(self, record):
        return len(
            super().format(
                logging.LogRecord(
                    name=record.name,
                    level=record.levelno,
                    pathname=record.pathname,
                    lineno=record.lineno,
                    msg="",
                    args=(),
                    exc_info=None,
                )
            )
        )

    def format(self, record):
        indent = " " * self.get_header_length(record)
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        head, *trailing = formatter.format(record).splitlines(True)
        text = head + "".join(indent + line for line in trailing)
        return text

# Placeholder for the actual log file path, to be set at runtime
LOG_FILE_NAME = "app.log" # Default log file name

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "custom": {
            "()": CustomFormatter,
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "custom",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "text_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "DEBUG",
            # filename will be set dynamically
            "filename": os.path.join(LOGS_DIR, LOG_FILE_NAME),
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000, # Example: 0.5 MB per log file
            "backupCount": 4,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default", "text_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "__main__": {
            "handlers": ["default", "text_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "mp_logger": {
            "handlers": ["default", "text_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

def setup_logging():
    """
    Configures the logging system.
    Dynamically sets the log file path relative to the application's root.
    """
    os.makedirs(LOGS_DIR, exist_ok=True) # Ensure the logs directory exists
    logging.config.dictConfig(LOGGING_CONFIG)

    # Confirm logging setup
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured. Log file: {LOGGING_CONFIG['handlers']['text_file']['filename']}")