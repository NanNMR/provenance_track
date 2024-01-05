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

def nan_user(plpy)->str:
    r = plpy.execute("select current_setting('nan.user')")
    return r[0]['current_setting']

def record(plpy: PlpyAPI):
    # noinspection PyUnresolvedReferences
    fqtn = f"{TD['schema_name']}_{TD['table_name']}"
    provenance_track_logger.warning(fqtn)
    r = plpy.execute(f"""select column_name 
        from information_schema.columns 
        where table_schema='provenance' and table_name='{fqtn}'""")
    if r.nrows() == 0:
        provenance_track_logger.warning(f"Table {fqtn} not tracked")
        return
    cols = [row['column_name'] for row in r]
    provenance_track_logger.debug(cols)
    # noinspection PyUnresolvedReferences
    event = TD['event']
    if event == "INSERT":
        pass

    # EVENT
    provenance_track_logger.debug(f'{fqtn} in provenance')


def set_log_level(level:str)->bool:
    try:
        provenance_track_logger.setLevel(getattr(logging,level))
        return True
    except Exception:
        provenance_track_logger.exception(f"set level {level}")
        return False
