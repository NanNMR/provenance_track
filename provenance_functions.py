import provenance_track.logsetup

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


CREATE or REPLACE PROCEDURE public.set_provenance_loglevel(level text)
LANGUAGE plpython3u 
AS $$ 
import provenance_track 
provenance_track.logsetup.set_loglevel(level)
$$;

CREATE or REPLACE FUNCTION public.get_provenance_loglevel()
LANGUAGE plpython3u 
AS $$ 
import provenance_track 
return provenance_track.logsetup.get_loginfo()
$$;
