import logging
import logging.config
import os
import socket

from .color_formatter import ColorFormatter

DEFAULT_FILES = {
    'dev': 'logger_config/info.conf',
    'test': 'logger_config/info.conf',
    'prod': 'logger_config/error.conf',
}


def build_logger() -> logging.Logger:
    """
    Create a logger instance we can import to anywhere, logs in format:
    2019-10-28 14:32:57,843 - module.method - INFO - Log message

    To use an instance of the logger, import with
        from lib.logger import LOGGER
    """
    # Set the color prop so we can access it from the config
    logging.ColorFormatter = ColorFormatter  # type: ignore

    # Read initial config file based on environment name, default to debug
    logging.config.fileConfig(
        DEFAULT_FILES.get(
            os.environ.get('ENV', ''), 
            'logger_config/debug.conf'))

    # Create and start listener on an open port
    port = 9001
    logging_config_listener = None
    while port < 9030:
        try:
            # Check if the socket is in use
            socket_validator = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
            socket_validator.connect(('localhost', port))
            socket_validator.close()
            port += 1
            continue
        # If the socket does not exist, Python raises this exception and we know we can use it
        except ConnectionRefusedError:
            logging_config_listener = logging.config.listen(port)
            logging_config_listener.start()
            print(f'Setup logging server on port {port}')
            if port == 9030:
                print('Out of logging ports! Please increase limit!')
            break
    if logging_config_listener is None:
        raise ValueError(
            'Unable to start logging server, all ports in use!')
    logger = logging.getLogger()  # Root logger
    return logger


LOGGER = build_logger()
