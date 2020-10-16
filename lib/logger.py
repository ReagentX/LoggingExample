import logging
import logging.config
import os
import socket

from .color_formatter import ColorFormatter


def build_logger() -> logging.Logger:
    """
    Create a logger instance we can import to anywhere, logs in format:
    2019-10-28 14:32:57,843 - chargemaster.views - INFO - Received request to GetChargemasterData

    To use an instance of the logger, import with
        from lib.logger import LOGGER
    """
    # Set the color prop so we can access it from the config
    logging.ColorFormatter = ColorFormatter  # type: ignore

    # Read initial config file if we are in a deployed environment
    if os.environ.get('ENV') in {'dev', 'test', 'prod'}:
        logging.config.fileConfig('logger_config/info.conf')
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
    else:
        # Use debug level logs as default for non-deployed dev
        logging.config.fileConfig('logger_config/debug.conf')
    logger = logging.getLogger()  # Root logger
    return logger


LOGGER = build_logger()
