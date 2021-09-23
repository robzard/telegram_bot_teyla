-- Table: public.movies

-- DROP TABLE public.movies;

CREATE TABLE IF NOT EXISTS public.movies
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    chat_id bigint,
    username character varying(300) COLLATE pg_catalog."default",
    full_name character varying(300) COLLATE pg_catalog."default",
    category_move character varying(300) COLLATE pg_catalog."default",
    button_name_move character varying(300) COLLATE pg_catalog."default",
    datetime_move timestamp with time zone NOT NULL,
    CONSTRAINT movies_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.movies
    OWNER to postgres;


-- Table: public.users

-- DROP TABLE public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    chat_id bigint,
    username character varying(300) COLLATE pg_catalog."default",
    full_name character varying(300) COLLATE pg_catalog."default",
    phone character varying(15) COLLATE pg_catalog."default",
    need_manager boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to postgres;


-- Table: public.userstext

-- DROP TABLE public.userstext;

CREATE TABLE IF NOT EXISTS public.userstext
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    chat_id text COLLATE pg_catalog."default",
    username text COLLATE pg_catalog."default",
    firstname text COLLATE pg_catalog."default",
    lastname text COLLATE pg_catalog."default",
    text text COLLATE pg_catalog."default",
    dateinsert timestamp with time zone,
    CONSTRAINT userstext_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.userstext
    OWNER to postgres;