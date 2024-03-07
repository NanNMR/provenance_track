import datetime
import logging
from typing import Iterable

from provenance_track import PlpyAPI, provenance_track_logger, TRACE


class ProvenanceException(Exception):
    pass


def format(value):
    if isinstance(value, int) or isinstance(value, float):
        return value
    return "'" + str(value) + "'"


def nan_user(plpy) -> str:
    ### current user, single quoted
    try:
        r = plpy.execute("select current_setting('nan.user')")
        return "'" + r[0]['current_setting'] + "'"
    except:
        raise ProvenanceException("nan.user not set in configuration?")


_PK = """SELECT a.attname AS column 
FROM   pg_index i
JOIN   pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
WHERE  i.indrelid = '{}'::regclass
AND    i.indisprimary"""
#
# build SQL insert with multiple columns
#
EVENT_MAP = {"INSERT": 0, "UPDATE": 1, "DELETE": 2, "TRUNCATE": 2}

NUMERIC_TYPES = ('integer', 'smallint', 'boolean', 'real', 'numeric')
STRING_TYPES = ('character varying', 'text', 'timestamp with time zone', 'uuid', 'jsonb','tstzrange')
QSTRING_TYPE = 'date'  # Python type requires conversion to string
ARRAY_TYPE = 'ARRAY'
USER_DEFINED = 'USER-DEFINED'
AS_TYPES = ()
SUPPORTED_TYPES = NUMERIC_TYPES + STRING_TYPES + (QSTRING_TYPE, ARRAY_TYPE, USER_DEFINED)

# DATE_TYPES = ('timestamp with time zone',)

translate_errors = []


def _translate(name, value, dtype) -> str | None:
    """Convert value into format suitable for postgresl"""
    if provenance_track_logger.isEnabledFor(logging.DEBUG):
        provenance_track_logger.debug(f"SQL type {dtype} Python type {type(value)}")
        provenance_track_logger.debug(str(value))
    if value is None:
        provenance_track_logger.log(TRACE, f"null {dtype}")
        return 'NULL'
    if isinstance(value, datetime.datetime):
        if value.tzinfo is None:
            v = value.strftime("'%Y-%m-%d %H:%M:%S.%f'")
        else:
            v = value.strftime("'%Y-%m-%d %H:%M:%S.%f%z'")
        provenance_track_logger.log(TRACE, f"{dtype} {value} to {v}")
        return v
    if dtype in STRING_TYPES:
        v = "'" + value.replace("'", "''") + "'"
        provenance_track_logger.log(TRACE, f"{dtype} {value} to {v}")
        return v
    if dtype in NUMERIC_TYPES:
        provenance_track_logger.log(TRACE, f"{dtype} {value} as str")
        return str(value)
    if dtype == QSTRING_TYPE:
        v = "'" + str(value).replace("'", "''") + "'"
        provenance_track_logger.log(TRACE, f"{dtype} {value} to {v}")
        return v
    #    if dtype in AS_TYPES:
    #        provenance_track_logger.log(TRACE, f"{dtype} {value} as is")
    #        return value
    if dtype == ARRAY_TYPE:
        qstrings = [f'"{v}"' for v in value]
        v = f"'{{{','.join(qstrings)}}}'"
        provenance_track_logger.log(TRACE, f"{dtype} array {value} as {v}")
        return v
    if dtype == USER_DEFINED:
        if isinstance(value, str):
            v = "'" + value.replace("'", "''") + "'"
            provenance_track_logger.log(TRACE, f"{dtype} {value} to {v}")
            return v
        elif isinstance(value, dict):
            translated = []
            for entry in value.values():
                if entry is None:
                    translated.append('null')
                elif isinstance(entry, str):
                    translated.append("'" + entry.replace("'", "''") + "'")
                elif isinstance(entry, bool):
                    translated.append("'t'" if entry else "'f'")
                elif isinstance(entry, int) or isinstance(entry, float):
                    translated.append(entry)
                else:
                    translate_errors.append(f"Unsupported USER_DEFINED type {value} {type(entry)} {entry}")
                    return None
            return f"({','.join(str(v) for v in translated)})"

    translate_errors.append(f"Unsupported type {name} {dtype} for value {value}")
    return None


#def disable_provenance(plpy: PlpyAPI):
#    provenance_track_logger.warning(f"Provenance disabled {nan_user(plpy)}")
#    DISABLE_SENTINEL.touch(exist_ok=True)


def record(plpy: PlpyAPI, TD)->None:
#    if DISABLE_SENTINEL.exists():
#        provenance_track_logger.warning(f"Disabled {TD}")
#        return
    trigger_depth =  plpy.execute('select pg_trigger_depth()')[0]['pg_trigger_depth']
    fqtn = f"{TD['table_schema']}_{TD['table_name']}"
    if trigger_depth > 1:
        provenance_track_logger.info(f"Exiting {fqtn} trigger depth {trigger_depth}")
        return
    provenance_track_logger.info(TD)
    dotted = f"{TD['table_schema']}.{TD['table_name']}"
    provenance_track_logger.info(fqtn)
    r = plpy.execute(f"""select column_name,data_type 
        from information_schema.columns 
        where table_schema='provenance' and table_name='{fqtn}'""")
    if r.nrows() == 0:
        provenance_track_logger.warning(f"Table {dotted} not tracked provenance.{fqtn} not found")
        return
    cols = [(row['column_name'], row['data_type']) for row in r if not row['column_name'].startswith('provenance_')]
    provenance_track_logger.debug(cols)
    event = TD['event']
    event_type = EVENT_MAP[event]
    source = 'new' if event_type < 2 else 'old'
    colspec = ','.join((c[0] for c in cols))
    translate_errors.clear()
    values = [nan_user(plpy), str(event_type)] + [_translate(c[0], TD[source][c[0]], c[1]) for c in cols]
    if not translate_errors:
        query = f"""insert into provenance.{fqtn} (provenance_user,provenance_event,{colspec})
                values ({','.join(values)})"""
        provenance_track_logger.debug(f"source {source} query {query}")
        r = plpy.execute(query)
        if r.nrows() != 1:
            raise ProvenanceException(f"{event} updated {r.nrows()}")
    else:
        raise ProvenanceException(','.join(translate_errors))

    # EVENT
    provenance_track_logger.debug(f'{fqtn} in provenance')


def supported_types() -> Iterable[str]:
    """Types currently supported"""
    return SUPPORTED_TYPES
