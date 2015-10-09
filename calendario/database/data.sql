--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO horarios;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO horarios;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO horarios;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO horarios;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO horarios;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO horarios;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
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


ALTER TABLE public.auth_user OWNER TO horarios;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO horarios;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO horarios;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO horarios;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO horarios;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO horarios;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: calendario_calendario; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_calendario (
    id integer NOT NULL,
    puntaje integer NOT NULL,
    estado character varying(3) NOT NULL,
    usuario_creador character varying(30) NOT NULL,
    fecha_creacion date NOT NULL,
    usuario_modificador character varying(30) NOT NULL,
    fecha_modificacion date NOT NULL,
    espacio_id integer NOT NULL
);


ALTER TABLE public.calendario_calendario OWNER TO horarios;

--
-- Name: calendario_calendario_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_calendario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_calendario_id_seq OWNER TO horarios;

--
-- Name: calendario_calendario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_calendario_id_seq OWNED BY calendario_calendario.id;


--
-- Name: calendario_coordinador; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_coordinador (
    id integer NOT NULL,
    espacio_id integer NOT NULL,
    especialidad_id integer NOT NULL,
    profesional_id integer NOT NULL
);


ALTER TABLE public.calendario_coordinador OWNER TO horarios;

--
-- Name: calendario_coordinador_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_coordinador_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_coordinador_id_seq OWNER TO horarios;

--
-- Name: calendario_coordinador_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_coordinador_id_seq OWNED BY calendario_coordinador.id;


--
-- Name: calendario_espacio; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_espacio (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    estado character varying(3) NOT NULL,
    usuario_creador character varying(30) NOT NULL,
    fecha_creacion date NOT NULL,
    usuario_modificador character varying(30) NOT NULL,
    fecha_modificacion date NOT NULL
);


ALTER TABLE public.calendario_espacio OWNER TO horarios;

--
-- Name: calendario_espacio_especialidades; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_espacio_especialidades (
    id integer NOT NULL,
    espacio_id integer NOT NULL,
    especialidad_id integer NOT NULL
);


ALTER TABLE public.calendario_espacio_especialidades OWNER TO horarios;

--
-- Name: calendario_espacio_especialidades_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_espacio_especialidades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_espacio_especialidades_id_seq OWNER TO horarios;

--
-- Name: calendario_espacio_especialidades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_espacio_especialidades_id_seq OWNED BY calendario_espacio_especialidades.id;


--
-- Name: calendario_espacio_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_espacio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_espacio_id_seq OWNER TO horarios;

--
-- Name: calendario_espacio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_espacio_id_seq OWNED BY calendario_espacio.id;


--
-- Name: calendario_espacio_profesionales; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_espacio_profesionales (
    id integer NOT NULL,
    espacio_id integer NOT NULL,
    profesional_id integer NOT NULL
);


ALTER TABLE public.calendario_espacio_profesionales OWNER TO horarios;

--
-- Name: calendario_espacio_profesionales_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_espacio_profesionales_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_espacio_profesionales_id_seq OWNER TO horarios;

--
-- Name: calendario_espacio_profesionales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_espacio_profesionales_id_seq OWNED BY calendario_espacio_profesionales.id;


--
-- Name: calendario_espaciorestriccion; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_espaciorestriccion (
    restriccion_ptr_id integer NOT NULL,
    espacio_id integer NOT NULL
);


ALTER TABLE public.calendario_espaciorestriccion OWNER TO horarios;

--
-- Name: calendario_especialidad; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_especialidad (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    carga_horaria_semanal integer NOT NULL,
    max_horas_diaria integer NOT NULL,
    estado character varying(3) NOT NULL,
    usuario_creador character varying(30) NOT NULL,
    fecha_creacion date NOT NULL,
    usuario_modificador character varying(30) NOT NULL,
    fecha_modificacion date NOT NULL
);


ALTER TABLE public.calendario_especialidad OWNER TO horarios;

--
-- Name: calendario_especialidad_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_especialidad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_especialidad_id_seq OWNER TO horarios;

--
-- Name: calendario_especialidad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_especialidad_id_seq OWNED BY calendario_especialidad.id;


--
-- Name: calendario_hora; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_hora (
    id integer NOT NULL,
    hora_desde time without time zone NOT NULL,
    hora_hasta time without time zone NOT NULL,
    espacio_id integer NOT NULL
);


ALTER TABLE public.calendario_hora OWNER TO horarios;

--
-- Name: calendario_hora_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_hora_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_hora_id_seq OWNER TO horarios;

--
-- Name: calendario_hora_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_hora_id_seq OWNED BY calendario_hora.id;


--
-- Name: calendario_horario; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_horario (
    id integer NOT NULL,
    hora_desde time without time zone NOT NULL,
    hora_hasta time without time zone NOT NULL,
    dia_semana integer NOT NULL,
    calendario_id integer NOT NULL,
    especialidad_id integer NOT NULL,
    profesional_id integer NOT NULL,
    penalizado integer NOT NULL
);


ALTER TABLE public.calendario_horario OWNER TO horarios;

--
-- Name: calendario_horario_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_horario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_horario_id_seq OWNER TO horarios;

--
-- Name: calendario_horario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_horario_id_seq OWNED BY calendario_horario.id;


--
-- Name: calendario_persona; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_persona (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    cuil character varying(11) NOT NULL,
    estado character varying(3) NOT NULL,
    usuario_creador character varying(30) NOT NULL,
    fecha_creacion date NOT NULL,
    usuario_modificador character varying(30) NOT NULL,
    fecha_modificacion date NOT NULL
);


ALTER TABLE public.calendario_persona OWNER TO horarios;

--
-- Name: calendario_persona_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_persona_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_persona_id_seq OWNER TO horarios;

--
-- Name: calendario_persona_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_persona_id_seq OWNED BY calendario_persona.id;


--
-- Name: calendario_profesional; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_profesional (
    persona_ptr_id integer NOT NULL
);


ALTER TABLE public.calendario_profesional OWNER TO horarios;

--
-- Name: calendario_profesional_especialidades; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_profesional_especialidades (
    id integer NOT NULL,
    profesional_id integer NOT NULL,
    especialidad_id integer NOT NULL
);


ALTER TABLE public.calendario_profesional_especialidades OWNER TO horarios;

--
-- Name: calendario_profesional_especialidades_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_profesional_especialidades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_profesional_especialidades_id_seq OWNER TO horarios;

--
-- Name: calendario_profesional_especialidades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_profesional_especialidades_id_seq OWNED BY calendario_profesional_especialidades.id;


--
-- Name: calendario_profesionalrestriccion; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_profesionalrestriccion (
    restriccion_ptr_id integer NOT NULL,
    profesional_id integer NOT NULL
);


ALTER TABLE public.calendario_profesionalrestriccion OWNER TO horarios;

--
-- Name: calendario_restriccion; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE calendario_restriccion (
    id integer NOT NULL,
    hora_desde time without time zone NOT NULL,
    hora_hasta time without time zone NOT NULL,
    dia_semana integer NOT NULL,
    estado character varying(3) NOT NULL,
    usuario_creador character varying(30) NOT NULL,
    fecha_creacion date NOT NULL,
    usuario_modificador character varying(30) NOT NULL,
    fecha_modificacion date NOT NULL
);


ALTER TABLE public.calendario_restriccion OWNER TO horarios;

--
-- Name: calendario_restriccion_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE calendario_restriccion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.calendario_restriccion_id_seq OWNER TO horarios;

--
-- Name: calendario_restriccion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE calendario_restriccion_id_seq OWNED BY calendario_restriccion.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
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


ALTER TABLE public.django_admin_log OWNER TO horarios;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO horarios;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO horarios;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO horarios;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO horarios;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: horarios
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO horarios;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: horarios
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: horarios; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO horarios;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_calendario ALTER COLUMN id SET DEFAULT nextval('calendario_calendario_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_coordinador ALTER COLUMN id SET DEFAULT nextval('calendario_coordinador_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio ALTER COLUMN id SET DEFAULT nextval('calendario_espacio_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_especialidades ALTER COLUMN id SET DEFAULT nextval('calendario_espacio_especialidades_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_profesionales ALTER COLUMN id SET DEFAULT nextval('calendario_espacio_profesionales_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_especialidad ALTER COLUMN id SET DEFAULT nextval('calendario_especialidad_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_hora ALTER COLUMN id SET DEFAULT nextval('calendario_hora_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_horario ALTER COLUMN id SET DEFAULT nextval('calendario_horario_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_persona ALTER COLUMN id SET DEFAULT nextval('calendario_persona_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional_especialidades ALTER COLUMN id SET DEFAULT nextval('calendario_profesional_especialidades_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_restriccion ALTER COLUMN id SET DEFAULT nextval('calendario_restriccion_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: horarios
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
22	Can add espacio	8	add_espacio
23	Can change espacio	8	change_espacio
24	Can delete espacio	8	delete_espacio
25	Can add hora	9	add_hora
26	Can change hora	9	change_hora
27	Can delete hora	9	delete_hora
28	Can add persona	10	add_persona
29	Can change persona	10	change_persona
30	Can delete persona	10	delete_persona
31	Can add profesional	11	add_profesional
32	Can change profesional	11	change_profesional
33	Can delete profesional	11	delete_profesional
34	Can add calendario	12	add_calendario
35	Can change calendario	12	change_calendario
36	Can delete calendario	12	delete_calendario
37	Can add horario	13	add_horario
38	Can change horario	13	change_horario
39	Can delete horario	13	delete_horario
40	Can add restriccion	14	add_restriccion
41	Can change restriccion	14	change_restriccion
42	Can delete restriccion	14	delete_restriccion
43	Can add espacio restriccion	15	add_espaciorestriccion
44	Can change espacio restriccion	15	change_espaciorestriccion
45	Can delete espacio restriccion	15	delete_espaciorestriccion
46	Can add profesional restriccion	16	add_profesionalrestriccion
47	Can change profesional restriccion	16	change_profesionalrestriccion
48	Can delete profesional restriccion	16	delete_profesionalrestriccion
55	Can add coordinador	19	add_coordinador
56	Can change coordinador	19	change_coordinador
57	Can delete coordinador	19	delete_coordinador
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('auth_permission_id_seq', 57, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$20000$AIfzWAHbfUKq$+rm8Sj/CABWA+8hfsvn4ILm7rTSB69cXspSJcSl0/rg=	2015-06-07 16:38:48.664428-03	t	admin				t	t	2015-06-07 16:38:24.713836-03
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: calendario_calendario; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_calendario (id, puntaje, estado, usuario_creador, fecha_creacion, usuario_modificador, fecha_modificacion, espacio_id) FROM stdin;
\.


--
-- Name: calendario_calendario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_calendario_id_seq', 18478, true);


--
-- Data for Name: calendario_coordinador; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_coordinador (id, espacio_id, especialidad_id, profesional_id) FROM stdin;
1	1	25	89
2	1	32	92
3	1	33	88
4	1	36	91
5	1	34	93
6	5	33	88
7	5	25	89
8	5	36	91
9	5	32	92
10	5	34	93
11	5	14	94
12	5	28	95
13	5	37	96
\.


--
-- Name: calendario_coordinador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_coordinador_id_seq', 13, true);


--
-- Data for Name: calendario_espacio; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_espacio (id, nombre, estado, usuario_creador, fecha_creacion, usuario_modificador, fecha_modificacion) FROM stdin;
1	1ro 1ra	ON	admin	2015-09-03	admin	2015-09-03
5	1ro 2da	ON	admin	2015-08-19	admin	2015-08-19
7	1ro 3ra	ON	admin	2015-08-19	admin	2015-08-19
9	2do 2da	ON	admin	2015-08-19	admin	2015-08-19
8	2do 1ra	ON	admin	2015-08-19	admin	2015-08-19
10	2do 3ra	ON	admin	2015-08-19	admin	2015-08-19
4	1ro 1ra	OFF	admin	2015-08-19	admin	2015-09-11
14	DES01	ON	admin	2015-10-09	admin	2015-10-09
\.


--
-- Data for Name: calendario_espacio_especialidades; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_espacio_especialidades (id, espacio_id, especialidad_id) FROM stdin;
45	1	34
46	1	25
47	1	36
48	1	32
49	1	33
55	5	25
56	5	32
57	5	33
58	5	36
59	5	34
60	5	37
61	5	28
62	5	14
\.


--
-- Name: calendario_espacio_especialidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_espacio_especialidades_id_seq', 62, true);


--
-- Name: calendario_espacio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_espacio_id_seq', 14, true);


--
-- Data for Name: calendario_espacio_profesionales; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_espacio_profesionales (id, espacio_id, profesional_id) FROM stdin;
1	1	88
2	1	89
3	1	91
4	1	92
5	1	93
17	5	89
18	5	91
19	5	92
20	5	93
21	5	94
22	5	88
23	5	95
24	5	96
\.


--
-- Name: calendario_espacio_profesionales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_espacio_profesionales_id_seq', 24, true);


--
-- Data for Name: calendario_espaciorestriccion; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_espaciorestriccion (restriccion_ptr_id, espacio_id) FROM stdin;
\.


--
-- Data for Name: calendario_especialidad; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_especialidad (id, nombre, carga_horaria_semanal, max_horas_diaria, estado, usuario_creador, fecha_creacion, usuario_modificador, fecha_modificacion) FROM stdin;
14	Lengua	5	2	ON	admin	2015-08-19	admin	2015-08-19
15	Matematica	5	2	ON	admin	2015-08-19	admin	2015-08-19
16	Sociales	5	2	ON	admin	2015-08-19	admin	2015-08-19
17	Naturales	5	2	ON	admin	2015-08-19	admin	2015-08-19
18	Tecnologia	3	2	ON	admin	2015-08-19	admin	2015-08-19
21	Ingles	3	2	ON	admin	2015-08-19	admin	2015-08-19
22	Educación Fisica	2	2	ON	admin	2015-08-19	admin	2015-08-19
23	Taller Ocupacional	2	2	ON	admin	2015-08-19	admin	2015-08-19
24	Espacio Integrador	2	2	ON	admin	2015-08-19	admin	2015-08-19
25	Biologia	5	2	ON	admin	2015-08-19	admin	2015-08-19
26	Historia	5	2	ON	admin	2015-08-19	admin	2015-08-19
27	Geografía	5	2	ON	admin	2015-08-19	admin	2015-08-19
28	Fisica	5	2	ON	admin	2015-08-19	admin	2015-08-19
29	Psicologia	3	2	ON	admin	2015-08-19	admin	2015-08-19
30	Espacio y Reflexion Curricular	2	2	ON	admin	2015-08-19	admin	2015-08-19
31	Teoria y Tecnica de la Organizacion Contable	5	2	ON	admin	2015-08-19	admin	2015-08-19
32	Derecho	5	2	ON	admin	2015-08-19	admin	2015-08-19
33	Economia	5	2	ON	admin	2015-08-19	admin	2015-08-19
35	Quimica	5	2	ON	admin	2015-08-19	admin	2015-08-19
36	Cultura	2	2	ON	admin	2015-08-19	admin	2015-08-19
37	Educación Civica	6	2	ON	admin	2015-08-19	admin	2015-08-19
38	Teoria y Finanzas Publicas	4	2	ON	admin	2015-08-19	admin	2015-08-19
39	Introduccion al Estado, Sociedad y Cultura	4	2	ON	admin	2015-08-19	admin	2015-08-19
40	Ingles Ll	3	4	ON	admin	2015-08-19	admin	2015-08-19
34	Administración Pública	2	2	ON	admin	2015-08-19	admin	2015-08-20
\.


--
-- Name: calendario_especialidad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_especialidad_id_seq', 42, true);


--
-- Data for Name: calendario_hora; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_hora (id, hora_desde, hora_hasta, espacio_id) FROM stdin;
1	18:15:00	18:55:00	1
2	18:55:00	19:35:00	1
4	19:45:00	20:25:00	1
5	20:25:00	21:00:00	1
6	21:05:00	22:45:00	1
12	18:15:00	18:55:00	4
13	18:55:00	19:35:00	4
14	19:45:00	20:25:00	4
16	20:25:00	21:00:00	4
17	21:00:00	21:45:00	4
18	21:45:00	22:25:00	4
19	22:25:00	23:00:00	4
23	18:15:00	18:55:00	5
24	18:55:00	19:35:00	5
25	19:45:00	20:25:00	5
26	20:25:00	21:05:00	5
27	21:05:00	21:45:00	5
28	21:45:00	22:25:00	5
29	22:25:00	23:05:00	5
\.


--
-- Name: calendario_hora_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_hora_id_seq', 29, true);


--
-- Data for Name: calendario_horario; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_horario (id, hora_desde, hora_hasta, dia_semana, calendario_id, especialidad_id, profesional_id, penalizado) FROM stdin;
\.


--
-- Name: calendario_horario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_horario_id_seq', 450015, true);


--
-- Data for Name: calendario_persona; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_persona (id, nombre, apellido, cuil, estado, usuario_creador, fecha_creacion, usuario_modificador, fecha_modificacion) FROM stdin;
89	Ariel E	Aburto	43561972935	ON	admin	2015-08-19	admin	2015-08-19
91	Celia A	Barriga	44034950194	ON	admin	2015-08-19	admin	2015-08-19
92	Adan I	Barrionuevo	23677500195	ON	admin	2015-08-19	admin	2015-08-19
93	Jessica	Barrios	69994576542	ON	admin	2015-08-19	admin	2015-08-19
94	Maria	Barros	86720294467	ON	admin	2015-08-19	admin	2015-08-19
95	Jose Maria	Barroso	53061949980	ON	admin	2015-08-19	admin	2015-08-19
96	Gerardo	Barsotti	41228989871	ON	admin	2015-08-19	admin	2015-08-19
97	Pablo	Barta	59367895849	ON	admin	2015-08-19	admin	2015-08-19
99	Maria	Bazan	96267639298	ON	admin	2015-08-19	admin	2015-08-19
100	Silvia	Castillo	33159597773	ON	admin	2015-08-19	admin	2015-08-19
101	Cesar	Castro	46877514111	ON	admin	2015-08-19	admin	2015-08-19
102	Ariel	Catalan	66895998851	ON	admin	2015-08-19	admin	2015-08-19
103	Carolina	Cataldo	98886339806	ON	admin	2015-08-19	admin	2015-08-19
104	Grisel	Cataneo	72746811916	ON	admin	2015-08-19	admin	2015-08-19
105	Juan	Catelican	37567630863	ON	admin	2015-08-19	admin	2015-08-19
106	Pablo	Catepillan	42840245484	ON	admin	2015-08-19	admin	2015-08-19
107	Maria	Cativa	87131223303	ON	admin	2015-08-19	admin	2015-08-19
108	Roberto	Centeno	96794708762	ON	admin	2015-08-19	admin	2015-08-19
109	Maria	Chaile	52484184051	ON	admin	2015-08-19	admin	2015-08-19
110	Eva	Del Valle	89165033814	ON	admin	2015-08-19	admin	2015-08-19
111	Alberto	Diaz	20021299850	ON	admin	2015-08-19	admin	2015-08-19
112	Miguel	Dominguez	62990934065	ON	admin	2015-08-19	admin	2015-08-19
113	Jose Maria	Doria	69507394593	ON	admin	2015-08-19	admin	2015-08-19
114	Luis	Dures	25098745201	ON	admin	2015-08-19	admin	2015-08-19
115	Rene	Duval	35827623916	ON	admin	2015-08-19	admin	2015-08-19
116	Ernesto	Echaniz	64591219202	ON	admin	2015-08-19	admin	2015-08-19
117	Gabriel	Errazu	64678313718	ON	admin	2015-08-19	admin	2015-08-19
118	Cristian	Echeverria	94399387750	ON	admin	2015-08-19	admin	2015-08-19
119	Dario	Escalante	64497802443	ON	admin	2015-08-19	admin	2015-08-19
120	Juan	Faviani	96386731954	ON	admin	2015-08-19	admin	2015-08-19
121	Sebastian	Fagetti	67364238794	ON	admin	2015-08-19	admin	2015-08-19
122	Irma	Faisca	70988244463	ON	admin	2015-08-19	admin	2015-08-19
123	Ernesto	Falcon	52324560100	ON	admin	2015-08-19	admin	2015-08-19
124	Aurora	Fernandez	42376639322	ON	admin	2015-08-19	admin	2015-08-19
125	Clara	Fernandez	56896450050	ON	admin	2015-08-19	admin	2015-08-19
128	Juan	Frias	67725592987	ON	admin	2015-08-19	admin	2015-08-19
129	Victor	Funes	39696872417	ON	admin	2015-08-19	admin	2015-08-19
130	Eloy	Galarza	49979006574	ON	admin	2015-08-19	admin	2015-08-19
131	Felix	Galeano	60900612077	ON	admin	2015-08-19	admin	2015-08-19
134	Angel	Gallardo	49054607849	ON	admin	2015-08-19	admin	2015-08-19
135	Estefania	Gomez	82112735415	ON	admin	2015-08-19	admin	2015-08-19
136	Daniela	Gonzalez	16688150182	ON	admin	2015-08-19	admin	2015-08-19
137	Gabriela	Gotuzzo	26320723575	ON	admin	2015-08-19	admin	2015-08-19
138	Onoria	Gramajo	43444950708	ON	admin	2015-08-19	admin	2015-08-19
139	Gustavo	Guazzone	24130781801	ON	admin	2015-08-19	admin	2015-08-19
140	Maria	Haro	48094353876	ON	admin	2015-08-19	admin	2015-08-19
141	Adriana	Hernandez	15526011111	ON	admin	2015-08-19	admin	2015-08-19
142	Norma	Herrera	21521903927	ON	admin	2015-08-19	admin	2015-08-19
143	Edemundo	Huechert	76325511458	ON	admin	2015-08-19	admin	2015-08-19
144	Daniela	Hidalgo	54223417458	ON	admin	2015-08-19	admin	2015-08-19
145	Gustavo	Howells	31674960052	ON	admin	2015-08-19	admin	2015-08-19
146	Estela	Haiquil	35038728114	ON	admin	2015-08-19	admin	2015-08-19
147	Elsa	Hualquilaf	54779717817	ON	admin	2015-08-19	admin	2015-08-19
148	Raul	Huerga	73094130480	ON	admin	2015-08-19	admin	2015-08-19
149	Esteban	Jones	80510916615	ON	admin	2015-08-19	admin	2015-08-19
98	Julio	Bartels	70752666159	ON	admin	2015-08-19	admin	2015-08-19
150	Rodrigo	Rodriguez	30000000	ON	admin	2015-08-19	admin	2015-08-19
161	Alan Franco	Marchán	23380460459	ON	admin	2015-08-19	admin	2015-08-19
88	Guillermina	Abril	47144474185	ON	admin	2015-08-19	admin	2015-08-21
\.


--
-- Name: calendario_persona_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_persona_id_seq', 172, true);


--
-- Data for Name: calendario_profesional; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_profesional (persona_ptr_id) FROM stdin;
88
89
91
92
93
94
95
96
97
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
128
129
130
131
98
150
161
\.


--
-- Data for Name: calendario_profesional_especialidades; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_profesional_especialidades (id, profesional_id, especialidad_id) FROM stdin;
5	89	25
6	91	36
8	92	32
10	93	34
11	94	14
12	88	15
13	88	33
14	95	28
15	96	37
\.


--
-- Name: calendario_profesional_especialidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_profesional_especialidades_id_seq', 15, true);


--
-- Data for Name: calendario_profesionalrestriccion; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_profesionalrestriccion (restriccion_ptr_id, profesional_id) FROM stdin;
9	88
10	88
11	88
12	89
13	89
14	91
15	91
16	92
17	93
18	93
19	94
20	95
21	96
22	96
\.


--
-- Data for Name: calendario_restriccion; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY calendario_restriccion (id, hora_desde, hora_hasta, dia_semana, estado, usuario_creador, fecha_creacion, usuario_modificador, fecha_modificacion) FROM stdin;
1	12:30:00	23:30:00	1	ON	admin	2015-08-20	admin	2015-08-20
2	10:00:00	11:00:00	1	ON	admin	2015-08-21	admin	2015-08-21
3	23:00:00	00:00:00	2	ON	admin	2015-08-21	admin	2015-08-21
4	18:30:00	20:30:00	1	ON	admin	2015-08-21	admin	2015-08-21
5	22:00:00	23:00:00	2	ON	admin	2015-08-21	admin	2015-08-21
6	20:00:00	21:30:00	4	ON	admin	2015-08-21	admin	2015-08-21
7	19:00:00	23:00:00	5	ON	admin	2015-08-21	admin	2015-08-21
9	18:00:00	19:00:00	2	ON	admin	2015-09-11	admin	2015-09-11
10	18:00:00	19:00:00	3	ON	admin	2015-09-11	admin	2015-09-11
11	18:00:00	19:00:00	4	ON	admin	2015-09-11	admin	2015-09-11
12	19:00:00	22:00:00	5	ON	admin	2015-09-11	admin	2015-09-11
13	19:00:00	22:00:00	1	ON	admin	2015-09-11	admin	2015-09-11
14	18:00:00	20:00:00	2	ON	admin	2015-10-09	admin	2015-10-09
15	20:30:00	22:00:00	4	ON	admin	2015-10-09	admin	2015-10-09
16	19:00:00	21:00:00	7	ON	admin	2015-10-09	admin	2015-10-09
17	18:00:00	19:30:00	3	ON	admin	2015-10-09	admin	2015-10-09
18	21:00:00	23:00:00	4	ON	admin	2015-10-09	admin	2015-10-09
19	18:00:00	21:00:00	1	ON	admin	2015-10-09	admin	2015-10-09
20	19:00:00	21:00:00	5	ON	admin	2015-10-09	admin	2015-10-09
21	18:00:00	20:00:00	2	ON	admin	2015-10-09	admin	2015-10-09
22	18:00:00	20:00:00	3	ON	admin	2015-10-09	admin	2015-10-09
\.


--
-- Name: calendario_restriccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('calendario_restriccion_id_seq', 22, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2015-06-07 16:40:33.933832-03	1	Lengua	1		7	1
2	2015-06-07 16:40:44.927338-03	2	Matematica	1		7	1
3	2015-06-07 16:40:53.87427-03	3	Historia	1		7	1
4	2015-06-07 16:44:54.415977-03	1	Perez, Pedro	1		8	1
5	2015-06-07 16:45:19.400257-03	2	Rodriguez, Rodrigo	1		8	1
6	2015-06-07 16:45:50.768621-03	3	Gonzalez, Gonzalo	1		8	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	calendario	especialidad
8	calendario	espacio
9	calendario	hora
10	calendario	persona
11	calendario	profesional
12	calendario	calendario
13	calendario	horario
14	calendario	restriccion
15	calendario	espaciorestriccion
16	calendario	profesionalrestriccion
19	calendario	coordinador
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('django_content_type_id_seq', 19, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-09-03 16:17:40.424794-03
2	auth	0001_initial	2015-09-03 16:17:41.471327-03
3	admin	0001_initial	2015-09-03 16:17:41.760717-03
4	contenttypes	0002_remove_content_type_name	2015-09-03 16:17:42.035316-03
5	auth	0002_alter_permission_name_max_length	2015-09-03 16:17:42.235566-03
6	auth	0003_alter_user_email_max_length	2015-09-03 16:17:42.343668-03
7	auth	0004_alter_user_username_opts	2015-09-03 16:17:42.435446-03
8	auth	0005_alter_user_last_login_null	2015-09-03 16:17:42.54365-03
9	auth	0006_require_contenttypes_0002	2015-09-03 16:17:42.560303-03
10	calendario	0001_initial	2015-09-03 16:17:44.608426-03
11	sessions	0001_initial	2015-09-03 16:17:44.805843-03
12	calendario	0002_auto_20150908_1755	2015-09-08 14:55:12.371774-03
27	calendario	0003_coordinador	2015-09-11 15:00:00.405398-03
28	calendario	0004_horario_penalizado	2015-09-18 17:01:10.979667-03
29	calendario	0005_remove_horario_penalizado	2015-09-18 17:37:40.931321-03
30	calendario	0006_horario_penalizado	2015-09-18 17:38:06.346502-03
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: horarios
--

SELECT pg_catalog.setval('django_migrations_id_seq', 30, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: horarios
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
c2poh5zd4odp7kdzn203qwh1iwu0e4vm	NWQwNDc5MGVhOGY4ZTY4ZGMxMjVlYjg0YmEzYzZkNjk3ZDlmOGE2Yjp7Il9hdXRoX3VzZXJfaGFzaCI6IjRiNzI3Mzk1NDlkMjcwZDM2ODAyOWJiZTdkZmU1MWY5OGJkZjU4ODQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2015-06-21 16:38:48.67542-03
dcw7vzdzr5f62n53x0gmuv01qqya7xkv	ZmM0M2QzYjRmMTU0ZWRlOGY1ZmQxOWFlMWViMDYwODIzZDFhMzhiOTp7Il9hdXRoX3VzZXJfaGFzaCI6ImM5Y2E3M2E4ZTgwNTBlMTY3OTIwYTg5NjgzODIwYjYwZWYwYzY0ZDMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2015-07-01 12:49:58.577-03
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: calendario_calendario_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_calendario
    ADD CONSTRAINT calendario_calendario_pkey PRIMARY KEY (id);


--
-- Name: calendario_coordinador_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_coordinador
    ADD CONSTRAINT calendario_coordinador_pkey PRIMARY KEY (id);


--
-- Name: calendario_espacio_especialidade_espacio_id_especialidad_id_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio_especialidades
    ADD CONSTRAINT calendario_espacio_especialidade_espacio_id_especialidad_id_key UNIQUE (espacio_id, especialidad_id);


--
-- Name: calendario_espacio_especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio_especialidades
    ADD CONSTRAINT calendario_espacio_especialidades_pkey PRIMARY KEY (id);


--
-- Name: calendario_espacio_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio
    ADD CONSTRAINT calendario_espacio_pkey PRIMARY KEY (id);


--
-- Name: calendario_espacio_profesionales_espacio_id_profesional_id_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio_profesionales
    ADD CONSTRAINT calendario_espacio_profesionales_espacio_id_profesional_id_key UNIQUE (espacio_id, profesional_id);


--
-- Name: calendario_espacio_profesionales_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_espacio_profesionales
    ADD CONSTRAINT calendario_espacio_profesionales_pkey PRIMARY KEY (id);


--
-- Name: calendario_espaciorestriccion_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT calendario_espaciorestriccion_pkey PRIMARY KEY (restriccion_ptr_id);


--
-- Name: calendario_especialidad_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_especialidad
    ADD CONSTRAINT calendario_especialidad_pkey PRIMARY KEY (id);


--
-- Name: calendario_hora_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_hora
    ADD CONSTRAINT calendario_hora_pkey PRIMARY KEY (id);


--
-- Name: calendario_horario_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT calendario_horario_pkey PRIMARY KEY (id);


--
-- Name: calendario_persona_cuil_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_persona
    ADD CONSTRAINT calendario_persona_cuil_key UNIQUE (cuil);


--
-- Name: calendario_persona_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_persona
    ADD CONSTRAINT calendario_persona_pkey PRIMARY KEY (id);


--
-- Name: calendario_profesional_especi_profesional_id_especialidad_i_key; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_profesional_especialidades
    ADD CONSTRAINT calendario_profesional_especi_profesional_id_especialidad_i_key UNIQUE (profesional_id, especialidad_id);


--
-- Name: calendario_profesional_especialidades_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_profesional_especialidades
    ADD CONSTRAINT calendario_profesional_especialidades_pkey PRIMARY KEY (id);


--
-- Name: calendario_profesional_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_profesional
    ADD CONSTRAINT calendario_profesional_pkey PRIMARY KEY (persona_ptr_id);


--
-- Name: calendario_profesionalrestriccion_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_profesionalrestriccion
    ADD CONSTRAINT calendario_profesionalrestriccion_pkey PRIMARY KEY (restriccion_ptr_id);


--
-- Name: calendario_restriccion_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY calendario_restriccion
    ADD CONSTRAINT calendario_restriccion_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_3ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_3ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_app_label_45f3b1d93ec8c61c_uniq; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_45f3b1d93ec8c61c_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: horarios; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_253ae2a6331666e8_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_group_name_253ae2a6331666e8_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_name_331666e8_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_group_name_331666e8_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_51b3b110094b8aae_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_user_username_51b3b110094b8aae_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: auth_user_username_94b8aae_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX auth_user_username_94b8aae_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: calendario_calendario_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_calendario_42380e88 ON calendario_calendario USING btree (espacio_id);


--
-- Name: calendario_coordinador_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_coordinador_42380e88 ON calendario_coordinador USING btree (espacio_id);


--
-- Name: calendario_coordinador_6e88626c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_coordinador_6e88626c ON calendario_coordinador USING btree (profesional_id);


--
-- Name: calendario_coordinador_8a03056c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_coordinador_8a03056c ON calendario_coordinador USING btree (especialidad_id);


--
-- Name: calendario_espacio_especialidades_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_espacio_especialidades_42380e88 ON calendario_espacio_especialidades USING btree (espacio_id);


--
-- Name: calendario_espacio_especialidades_8a03056c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_espacio_especialidades_8a03056c ON calendario_espacio_especialidades USING btree (especialidad_id);


--
-- Name: calendario_espacio_profesionales_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_espacio_profesionales_42380e88 ON calendario_espacio_profesionales USING btree (espacio_id);


--
-- Name: calendario_espacio_profesionales_6e88626c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_espacio_profesionales_6e88626c ON calendario_espacio_profesionales USING btree (profesional_id);


--
-- Name: calendario_espacio_restriccion_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_espacio_restriccion_42380e88 ON calendario_espaciorestriccion USING btree (espacio_id);


--
-- Name: calendario_espaciorestriccion_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_espaciorestriccion_42380e88 ON calendario_espaciorestriccion USING btree (espacio_id);


--
-- Name: calendario_hora_42380e88; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_hora_42380e88 ON calendario_hora USING btree (espacio_id);


--
-- Name: calendario_horario_0a9eef5d; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_horario_0a9eef5d ON calendario_horario USING btree (calendario_id);


--
-- Name: calendario_horario_6e88626c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_horario_6e88626c ON calendario_horario USING btree (profesional_id);


--
-- Name: calendario_horario_8a03056c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_horario_8a03056c ON calendario_horario USING btree (especialidad_id);


--
-- Name: calendario_persona_cuil_3a4b5b83_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_persona_cuil_3a4b5b83_like ON calendario_persona USING btree (cuil varchar_pattern_ops);


--
-- Name: calendario_persona_cuil_4e81ec5c5b4a47d_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_persona_cuil_4e81ec5c5b4a47d_like ON calendario_persona USING btree (cuil varchar_pattern_ops);


--
-- Name: calendario_profesional_especialidades_6e88626c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_profesional_especialidades_6e88626c ON calendario_profesional_especialidades USING btree (profesional_id);


--
-- Name: calendario_profesional_especialidades_8a03056c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_profesional_especialidades_8a03056c ON calendario_profesional_especialidades USING btree (especialidad_id);


--
-- Name: calendario_profesional_restriccion_6e88626c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_profesional_restriccion_6e88626c ON calendario_profesionalrestriccion USING btree (profesional_id);


--
-- Name: calendario_profesionalrestriccion_6e88626c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX calendario_profesionalrestriccion_6e88626c ON calendario_profesionalrestriccion USING btree (profesional_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_461cfeaa630ca218_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX django_session_session_key_461cfeaa630ca218_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_session_session_key_630ca218_like; Type: INDEX; Schema: public; Owner: horarios; Tablespace: 
--

CREATE INDEX django_session_session_key_630ca218_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: D1929cf99f8a46028d62cb93681b9230; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional_especialidades
    ADD CONSTRAINT "D1929cf99f8a46028d62cb93681b9230" FOREIGN KEY (profesional_id) REFERENCES calendario_profesional(persona_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D2656d7ec5bd0b097d707c5d8cab848e; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_profesionales
    ADD CONSTRAINT "D2656d7ec5bd0b097d707c5d8cab848e" FOREIGN KEY (profesional_id) REFERENCES calendario_profesional(persona_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D46c1980869b84a4a3e8f8d5d82b4c89; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT "D46c1980869b84a4a3e8f8d5d82b4c89" FOREIGN KEY (profesional_id) REFERENCES calendario_profesional(persona_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D65078a745b92b6df2a5d1da17d08eae; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesionalrestriccion
    ADD CONSTRAINT "D65078a745b92b6df2a5d1da17d08eae" FOREIGN KEY (profesional_id) REFERENCES calendario_profesional(persona_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D683b8c9d17fa5158869a73a4db9d9ba; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesionalrestriccion
    ADD CONSTRAINT "D683b8c9d17fa5158869a73a4db9d9ba" FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D9c78d03e15a18e2f25a1c434e0c7b4b; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT "D9c78d03e15a18e2f25a1c434e0c7b4b" FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: a180a8029614a93ac2302656ad61fdf4; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_coordinador
    ADD CONSTRAINT a180a8029614a93ac2302656ad61fdf4 FOREIGN KEY (profesional_id) REFERENCES calendario_profesional(persona_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_508cf46651277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_508cf46651277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permiss_permission_id_23962d04_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_23962d04_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_689710a9a73b7457_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_58c48ba9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_58c48ba9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_51277a81_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_51277a81_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_384b62483d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_30a071c9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_30a071c9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_24702650_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_24702650_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_3d7071f0_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_3d7071f0_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_7f0938558328534a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: c6d89922d113e121f82dafd8dcbf1e03; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional_especialidades
    ADD CONSTRAINT c6d89922d113e121f82dafd8dcbf1e03 FOREIGN KEY (profesional_id) REFERENCES calendario_profesional(persona_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calen_calendario_id_97ffe298b548c51_fk_calendario_calendario_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT calen_calendario_id_97ffe298b548c51_fk_calendario_calendario_id FOREIGN KEY (calendario_id) REFERENCES calendario_calendario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calend_persona_ptr_id_2cece4cc88c61143_fk_calendario_persona_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional
    ADD CONSTRAINT calend_persona_ptr_id_2cece4cc88c61143_fk_calendario_persona_id FOREIGN KEY (persona_ptr_id) REFERENCES calendario_persona(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calend_restriccion_ptr_id_21b2b742_fk_calendario_restriccion_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT calend_restriccion_ptr_id_21b2b742_fk_calendario_restriccion_id FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calend_restriccion_ptr_id_2a867cbe_fk_calendario_restriccion_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT calend_restriccion_ptr_id_2a867cbe_fk_calendario_restriccion_id FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calend_restriccion_ptr_id_61021b94_fk_calendario_restriccion_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesionalrestriccion
    ADD CONSTRAINT calend_restriccion_ptr_id_61021b94_fk_calendario_restriccion_id FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calend_restriccion_ptr_id_720d03b8_fk_calendario_restriccion_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesionalrestriccion
    ADD CONSTRAINT calend_restriccion_ptr_id_720d03b8_fk_calendario_restriccion_id FOREIGN KEY (restriccion_ptr_id) REFERENCES calendario_restriccion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendar_especialidad_id_5c829887_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT calendar_especialidad_id_5c829887_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendar_especialidad_id_5d7332ff_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_coordinador
    ADD CONSTRAINT calendar_especialidad_id_5d7332ff_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendar_especialidad_id_6259fbaf_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_especialidades
    ADD CONSTRAINT calendar_especialidad_id_6259fbaf_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendari_especialidad_id_84a8c59_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional_especialidades
    ADD CONSTRAINT calendari_especialidad_id_84a8c59_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_calenda_espacio_id_67a90411_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_calendario
    ADD CONSTRAINT calendario_calenda_espacio_id_67a90411_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_coordin_espacio_id_40ef9ea6_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_coordinador
    ADD CONSTRAINT calendario_coordin_espacio_id_40ef9ea6_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio__espacio_id_8b3bae1_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_profesionales
    ADD CONSTRAINT calendario_espacio__espacio_id_8b3bae1_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_espacio_id_516d95f8_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_especialidades
    ADD CONSTRAINT calendario_espacio_espacio_id_516d95f8_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_espacio_id_6350f60e_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT calendario_espacio_espacio_id_6350f60e_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_espacio_id_7ad4bdf2_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT calendario_espacio_espacio_id_7ad4bdf2_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_id_266a22649856fbef_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_calendario
    ADD CONSTRAINT calendario_espacio_id_266a22649856fbef_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_id_318d6bbc516d95f8_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_especialidades
    ADD CONSTRAINT calendario_espacio_id_318d6bbc516d95f8_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_id_4bb1c202f134affb_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_hora
    ADD CONSTRAINT calendario_espacio_id_4bb1c202f134affb_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_espacio_id_7221ddb8852b420e_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espaciorestriccion
    ADD CONSTRAINT calendario_espacio_id_7221ddb8852b420e_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_h_calendario_id_74ab73af_fk_calendario_calendario_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT calendario_h_calendario_id_74ab73af_fk_calendario_calendario_id FOREIGN KEY (calendario_id) REFERENCES calendario_calendario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_hora_espacio_id_ecb5005_fk_calendario_espacio_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_hora
    ADD CONSTRAINT calendario_hora_espacio_id_ecb5005_fk_calendario_espacio_id FOREIGN KEY (espacio_id) REFERENCES calendario_espacio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: calendario_pro_persona_ptr_id_7739eebd_fk_calendario_persona_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional
    ADD CONSTRAINT calendario_pro_persona_ptr_id_7739eebd_fk_calendario_persona_id FOREIGN KEY (persona_ptr_id) REFERENCES calendario_persona(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_697914295151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_697914295151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_5151027a_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_5151027a_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_1c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_1c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: especialidad_id_17810e6ea37d6779_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_horario
    ADD CONSTRAINT especialidad_id_17810e6ea37d6779_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: especialidad_id_2dc8f431084a8c59_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_profesional_especialidades
    ADD CONSTRAINT especialidad_id_2dc8f431084a8c59_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: especialidad_id_74cbae319da60451_fk_calendario_especialidad_id; Type: FK CONSTRAINT; Schema: public; Owner: horarios
--

ALTER TABLE ONLY calendario_espacio_especialidades
    ADD CONSTRAINT especialidad_id_74cbae319da60451_fk_calendario_especialidad_id FOREIGN KEY (especialidad_id) REFERENCES calendario_especialidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

