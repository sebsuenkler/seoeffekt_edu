--
-- PostgreSQL database dump
--

-- Dumped from database version 11.10 (Debian 11.10-1.pgdg100+1)
-- Dumped by pg_dump version 13.1 (Debian 13.1-1.pgdg100+1)

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

--
-- Name: tablefunc; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;


--
-- Name: EXTENSION tablefunc; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';


--
-- Name: tsm_system_rows; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS tsm_system_rows WITH SCHEMA public;


--
-- Name: EXTENSION tsm_system_rows; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION tsm_system_rows IS 'TABLESAMPLE method which accepts number of rows as a limit';


--
-- Name: _final_median(numeric[]); Type: FUNCTION; Schema: public; Owner: seo
--

CREATE FUNCTION public._final_median(numeric[]) RETURNS numeric
    LANGUAGE sql IMMUTABLE
    AS $_$
   SELECT AVG(val)
   FROM (
     SELECT val
     FROM unnest($1) val
     ORDER BY 1
     LIMIT  2 - MOD(array_upper($1, 1), 2)
     OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
   ) sub;
$_$;


ALTER FUNCTION public._final_median(numeric[]) OWNER TO seo;

--
-- Name: median(numeric); Type: AGGREGATE; Schema: public; Owner: seo
--

CREATE AGGREGATE public.median(numeric) (
    SFUNC = array_append,
    STYPE = numeric[],
    INITCOND = '{}',
    FINALFUNC = public._final_median
);


ALTER AGGREGATE public.median(numeric) OWNER TO seo;

SET default_tablespace = '';

--
-- Name: classifications; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.classifications (
    classifications_hash text,
    classifications_result text,
    classifications_date date,
    classifications_id integer NOT NULL,
    classifications_classification text
);


ALTER TABLE public.classifications OWNER TO seo;

--
-- Name: classifications_classifications_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.classifications_classifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.classifications_classifications_id_seq OWNER TO seo;

--
-- Name: classifications_classifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.classifications_classifications_id_seq OWNED BY public.classifications.classifications_id;


--
-- Name: evaluations; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.evaluations (
    evaluations_results_hash character(32),
    evaluations_module text,
    evaluations_result text,
    evaluations_date date,
    evaluations_progress integer,
    evaluations_id integer NOT NULL
);


ALTER TABLE public.evaluations OWNER TO seo;

--
-- Name: evaluations_evaluations_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.evaluations_evaluations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.evaluations_evaluations_id_seq OWNER TO seo;

--
-- Name: evaluations_evaluations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.evaluations_evaluations_id_seq OWNED BY public.evaluations.evaluations_id;


--
-- Name: queries; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.queries (
    queries_studies_id integer,
    queries_query text,
    queries_comment text,
    queries_progress integer,
    queries_id integer NOT NULL,
    queries_date text
);


ALTER TABLE public.queries OWNER TO seo;

--
-- Name: queries_queries_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.queries_queries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.queries_queries_id_seq OWNER TO seo;

--
-- Name: queries_queries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.queries_queries_id_seq OWNED BY public.queries.queries_id;


--
-- Name: results; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.results (
    results_queries_id integer,
    results_studies_id integer,
    results_scrapers_id integer,
    results_import integer,
    results_ip text,
    results_hash character(32),
    results_main_hash text,
    results_contact_hash text,
    results_se text,
    results_position integer,
    results_url text,
    results_main text,
    results_contact text,
    results_date date,
    results_timestamp timestamp without time zone,
    results_progress integer,
    results_id integer NOT NULL
);


ALTER TABLE public.results OWNER TO seo;

--
-- Name: results_results_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.results_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.results_results_id_seq OWNER TO seo;

--
-- Name: results_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.results_results_id_seq OWNED BY public.results.results_id;


--
-- Name: scrapers; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.scrapers (
    scrapers_queries_id integer,
    scrapers_studies_id integer,
    scrapers_queries_query text,
    scrapers_se text,
    scrapers_start integer,
    scrapers_date date,
    scrapers_progress integer,
    scrapers_id integer NOT NULL
);


ALTER TABLE public.scrapers OWNER TO seo;

--
-- Name: scrapers_scrapers_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.scrapers_scrapers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scrapers_scrapers_id_seq OWNER TO seo;

--
-- Name: scrapers_scrapers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.scrapers_scrapers_id_seq OWNED BY public.scrapers.scrapers_id;


--
-- Name: serps; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.serps (
    serps_queries_id integer,
    serps_result text,
    serps_scrapers_result integer,
    serps_date date,
    serps_id integer NOT NULL,
    serps_se text
);


ALTER TABLE public.serps OWNER TO seo;

--
-- Name: serps_serps_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.serps_serps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.serps_serps_id_seq OWNER TO seo;

--
-- Name: serps_serps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.serps_serps_id_seq OWNED BY public.serps.serps_id;


--
-- Name: sources; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.sources (
    sources_hash text,
    sources_source text,
    sources_urls text,
    sources_comments text,
    sources_date date,
    sources_progress integer,
    sources_id integer NOT NULL,
    sources_speed real
);


ALTER TABLE public.sources OWNER TO seo;

--
-- Name: sources_sources_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.sources_sources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sources_sources_id_seq OWNER TO seo;

--
-- Name: sources_sources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.sources_sources_id_seq OWNED BY public.sources.sources_id;


--
-- Name: studies; Type: TABLE; Schema: public; Owner: seo
--

CREATE TABLE public.studies (
    studies_name text,
    studies_comment text,
    studies_date date,
    studies_id integer NOT NULL,
    import integer,
    studies_se text
);


ALTER TABLE public.studies OWNER TO seo;

--
-- Name: studies_studies_id_seq; Type: SEQUENCE; Schema: public; Owner: seo
--

CREATE SEQUENCE public.studies_studies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.studies_studies_id_seq OWNER TO seo;

--
-- Name: studies_studies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: seo
--

ALTER SEQUENCE public.studies_studies_id_seq OWNED BY public.studies.studies_id;


--
-- Name: classifications classifications_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.classifications ALTER COLUMN classifications_id SET DEFAULT nextval('public.classifications_classifications_id_seq'::regclass);


--
-- Name: evaluations evaluations_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.evaluations ALTER COLUMN evaluations_id SET DEFAULT nextval('public.evaluations_evaluations_id_seq'::regclass);


--
-- Name: queries queries_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.queries ALTER COLUMN queries_id SET DEFAULT nextval('public.queries_queries_id_seq'::regclass);


--
-- Name: results results_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.results ALTER COLUMN results_id SET DEFAULT nextval('public.results_results_id_seq'::regclass);


--
-- Name: scrapers scrapers_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.scrapers ALTER COLUMN scrapers_id SET DEFAULT nextval('public.scrapers_scrapers_id_seq'::regclass);


--
-- Name: serps serps_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.serps ALTER COLUMN serps_id SET DEFAULT nextval('public.serps_serps_id_seq'::regclass);


--
-- Name: sources sources_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.sources ALTER COLUMN sources_id SET DEFAULT nextval('public.sources_sources_id_seq'::regclass);


--
-- Name: studies studies_id; Type: DEFAULT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.studies ALTER COLUMN studies_id SET DEFAULT nextval('public.studies_studies_id_seq'::regclass);


--
-- Name: classifications classifications_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.classifications
    ADD CONSTRAINT classifications_pkey PRIMARY KEY (classifications_id);


--
-- Name: evaluations evaluations_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.evaluations
    ADD CONSTRAINT evaluations_pkey PRIMARY KEY (evaluations_id);


--
-- Name: queries queries_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.queries
    ADD CONSTRAINT queries_pkey PRIMARY KEY (queries_id);


--
-- Name: queries queries_queries_studies_id_queries_query_key; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.queries
    ADD CONSTRAINT queries_queries_studies_id_queries_query_key UNIQUE (queries_studies_id, queries_query);


--
-- Name: results results_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_pkey PRIMARY KEY (results_id);


--
-- Name: results results_results_queries_id_results_hash_results_se_results__key; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_results_queries_id_results_hash_results_se_results__key UNIQUE (results_queries_id, results_hash, results_se, results_url);


--
-- Name: scrapers scrapers_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.scrapers
    ADD CONSTRAINT scrapers_pkey PRIMARY KEY (scrapers_id);


--
-- Name: scrapers scrapers_scrapers_queries_id_scrapers_studies_id_scrapers_q_key; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.scrapers
    ADD CONSTRAINT scrapers_scrapers_queries_id_scrapers_studies_id_scrapers_q_key UNIQUE (scrapers_queries_id, scrapers_studies_id, scrapers_queries_query, scrapers_se, scrapers_start);


--
-- Name: serps serps_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.serps
    ADD CONSTRAINT serps_pkey PRIMARY KEY (serps_id);


--
-- Name: sources sources_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (sources_id);


--
-- Name: studies studies_pkey; Type: CONSTRAINT; Schema: public; Owner: seo
--

ALTER TABLE ONLY public.studies
    ADD CONSTRAINT studies_pkey PRIMARY KEY (studies_id);


--
-- Name: indx001; Type: INDEX; Schema: public; Owner: seo
--

CREATE INDEX indx001 ON public.evaluations USING btree (evaluations_results_hash);


--
-- Name: indx002; Type: INDEX; Schema: public; Owner: seo
--

CREATE INDEX indx002 ON public.results USING btree (results_hash);


--
-- PostgreSQL database dump complete
--
