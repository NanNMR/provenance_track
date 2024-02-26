
import importlib.metadata 
import logging
import sys
from pathlib import Path
from provenance_track.plpyapi import PyResult,PlpyAPI
from provenance_track.logsetup import setup_logging, set_loglevel,get_loginfo
from provenance_track.provenance import nan_user, record, disable_provenance

__version__ =  importlib.metadata.version('provenance_track')

TRACE= 5
"""Trace logging level"""
DISABLE_SENTINEL = Path('/var/tmp/noprovenance')


provenance_track_logger = logging.getLogger(__name__)

setup_logging()
provenance_track_logger.warning(f'loading {sys.version_info}')


