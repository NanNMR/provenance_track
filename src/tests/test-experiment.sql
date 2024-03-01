select set_provenance_loglevel('DEBUG');
update nanexperiment.experiment set person_id = 162 where id =
(select max(id) from nanexperiment.experiment where person_id != 162)
