import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': RED,
    'INFO': CYAN,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE,
}

RESET_SEQ = "\u001b[0m"
COLOR_SEQ = "\u001b[%dm"
BOLD_SEQ = "\033[1m"


class ColorFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record: logging.LogRecord):
        levelname = record.levelname
        color = COLOR_SEQ % (30 + COLORS[levelname])
        message = logging.Formatter.format(self, record)
        # Remove quotes added by format()
        message = message.strip()[1:len(message) - 1]
        message = message.replace('$RESET', RESET_SEQ) \
                         .replace('$BOLD',  BOLD_SEQ) \
                         .replace('$COLOR', color)
        for key, value in COLORS.items():
            message = message.replace('$' + key,    COLOR_SEQ % (value+30)) \
                             .replace('$BG-' + key, COLOR_SEQ % (value+40))
        return message + RESET_SEQ
