CREATE LANGUAGE plpython3u;

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
INSERT or UPDATE or DELETE 
ON public.pdata FOR EACH ROW EXECUTE PROCEDURE public.record_provenance() ;

DROP TRIGGER pdata_truncate on public.pdata;
CREATE TRIGGER pdata_truncate
BEFORE
TRUNCATE
ON public.pdata EXECUTE PROCEDURE public.dont_truncate_provenance();

