-- query to find any unmapped types in provenance
select distinct(data_type) from information_schema.columns where table_schema='provenance' and data_type not in (select get_provenance_types());
