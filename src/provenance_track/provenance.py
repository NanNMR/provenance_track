from typing import Any
from pathlib import Path
import inspect
import os

from provenance_track import PlpyAPI


def record(plpy: PlpyAPI):
    #noinspection PyUnresolvedReferences
    fqtn = f"{TD['table_name']}_{TD['schema_name']}"
