import logging
from logging.handlers import RotatingFileHandler

from scrapy.utils.log import configure_logging


configure_logging(install_root_handler=False)

# custom logging settings
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
log_level = logging.INFO
log_file = "log.log"

logging.basicConfig(
    format=log_format,
    level=log_level
)

rotating_file_log = RotatingFileHandler(log_file, maxBytes=1024*1024*1024, backupCount=5, encoding="utf-8")
rotating_file_log.setFormatter(logging.Formatter(log_format))

root_logger = logging.getLogger()
root_logger.addHandler(rotating_file_log)
