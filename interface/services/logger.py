import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(logfile: str = None, level: int = logging.INFO):
    logger = logging.getLogger()
    if logger.handlers:
        return logger
    logger.setLevel(level)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # file handler
    if logfile:
        p = Path(logfile)
        p.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=5)
        fh.setLevel(level)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger

# Initialize default logger for integration
default_log = setup_logging(logfile='logs/integration.log', level=logging.DEBUG)
