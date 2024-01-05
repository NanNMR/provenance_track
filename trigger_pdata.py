CREATE LANGUAGE plpython3u;

CREATE or REPLACE FUNCTION public.upper_p() 
  RETURNS TRIGGER
LANGUAGE plpython3u 
AS $$ 
import datetime 
import plpy
import provenance_track
provenance_track.explore(plpy)
plpy.info(provenance_track.__version__)
newdata = TD["new"]
n = TD["new"]["name"]
uname = n.upper()
if n == uname: 
    plpy.debug("No change")
    return "OK"
n = TD["new"]["name"] = uname
plpy.info(f"make name {uname}")
#r = plpy.execute("select current_setting('nan.user')") 
#cu = r[0]['current_setting']
#plpy.info(f'{type(cu)} {cu}')
r = plpy.execute('select now()')
provenance_track.explore(r)

#plpy.info(provenance_track.nan_user())

return "MODIFY"
$$;

CREATE or REPLACE FUNCTION public.do_query() 
  RETURNS TRIGGER
LANGUAGE plpython3u 
AS $$ 
import plpy
r = plpy.execute('select name from public.pdata',2)
plpy.info(r[0]['namex'])
plpy.info(r[1]['name'])

return "OK"
$$;

DROP TRIGGER pdata_trigger on public.pdata;
CREATE TRIGGER pdata_trigger 
BEFORE
INSERT or UPDATE 
ON public.pdata FOR EACH ROW EXECUTE PROCEDURE public.upper_p() 
--ON public.pdata FOR EACH ROW EXECUTE PROCEDURE public.do_query()

