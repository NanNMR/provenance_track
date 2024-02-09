
import importlib.metadata 
import logging

TRACE= 5
"""Trace logging level"""


provenance_track_logger = logging.getLogger(__name__)
from provenance_track.plpyapi import PyResult,PlpyAPI
from provenance_track.logsetup import setup_logging, set_loglevel,get_loginfo
from provenance_track.provenance import nan_user, record

__version__ =  importlib.metadata.version('provenance_track') 
setup_logging()
provenance_track_logger.warning('loading')

