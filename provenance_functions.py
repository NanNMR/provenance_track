CREATE LANGUAGE plpython3u;

CREATE or REPLACE FUNCTION public.record_provenance()
  RETURNS TRIGGER
LANGUAGE plpython3u 
AS $$ 
import datetime 
import plpy
import provenance_track 
from provenance_track import provenance_track_logger, record
plpy.info(provenance_track.__version__)
record(plpy,TD)
return "OK"
$$;

CREATE or REPLACE FUNCTION public.dont_truncate_provenance()
  RETURNS TRIGGER
LANGUAGE plpython3u 
AS $$ 
raise ValueError(f"truncate of provenance tracked table {TD['table_schema']}.{TD['table_name']} not supported. Use delete.")
$$;


CREATE or REPLACE PROCEDURE public.set_provenance_loglevel(level text)
LANGUAGE plpython3u 
AS $$ 
import provenance_track 
provenance_track.logsetup.set_loglevel(level)
$$;


CREATE or REPLACE FUNCTION public.get_provenance_loginfo()
  RETURNS TEXT
LANGUAGE plpython3u 
AS $$ 
import provenance_track 
return provenance_track.logsetup.get_loginfo()
$$;
