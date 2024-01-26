import logging.handlers
import os
from pathlib import Path

from provenance_track import provenance_track_logger

class ReadableFileHandler(logging.handlers.RotatingFileHandler):

    def doRollover(self):
        super().doRollover()
        os.chmod(self.baseFilename, 0o644)



def setup_logging():
    if not os.getenv('NO_PROVENANCE_TRACK_LOG',False):
        Path('/var/log/nan.d').mkdir(parents=True, exist_ok=True)
        handler = logging.handlers.TimedRotatingFileHandler('/var/log/nan.d/provenance', when='h', interval=1, utc=True)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        provenance_track_logger.addHandler(handler)

