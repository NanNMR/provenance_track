import logging
from typing import Any
from pathlib import Path
import inspect
import os

import yaml

from provenance_track import PlpyAPI, provenance_track_logger
_PMAP = "nmrhub_provenance"
# noinspection PyUnresolvedReferences
if _PMAP not in GD:
    with open('/etc/nan.d/provenance.yaml') as f:
        # noinspection PyUnresolvedReferences
        GD[_PMAP] = yaml.safe_load((f))


# noinspection PyUnresolvedReferences
def record(plpy: PlpyAPI):
    print(TD)
    fqtn = f"{TD['table_name']}_{TD['schema_name']}"
    provenance_track_logger.warning(fqtn)

def set_log_level(level:str)->bool:
    try:
        provenance_track_logger.setLevel(getattr(logging,level))
        return True
    except Exception:
        provenance_track_logger.exception(f"set level {level}")
        return False

