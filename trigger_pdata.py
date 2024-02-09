import provenance_track.logsetup

CREATE LANGUAGE plpython3u;

CREATE or REPLACE FUNCTION public.record_ch() 
  RETURNS TRIGGER
LANGUAGE plpython3u 
AS $$ 
import datetime 
import plpy
import provenance_track 
from provenance_track import provenance_track_logger, record
plpy.warning('trigger fire')
plpy.info(provenance_track.__version__)
provenance_track.logsetup.set_loglevel('DEBUG')
record(plpy,TD)

#plpy.info(provenance_track.nan_user())

return "OK"
$$;

CREATE or REPLACE FUNCTION public.do_query() 
  RETURNS TRIGGER
LANGUAGE plpython3u 
AS $$ 
import plpy
plpy.info(f'GD is {GD}')

return "OK"
$$;

DROP TRIGGER pdata_trigger on public.pdata;
CREATE TRIGGER pdata_trigger 
BEFORE
INSERT or UPDATE or DELETE or TRUNCATE
ON public.pdata FOR EACH ROW EXECUTE PROCEDURE public.record_ch() 
--ON public.pdata FOR EACH ROW EXECUTE PROCEDURE public.do_query()

