import logging
import logging.handlers
import os
from pathlib import Path

from provenance_track import provenance_track_logger, TRACE

_LOG_FILE = '/var/log/nan.d/provenance'

class ReadableFileHandler(logging.handlers.TimedRotatingFileHandler):




    def doRollover(self):
        super().doRollover()
        os.chmod(self.baseFilename, 0o644)



def setup_logging():
    Path('/var/log/nan.d').mkdir(parents=True, exist_ok=True)
    try:
        handler = ReadableFileHandler(_LOG_FILE, when='h', interval=1, utc=True)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        provenance_track_logger.addHandler(handler)
    except PermissionError as pe:
        provenance_track_logger.warning(f"provenance_track unlogged {pe}")


def set_loglevel(level: str) -> bool:
    """Set level name"""
    try:
        if hasattr(logging,level):
            provenance_track_logger.setLevel(getattr(logging, level))
        elif level == 'TRACE':
            provenance_track_logger.setLevel(TRACE)
        else:
            provenance_track_logger.setLevel(int(level))
        return True
    except Exception:
        provenance_track_logger.exception(f"set level {level}")
        return False

def get_loginfo() -> str:
    """Return log file name and level"""
    n = logging.getLevelName(provenance_track_logger.getEffectiveLevel())
    return f"{_LOG_FILE} {n}"
