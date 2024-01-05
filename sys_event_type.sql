create schema provenance;
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Ubuntu 15.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 15.5 (Ubuntu 15.5-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: sys_event_type; Type: TABLE; Schema: provenance; Owner: gweatherby
--

CREATE TABLE provenance.sys_event_type (
    id integer NOT NULL,
    description text NOT NULL
);


ALTER TABLE provenance.sys_event_type OWNER TO gweatherby;

--
-- Data for Name: sys_event_type; Type: TABLE DATA; Schema: provenance; Owner: gweatherby
--

COPY provenance.sys_event_type (id, description) FROM stdin;
0	insert
1	update
2	delete
\.


--
-- Name: sys_event_type provenancesys_event_type_pk; Type: CONSTRAINT; Schema: provenance; Owner: gweatherby
--

ALTER TABLE ONLY provenance.sys_event_type
    ADD CONSTRAINT provenancesys_event_type_pk PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

