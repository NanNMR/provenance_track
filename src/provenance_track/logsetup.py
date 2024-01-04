import logging.handlers
from pathlib import Path

from provenance_track import provenance_track_logger


def setup_logging():
    Path('/var/log/nan.d').mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.TimedRotatingFileHandler('/var/log/nan.d/provenance', when='h', interval=1, utc=True)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    provenance_track_logger.addHandler(handler)

