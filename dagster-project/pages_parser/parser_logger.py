import logging
import colorlog

__all__ = (
    "logger"
)

# format logs
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
color_format = '%(log_color)s' + log_format
formatter_console = colorlog.ColoredFormatter(color_format)
formatter_file = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# all logs
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter_console)
logger.addHandler(console_handler)
