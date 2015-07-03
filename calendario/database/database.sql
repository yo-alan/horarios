--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.12
-- Dumped by pg_dump version 9.2.12
-- Started on 2015-07-03 11:09:25

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 202 (class 3079 OID 11727)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2166 (class 0 OID 0)
-- Dependencies: 202
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 175 (class 1259 OID 16464)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO django;

--
-- TOC entry 174 (class 1259 OID 16462)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO django;

--
-- TOC entry 2167 (class 0 OID 0)
-- Dependencies: 174
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 177 (class 1259 OID 16474)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO django;

--
-- TOC entry 176 (class 1259 OID 16472)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO django;

--
-- TOC entry 2168 (class 0 OID 0)
-- Dependencies: 176
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 173 (class 1259 OID 16454)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO django;

--
-- TOC entry 172 (class 1259 OID 16452)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO django;

--
-- TOC entry 2169 (class 0 OID 0)
-- Dependencies: 172
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 179 (class 1259 OID 16484)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO django;

--
-- TOC entry 181 (class 1259 OID 16494)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO django;

--
-- TOC entry 180 (class 1259 OID 16492)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO django;

--
-- TOC entry 2170 (class 0 OID 0)
-- Dependencies: 180
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 178 (class 1259 OID 16482)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO django;

--
-- TOC entry 2171 (class 0 OID 0)
-- Dependencies: 178
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 183 (class 1259 OID 16504)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO django;

--
-- TOC entry 182 (class 1259 OID 16502)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO django;

--
-- TOC entry 2172 (class 0 OID 0)
-- Dependencies: 182
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 187 (class 1259 OID 16582)
-- Name: calendario_calendario; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_calendario (
    id integer NOT NULL,
    puntaje integer NOT NULL,
    espacio_id integer NOT NULL
);


ALTER TABLE public.calendario_calendario OWNER TO django;

--
-- TOC entry 186 (class 1259 OID 16580)
-- Name: calendario_calendario_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE calendario_calendario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_calendario_id_seq OWNER TO django;

--
-- TOC entry 2173 (class 0 OID 0)
-- Dependencies: 186
-- Name: calendario_calendario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE calendario_calendario_id_seq OWNED BY calendario_calendario.id;


--
-- TOC entry 189 (class 1259 OID 16590)
-- Name: calendario_espacio; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_espacio (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.calendario_espacio OWNER TO django;

--
-- TOC entry 188 (class 1259 OID 16588)
-- Name: calendario_espacio_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE calendario_espacio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_espacio_id_seq OWNER TO django;

--
-- TOC entry 2174 (class 0 OID 0)
-- Dependencies: 188
-- Name: calendario_espacio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE calendario_espacio_id_seq OWNED BY calendario_espacio.id;


--
-- TOC entry 198 (class 1259 OID 16702)
-- Name: calendario_espacio_restriccion; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_espacio_restriccion (
    restriccion_ptr_id integer NOT NULL,
    espacio_id integer NOT NULL
);


ALTER TABLE public.calendario_espacio_restriccion OWNER TO django;

--
-- TOC entry 191 (class 1259 OID 16598)
-- Name: calendario_especialidad; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_especialidad (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    carga_horaria_semanal integer NOT NULL,
    max_horas_diaria integer NOT NULL
);


ALTER TABLE public.calendario_especialidad OWNER TO django;

--
-- TOC entry 190 (class 1259 OID 16596)
-- Name: calendario_especialidad_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE calendario_especialidad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_especialidad_id_seq OWNER TO django;

--
-- TOC entry 2175 (class 0 OID 0)
-- Dependencies: 190
-- Name: calendario_especialidad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE calendario_especialidad_id_seq OWNED BY calendario_especialidad.id;


--
-- TOC entry 193 (class 1259 OID 16606)
-- Name: calendario_horario; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_horario (
    id integer NOT NULL,
    hora_desde time without time zone NOT NULL,
    hora_hasta time without time zone NOT NULL,
    dia_semana integer NOT NULL,
    calendario_id integer NOT NULL,
    profesional_id integer NOT NULL
);


ALTER TABLE public.calendario_horario OWNER TO django;

--
-- TOC entry 192 (class 1259 OID 16604)
-- Name: calendario_horario_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE calendario_horario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_horario_id_seq OWNER TO django;

--
-- TOC entry 2176 (class 0 OID 0)
-- Dependencies: 192
-- Name: calendario_horario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE calendario_horario_id_seq OWNED BY calendario_horario.id;


--
-- TOC entry 200 (class 1259 OID 16709)
-- Name: calendario_persona; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_persona (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    cuil character varying(11) NOT NULL
);


ALTER TABLE public.calendario_persona OWNER TO django;

--
-- TOC entry 199 (class 1259 OID 16707)
-- Name: calendario_persona_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE calendario_persona_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_persona_id_seq OWNER TO django;

--
-- TOC entry 2177 (class 0 OID 0)
-- Dependencies: 199
-- Name: calendario_persona_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE calendario_persona_id_seq OWNED BY calendario_persona.id;


--
-- TOC entry 194 (class 1259 OID 16614)
-- Name: calendario_profesional; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_profesional (
    especialidad_id integer NOT NULL,
    persona_ptr_id integer NOT NULL
);


ALTER TABLE public.calendario_profesional OWNER TO django;

--
-- TOC entry 201 (class 1259 OID 16717)
-- Name: calendario_profesional_restriccion; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_profesional_restriccion (
    restriccion_ptr_id integer NOT NULL,
    profesional_id integer NOT NULL
);


ALTER TABLE public.calendario_profesional_restriccion OWNER TO django;

--
-- TOC entry 196 (class 1259 OID 16622)
-- Name: calendario_restriccion; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE calendario_restriccion (
    id integer NOT NULL,
    hora_desde time without time zone NOT NULL,
    hora_hasta time without time zone NOT NULL,
    dia_semana integer NOT NULL
);


ALTER TABLE public.calendario_restriccion OWNER TO django;

--
-- TOC entry 195 (class 1259 OID 16620)
-- Name: calendario_restriccion_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE calendario_restriccion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_restriccion_id_seq OWNER TO django;

--
-- TOC entry 2178 (class 0 OID 0)
-- Dependencies: 195
-- Name: calendario_restriccion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE calendario_restriccion_id_seq OWNED BY calendario_restriccion.id;


--
-- TOC entry 185 (class 1259 OID 16558)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO django;

--
-- TOC entry 184 (class 1259 OID 16556)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO django;

--
-- TOC entry 2179 (class 0 OID 0)
-- Dependencies: 184
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- TOC entry 171 (class 1259 OID 16444)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO django;

--
-- TOC entry 170 (class 1259 OID 16442)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO django;

--
-- TOC entry 2180 (class 0 OID 0)
-- Dependencies: 170
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 169 (class 1259 OID 16433)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO django;

--
-- TOC entry 168 (class 1259 OID 16431)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO django;

--
-- TOC entry 2181 (class 0 OID 0)
-- Dependencies: 168
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 197 (class 1259 OID 16654)
-- Name: django_session; Type: TABLE; Schema: public; Owner: django; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO django;

--
-- TOC entry 1916 (class 2604 OID 16467)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 1917 (class 2604 OID 16477)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 1915 (class 2604 OID 16457)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 1918 (class 2604 OID 16487)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 1919 (class 2604 OID 16497)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 1920 (class 2604 OID 16507)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 1923 (class 2604 OID 16585)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_calendario ALTER COLUMN id SET DEFAULT nextval('calendario_calendario_id_seq'::regclass);


--
-- TOC entry 1924 (class 2604 OID 16593)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_espacio ALTER COLUMN id SET DEFAULT nextval('calendario_espacio_id_seq'::regclass);


--
-- TOC entry 1925 (class 2604 OID 16601)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_especialidad ALTER COLUMN id SET DEFAULT nextval('calendario_especialidad_id_seq'::regclass);


--
-- TOC entry 1926 (class 2604 OID 16609)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_horario ALTER COLUMN id SET DEFAULT nextval('calendario_horario_id_seq'::regclass);


--
-- TOC entry 1928 (class 2604 OID 16712)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_persona ALTER COLUMN id SET DEFAULT nextval('calendario_persona_id_seq'::regclass);


--
-- TOC entry 1927 (class 2604 OID 16625)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_restriccion ALTER COLUMN id SET DEFAULT nextval('calendario_restriccion_id_seq'::regclass);


--
-- TOC entry 1921 (class 2604 OID 16561)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- TOC entry 1914 (class 2604 OID 16447)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 1913 (class 2604 OID 16436)
-- Name: id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 2132 (class 0 OID 16464)
-- Dependencies: 175
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: django
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 2182 (class 0 OID 0)
-- Dependencies: 174
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- TOC entry 2134 (class 0 OID 16474)
-- Dependencies: 177
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: django
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2183 (class 0 OID 0)
-- Dependencies: 176
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 2130 (class 0 OID 16454)
-- Dependencies: 173
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: django
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add especialidad	7	add_especialidad
20	Can change especialidad	7	change_especialidad
21	Can delete especialidad	7	delete_especialidad
22	Can add profesional	8	add_profesional
23	Can change profesional	8	change_profesional
24	Can delete profesional	8	delete_profesional
25	Can add calendario	9	add_calendario
26	Can change calendario	9	change_calendario
27	Can delete calendario	9	delete_calendario
28	Can add horario	10	add_horario
29	Can change horario	10	change_horario
30	Can delete horario	10	delete_horario
31	Can add restriccion	11	add_restriccion
32	Can change restriccion	11	change_restriccion
33	Can delete restriccion	11	delete_restriccion
34	Can add espacio	12	add_espacio
35	Can change espacio	12	change_espacio
36	Can delete espacio	12	delete_espacio
37	Can add persona	13	add_persona
38	Can change persona	13	change_persona
39	Can delete persona	13	delete_persona
40	Can add espacio_restriccion	14	add_espacio_restriccion
41	Can change espacio_restriccion	14	change_espacio_restriccion
42	Can delete espacio_restriccion	14	delete_espacio_restriccion
43	Can add profesional_restriccion	15	add_profesional_restriccion
44	Can change profesional_restriccion	15	change_profesional_restriccion
45	Can delete profesional_restriccion	15	delete_profesional_restriccion
\.


--
-- TOC entry 2184 (class 0 OID 0)
-- Dependencies: 172
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('auth_permission_id_seq', 45, true);


--
-- TOC entry 2136 (class 0 OID 16484)
-- Dependencies: 179
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: django
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$20000$4GR2HvMLeNbH$PIn+1tJ0n3Ars8rnWtODFq6UXATpUoFDXzPwt2uiqnQ=	2015-06-17 12:49:58.515-03	t	admin				t	t	2015-06-17 12:49:41.838-03
\.


--
-- TOC entry 2138 (class 0 OID 16494)
-- Dependencies: 181
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: django
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 2185 (class 0 OID 0)
-- Dependencies: 180
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- TOC entry 2186 (class 0 OID 0)
-- Dependencies: 178
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- TOC entry 2140 (class 0 OID 16504)
-- Dependencies: 183
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: django
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2187 (class 0 OID 0)
-- Dependencies: 182
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 2144 (class 0 OID 16582)
-- Dependencies: 187
-- Data for Name: calendario_calendario; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_calendario (id, puntaje, espacio_id) FROM stdin;
\.


--
-- TOC entry 2188 (class 0 OID 0)
-- Dependencies: 186
-- Name: calendario_calendario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('calendario_calendario_id_seq', 1650, true);


--
-- TOC entry 2146 (class 0 OID 16590)
-- Dependencies: 189
-- Data for Name: calendario_espacio; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_espacio (id, nombre) FROM stdin;
1	1ro 1ra
\.


--
-- TOC entry 2189 (class 0 OID 0)
-- Dependencies: 188
-- Name: calendario_espacio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('calendario_espacio_id_seq', 1, true);


--
-- TOC entry 2155 (class 0 OID 16702)
-- Dependencies: 198
-- Data for Name: calendario_espacio_restriccion; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_espacio_restriccion (restriccion_ptr_id, espacio_id) FROM stdin;
\.


--
-- TOC entry 2148 (class 0 OID 16598)
-- Dependencies: 191
-- Data for Name: calendario_especialidad; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_especialidad (id, nombre, carga_horaria_semanal, max_horas_diaria) FROM stdin;
14	Lengua	5	2
15	Matematica	5	2
16	Sociales	5	2
17	Naturales	5	2
18	Tecnologia	3	2
19	Construccion Ciudadana	3	2
20	Lenguaje Artístico	2	2
21	Ingles	3	2
22	Educación Fisica	2	2
23	Taller Ocupacional	2	2
24	Espacio Integrador	2	2
25	Biologia	5	2
26	Historia	5	2
27	Geografía	5	2
28	Fisica	5	2
29	Psicologia	3	2
30	Espacio y Reflexion Curricular	2	2
31	Teoria y Tecnica de la Organizacion Contable	5	2
32	Derecho	5	2
33	Economia	5	2
34	Administracion Publica	5	2
35	Quimica	5	2
36	Cultura	2	2
37	Educación Civica	6	2
38	Teoria y Finanzas Publicas	4	2
39	Introduccion al Estado, Sociedad y Cultura	4	2
\.


--
-- TOC entry 2190 (class 0 OID 0)
-- Dependencies: 190
-- Name: calendario_especialidad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('calendario_especialidad_id_seq', 39, true);


--
-- TOC entry 2150 (class 0 OID 16606)
-- Dependencies: 193
-- Data for Name: calendario_horario; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_horario (id, hora_desde, hora_hasta, dia_semana, calendario_id, profesional_id) FROM stdin;
\.


--
-- TOC entry 2191 (class 0 OID 0)
-- Dependencies: 192
-- Name: calendario_horario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('calendario_horario_id_seq', 58932, true);


--
-- TOC entry 2157 (class 0 OID 16709)
-- Dependencies: 200
-- Data for Name: calendario_persona; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_persona (id, nombre, apellido, cuil) FROM stdin;
81	Juan	Abadie	98364609063
82	Emir	Abait	44807523850
83	Amelia E	Aballay	72547059110
84	Calos A	Abalos	74671538355
85	Claudia	Abarsua	18596741596
86	Yanina	Abbet	71895576673
87	Romina	Abelen	12224134817
88	Guillermo	Abril	47144474185
89	Ariel E	Aburto	43561972935
90	Albina	Barrientos	21589982652
91	Celia A	Barriga	44034950194
92	Adan I	Barrionuevo	23677500195
93	Jessica	Barrios	69994576542
94	Maria	Barros	86720294467
95	Jose Maria	Barroso	53061949980
96	Gerardo	Barsotti	41228989871
97	Pablo	Barta	59367895849
98	Julio	Bartels	70752666159
99	Maria	Bazan	96267639298
100	Silvia	Castillo	33159597773
101	Cesar	Castro	46877514111
102	Ariel	Catalan	66895998851
103	Carolina	Cataldo	98886339806
104	Grisel	Cataneo	72746811916
105	Juan	Catelican	37567630863
106	Pablo	Catepillan	42840245484
107	Maria	Cativa	87131223303
108	Roberto	Centeno	96794708762
109	Maria	Chaile	52484184051
110	Eva	Del Valle	89165033814
111	Alberto	Diaz	20021299850
112	Miguel	Dominguez	62990934065
113	Jose Maria	Doria	69507394593
114	Luis	Dures	25098745201
115	Rene	Duval	35827623916
116	Ernesto	Echaniz	64591219202
117	Gabriel	Errazu	64678313718
118	Cristian	Echeverria	94399387750
119	Dario	Escalante	64497802443
120	Juan	Faviani	96386731954
121	Sebastian	Fagetti	67364238794
122	Irma	Faisca	70988244463
123	Ernesto	Falcon	52324560100
124	Aurora	Fernandez	42376639322
125	Clara	Fernandez	56896450050
126	Marcelina	Flores	59022688644
127	Mauro	Freidiaz	41279995865
128	Juan	Frias	67725592987
129	Victor	Funes	39696872417
130	Eloy	Galarza	49979006574
131	Felix	Galeano	60900612077
132	Jorge	Galiano	78476636636
133	Aldo	Galindo	18622081710
134	Angel	Gallardo	49054607849
135	Estefania	Gomez	82112735415
136	Daniela	Gonzalez	16688150182
137	Gabriela	Gotuzzo	26320723575
138	Onoria	Gramajo	43444950708
139	Gustavo	Guazzone	24130781801
140	Maria	Haro	48094353876
141	Adriana	Hernandez	15526011111
142	Norma	Herrera	21521903927
143	Edemundo	Huechert	76325511458
144	Daniela	Hidalgo	54223417458
145	Gustavo	Howells	31674960052
146	Estela	Haiquil	35038728114
147	Elsa	Hualquilaf	54779717817
148	Raul	Huerga	73094130480
149	Esteban	Jones	80510916615
\.


--
-- TOC entry 2192 (class 0 OID 0)
-- Dependencies: 199
-- Name: calendario_persona_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('calendario_persona_id_seq', 149, true);


--
-- TOC entry 2151 (class 0 OID 16614)
-- Dependencies: 194
-- Data for Name: calendario_profesional; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_profesional (especialidad_id, persona_ptr_id) FROM stdin;
14	81
15	82
16	83
17	84
18	85
19	86
20	87
21	88
22	89
23	90
24	91
25	92
26	93
27	94
28	95
29	96
30	97
31	98
32	99
33	100
34	101
35	102
36	103
37	104
38	105
39	106
39	107
38	108
37	109
36	110
35	111
34	112
33	113
32	114
31	115
30	116
29	117
28	118
27	119
26	120
25	121
24	122
23	123
22	124
21	125
20	126
19	127
18	128
17	129
16	130
15	131
14	132
14	133
\.


--
-- TOC entry 2158 (class 0 OID 16717)
-- Dependencies: 201
-- Data for Name: calendario_profesional_restriccion; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_profesional_restriccion (restriccion_ptr_id, profesional_id) FROM stdin;
\.


--
-- TOC entry 2153 (class 0 OID 16622)
-- Dependencies: 196
-- Data for Name: calendario_restriccion; Type: TABLE DATA; Schema: public; Owner: django
--

COPY calendario_restriccion (id, hora_desde, hora_hasta, dia_semana) FROM stdin;
\.


--
-- TOC entry 2193 (class 0 OID 0)
-- Dependencies: 195
-- Name: calendario_restriccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('calendario_restriccion_id_seq', 1, false);


--
-- TOC entry 2142 (class 0 OID 16558)
-- Dependencies: 185
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: django
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2015-06-17 12:50:59.588-03	2	Matematica	1		7	1
\.


--
-- TOC entry 2194 (class 0 OID 0)
-- Dependencies: 184
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, true);


--
-- TOC entry 2128 (class 0 OID 16444)
-- Dependencies: 171
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: django
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	calendario	especialidad
8	calendario	profesional
9	calendario	calendario
10	calendario	horario
11	calendario	restriccion
12	calendario	espacio
13	calendario	persona
14	calendario	espacio_restriccion
15	calendario	profesional_restriccion
\.


--
-- TOC entry 2195 (class 0 OID 0)
-- Dependencies: 170
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('django_content_type_id_seq', 15, true);


--
-- TOC entry 2126 (class 0 OID 16433)
-- Dependencies: 169
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: django
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-06-12 13:47:08.713-03
2	auth	0001_initial	2015-06-12 13:47:09.04-03
3	admin	0001_initial	2015-06-12 13:47:09.087-03
4	contenttypes	0002_remove_content_type_name	2015-06-12 13:47:09.149-03
5	auth	0002_alter_permission_name_max_length	2015-06-12 13:47:09.165-03
6	auth	0003_alter_user_email_max_length	2015-06-12 13:47:09.196-03
7	auth	0004_alter_user_username_opts	2015-06-12 13:47:09.212-03
8	auth	0005_alter_user_last_login_null	2015-06-12 13:47:09.227-03
9	auth	0006_require_contenttypes_0002	2015-06-12 13:47:09.227-03
10	calendario	0001_initial	2015-06-12 13:47:09.305-03
11	calendario	0002_auto_20150607_1944	2015-06-12 13:47:09.383-03
12	calendario	0003_auto_20150607_1954	2015-06-12 13:47:09.399-03
13	calendario	0004_auto_20150612_1346	2015-06-12 13:47:09.446-03
14	sessions	0001_initial	2015-06-12 13:47:09.508-03
15	calendario	0002_auto_20150623_0942	2015-06-23 09:43:07.85-03
16	calendario	0003_auto_20150629_0916	2015-06-29 09:19:18.67-03
17	calendario	0004_auto_20150629_0919	2015-06-29 09:21:16.49-03
\.


--
-- TOC entry 2196 (class 0 OID 0)
-- Dependencies: 168
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('django_migrations_id_seq', 17, true);


--
-- TOC entry 2154 (class 0 OID 16654)
-- Dependencies: 197
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: django
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
dcw7vzdzr5f62n53x0gmuv01qqya7xkv	ZmM0M2QzYjRmMTU0ZWRlOGY1ZmQxOWFlMWViMDYwODIzZDFhMzhiOTp7Il9hdXRoX3VzZXJfaGFzaCI6ImM5Y2E3M2E4ZTgwNTBlMTY3OTIwYTg5NjgzODIwYjYwZWYwYzY0ZDMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2015-07-01 12:49:58.577-03
\.


--
-- TOC entry 1942 (class 2606 OID 16471)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 1948 (class 2606 OID 16481)
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- TOC entry 1950 (class 2606 OID 16479)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 1944 (class 2606 OID 16469)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 1937 (class 2606 OID 16461)
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- TOC entry 1939 (class 2606 OID 16459)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 1959 (class 2606 OID 16499)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 1961 (class 2606 OID 16501)
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- TOC entry 1952 (class 2606 OID 16489)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 1965 (class 2606 OID 16509)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 1967 (class 2606 OID 16511)
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- TOC entry 1955 (class 2606 OID 16491)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 1974 (class 2606 OID 16587)
-- Name: calendario_calendario_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_calendario
    ADD CONSTRAINT calendario_calendario_pkey PRIMARY KEY (id);


--
-- TOC entry 1976 (class 2606 OID 16595)
-- Name: calendario_espacio_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio
    ADD CONSTRAINT calendario_espacio_pkey PRIMARY KEY (id);


--
-- TOC entry 1994 (class 2606 OID 16706)
-- Name: calendario_espacio_restriccion_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio_restriccion
    ADD CONSTRAINT calendario_espacio_restriccion_pkey PRIMARY KEY (restriccion_ptr_id);


--
-- TOC entry 1978 (class 2606 OID 16603)
-- Name: calendario_especialidad_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_especialidad
    ADD CONSTRAINT calendario_especialidad_pkey PRIMARY KEY (id);


--
-- TOC entry 1982 (class 2606 OID 16611)
-- Name: calendario_horario_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT calendario_horario_pkey PRIMARY KEY (id);


--
-- TOC entry 1997 (class 2606 OID 16716)
-- Name: calendario_persona_cuil_key; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_persona
    ADD CONSTRAINT calendario_persona_cuil_key UNIQUE (cuil);


--
-- TOC entry 1999 (class 2606 OID 16714)
-- Name: calendario_persona_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_persona
    ADD CONSTRAINT calendario_persona_pkey PRIMARY KEY (id);


--
-- TOC entry 1985 (class 2606 OID 16755)
-- Name: calendario_profesional_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_profesional
    ADD CONSTRAINT calendario_profesional_pkey PRIMARY KEY (persona_ptr_id);


--
-- TOC entry 2002 (class 2606 OID 16721)
-- Name: calendario_profesional_restriccion_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_profesional_restriccion
    ADD CONSTRAINT calendario_profesional_restriccion_pkey PRIMARY KEY (restriccion_ptr_id);


--
-- TOC entry 1987 (class 2606 OID 16627)
-- Name: calendario_restriccion_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY calendario_restriccion
    ADD CONSTRAINT calendario_restriccion_pkey PRIMARY KEY (id);


--
-- TOC entry 1971 (class 2606 OID 16567)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 1932 (class 2606 OID 16451)
-- Name: django_content_type_app_label_3ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_3ec8c61c_uniq UNIQUE (app_label, model);


--
-- TOC entry 1934 (class 2606 OID 16449)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 1930 (class 2606 OID 16441)
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 1990 (class 2606 OID 16661)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: django; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 1940 (class 1259 OID 16518)
-- Name: auth_group_name_331666e8_like; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_group_name_331666e8_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 1945 (class 1259 OID 16529)
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 1946 (class 1259 OID 16530)
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 1935 (class 1259 OID 16517)
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- TOC entry 1956 (class 1259 OID 16543)
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- TOC entry 1957 (class 1259 OID 16542)
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- TOC entry 1962 (class 1259 OID 16555)
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 1963 (class 1259 OID 16554)
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 1953 (class 1259 OID 16531)
-- Name: auth_user_username_94b8aae_like; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX auth_user_username_94b8aae_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 1972 (class 1259 OID 16690)
-- Name: calendario_calendario_42380e88; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_calendario_42380e88 ON calendario_calendario USING btree (espacio_id);


--
-- TOC entry 1992 (class 1259 OID 16732)
-- Name: calendario_espacio_restriccion_42380e88; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_espacio_restriccion_42380e88 ON calendario_espacio_restriccion USING btree (espacio_id);


--
-- TOC entry 1979 (class 1259 OID 16633)
-- Name: calendario_horario_0a9eef5d; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_horario_0a9eef5d ON calendario_horario USING btree (calendario_id);


--
-- TOC entry 1980 (class 1259 OID 16640)
-- Name: calendario_horario_6e88626c; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_horario_6e88626c ON calendario_horario USING btree (profesional_id);


--
-- TOC entry 1995 (class 1259 OID 16733)
-- Name: calendario_persona_cuil_3a4b5b83_like; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_persona_cuil_3a4b5b83_like ON calendario_persona USING btree (cuil varchar_pattern_ops);


--
-- TOC entry 1983 (class 1259 OID 16639)
-- Name: calendario_profesional_8a03056c; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_profesional_8a03056c ON calendario_profesional USING btree (especialidad_id);


--
-- TOC entry 2000 (class 1259 OID 16739)
-- Name: calendario_profesional_restriccion_6e88626c; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX calendario_profesional_restriccion_6e88626c ON calendario_profesional_restriccion USING btree (profesional_id);


--
-- TOC entry 1968 (class 1259 OID 16578)
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 1969 (class 1259 OID 16579)
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- TOC entry 1988 (class 1259 OID 16662)
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- TOC entry 1991 (class 1259 OID 16663)
-- Name: django_session_session_key_630ca218_like; Type: INDEX; Schema: public; Owner: django; Tablespace: 
--

CREATE INDEX django_session_session_key_630ca218_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2005 (class 2606 OID 16524)
-- Name: auth_group_permiss_permission_id_23962d04_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_23962d04_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2004 (class 2606 OID 16519)
-- Name: auth_group_permissions_group_id_58c48ba9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_58c48ba9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2003 (class 2606 OID 16512)
-- Name: auth_permiss_content_type_id_51277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_51277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2007 (class 2606 OID 16537)
-- Name: auth_user_groups_group_id_30a071c9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_30a071c9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2006 (class 2606 OID 16532)
-- Name: auth_user_groups_user_id_24702650_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_24702650_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2009 (class 2606 OID 16549)
-- Name: auth_user_user_per_permission_id_3d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_3d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2008 (class 2606 OID 16544)
-- Name: auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2016 (class 2606 OID 16722)
-- Name: calend_restriccion_ptr_id_2a867cbe_fk_calendario_restriccion_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_espacio_restriccion
    ADD CONSTRAINT calend_restriccion_ptr_id_2a867cbe_fk_calendario_restriccion_id FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2018 (class 2606 OID 16734)
-- Name: calend_restriccion_ptr_id_720d03b8_fk_calendario_restriccion_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_profesional_restriccion
    ADD CONSTRAINT calend_restriccion_ptr_id_720d03b8_fk_calendario_restriccion_id FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2014 (class 2606 OID 16634)
-- Name: calendar_especialidad_id_77e8c21b_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_profesional
    ADD CONSTRAINT calendar_especialidad_id_77e8c21b_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2012 (class 2606 OID 16691)
-- Name: calendario_calenda_espacio_id_67a90411_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_calendario
    ADD CONSTRAINT calendario_calenda_espacio_id_67a90411_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2017 (class 2606 OID 16727)
-- Name: calendario_espacio_espacio_id_7ad4bdf2_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_espacio_restriccion
    ADD CONSTRAINT calendario_espacio_espacio_id_7ad4bdf2_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2013 (class 2606 OID 16628)
-- Name: calendario_h_calendario_id_74ab73af_fk_calendario_calendario_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT calendario_h_calendario_id_74ab73af_fk_calendario_calendario_id FOREIGN KEY (calendario_id) REFERENCES calendario_calendario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2015 (class 2606 OID 16761)
-- Name: calendario_pro_persona_ptr_id_7739eebd_fk_calendario_persona_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY calendario_profesional
    ADD CONSTRAINT calendario_pro_persona_ptr_id_7739eebd_fk_calendario_persona_id FOREIGN KEY (persona_ptr_id) REFERENCES calendario_persona(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2010 (class 2606 OID 16568)
-- Name: django_admin_content_type_id_5151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_5151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2011 (class 2606 OID 16573)
-- Name: django_admin_log_user_id_1c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_1c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2165 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-07-03 11:09:26

--
-- PostgreSQL database dump complete
--

