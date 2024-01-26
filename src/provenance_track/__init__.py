
import importlib.metadata 
import logging


provenance_track_logger = logging.getLogger(__name__)
from provenance_track.plpyapi import PyResult,PlpyAPI
from provenance_track.logsetup import setup_logging
from provenance_track.provenance import nan_user,set_log_level,record

__version__ =  importlib.metadata.version('provenance_track') 
setup_logging()
provenance_track_logger.warning('loading')

