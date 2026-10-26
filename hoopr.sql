--
-- PostgreSQL database dump
--

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-09-26 08:28:39

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS "hooprCBBD";
--
-- TOC entry 5427 (class 1262 OID 16516)
-- Name: hooprCBBD; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "hooprCBBD" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Pakistan.1252';


ALTER DATABASE "hooprCBBD" OWNER TO postgres;

\unrestrict LlteUceiaSVa6gC5s9nywWtt1fX2UMQEfC4MVc1XoYv7QLSdOSmzwoxQPlOVeS3
\connect "hooprCBBD"
\restrict LlteUceiaSVa6gC5s9nywWtt1fX2UMQEfC4MVc1XoYv7QLSdOSmzwoxQPlOVeS3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 5428 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 885 (class 1247 OID 17360)
-- Name: arch_group; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.arch_group AS ENUM (
    'guard',
    'wing',
    'big'
);


ALTER TYPE public.arch_group OWNER TO postgres;

--
-- TOC entry 888 (class 1247 OID 17368)
-- Name: attr_category; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.attr_category AS ENUM (
    'physical',
    'on_court',
    'misc'
);


ALTER TYPE public.attr_category OWNER TO postgres;

--
-- TOC entry 903 (class 1247 OID 17418)
-- Name: board_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.board_t AS ENUM (
    'uga_roster',
    'pre_portal',
    'transfer_portal',
    'high_school',
    'watch_list'
);


ALTER TYPE public.board_t OWNER TO postgres;

--
-- TOC entry 891 (class 1247 OID 17376)
-- Name: comp_level; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.comp_level AS ENUM (
    'high_major_proven',
    'high_major',
    'mid_major',
    'low_major'
);


ALTER TYPE public.comp_level OWNER TO postgres;

--
-- TOC entry 915 (class 1247 OID 17462)
-- Name: comparator_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.comparator_t AS ENUM (
    'numeric_higher_better',
    'numeric_lower_better',
    'ordinal_1_5',
    'enum_label'
);


ALTER TYPE public.comparator_t OWNER TO postgres;

--
-- TOC entry 909 (class 1247 OID 17440)
-- Name: contract_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.contract_status AS ENUM (
    'draft',
    'offered',
    'executed',
    'expired',
    'terminated'
);


ALTER TYPE public.contract_status OWNER TO postgres;

--
-- TOC entry 906 (class 1247 OID 17430)
-- Name: funding_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.funding_t AS ENUM (
    'rev_share',
    'alt_funding',
    'apparel',
    'misc_benefit'
);


ALTER TYPE public.funding_t OWNER TO postgres;

--
-- TOC entry 999 (class 1247 OID 18040)
-- Name: game_type_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.game_type_t AS ENUM (
    'STD',
    'TRNMNT'
);


ALTER TYPE public.game_type_t OWNER TO postgres;

--
-- TOC entry 912 (class 1247 OID 17452)
-- Name: job_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.job_status AS ENUM (
    'running',
    'ok',
    'failed',
    'partial'
);


ALTER TYPE public.job_status OWNER TO postgres;

--
-- TOC entry 894 (class 1247 OID 17386)
-- Name: provenance_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.provenance_t AS ENUM (
    'measured',
    'estimated',
    'listed',
    'stale'
);


ALTER TYPE public.provenance_t OWNER TO postgres;

--
-- TOC entry 897 (class 1247 OID 17396)
-- Name: role_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.role_t AS ENUM (
    'gm',
    'coach',
    'analyst',
    'admin'
);


ALTER TYPE public.role_t OWNER TO postgres;

--
-- TOC entry 900 (class 1247 OID 17406)
-- Name: roster_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roster_status AS ENUM (
    'active',
    'committed',
    'target',
    'departed',
    'drafted'
);


ALTER TYPE public.roster_status OWNER TO postgres;

--
-- TOC entry 996 (class 1247 OID 18032)
-- Name: season_type_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.season_type_t AS ENUM (
    'preseason',
    'regular',
    'postseason'
);


ALTER TYPE public.season_type_t OWNER TO postgres;

--
-- TOC entry 882 (class 1247 OID 17350)
-- Name: tier_t; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tier_t AS ENUM (
    'DG',
    'LG',
    'Y',
    'R'
);


ALTER TYPE public.tier_t OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 240 (class 1259 OID 17783)
-- Name: agent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agent (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    agency text,
    contact_email text,
    phone text
);


ALTER TABLE public.agent OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17524)
-- Name: archetype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.archetype (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    group_name public.arch_group NOT NULL,
    okg_attribute_key text NOT NULL,
    version integer DEFAULT 1 NOT NULL,
    effective_from date DEFAULT CURRENT_DATE NOT NULL
);


ALTER TABLE public.archetype OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 17541)
-- Name: archetype_attribute; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.archetype_attribute (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    archetype_id uuid NOT NULL,
    attribute_key text NOT NULL,
    label text NOT NULL,
    category public.attr_category NOT NULL,
    comparator_type public.comparator_t NOT NULL,
    is_okg boolean DEFAULT false NOT NULL,
    display_order smallint NOT NULL
);


ALTER TABLE public.archetype_attribute OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 17641)
-- Name: attribute_grade; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attribute_grade (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    grade_run_id uuid NOT NULL,
    attribute_id uuid NOT NULL,
    observation_id uuid,
    scouting_score_id uuid,
    raw_value text,
    tier public.tier_t,
    matched_band_id uuid,
    CONSTRAINT attribute_grade_check CHECK ((num_nonnulls(observation_id, scouting_score_id) <= 1))
);


ALTER TABLE public.attribute_grade OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17835)
-- Name: audit_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_log (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    actor_id uuid,
    action text NOT NULL,
    entity_type text NOT NULL,
    entity_id uuid,
    before jsonb,
    after jsonb,
    at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.audit_log OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 17574)
-- Name: band; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.band (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    band_set_id uuid NOT NULL,
    attribute_id uuid NOT NULL,
    tier public.tier_t NOT NULL,
    min_value numeric,
    max_value numeric,
    enum_label text,
    ordinal_min smallint,
    ordinal_max smallint,
    eval_order smallint NOT NULL
);


ALTER TABLE public.band OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17558)
-- Name: band_set; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.band_set (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    scope text DEFAULT 'power_four'::text NOT NULL,
    version integer DEFAULT 1 NOT NULL,
    authored_by text,
    ratified_by text,
    effective_from date DEFAULT CURRENT_DATE NOT NULL,
    notes text
);


ALTER TABLE public.band_set OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17754)
-- Name: board; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.board (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    board_type public.board_t NOT NULL,
    season text,
    created_by uuid,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.board OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 17770)
-- Name: board_entry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.board_entry (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    board_id uuid NOT NULL,
    player_id uuid NOT NULL,
    rank smallint,
    tag text,
    note text,
    added_by uuid,
    added_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.board_entry OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 17653)
-- Name: calibration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calibration (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    dollar_multiplier numeric,
    iow_scale text,
    source_note text,
    sample_size integer,
    version integer DEFAULT 1 NOT NULL,
    effective_from date DEFAULT CURRENT_DATE NOT NULL,
    is_placeholder boolean DEFAULT true NOT NULL
);


ALTER TABLE public.calibration OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 17793)
-- Name: contract; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contract (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_id uuid NOT NULL,
    agent_id uuid,
    season_start text NOT NULL,
    season_end text,
    total_value numeric,
    funding_type public.funding_t,
    has_nba_optout boolean DEFAULT false NOT NULL,
    stepdown_pct numeric(5,2),
    buyout_terms text,
    prepayment numeric,
    status public.contract_status DEFAULT 'draft'::public.contract_status NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.contract OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 17810)
-- Name: contract_term; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contract_term (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    contract_id uuid NOT NULL,
    season text NOT NULL,
    base_value numeric,
    rev_share numeric,
    nil_value numeric,
    apparel numeric,
    misc_benefits numeric
);


ALTER TABLE public.contract_term OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 18070)
-- Name: game; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    vendor text DEFAULT 'cbbd'::text NOT NULL,
    vendor_event_id text NOT NULL,
    season smallint NOT NULL,
    season_label text NOT NULL,
    season_type public.season_type_t NOT NULL,
    game_type public.game_type_t,
    tournament text,
    start_date timestamp with time zone,
    game_date date NOT NULL,
    neutral_site boolean DEFAULT false NOT NULL,
    conference_game boolean,
    game_minutes smallint,
    CONSTRAINT game_game_minutes_check CHECK (((game_minutes IS NULL) OR ((game_minutes >= 40) AND (((game_minutes)::integer % 5) = 0))))
);


ALTER TABLE public.game OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 18092)
-- Name: game_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_team (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    game_id uuid NOT NULL,
    team_id uuid NOT NULL,
    opponent_id uuid NOT NULL,
    is_home boolean NOT NULL,
    team_seed smallint,
    opponent_seed smallint,
    team_game_number smallint,
    days_rest smallint,
    team_score smallint NOT NULL,
    opp_score smallint NOT NULL,
    result text GENERATED ALWAYS AS (
CASE
    WHEN (team_score > opp_score) THEN 'W'::text
    ELSE 'L'::text
END) STORED,
    team_minutes smallint,
    team_pace numeric(5,2),
    team_possessions smallint,
    team_fga smallint,
    team_fta smallint,
    team_turnovers smallint,
    team_total_reb smallint,
    team_off_reb smallint,
    team_def_reb smallint,
    opp_total_reb smallint,
    team_rating numeric(6,2),
    opp_rating numeric(6,2),
    CONSTRAINT game_team_check CHECK ((team_id <> opponent_id)),
    CONSTRAINT game_team_check1 CHECK (((team_off_reb IS NULL) OR (team_def_reb IS NULL) OR (team_total_reb IS NULL) OR (team_total_reb = (team_off_reb + team_def_reb)))),
    CONSTRAINT game_team_days_rest_check CHECK (((days_rest IS NULL) OR (days_rest >= 0))),
    CONSTRAINT game_team_team_minutes_check CHECK (((team_minutes IS NULL) OR ((team_minutes >= 200) AND (((team_minutes)::integer % 25) = 0))))
);


ALTER TABLE public.game_team OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17619)
-- Name: grade_run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grade_run (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_season_id uuid NOT NULL,
    archetype_id uuid NOT NULL,
    band_set_id uuid NOT NULL,
    algo_version text NOT NULL,
    aggregation_method text DEFAULT 'unweighted_mean'::text NOT NULL,
    overall_tier public.tier_t,
    mean_score numeric(4,2),
    spread numeric(4,2),
    graded_count smallint NOT NULL,
    total_count smallint DEFAULT 15 NOT NULL,
    is_override boolean DEFAULT false NOT NULL,
    created_by uuid,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.grade_run OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 17821)
-- Name: job_run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_run (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    connector text NOT NULL,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    finished_at timestamp with time zone,
    status public.job_status DEFAULT 'running'::public.job_status NOT NULL,
    records_in integer,
    records_written integer,
    snapshot_uri text,
    error text
);


ALTER TABLE public.job_run OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 17669)
-- Name: market_benchmark; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.market_benchmark (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    archetype_id uuid NOT NULL,
    tier public.tier_t NOT NULL,
    competition_bucket public.comp_level,
    role_bucket text,
    conference_filter text,
    value_low numeric,
    value_mid numeric,
    value_high numeric,
    sample_size integer,
    source text,
    as_of date
);


ALTER TABLE public.market_benchmark OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17587)
-- Name: observation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.observation (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_season_id uuid NOT NULL,
    metric_key text NOT NULL,
    value_num numeric,
    value_text text,
    provenance public.provenance_t NOT NULL,
    source_vendor text NOT NULL,
    usage_scope text[] DEFAULT '{internal}'::text[] NOT NULL,
    observed_at date,
    ingested_at timestamp with time zone DEFAULT now() NOT NULL,
    raw_snapshot_uri text
);


ALTER TABLE public.observation OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17471)
-- Name: player; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    full_name text NOT NULL,
    birth_date date,
    class_year smallint,
    primary_position text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    first_name text,
    last_name text,
    birth_city text,
    birth_state text,
    birth_country text,
    hometown_city text,
    hometown_state text,
    hometown_country text,
    hometown_lat numeric(8,5),
    hometown_lon numeric(9,5),
    start_season smallint,
    end_season smallint
);


ALTER TABLE public.player OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 18130)
-- Name: player_game; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player_game (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_season_id uuid NOT NULL,
    game_team_id uuid NOT NULL,
    starter boolean DEFAULT false NOT NULL,
    did_not_play boolean DEFAULT false NOT NULL,
    ejected boolean DEFAULT false NOT NULL,
    minutes smallint,
    points smallint,
    fgm smallint,
    fga smallint,
    tpm smallint,
    tpa smallint,
    ftm smallint,
    fta smallint,
    two_made smallint GENERATED ALWAYS AS ((fgm - tpm)) STORED,
    two_att smallint GENERATED ALWAYS AS ((fga - tpa)) STORED,
    offensive_reb smallint,
    defensive_reb smallint,
    total_reb smallint GENERATED ALWAYS AS ((offensive_reb + defensive_reb)) STORED,
    assists smallint,
    turnovers smallint,
    steals smallint,
    blocks smallint,
    fouls smallint,
    CONSTRAINT player_game_check CHECK ((NOT (did_not_play AND starter))),
    CONSTRAINT player_game_check1 CHECK ((num_nulls(minutes, points, fgm, fga, tpm, tpa, ftm, fta, offensive_reb, defensive_reb, assists, turnovers, steals, blocks, fouls) =
CASE
    WHEN did_not_play THEN 15
    ELSE 0
END)),
    CONSTRAINT player_game_check2 CHECK ((did_not_play OR ((fgm <= fga) AND (tpm <= tpa) AND (ftm <= fta) AND (tpa <= fga)))),
    CONSTRAINT player_game_check3 CHECK ((did_not_play OR (points = (((2 * (fgm - tpm)) + (3 * tpm)) + ftm)))),
    CONSTRAINT player_game_minutes_check CHECK (((minutes IS NULL) OR ((minutes >= 0) AND (minutes <= 75))))
);


ALTER TABLE public.player_game OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 18165)
-- Name: player_game_metric; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player_game_metric (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_game_id uuid NOT NULL,
    points_per40 numeric(8,4),
    points_per40_tier public.tier_t,
    ts_pct numeric(6,2),
    ts_pct_tier public.tier_t,
    three_pt_pct numeric(6,2),
    three_pt_pct_tier public.tier_t,
    ft_rate numeric(6,2),
    ft_rate_tier public.tier_t,
    usage_pct numeric(6,2),
    usage_pct_tier public.tier_t,
    ast_per_tov numeric(6,2),
    ast_per_tov_tier public.tier_t,
    trb_pct numeric(8,4),
    trb_pct_tier public.tier_t,
    stocks_per40 numeric(8,4),
    stocks_per40_tier public.tier_t,
    fg_pct numeric(6,2),
    two_pct numeric(6,2),
    ft_pct numeric(6,2),
    efg_pct numeric(6,2),
    oreb_pct numeric(6,2),
    off_rating numeric(6,2),
    def_rating numeric(6,2),
    net_rating numeric(6,2),
    game_score numeric(6,2),
    rate_reliable boolean,
    CONSTRAINT player_game_metric_check CHECK ((((points_per40 IS NULL) = (points_per40_tier IS NULL)) AND ((ts_pct IS NULL) = (ts_pct_tier IS NULL)) AND ((three_pt_pct IS NULL) = (three_pt_pct_tier IS NULL)) AND ((ft_rate IS NULL) = (ft_rate_tier IS NULL)) AND ((usage_pct IS NULL) = (usage_pct_tier IS NULL)) AND ((ast_per_tov IS NULL) = (ast_per_tov_tier IS NULL)) AND ((trb_pct IS NULL) = (trb_pct_tier IS NULL)) AND ((stocks_per40 IS NULL) = (stocks_per40_tier IS NULL))))
);


ALTER TABLE public.player_game_metric OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17513)
-- Name: player_season; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player_season (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_id uuid NOT NULL,
    team_id uuid,
    season text NOT NULL,
    games_played smallint,
    minutes_pct numeric(5,2),
    possessions integer,
    competition_faced public.comp_level,
    jersey smallint,
    season_in_program smallint
);


ALTER TABLE public.player_season OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17483)
-- Name: player_source_ref; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.player_source_ref (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_id uuid NOT NULL,
    vendor text NOT NULL,
    vendor_player_id text NOT NULL,
    confidence numeric(4,3) DEFAULT 1 NOT NULL,
    resolved_by text DEFAULT 'auto'::text NOT NULL,
    resolved_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.player_source_ref OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17725)
-- Name: role_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_permission (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    role public.role_t NOT NULL,
    resource text NOT NULL,
    field_path text NOT NULL,
    can_read boolean DEFAULT false NOT NULL,
    can_write boolean DEFAULT false NOT NULL
);


ALTER TABLE public.role_permission OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 17741)
-- Name: roster_membership; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roster_membership (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_id uuid NOT NULL,
    team_id uuid NOT NULL,
    season text NOT NULL,
    status public.roster_status NOT NULL,
    eligibility_left smallint,
    joined_at date,
    departed_at date
);


ALTER TABLE public.roster_membership OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 17680)
-- Name: scarcity_rule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scarcity_rule (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    archetype_id uuid,
    tier public.tier_t,
    condition_expr text,
    multiplier numeric,
    authored_by text,
    effective_from date DEFAULT CURRENT_DATE NOT NULL
);


ALTER TABLE public.scarcity_rule OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 17604)
-- Name: scouting_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scouting_score (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_season_id uuid NOT NULL,
    attribute_id uuid NOT NULL,
    tier public.tier_t,
    ordinal smallint,
    enum_label text,
    evaluator_id uuid NOT NULL,
    note text,
    submitted_at timestamp with time zone DEFAULT now() NOT NULL,
    superseded_by uuid,
    CONSTRAINT scouting_score_ordinal_check CHECK (((ordinal >= 1) AND (ordinal <= 5)))
);


ALTER TABLE public.scouting_score OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 17707)
-- Name: staff_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff_user (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email text NOT NULL,
    display_name text NOT NULL,
    role public.role_t NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.staff_user OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17501)
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL,
    conference text,
    level public.comp_level,
    is_uga boolean DEFAULT false NOT NULL
);


ALTER TABLE public.team OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 18045)
-- Name: team_source_ref; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team_source_ref (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    team_id uuid NOT NULL,
    vendor text NOT NULL,
    vendor_team_id text NOT NULL,
    confidence numeric(4,3) DEFAULT 1 NOT NULL,
    resolved_by text DEFAULT 'auto'::text NOT NULL,
    resolved_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.team_source_ref OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17691)
-- Name: valuation_run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.valuation_run (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    player_season_id uuid NOT NULL,
    grade_run_id uuid NOT NULL,
    calibration_id uuid NOT NULL,
    projected_minutes numeric,
    production_value numeric,
    impact_on_winning numeric,
    market_value_low numeric,
    market_value_mid numeric,
    market_value_high numeric,
    scarcity_mult numeric,
    derivation jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.valuation_run OWNER TO postgres;

--
-- TOC entry 5412 (class 0 OID 17783)
-- Dependencies: 240
-- Data for Name: agent; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 5395 (class 0 OID 17524)
-- Dependencies: 223
-- Data for Name: archetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.archetype VALUES
	('8cb2307d-9367-5565-99c8-15885bec98ae', 'combo_guard', 'Combo Guard', 'guard', 'ts_pct', 1, '2026-09-26'),
	('279f1f45-d0f8-5406-852a-79633f5cec33', 'floor_general', 'Floor General', 'guard', 'ts_pct', 1, '2026-09-26'),
	('aeabec0d-9a75-5e5e-b8ee-73e1fefea12e', 'guard', 'Guard', 'guard', 'ts_pct', 1, '2026-09-26'),
	('9b90d4b6-65ea-5fa7-bc1e-0bf738ab0f51', 'traditional_big', 'Traditional Big', 'big', 'ts_pct', 1, '2026-09-26'),
	('64a55e93-5887-54fd-adc2-62c754f41cab', 'traditional_forward', 'Traditional Forward', 'big', 'ts_pct', 1, '2026-09-26'),
	('3fe55dad-6d31-5f09-85dd-309000717558', 'wing', 'Wing', 'wing', 'ts_pct', 1, '2026-09-26') ON CONFLICT DO NOTHING;


--
-- TOC entry 5396 (class 0 OID 17541)
-- Dependencies: 224
-- Data for Name: archetype_attribute; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.archetype_attribute VALUES
	('71969361-db91-5055-a8b5-f0f3da94d8ed', '8cb2307d-9367-5565-99c8-15885bec98ae', 'height_in', 'Height', 'physical', 'numeric_higher_better', false, 0),
	('9b3c8b71-99a4-54b3-9c5e-6407f63c00f5', '8cb2307d-9367-5565-99c8-15885bec98ae', 'weight_lb', 'Weight', 'physical', 'numeric_higher_better', false, 1),
	('bf4fa778-1dd7-51bd-8668-32e0b8808066', '279f1f45-d0f8-5406-852a-79633f5cec33', 'height_in', 'Height', 'physical', 'numeric_higher_better', false, 0),
	('9130b146-1bd3-5c1c-9212-988af2e7446e', '279f1f45-d0f8-5406-852a-79633f5cec33', 'weight_lb', 'Weight', 'physical', 'numeric_higher_better', false, 1),
	('13b71f82-37ae-5198-ac5d-683ac4707910', 'aeabec0d-9a75-5e5e-b8ee-73e1fefea12e', 'height_in', 'Height', 'physical', 'numeric_higher_better', false, 0),
	('be9fe335-05a5-5821-9138-89a2102c2844', 'aeabec0d-9a75-5e5e-b8ee-73e1fefea12e', 'weight_lb', 'Weight', 'physical', 'numeric_higher_better', false, 1),
	('c595f8a5-ddf9-585c-b137-b73b833da085', '9b90d4b6-65ea-5fa7-bc1e-0bf738ab0f51', 'height_in', 'Height', 'physical', 'numeric_higher_better', false, 0),
	('6ff5b127-7ffa-5fcc-82c1-28428f721d25', '9b90d4b6-65ea-5fa7-bc1e-0bf738ab0f51', 'weight_lb', 'Weight', 'physical', 'numeric_higher_better', false, 1),
	('2d707fd1-8403-55d2-88eb-a5f93467bd7f', '64a55e93-5887-54fd-adc2-62c754f41cab', 'height_in', 'Height', 'physical', 'numeric_higher_better', false, 0),
	('6c768351-6b80-5034-87e5-0d6da7a759ea', '64a55e93-5887-54fd-adc2-62c754f41cab', 'weight_lb', 'Weight', 'physical', 'numeric_higher_better', false, 1),
	('1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', '3fe55dad-6d31-5f09-85dd-309000717558', 'height_in', 'Height', 'physical', 'numeric_higher_better', false, 0),
	('58a18bb2-5040-5660-8e4b-3bdebfef0d1a', '3fe55dad-6d31-5f09-85dd-309000717558', 'weight_lb', 'Weight', 'physical', 'numeric_higher_better', false, 1) ON CONFLICT DO NOTHING;


--
-- TOC entry 5402 (class 0 OID 17641)
-- Dependencies: 230
-- Data for Name: attribute_grade; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.attribute_grade VALUES
	('4e540759-c007-5b81-ae62-e7c5c7a3ddd1', 'd2a95863-d7f3-553e-be25-c66c9131e4bb', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('08ef3224-977b-560c-b61c-8cf4f4058611', 'd2a95863-d7f3-553e-be25-c66c9131e4bb', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('89105bfc-07de-5f1d-b3c2-c64bc5115eeb', '38c4458c-08b8-5239-99e4-0601cb0c177d', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('c504e50b-3b22-5ed8-a26f-1edc948f0c41', '38c4458c-08b8-5239-99e4-0601cb0c177d', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('6eb048f2-4134-5f64-b54e-13a686c8d52d', 'e56b2d97-0f57-50b0-be25-9d591551145c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('0259e3f7-25f1-52fa-9084-a3432e98a49f', 'e56b2d97-0f57-50b0-be25-9d591551145c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('7247eebe-1380-5d39-b6c8-ede2511908af', 'a557f372-28ff-5666-a3dc-7777b2944f8b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('cf634f17-4cc1-5141-80a7-363077db44db', 'a557f372-28ff-5666-a3dc-7777b2944f8b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '227.0', 'DG', NULL),
	('a56c61a7-31d1-5ad1-9708-cb0d1aad78b7', 'f818f21c-358c-5741-be32-a4ded583b5c6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('0ed1dac5-90e6-5fba-b84a-5d4ece0c52b8', 'f818f21c-358c-5741-be32-a4ded583b5c6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('8f12bf80-5d5b-5e98-8e2c-bde826885d6a', '20b7d566-1ca9-55f1-a5a3-8e217c0fb799', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('461f0b32-826c-5625-8245-3199bf136a68', '20b7d566-1ca9-55f1-a5a3-8e217c0fb799', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '250.0', 'DG', NULL),
	('c1d8f922-51b9-50ab-96dd-5a3b97387022', 'a9db6acb-ab34-5a50-a6e2-c5d048b540aa', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('1689b392-1853-5516-bfd8-82e1d1cc5098', 'a9db6acb-ab34-5a50-a6e2-c5d048b540aa', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '240.0', 'LG', NULL),
	('c3e925d3-f8f7-5411-a0fd-1aa9ec5be12d', '07bb21ed-80d5-5a12-9add-e3fa5cd3929a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('53346e26-0b41-5e2d-87bb-be69262c3bf7', '07bb21ed-80d5-5a12-9add-e3fa5cd3929a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('9d222d8a-af11-5f76-9825-4646ef6b831a', 'cb0fc30e-1b17-5d4b-850e-2f157f6d652f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('51c265b5-246e-5a0f-95d8-5a787f3a02d0', 'cb0fc30e-1b17-5d4b-850e-2f157f6d652f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '224.0', 'DG', NULL),
	('5a005a67-a245-565d-ad7d-76d0dd139ec3', '122f0321-09e4-5f99-89bf-bd8bafc4a82a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('1d6fd5be-3e16-5a91-8cbf-69ba1e1f3678', '122f0321-09e4-5f99-89bf-bd8bafc4a82a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('02546d1c-d42d-5961-b059-1b3cc42e77a2', 'c3a4dd53-2757-57a4-a87d-d86943e139ac', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('3496e629-3242-51a5-92cd-eed72910f8ae', 'c3a4dd53-2757-57a4-a87d-d86943e139ac', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('662d2ecc-5650-5a14-9aa1-5bcb519dff13', '6a411895-f71f-51c3-a8ca-42e127117d96', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('b5ed0215-5d54-56b3-a6c8-43711e47f9cb', '6a411895-f71f-51c3-a8ca-42e127117d96', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('02b1f42c-8bf2-5481-9056-b9276d73dfd0', 'aa3be8ac-8056-5616-bcc3-9f1d1a2bd223', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('2ec31c6f-cbe3-504b-8320-9fbfaecb766a', 'aa3be8ac-8056-5616-bcc3-9f1d1a2bd223', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '216.0', 'DG', NULL),
	('286c7c3a-9d54-5290-b141-01931f2bfcfd', '817da438-b745-5cb3-ba08-681de26a8376', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('c36c729d-51ce-5467-b4ae-c3a66183a337', '817da438-b745-5cb3-ba08-681de26a8376', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('bbc103bd-0ad0-5b18-b6ed-1b4736a776b6', 'd1633a01-a665-59ab-ae08-60d8b5ef7fec', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '84.0', 'DG', NULL),
	('529d26b2-6778-5f67-8bcd-8a1c22ef7e96', 'd1633a01-a665-59ab-ae08-60d8b5ef7fec', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '259.0', 'DG', NULL),
	('f8796a09-67e1-53dd-bc5e-3db78c959f21', '5009a21c-0b3f-5fef-8b1e-9f4a5ea6424c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('1a919790-f88c-55f0-9b70-b2bd6ec5ced5', '5009a21c-0b3f-5fef-8b1e-9f4a5ea6424c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('9f6936d4-54f4-52fe-8e7c-eb1785b31918', '6b15e4e5-8717-5219-9bcd-f41e69c817e4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('b67a3469-1042-5c2c-a07b-7a5dd1d0cf72', '6b15e4e5-8717-5219-9bcd-f41e69c817e4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '219.0', 'DG', NULL),
	('dc398a3a-c918-5882-a157-b5305c105f55', '0ac50c7a-4e26-586a-a957-6cbb27d5f17f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('aeba9cf6-5506-5695-9aca-67b49879f9cb', '0ac50c7a-4e26-586a-a957-6cbb27d5f17f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('06ae4607-d0df-57b0-903f-138a55a38007', '011cde4a-e63e-56eb-8635-fd361bdd3806', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '81.0', 'DG', NULL),
	('bd3d1873-47e5-568b-9ba2-5269b6460798', '011cde4a-e63e-56eb-8635-fd361bdd3806', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('1d7e6ca3-dc12-5318-b8f8-d9c946b16444', 'ac7a2a31-2555-5bc7-afb4-40c9c9a98074', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('7f9301f8-b250-586e-bb88-89077623a6e1', 'ac7a2a31-2555-5bc7-afb4-40c9c9a98074', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('8d34246f-b7a9-54f5-ae6e-fd2aae860b56', '6a5ea2db-dc2b-5c99-ae15-716ffa933b11', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('17236dfd-7238-5637-bd8c-b51489d28295', '6a5ea2db-dc2b-5c99-ae15-716ffa933b11', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '209.0', 'DG', NULL),
	('8198240f-6ccd-5018-b7b6-69419fd360d4', '43441ef6-3305-589c-97eb-133086226f1e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('9d931bda-65e0-5035-8732-7ffb518fc27e', '43441ef6-3305-589c-97eb-133086226f1e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '218.0', 'DG', NULL),
	('3dd213cb-db49-5f2f-a372-19fb68a13cde', 'b1f3adea-0057-5df7-bd14-e6d9073a1af7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('6108ff5f-8781-5c24-bd9d-e6655dd1fa5a', 'b1f3adea-0057-5df7-bd14-e6d9073a1af7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('e5e7b1e5-587d-587b-bbd0-fea357a73d92', '36237266-42cc-5c60-a84b-71a405158a6e', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '81.0', 'LG', NULL),
	('dceebd1c-9d14-53b7-81be-9f1003eaf826', '36237266-42cc-5c60-a84b-71a405158a6e', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '255.0', 'DG', NULL),
	('e1a36c8e-0ecd-5313-85ee-806c6b57b163', 'e4dbff65-94ea-57c8-834f-f5592c74ad7f', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('2a10c190-42b7-5602-b6a4-412c72cefbea', 'e4dbff65-94ea-57c8-834f-f5592c74ad7f', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '257.0', 'DG', NULL),
	('b7062075-44c9-5f61-a9a9-49361b34cd97', '6a48c1f1-9f9b-5af6-a36c-a98e1453d815', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('b5542af4-9486-583a-8f40-d0dfe3b46af8', '6a48c1f1-9f9b-5af6-a36c-a98e1453d815', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('1f3ce375-d002-5cb5-8f72-fdb858f5e2f8', '4fbe48dd-e36c-5088-bbe4-144cedcb1c7a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('b4288774-2097-5e97-89f7-02e7152d0024', '4fbe48dd-e36c-5088-bbe4-144cedcb1c7a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '220.0', 'DG', NULL),
	('12b1216e-661f-58ad-9694-691b1b6567f6', '8a4b0ecd-9695-5732-9bed-66df948817b1', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('82fc4a2d-b943-5ce9-a1d7-4329c5bf6af8', '8a4b0ecd-9695-5732-9bed-66df948817b1', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('fd93db1e-a789-5f22-9355-a16fce5fc253', '8aa08451-59e3-5241-ace6-0e2d0c4f404b', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('e5a69e43-f6ac-5522-8bef-5296a9dedc9f', '8aa08451-59e3-5241-ace6-0e2d0c4f404b', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '255.0', 'DG', NULL),
	('ffdf41e0-99ff-5ad6-9923-780e59cd15a8', 'f1c07ff5-63ed-5ea8-a71f-a4c3ed82a56d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('fb0e84b7-b29f-5a67-85f1-b29653d00796', 'f1c07ff5-63ed-5ea8-a71f-a4c3ed82a56d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('712a3f02-be5e-52d7-a9c6-009fd878da8b', '4f56d7f2-11d0-5e0b-9cb7-e3e2345561fa', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('2320fce2-1676-5e5c-bceb-387157e50f50', '4f56d7f2-11d0-5e0b-9cb7-e3e2345561fa', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('9ff543ac-906f-56e0-b0c5-4e097ffa629b', '924b936f-a1bd-5e7b-b054-6a5f5ec238f9', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '81.0', 'LG', NULL),
	('daa955c4-7d28-5a7d-824b-c8da5767a8c4', '924b936f-a1bd-5e7b-b054-6a5f5ec238f9', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '205.0', 'R', NULL),
	('ccf54060-5f21-5650-bab9-aea5977484d8', '2fd6779f-67bc-52c0-86f9-57bb0696accc', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('93e8a9df-f73d-5c53-a517-8da335c77983', '2fd6779f-67bc-52c0-86f9-57bb0696accc', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('27d4814c-e7d6-5b52-8470-6380c7b4c394', '32b7f4e8-2edf-5581-85e6-81db08a73c86', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('ed80c904-5410-5288-933a-9315cd0711eb', '32b7f4e8-2edf-5581-85e6-81db08a73c86', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('cf86403d-e887-5697-845a-c91349ac74c1', 'f7414379-41b8-5fd8-b1f0-71913069b1b7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('c835582a-8b43-53ea-ae65-4d3d86952a2b', 'f7414379-41b8-5fd8-b1f0-71913069b1b7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('02a68d2d-5152-53f6-a0ca-b50ac60638f5', '0020fa47-3d3e-5597-8654-cf479f7acebf', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('741056a4-3428-5871-a578-a778b91379a6', '0020fa47-3d3e-5597-8654-cf479f7acebf', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('5c4c47e2-330d-5e0b-97ca-13ff3ea22ccf', '3c1742ec-4ed3-58bf-a1db-e5f1d6c609a5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('a713ada8-07ce-5972-93ca-a325f89da324', '3c1742ec-4ed3-58bf-a1db-e5f1d6c609a5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('6231deaa-76e9-5a8f-a7fe-0a995e2c1017', '8bb65614-ce6a-51d7-a1f2-9bca9cb49f94', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('9dbea07a-56ef-54a9-b32a-3a45637ca685', '8bb65614-ce6a-51d7-a1f2-9bca9cb49f94', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('d1e88649-a9ce-534e-9847-633e57031126', '0dd44f4f-cd84-5a9e-aade-d317b86c5c5b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('296d7af6-9561-538b-8a5b-6cbbc9a13bc9', '0dd44f4f-cd84-5a9e-aade-d317b86c5c5b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '270.0', 'DG', NULL),
	('4819ccab-1be4-5d96-8882-d7cd1be69df2', '6217fe9b-12d8-5066-be09-23eeda1344fd', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('179a7421-19b0-5fae-b18a-20f5639620dd', '6217fe9b-12d8-5066-be09-23eeda1344fd', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('abf52b7e-b341-5ac2-827d-5f831be022e6', 'cdd85d32-0d06-5342-9a5d-d76c18810605', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('5cdc2d56-f683-52f1-936e-17f529a24680', 'cdd85d32-0d06-5342-9a5d-d76c18810605', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('cff4e31a-c1a0-5beb-8e64-ba8a99ead678', '6ef9cc7f-2e22-5675-9790-d1f0497e1ba8', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '70.0', 'R', NULL),
	('d33ace44-da1e-5a5a-bd22-6819b9f4d056', '6ef9cc7f-2e22-5675-9790-d1f0497e1ba8', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('30476953-3439-53b7-9908-47d6c6cd5694', '3b96a087-2638-555f-a76e-45577c8adf49', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '80.0', 'DG', NULL),
	('8c609570-997f-529a-a280-7437faca0f9a', '3b96a087-2638-555f-a76e-45577c8adf49', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('f3d69d5a-09f4-5410-bedf-8aea1d7b575c', '48adf641-6363-5dc8-b403-0558dd95e2f5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('e1ba03e3-6dbf-510d-ad47-2e4f5156c0dd', '48adf641-6363-5dc8-b403-0558dd95e2f5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('2c9474f4-cb1a-5002-bad3-da170672226b', '58653070-1bd7-52ac-8c7b-4a1aa03eb9d6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('5355f592-c30e-536e-b32c-613ecc12da80', '58653070-1bd7-52ac-8c7b-4a1aa03eb9d6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '160.0', 'R', NULL),
	('41155a20-0969-5f05-8b4d-dc1c9f265f6a', 'b5f96235-46ed-58fc-b598-7a93d6663030', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('113fd455-dcd9-5b4c-98ec-f134068e3d3c', 'b5f96235-46ed-58fc-b598-7a93d6663030', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '250.0', 'DG', NULL),
	('79b5a98f-4be5-554f-b36e-d35b5c5b53a3', '7cb98a2b-a39d-5f93-b4ea-b62faa152592', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('31bf7a1b-30f6-5ac4-b857-cbe404e2fa3b', '7cb98a2b-a39d-5f93-b4ea-b62faa152592', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('579798aa-ec13-5ec5-b5ae-81f67fff68e1', '59dc8e39-50c9-5a45-95c6-04b5e2d7e956', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('550daa04-0558-571c-a4e8-131bab2e6da8', '59dc8e39-50c9-5a45-95c6-04b5e2d7e956', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('188b9286-77e8-5c4a-adad-4794e9bc8efe', 'c7d27bf4-b909-5116-9ace-c03ab9b5a271', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('1ce96ec9-f6df-5037-94c6-747ceeac80eb', 'c7d27bf4-b909-5116-9ace-c03ab9b5a271', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('4526b063-47ab-54dd-be34-423dce4ba923', '805a2e87-7281-5818-b843-3b557e3c3edd', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '85.0', 'DG', NULL),
	('6bf7e6b8-d9ba-5d2c-a3d1-50e5f5aee511', '805a2e87-7281-5818-b843-3b557e3c3edd', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('91b94f37-ab9b-5081-8a5c-303bc49a82f8', '8da1345e-12b3-59a1-bb94-7bf93312a85e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('ed93eb0c-b216-5793-a81e-2a784f6e32f9', '8da1345e-12b3-59a1-bb94-7bf93312a85e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('811a6337-19d7-5a76-a786-e6c1ef4459f9', 'd3b67195-54cb-54b0-b59c-2faad236cbe1', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '85.0', 'DG', NULL),
	('5e9f2e92-2b2e-5dc0-994c-7cdbad3545bc', 'd3b67195-54cb-54b0-b59c-2faad236cbe1', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '285.0', 'DG', NULL),
	('271fe471-c329-53ac-a8db-7006c15d2a20', 'baa79651-1691-5e76-b605-5018d1847a83', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('28956bbb-3f42-5da6-b676-6141daf03c1d', 'baa79651-1691-5e76-b605-5018d1847a83', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('8f42b7a6-27a4-523e-9076-fef3dba6cbd4', 'd136c9ac-a228-51c6-b1fa-b1116e6b1194', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('f99c2e29-7493-5470-bc69-b0245be3828e', 'd136c9ac-a228-51c6-b1fa-b1116e6b1194', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('0b9e06ed-ff4b-52b4-996d-b006bfe8fcb1', '72a63b8b-eebc-5cdf-b0f8-1f891ce93cc2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('b0d5534f-c90e-56f8-bd69-6ea6a46be6d4', '72a63b8b-eebc-5cdf-b0f8-1f891ce93cc2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '182.0', 'Y', NULL),
	('82457e9c-2fbb-529e-a587-27dfaa8fc567', 'ac2b9fe5-1bbc-552b-a018-21e90e3c6177', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('fcf4c705-eb22-58f2-a111-449751d80c62', 'ac2b9fe5-1bbc-552b-a018-21e90e3c6177', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('528c9458-dd09-5198-bccf-9b37cc59914b', 'd5653c44-3f70-5d1b-9f06-4e8fa1d5699b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('cfa70161-7c12-5183-b524-15aec8cc3563', 'd5653c44-3f70-5d1b-9f06-4e8fa1d5699b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('9c1aabdf-f725-5eb0-a02e-aac8db4e2434', '37f4fe0b-ba46-5c40-8bd9-bd7a8a658d11', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('45edcb24-e3a1-55ab-b4d7-1a936a913fa1', '37f4fe0b-ba46-5c40-8bd9-bd7a8a658d11', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('f05ecc97-9393-5f68-acf0-2fb796136d82', '33ee22c5-5aff-5aab-bf81-559c27096dd6', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('f29c9432-f90a-5e34-b20b-2005b1f4a80a', '33ee22c5-5aff-5aab-bf81-559c27096dd6', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '228.0', 'DG', NULL),
	('471abcb5-6042-57ae-a947-52a22859d309', '141433eb-13e6-553a-82f8-35e15c65ca5a', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('2b584010-90b7-5897-b5a1-35ab281378d7', '141433eb-13e6-553a-82f8-35e15c65ca5a', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('f28bd1c2-2ba0-5442-8687-8f5b84c53e2c', '2fb4f035-74f8-5fb2-8258-1bdf7b44c591', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('beb91cbd-4131-5002-9712-db4046ee11e0', '2fb4f035-74f8-5fb2-8258-1bdf7b44c591', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('9ebf4667-1314-5bf8-828b-5dacb5649e70', 'c11afa19-3464-53fe-bc04-222508b03787', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('e49daf9f-96a1-51da-911c-e594b396e874', 'c11afa19-3464-53fe-bc04-222508b03787', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('7cb460eb-9848-5780-9a5c-47969978f2ec', '42707aee-3134-585b-bcef-61759be30b65', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('a646cb07-3bd5-5793-b3ae-13a64a63df88', '42707aee-3134-585b-bcef-61759be30b65', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('0cee2260-8cf6-5978-b76c-7694bede0281', '3e04b56c-e952-5e43-8c6a-6f564f2e3215', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('6ff767b9-61c2-5758-87ad-92394229a8e7', '3e04b56c-e952-5e43-8c6a-6f564f2e3215', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '201.0', 'Y', NULL),
	('56f6df15-0d94-582d-9f40-06fc705c128d', 'c8e24662-9841-5979-812f-85d5f17d78f9', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('bc99a698-660c-5316-89c3-4c0fcd1ec5fe', 'c8e24662-9841-5979-812f-85d5f17d78f9', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('9319548e-e666-557f-9ae8-ca120f86dc52', '47a0c8ab-f100-584c-823e-4b13ee8f4cb2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('43b3a796-16dd-50f6-8ce4-65c1ec0edfeb', '47a0c8ab-f100-584c-823e-4b13ee8f4cb2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('f088417f-c864-5d7a-9a63-079173a7868f', '6269e609-066c-5239-ae02-1e696c8f7fad', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('0254db68-69e8-52d8-aaac-16a7cd2495d9', '6269e609-066c-5239-ae02-1e696c8f7fad', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '240.0', 'DG', NULL),
	('00ccbc5f-6d61-5ec6-a38e-b03dd1c4ea69', 'da6031b8-4c3f-5a74-a144-687c880c2a28', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('5d6b1ad5-f503-5c9b-a9cb-84686eecd9c1', 'da6031b8-4c3f-5a74-a144-687c880c2a28', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('ab30cbeb-6869-5b03-a523-4ee5a465e83d', '7a77ca91-407d-52a0-b3b7-f354ec1542ed', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '84.0', 'DG', NULL),
	('81152246-d876-5a05-9818-bbfc1b979ee3', '7a77ca91-407d-52a0-b3b7-f354ec1542ed', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '240.0', 'LG', NULL),
	('d58fc992-d504-5999-90a6-e4d89950f1c9', '2b00d5c2-ce6c-51d5-8b9a-c8c1559923be', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('5d00b588-f1e8-5ccf-b1c2-5ea54d71e006', '2b00d5c2-ce6c-51d5-8b9a-c8c1559923be', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('f61cd715-aa9d-5e82-b8f0-184efe615fba', '2de296c4-8d81-5aba-a2cc-7abcba2f76a8', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('b8461468-4337-5a65-8375-5af5d05d776c', '2de296c4-8d81-5aba-a2cc-7abcba2f76a8', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('7584a0bf-a1c8-5bbe-aa81-0751075b7b5d', '1c0ab5ad-1405-58b7-b9f7-32b08fb9f4cc', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('89ecae06-43c1-5a88-bcaf-a6bb728df168', '1c0ab5ad-1405-58b7-b9f7-32b08fb9f4cc', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('d15b8ba7-5888-5e76-b04c-cdd8da05b07b', '0298ba85-6752-5f15-839b-c7fe56b9881d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('52745cd3-5aea-5ef3-be86-50b2252cd542', '0298ba85-6752-5f15-839b-c7fe56b9881d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('a0dcd0d8-24ec-53ce-a974-f50d1ec0d4e5', '0f877da2-5b0f-506e-a314-b99456c7e511', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('9de92e92-988a-5259-92e5-533f85c4ee8e', '0f877da2-5b0f-506e-a314-b99456c7e511', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('d5eab2ff-6431-5667-a822-98b0f55542c5', 'adf5a1f5-6d2e-5d93-81ee-bea365d93214', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('07d7e113-6fb9-51fe-9b60-4b10bf1147ad', 'adf5a1f5-6d2e-5d93-81ee-bea365d93214', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '250.0', 'DG', NULL),
	('07184ae7-5228-5d32-b690-983ec407f112', '8ec90b9b-ee09-56ba-91d8-6d45c6a193b6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('936c1bbe-9f24-5027-9a3c-dc6f6537030d', '8ec90b9b-ee09-56ba-91d8-6d45c6a193b6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '160.0', 'R', NULL),
	('a114a916-23c7-5e38-ab63-b4437a411b85', 'aaba3d66-b227-54c9-af3d-b73c5dc77824', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('0e172425-98c0-5207-aa93-06384b0cbb54', 'aaba3d66-b227-54c9-af3d-b73c5dc77824', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('1a606c9e-c736-52cd-95dc-071afa899cf5', 'c995acb9-e3cf-521e-89c5-9cfd32cc1765', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('0348edf8-6e3b-534a-9706-9b62ab96fd03', 'c995acb9-e3cf-521e-89c5-9cfd32cc1765', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('21a9e5f4-40a8-5e11-9bf9-d61156660594', 'aa162856-59d5-5fb7-a648-de5c55dfab33', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('61ffec6d-5c17-5024-96db-7226cd80604c', 'aa162856-59d5-5fb7-a648-de5c55dfab33', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '180.0', 'R', NULL),
	('9ea79328-2785-55dd-8ff4-d55c6b504f28', 'e477b534-031b-57dd-bc31-f533b189dfd4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('8739b627-dd78-5378-89d3-50b6dc88affe', 'e477b534-031b-57dd-bc31-f533b189dfd4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('b4719be4-23f0-5cd4-9103-283a4541312d', '3eedf21f-66d7-5d16-99de-ad8ce33c575f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('0917370b-460b-54d4-9f5a-b4cdada13906', '3eedf21f-66d7-5d16-99de-ad8ce33c575f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('fb6c5187-fa46-57bb-ae9c-758b4f9182a8', '9cfcc1bf-7b67-5090-a42a-4c31eb7f4f56', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('f03c29b9-2148-53a7-a5b6-fad3cfda48b5', '9cfcc1bf-7b67-5090-a42a-4c31eb7f4f56', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('745e460b-ac04-5cb3-9344-cd0caf71adf9', '018039b8-1e05-5f2d-8324-b96f6925fc0a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('b417f9d3-d62b-56a1-be56-8e9e6720411b', '018039b8-1e05-5f2d-8324-b96f6925fc0a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('24eb57ad-dcd4-5786-bf91-e8fdc50c652d', '56350743-e9ba-5bf3-abfd-35a404e1c183', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('5a8de8d9-a561-54ed-b08f-058b5bce4eef', '56350743-e9ba-5bf3-abfd-35a404e1c183', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('393182b4-58d2-592e-a33d-3925f656fe7c', '0ea12ca0-2e34-5e55-b0fd-c49ce321c388', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('1d6104ce-e539-55c7-91b7-376f4fbccd33', '0ea12ca0-2e34-5e55-b0fd-c49ce321c388', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('3b26b8a4-73f7-57fd-b4e4-943db15efed7', 'dd79cb27-722a-5eba-a2c9-30c6076ac2d3', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('02ec828b-f1ac-529a-8007-9e5b40c3d0bf', 'dd79cb27-722a-5eba-a2c9-30c6076ac2d3', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('d57be614-062b-5899-80ff-38fdfb78d951', '5caf3b60-bbab-5331-9f3e-1350427ab435', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('e28d5c9a-c8ff-59a2-b716-311eee575261', '5caf3b60-bbab-5331-9f3e-1350427ab435', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '204.0', 'Y', NULL),
	('c7737cc0-ea55-5bfb-8d41-54a9f1e5ea9e', 'ca519969-4f99-5fb2-8a2a-369e55d4833a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('51fe0556-7b4f-5713-9538-dca9c950c559', 'ca519969-4f99-5fb2-8a2a-369e55d4833a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('cfee2f45-a2bb-5f7b-b42e-37463300fef7', '053b8fd4-dfb9-5f26-930b-79dcd6e04e3c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('b5946fb6-f770-505d-b4e8-e6dcda6c6fcd', '053b8fd4-dfb9-5f26-930b-79dcd6e04e3c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('d7fc01f7-4a5d-5429-aaf8-ff8dd6e07a65', '05b554be-82bd-5fff-b0c2-d707433736ea', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('4918e2bf-f699-582f-aed7-f1b74788dac9', '05b554be-82bd-5fff-b0c2-d707433736ea', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('a6c10c20-2b78-5edd-9bd4-dd46d2384b97', '81a5cae1-c3cf-588e-90ca-c8f6ab33b042', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '81.0', 'LG', NULL),
	('46d269d4-2815-5a2d-bc2c-edf99343d42e', '81a5cae1-c3cf-588e-90ca-c8f6ab33b042', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '233.0', 'Y', NULL),
	('cd39bffb-2e1f-5add-b041-5297ad8d5eee', '6125c75f-be96-5f3d-ad15-072b8ccf8ac0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('7db31702-ce5d-533f-a09d-fd3d68e798c8', '6125c75f-be96-5f3d-ad15-072b8ccf8ac0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('afe9aad8-850b-580d-803b-032eb7cab854', '982a6f0e-02e2-5bdc-917c-a7ec849b8acc', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('852cc8b5-6742-551f-b7ad-bd86a60afd5c', '982a6f0e-02e2-5bdc-917c-a7ec849b8acc', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('303df0b5-d12e-537b-8768-340cd3cbb48b', '4f37c201-e9f4-5a27-8325-62ed2d645796', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('b393885b-94f1-5ebb-b6e7-7cbed09aad3f', '4f37c201-e9f4-5a27-8325-62ed2d645796', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('080f3e20-aeb0-5abd-9295-f282469dc8c1', '2758d725-11b7-5496-a7f8-56edc9736031', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('20ec9ec3-e85f-500c-8bc9-e58c7c4fd3f9', '2758d725-11b7-5496-a7f8-56edc9736031', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '235.0', 'DG', NULL),
	('d7df585e-9af8-53a4-a678-c245d52de1cb', 'cc5d88b2-8721-523b-9492-a052175c3d2c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('4f37d28e-ac5d-5b74-9141-faa55bb61ba9', 'cc5d88b2-8721-523b-9492-a052175c3d2c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '240.0', 'DG', NULL),
	('8fff97e6-1342-5c45-97f8-fbec53097775', '8972f9fe-2fb9-57c3-bbf7-e4cf46ae0577', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('e1e365cc-6989-525f-a422-0ebe104342c1', '8972f9fe-2fb9-57c3-bbf7-e4cf46ae0577', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('4ad4b28e-9963-513a-91d1-e1abbdb7c298', '9fe53a0c-a958-5652-92f7-5af92c81159b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('e46a01e4-c8a6-5a58-a2e9-8827dacb3cdc', '9fe53a0c-a958-5652-92f7-5af92c81159b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '220.0', 'DG', NULL),
	('e0f7ac8d-ff9e-57ce-a518-7a611e0c39d3', '59723173-483f-57e5-8415-2c486b3934c3', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('6fe1c9a1-59b0-5090-a0a0-fb2db9f36326', '59723173-483f-57e5-8415-2c486b3934c3', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '183.0', 'Y', NULL),
	('fbe926ef-4749-57f6-96db-0a4e4123ca6f', 'e5de0805-d253-5598-9a8b-44b66652f2be', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('f95514e6-ba77-5f53-ba23-6b961693197c', 'e5de0805-d253-5598-9a8b-44b66652f2be', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('b0b890dd-28ec-5fdf-b34d-603d5da84c69', '55832345-b016-52ac-a821-9284fd1bc8e5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('504017cc-90b3-53a9-9c58-57e39635d08c', '55832345-b016-52ac-a821-9284fd1bc8e5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('2c3cb51a-9f84-570f-8e71-9d5ab75c92b0', '1553d4a7-1853-5447-8fb7-53bf948be45a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('b2331578-f02a-5e74-b73c-5662aac9e60b', '1553d4a7-1853-5447-8fb7-53bf948be45a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('fecab837-8c93-5eb6-9728-bc814dcad6ef', '31acccbf-4b58-5ea0-99f7-eeb2e84f8b6b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('20e8f412-d775-52b7-81b2-d2bb676ef4d4', '31acccbf-4b58-5ea0-99f7-eeb2e84f8b6b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('6539eb5c-bf1f-5b8e-99a9-91626c8e18f0', '3aa22bd2-d49f-5352-b12c-69a4d74bb43f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('933b0b8e-2c3c-582c-bca7-5a395318fecc', '3aa22bd2-d49f-5352-b12c-69a4d74bb43f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('4dcdd760-1ca5-52c7-8b6c-19e2e0c6803b', '945a7d11-c6f7-56ff-bb4e-bd2dd760bfdf', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('d34b0236-772f-59f3-aa4d-d2f1753c4f1b', '945a7d11-c6f7-56ff-bb4e-bd2dd760bfdf', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '250.0', 'DG', NULL),
	('b76ab94e-3dc2-5761-b042-526b3e1efcaa', '2b594c9a-d30e-5bb3-8e9e-494997cf0103', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('870dea64-2541-500f-b44c-e0ab1701d099', '2b594c9a-d30e-5bb3-8e9e-494997cf0103', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('3368c8d9-89d0-57ad-9feb-ccb69cd143ba', 'a0bf8198-99e5-5438-9403-24e79656d6cf', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('24ff5434-9776-52e4-93df-cebfe7284304', 'a0bf8198-99e5-5438-9403-24e79656d6cf', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('b7c739b9-fa07-5fc4-8b73-a5e8f052a4bc', '44e8866c-2d7b-5dc0-9c01-6469b1588056', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('3a738b10-3acb-5b88-b1ce-1747bd3d764c', '44e8866c-2d7b-5dc0-9c01-6469b1588056', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('c77920e8-209b-5bab-b43b-448882d6bf0d', '12ecef6b-6187-555e-b589-a45180078fc5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('027a358a-19b1-5af8-aafb-185a68c395d7', '12ecef6b-6187-555e-b589-a45180078fc5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('763b69aa-5423-51d6-b255-cc4849ae79de', '60c68e17-a95a-5b96-a632-971abbb67fad', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('d08f91ac-099b-506f-90a1-bad1ac60c7d8', '60c68e17-a95a-5b96-a632-971abbb67fad', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('c937f7b8-f0fd-5014-87c1-e59afe3a1738', '57928b3c-8059-5f33-94d1-088103160be3', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('991a7eae-9b86-5c99-bdc8-ad77d5a87d13', '57928b3c-8059-5f33-94d1-088103160be3', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('b26bc6d1-08f3-5b67-802b-851514d0fc80', '4b9b4554-9166-562c-8c53-e29d5e5763ec', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('72df667c-62c1-534c-b99f-4944f8e391d8', '4b9b4554-9166-562c-8c53-e29d5e5763ec', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('8d29a522-19a5-59ff-b08c-58b838e7f483', '137d233f-4fcc-55c3-950d-c2a8d0b367f6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('2d1e237b-93f5-524d-a97d-98970447d719', '137d233f-4fcc-55c3-950d-c2a8d0b367f6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('91b94ba2-b12b-5332-a690-d905298cbf58', '7a5c2806-6b34-5ab8-b2c6-7b87f68debd3', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('75eadf04-bd24-5007-a11b-675a8546798b', '7a5c2806-6b34-5ab8-b2c6-7b87f68debd3', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('e31a26b5-d8d8-5f78-94c0-093c9b3ebf70', 'fcb0be16-75d1-511b-93b6-5d76499a31dd', 'bf4fa778-1dd7-51bd-8668-32e0b8808066', NULL, NULL, '73.0', 'LG', NULL),
	('bb8eb13a-52cb-58da-be65-66df8cb8fc33', 'fcb0be16-75d1-511b-93b6-5d76499a31dd', '9130b146-1bd3-5c1c-9212-988af2e7446e', NULL, NULL, '175.0', 'Y', NULL),
	('738bf4b2-3b10-525b-aae5-2836f1f434f7', '16d67c65-55f8-511a-ad78-239de7ba6495', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('6251f47b-d4a0-51a1-a136-b8fe9610b725', '16d67c65-55f8-511a-ad78-239de7ba6495', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('f287a34f-0aae-5049-80f3-855a7c8a34e5', '0ecbfd6b-6d20-5ca7-881d-e0939ae19722', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('673341df-2f8c-5e1e-963a-6e66c687ff60', '0ecbfd6b-6d20-5ca7-881d-e0939ae19722', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('8947b57b-eba6-506c-88e3-7550c179356e', 'b8cd2005-46f9-51d7-a193-16c35166bcee', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '83.0', 'DG', NULL),
	('a1ae311f-56e2-5100-8091-75afc3242b04', 'b8cd2005-46f9-51d7-a193-16c35166bcee', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '240.0', 'LG', NULL),
	('22db9c54-42b4-5e49-88ec-04771835e6af', '11a02371-2ce9-5c51-95a7-dd84e269fd7d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('3d832323-d782-570c-8fa1-0ade9ba7ad85', '11a02371-2ce9-5c51-95a7-dd84e269fd7d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('afcf0efb-7785-5785-8a80-54879b8c8860', '4076a688-10b3-5210-9a27-e13855481a47', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('dbad1124-7a98-5d72-99b9-f4070c086938', '4076a688-10b3-5210-9a27-e13855481a47', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('0b1edf4d-9e1e-5682-afa3-d7e067e64609', 'd334ac1c-e6a1-5210-9577-c4e45f9e4b0e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('c7c03cec-0a2b-5035-b024-18c67a8ef900', 'd334ac1c-e6a1-5210-9577-c4e45f9e4b0e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('b1b5b129-4aa4-5763-8b61-f3a4f4876013', 'ff440982-c902-5cbe-ad34-e1a8a7a6593b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('00ac8af0-0804-592a-a5a8-dc2421cda58e', 'ff440982-c902-5cbe-ad34-e1a8a7a6593b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('38d18fb8-405c-5718-918c-e430ecd1e2c8', 'dd9275ca-f5b4-54a7-a7ba-2fa6a2675e10', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('f12eabb5-ee85-5a4b-b032-fad7538ad949', 'dd9275ca-f5b4-54a7-a7ba-2fa6a2675e10', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('2d3445f5-1dd7-5942-bc14-d892fa4db41e', 'eea170d3-4104-5933-9f92-32ca80f20e15', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('393ff374-aa74-5eae-a773-9b65ba69dc08', 'eea170d3-4104-5933-9f92-32ca80f20e15', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('a4bf0879-85fb-5938-b314-8697695e29e4', '3ad4fb27-bd50-502b-9bb0-51e4d696a685', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('e297604b-51fe-55a3-86e9-3c8f8899cee4', '3ad4fb27-bd50-502b-9bb0-51e4d696a685', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('b6e281c8-7f9a-5c3e-befe-b607ff7f4662', 'cd43d7e6-74c8-5715-9267-705e9054fe58', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('e3a44ba7-f408-560a-8a65-856bfb960936', 'cd43d7e6-74c8-5715-9267-705e9054fe58', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('506c461b-ed1d-59e6-89f6-f93c122888d0', 'bc16d17a-0f7c-51b5-a227-7ed5e07ca3b5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('a22e01bc-8bef-5000-8052-d7efe5b220a6', 'bc16d17a-0f7c-51b5-a227-7ed5e07ca3b5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('d3b0fa9a-e951-50ea-8428-8514de963e6c', 'b60f48e5-c897-537a-8f8a-f9463faeda09', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('b891f5f0-0d22-5e96-b357-5cd8538ec3c3', 'b60f48e5-c897-537a-8f8a-f9463faeda09', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('12743e70-16aa-5091-9fb4-cfae813c0ffa', '35bc85f9-7b6a-5a37-92ed-e1e92a99fe69', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('75bf08a5-4b86-5464-b2a0-47dfdeffbf1e', '35bc85f9-7b6a-5a37-92ed-e1e92a99fe69', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('0ee2834e-dc72-5130-b4e3-9be1963f95ac', 'db938f9e-7ccb-52dd-9fe8-39c77e00073b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('0fd5920b-7254-5213-a59c-6d4450a96078', 'db938f9e-7ccb-52dd-9fe8-39c77e00073b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '165.0', 'R', NULL),
	('247333ed-69eb-5dac-9205-98c3c7dfc509', '287b8782-3f29-51d7-aac3-881fd8c82e76', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('5a6ac4db-64d5-56fe-8e4f-027d77a782a7', '287b8782-3f29-51d7-aac3-881fd8c82e76', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('b3924172-2a6e-511a-a933-e40321cdf11d', 'd121aeca-675c-5f16-88e8-ebd0b59064cf', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('d86b976f-26fc-5cb2-9783-2b5b400fc2d9', 'd121aeca-675c-5f16-88e8-ebd0b59064cf', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '245.0', 'DG', NULL),
	('e466c2b2-d9d8-5bdd-96d6-e871d39ec3ca', 'e6a3e67b-ea39-5ef8-b93b-dfcbd75597fa', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('f76b6455-0395-5c20-acc5-d83c0fe0ff76', 'e6a3e67b-ea39-5ef8-b93b-dfcbd75597fa', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '218.0', 'DG', NULL),
	('40955368-1fe3-5454-a83b-92bd7e7d868e', 'da5e342d-d83f-5864-97ea-a7d28bd93843', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('81e9e109-62f9-56f0-8b1f-4934a11b6344', 'da5e342d-d83f-5864-97ea-a7d28bd93843', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '222.0', 'DG', NULL),
	('11d0a5c5-94a6-5281-bbe0-552fd6ce2b6d', '5ddb3de1-10df-5df7-a005-24345c58480b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('5ecd783b-c872-5c85-becd-379ce86e655d', '5ddb3de1-10df-5df7-a005-24345c58480b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '193.0', 'LG', NULL),
	('36f07a29-fbd2-5023-91d8-3b3e4a20986f', '4d9d037d-56b9-5107-9051-e1c8adb39d41', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('861cffe8-15f7-592b-a76d-2263c2e78a8b', '4d9d037d-56b9-5107-9051-e1c8adb39d41', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('1e1fa9b8-645d-5892-b9a5-1eedddb11c49', 'bcbf7370-c62d-5cbb-b312-bd64222a228d', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('68050a2b-dc01-54f8-9457-fdf724459606', 'bcbf7370-c62d-5cbb-b312-bd64222a228d', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('c9c83d68-469e-57fd-812c-d2867171cde0', 'b2b75f70-9d60-57b0-9564-295e22590b16', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('adf8eeb4-943a-5381-ae53-6a61b9b817e5', 'b2b75f70-9d60-57b0-9564-295e22590b16', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('d138de2e-a944-5e79-b376-6907da5abd73', '04b658e9-3818-5093-bbc9-2ada015332e0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('e4ecea25-e2d2-50b4-be9d-0ed260653275', '04b658e9-3818-5093-bbc9-2ada015332e0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('3423708d-40cb-547b-b0cc-0e749d565fd4', 'd087fc19-0df3-5974-9627-4c83dd4c1424', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('340ce192-4ed9-5898-9833-1ac5d01c938c', 'd087fc19-0df3-5974-9627-4c83dd4c1424', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('ac986bee-f607-57f7-b421-98c8489aa83a', 'e5cca720-be34-571c-97dd-10f2d7359de2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('52a39477-703b-5c97-a980-fa1a3e71a4ee', 'e5cca720-be34-571c-97dd-10f2d7359de2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('0b473347-daee-5d92-af1b-97d0ed28464b', '0e6aa7c1-5798-59ff-bdb0-ebf08ba5e1e7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('770afce5-1c1d-5d9a-ab8f-79e11a6d8b4d', '0e6aa7c1-5798-59ff-bdb0-ebf08ba5e1e7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '187.0', 'R', NULL),
	('df97ef95-3e42-5cfd-9c08-78657a1726a4', '6b53468e-ded7-569b-b4a7-1e302908da6a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '69.0', 'R', NULL),
	('54abe53a-d5c4-5e82-81fc-21e02ee1a7e5', '6b53468e-ded7-569b-b4a7-1e302908da6a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '160.0', 'R', NULL),
	('130d0942-bce1-5186-bfe5-e2e962a90f80', '1cbae818-dace-5276-b760-58d548855d55', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('90e9cdd7-cde2-5fba-b652-2a99bc7b6b61', '1cbae818-dace-5276-b760-58d548855d55', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('9439e4f6-46e1-5687-806e-1934acd60c61', 'a777a8dc-627a-57ee-a3f3-a65767ef0f9e', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '82.0', 'LG', NULL),
	('219b8acb-2ac1-5f6b-a771-ff77094859ff', 'a777a8dc-627a-57ee-a3f3-a65767ef0f9e', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '230.0', 'Y', NULL),
	('fb44e596-64c0-5270-8305-1c58ba411225', '76404c5c-8cf5-5887-a6a2-3e7b06b30317', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('051b5901-2a9e-59f1-b619-d86ae4b654cc', '76404c5c-8cf5-5887-a6a2-3e7b06b30317', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('e3feee67-d44f-5ad0-bb70-7cbefb329956', 'd1a8119f-daec-5583-aa28-f22f347aa3b0', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '77.0', 'LG', NULL),
	('9aec9c43-904b-5c02-92cf-6268520f9373', 'd1a8119f-daec-5583-aa28-f22f347aa3b0', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '203.0', 'Y', NULL),
	('30808172-175d-59d2-945a-a15ca6097250', '60034370-c44a-5dbd-bba6-d164c22ea2cd', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('93edd64d-9f25-5d8a-a58e-34be8dc66b13', '60034370-c44a-5dbd-bba6-d164c22ea2cd', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('0c36aafc-9123-5d0f-a1a1-b1280608acd7', '2f4549dd-9257-58a5-be02-9a918fe390e2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '80.0', 'DG', NULL),
	('2d5c1208-2a86-5142-8814-52c065f4f468', '2f4549dd-9257-58a5-be02-9a918fe390e2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('82b1221c-a7dc-5416-9da7-451d199a802d', '9b7d9886-c50b-5777-8154-f321fd6cdc56', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('c687ffe7-64db-5139-8393-64eb4b86c653', '9b7d9886-c50b-5777-8154-f321fd6cdc56', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('7a7e53b4-573f-502a-9fcb-4ed06d145c20', '6b0fe83a-32d3-5c31-9e7a-26fa79e78752', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('0c56300c-75ec-51c5-9755-14a3e1f57fac', '6b0fe83a-32d3-5c31-9e7a-26fa79e78752', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('4cd4b601-178d-5b52-97c2-f0a43b4f5820', 'b95e7965-3678-5f5a-ac19-9261ab5b6ea1', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('27ad9d57-1188-56b3-8556-da69157debf1', 'b95e7965-3678-5f5a-ac19-9261ab5b6ea1', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '214.0', 'LG', NULL),
	('d4d6d66d-a20a-52d2-8854-5fe43231d0de', '9888004c-e6fa-5010-be94-bfb6e1e2a22b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('20ea679c-4256-5c5b-9b4d-fb1c73a1e7a3', '9888004c-e6fa-5010-be94-bfb6e1e2a22b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('5ee5c988-7e66-5d11-81af-8b582a8b2ff9', '8c77dccb-57db-5fad-bf09-7200e8d1f10b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('62cd1da3-d1b7-5191-a11e-5b58e2731fce', '8c77dccb-57db-5fad-bf09-7200e8d1f10b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('474b6557-9403-5c8c-87fe-ae27d230787a', 'dd28cf9c-82f7-5eff-8c15-97f5999d9d71', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('9e2d65ad-227f-58e9-b067-8d21d822a7fc', 'dd28cf9c-82f7-5eff-8c15-97f5999d9d71', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('f405a5eb-e4e6-5f54-8581-a1b82fd831f8', '8da4aeec-bd66-52ff-89c5-15a6dc96ba24', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('d6d16d0c-7adc-5708-89d1-682181283dd6', '8da4aeec-bd66-52ff-89c5-15a6dc96ba24', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '207.0', 'DG', NULL),
	('32c557a8-026f-591f-83c7-0f48cd8d6079', '721f07f6-6d13-5466-a4ed-758a87d776a8', 'bf4fa778-1dd7-51bd-8668-32e0b8808066', NULL, NULL, '73.0', 'LG', NULL),
	('666712f9-5ddc-56fb-b1cd-5c9518c57bb9', '721f07f6-6d13-5466-a4ed-758a87d776a8', '9130b146-1bd3-5c1c-9212-988af2e7446e', NULL, NULL, '170.0', 'Y', NULL),
	('cd38c0db-885c-54a8-baff-a4161441b38b', 'd435cf30-8408-5149-8fe9-5d0dff338081', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('350eaee2-14ff-536d-a8f7-af2d335d641a', 'd435cf30-8408-5149-8fe9-5d0dff338081', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('a9aee2e0-594e-59cd-a1c2-41818d690f6f', '51cb9b91-6f35-5abc-bdb1-69d5508fadd5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '80.0', 'DG', NULL),
	('872e16ff-9750-5863-9644-564137a517d3', '51cb9b91-6f35-5abc-bdb1-69d5508fadd5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '240.0', 'DG', NULL),
	('3ddc34b0-4908-5c89-b273-e206ecfe9141', '9493f33c-e8c9-58fe-9617-6f4272e81acf', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('3f1b90c4-835e-5b50-9f1f-dede7a02e573', '9493f33c-e8c9-58fe-9617-6f4272e81acf', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '181.0', 'Y', NULL),
	('a60b51cb-e24e-537d-ab0f-93782f2e250f', 'fca14b1a-22a6-5d02-abf6-05b8122f6354', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('21bb4024-c0ac-5309-96ee-b53cea22ebb1', 'fca14b1a-22a6-5d02-abf6-05b8122f6354', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('3e4eaff9-033f-5bf3-827f-09d9da1cb5cb', 'bc3fffb5-ff33-51c2-b7be-1b57bdae0048', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('96320071-19a2-593b-a57e-809cf0ac8085', 'bc3fffb5-ff33-51c2-b7be-1b57bdae0048', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '245.0', 'DG', NULL),
	('1a4f70c2-e925-5052-ade5-a5149b7d1802', '303ccb05-354c-5454-8460-47ca1d650457', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('16bbab9a-cbee-5abd-bfc6-09aa3f10f3c4', '303ccb05-354c-5454-8460-47ca1d650457', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '240.0', 'DG', NULL),
	('3a1d84d8-7141-5440-a0e4-ef701152a4d1', 'a49bf7a5-4f46-5e38-862f-6f2486f89909', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('713f6039-7a82-53d5-b592-b878ab9d02db', 'a49bf7a5-4f46-5e38-862f-6f2486f89909', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('69cc2b71-0b0b-5b5f-b184-a9a37de9bf97', 'a00890cd-757a-5981-ba06-646b44d065a8', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('047d059c-cc98-5061-8c98-c0af25c297bc', 'a00890cd-757a-5981-ba06-646b44d065a8', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('f5c75fdf-e163-5c2c-bfea-ee544e4986c9', '716387d6-ca3e-5152-a093-e1e159f17ead', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('db25cb71-d6ca-5848-abc8-9e989856914c', '716387d6-ca3e-5152-a093-e1e159f17ead', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('c3a47591-ea03-552d-b771-91b0b10ea1d6', '9de633d0-dae1-5ef5-b241-9be12d1b0444', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('78fac183-03cc-5f0a-a508-46893325e97b', '9de633d0-dae1-5ef5-b241-9be12d1b0444', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '230.0', 'Y', NULL),
	('afc2128b-0b14-5bdb-9e41-d39a4bdfd9ea', 'f10e6047-bd41-59c1-95dc-53d0caf54346', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('1ab85c24-ef7c-5fdb-a4a9-f227e1584799', 'f10e6047-bd41-59c1-95dc-53d0caf54346', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('6342bf45-374f-558f-a07a-f521f92f109d', 'c7172da5-2009-50cc-9786-59b294516017', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('912ef337-69d6-53ed-be09-c3386945e29a', 'c7172da5-2009-50cc-9786-59b294516017', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('99bd836f-a1e6-556b-9f0c-87fcc6cb7080', '6c4202ea-ffe0-5d84-a084-617cf8e2fd5f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('233effad-dc43-597c-86cc-4716d8f27191', '6c4202ea-ffe0-5d84-a084-617cf8e2fd5f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('4bfc930d-8183-5325-a8ba-d6a9fd54673c', '5e724ca7-18cd-5679-a674-0b67376a7916', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('b5e3ca58-69ac-57d8-9195-17bf74632e3d', '5e724ca7-18cd-5679-a674-0b67376a7916', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('b5092243-6c26-503f-97bf-1a0c18c2fc35', 'c1ca741b-1505-5b65-895b-95e99269852d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('ad585957-5f7f-56a1-bc6f-288fe79ccd7b', 'c1ca741b-1505-5b65-895b-95e99269852d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('f45f296d-42ff-59df-a33b-c9977e4d0b80', '84b14571-6a12-5ae3-bc9e-c906a4807ec2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('372923d5-5ad9-58ac-9c88-4d1e7f82bad5', '84b14571-6a12-5ae3-bc9e-c906a4807ec2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('58b60b82-08b1-59f8-ab0a-41af4cd08d07', '80b3e7e0-db2e-52dc-847f-1fe68d5dba4b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('555d744b-e9df-5395-abfe-cbf6bf4bc8dd', '80b3e7e0-db2e-52dc-847f-1fe68d5dba4b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '166.0', 'R', NULL),
	('ba6c2041-33b1-5e63-98d2-6ffeeb06ebad', '41cff46f-0902-5061-8d33-1470a08478bf', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('eeeaeaa2-3461-59d9-bb3e-c5186ecc361e', '41cff46f-0902-5061-8d33-1470a08478bf', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('500b8bb2-7092-5ee6-8d6d-497a64ef5ce4', 'f31b6c99-16c1-504b-861b-cf4645d6b977', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('23b4373a-7121-505a-a145-d9032d7660a6', 'f31b6c99-16c1-504b-861b-cf4645d6b977', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('ef17d723-a946-56f6-9ba6-3bb9351aceab', '70f94e78-90bc-5d2a-807d-4980d5087a33', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('49726882-1bd3-536c-9bc2-164cd30d2a19', '70f94e78-90bc-5d2a-807d-4980d5087a33', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('3ed2f24c-ab71-5ede-92d3-f348bf4fc495', '7dda843b-7530-5a7a-b23f-1a73f5124cc6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('78b524b7-023b-5442-9766-a16db8c283c5', '7dda843b-7530-5a7a-b23f-1a73f5124cc6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '184.0', 'Y', NULL),
	('21f8caa4-94af-5350-8c53-9c7f9cc49612', '144119e2-0740-56e8-8208-41e96797edda', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('2c40fa41-3966-563e-99da-d8a8be5238eb', '144119e2-0740-56e8-8208-41e96797edda', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '190.0', 'R', NULL),
	('cdbc8061-f975-5e76-9902-09866d082627', '41eac55d-60f4-583e-939b-26891ae64341', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('1677a843-f209-5460-856a-9f8e4c8d9df7', '41eac55d-60f4-583e-939b-26891ae64341', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('4943c401-4b93-5354-b921-feee55bed604', 'a15e64c0-eb22-54e6-b791-80c2e9d4bf13', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '81.0', 'DG', NULL),
	('9c1e4f77-bbab-5e14-b600-df12e1de9b59', 'a15e64c0-eb22-54e6-b791-80c2e9d4bf13', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '225.0', 'DG', NULL),
	('19bf9bd0-0ae2-5afa-92d1-106137c01ff9', 'c1f91bcf-4452-5ca2-97f5-a4f96e1c6aed', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('880c5473-510b-5db2-abfe-755b6969a4b1', 'c1f91bcf-4452-5ca2-97f5-a4f96e1c6aed', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('00a1ee59-ad6a-5632-b77c-81b33fb9d61e', 'a04ea3c1-f4ed-5b2b-9566-5b8338be827a', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('d69c6b7a-39fd-5390-9ca6-0d43020fa971', 'a04ea3c1-f4ed-5b2b-9566-5b8338be827a', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('72db3b5a-9f2e-5362-82ae-5dcb22060a96', 'fda8724d-9ba8-53c0-aa35-bf4b988abf08', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('69fe06af-4fcf-55a2-8e28-809859adb206', 'fda8724d-9ba8-53c0-aa35-bf4b988abf08', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('1b2874e0-5e35-5f1f-8326-6f4d4d7c0d2d', 'df4f4f93-79be-5937-ab8c-b7a50d65fe2d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('7b4485c2-9983-5dd2-992d-51d11990df71', 'df4f4f93-79be-5937-ab8c-b7a50d65fe2d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('87970e26-f187-5b78-9e3c-a22792fd1d43', '50d59dd6-d057-5f67-a7cc-467692c5679b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('1bc5c265-2ab8-5be9-8034-e3e588154836', '50d59dd6-d057-5f67-a7cc-467692c5679b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('b77f9de5-10df-5238-81cf-4408a2ade436', 'eb2c0639-ea02-57ea-9ee2-98fc6eb3f265', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('9bbc8fc7-e102-5d79-8697-c50df75e1755', 'eb2c0639-ea02-57ea-9ee2-98fc6eb3f265', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '167.0', 'R', NULL),
	('56ed5e77-d6eb-52e7-a892-e090dfaa41a7', '9226ac27-d962-5275-8d7d-1703598a9b68', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('e0f0c511-fddd-5f84-807e-3a0ec40ae63f', '9226ac27-d962-5275-8d7d-1703598a9b68', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('09f7fc04-9f9d-557b-9a8b-dd15b4c29831', '91ab568b-afe1-55b7-b3f4-4a2ce2fe29e7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('be38b5db-65ab-5193-a447-51babd798535', '91ab568b-afe1-55b7-b3f4-4a2ce2fe29e7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('b63c95f9-3732-53cd-bb6f-7d7997d01c0b', '45a87a2c-3204-5331-9b64-9bb90957d7e6', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('21095c7c-19d8-5b26-a847-f9228455eeef', '45a87a2c-3204-5331-9b64-9bb90957d7e6', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('57680386-9f96-53ca-9d13-3b3264d1bcba', '82f560ef-5e54-5349-a977-93662ce68e13', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '83.0', 'DG', NULL),
	('4c42e391-d9f5-58de-bcab-7d8bad27cc3d', '82f560ef-5e54-5349-a977-93662ce68e13', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '235.0', 'LG', NULL),
	('2ca005d0-2935-5ee8-af1a-ce99e0694ad4', 'c8e43e68-d602-5ac9-8b42-2d6a1dd0afc5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '80.0', 'DG', NULL),
	('6c212402-fa0e-5d04-99b6-57a21b094946', 'c8e43e68-d602-5ac9-8b42-2d6a1dd0afc5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('f185eab3-2212-5faa-bf2f-118aabcffe3a', '115d2f0b-9e20-597a-80f0-921b37f43da2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('ec18f648-3236-52f6-8a3b-a2c4f8245bf3', '115d2f0b-9e20-597a-80f0-921b37f43da2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('0ede8d6a-62e3-5a15-8eb1-1094becd8c86', 'c22ec146-f98e-587c-a9d8-41cd4c3405bf', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('f00e42e4-9578-51d7-9c4c-584914c3d171', 'c22ec146-f98e-587c-a9d8-41cd4c3405bf', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('b1025ee7-2f5b-5827-bcd9-d99f4f678905', 'c182a4ca-f21b-5fd7-b894-b90d634a8c32', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('493fc5c2-a720-5a2b-8d62-d07b03e02b48', 'c182a4ca-f21b-5fd7-b894-b90d634a8c32', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '228.0', 'DG', NULL),
	('74bc3ada-e944-5cc3-afd9-f35e186e6632', '80bc1a2c-bd71-5eee-bf9c-47c951fd9c92', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('a9117403-f492-5cb3-8934-e01e82001bc5', '80bc1a2c-bd71-5eee-bf9c-47c951fd9c92', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('eb50fea3-44ce-5864-a994-dd8c9a542c9b', '0a21a0bd-7319-5246-9b3d-5bf5a83d7354', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '70.0', 'R', NULL),
	('f2b55554-575b-5baa-9539-34b71fcb967d', '0a21a0bd-7319-5246-9b3d-5bf5a83d7354', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('5648e725-0aa1-5123-baa4-44939a4db9b5', 'f4b5a8ed-1a79-5d34-b529-00a0073d8357', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('f063d573-af1b-5478-b522-12a08a8a9b65', 'f4b5a8ed-1a79-5d34-b529-00a0073d8357', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('b9448f7f-76f5-589e-bcc4-18039a0fe955', 'f3b5b808-3084-511f-a15c-25ea75bcba01', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('8993c718-3fbf-54b3-a705-af2782fdbe2b', 'f3b5b808-3084-511f-a15c-25ea75bcba01', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('4ecb3434-b4c9-51e2-925d-a74b476c524b', '151c96fd-a8cb-56a9-ab1c-03c3e36c7b7d', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('fc1e2940-4b65-5a67-b96e-e178418492e5', '151c96fd-a8cb-56a9-ab1c-03c3e36c7b7d', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '212.0', 'LG', NULL),
	('636cb4d2-9cd3-5fa7-8659-20943a53d8a7', '883b9aeb-c4da-5c41-a53f-cc70a4643144', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('899f3439-9074-5e4d-99d2-6d447a752e8c', '883b9aeb-c4da-5c41-a53f-cc70a4643144', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '230.0', 'DG', NULL),
	('176b7067-170b-5f4c-9e23-d130f9a72ad5', '0731ec8c-77a7-5547-8cc3-ccdcb3fa4482', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('48b64485-1453-5cbb-a3bb-8fa9ed36f25f', '0731ec8c-77a7-5547-8cc3-ccdcb3fa4482', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('be6fe9b3-ec72-59e5-a8fd-5f34995a2eca', '95bff9ac-e9a3-546d-85e3-bc128fac1a92', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('3cda2065-fee8-5d2e-aa9c-0d2047ad2470', '95bff9ac-e9a3-546d-85e3-bc128fac1a92', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('6ac5afd2-90c5-5529-be38-97bea2ef05a6', 'e127c369-8ce8-5326-88b1-543779b52481', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('de3ffe66-030f-5798-b1e8-50ac20cd9420', 'e127c369-8ce8-5326-88b1-543779b52481', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('860948df-bd52-5c78-a6c9-1e44da6ee97f', '18fa1b08-7e4f-59a1-9b1b-56511cd51d49', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('c6b07502-fd64-5136-b62b-8eb5fd75c20b', '18fa1b08-7e4f-59a1-9b1b-56511cd51d49', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('07566621-44be-50eb-bbb2-19a66c394f0f', 'c9f8a945-ca3e-5e15-92b4-aa8613fc674f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('38ef32de-7af0-5fa1-aa27-d5bf6e5ac32e', 'c9f8a945-ca3e-5e15-92b4-aa8613fc674f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '209.0', 'LG', NULL),
	('933482ed-621b-56f6-899d-58c0b2b99306', '5bbfbc6e-79db-5809-b293-3b0058ce2c42', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('84f83286-f6f6-5da5-892a-e959af0d9e69', '5bbfbc6e-79db-5809-b293-3b0058ce2c42', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('565cf269-0a78-5645-853f-2d8df78625aa', '3a211fed-524c-5040-8c16-99426692867e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('398e9553-e582-55bd-a78d-d042d6f8bc09', '3a211fed-524c-5040-8c16-99426692867e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '203.0', 'DG', NULL),
	('52411d44-37ca-57a7-b137-a34cf10429fa', '670e730a-7181-5d7c-ad3b-616b18556401', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('4a7b0e61-7f41-50c3-beb2-925c3fb49330', '670e730a-7181-5d7c-ad3b-616b18556401', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('1e789c5b-9749-5490-9982-eb70f757a507', '6ad2bae8-0e90-551d-9682-6477f803e4c5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('ed0bde6e-e7ad-59e0-800c-002d96789e7b', '6ad2bae8-0e90-551d-9682-6477f803e4c5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('8d98283d-4486-51b3-9f18-bcf7c14593e7', 'b2c249cd-ee89-5660-85e5-b7a513410cc7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('e71ae5d7-5550-50c2-986a-485866642569', 'b2c249cd-ee89-5660-85e5-b7a513410cc7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('0743614d-bd97-507e-9d90-0ad459c1afe4', 'cd4bed73-ffb9-59f3-88a5-82e4d47a8a36', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('7c27ae9a-102a-5dba-b9da-f89f6ed984c0', 'cd4bed73-ffb9-59f3-88a5-82e4d47a8a36', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '198.0', 'LG', NULL),
	('c281367f-aa5d-5a50-9798-0068367a614d', 'fb2aeb38-4bea-57c1-bd73-427496f517b5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('1944ce24-ac99-5db0-b078-d965216afef8', 'fb2aeb38-4bea-57c1-bd73-427496f517b5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '245.0', 'DG', NULL),
	('e93826fb-d7b2-5480-ae36-2d621d36d6db', 'd417ecbe-25c6-5be4-b966-181fb299b961', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('08b5b26a-4f47-597b-9d8c-1675a94c4c7a', 'd417ecbe-25c6-5be4-b966-181fb299b961', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('2d1c177b-00bc-5fa1-860f-86af96bba783', '23d6cdf8-86c5-5fe5-8c45-21688bffd982', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('add5703d-da42-5e72-8d34-f344db334849', '23d6cdf8-86c5-5fe5-8c45-21688bffd982', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('11cb9167-f49b-58cf-af8a-a775c45b549f', 'f2601af9-5b95-5a8c-a660-2762f2f47887', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('3d8f61e4-148b-52f2-acb7-816e6f2c22f4', 'f2601af9-5b95-5a8c-a660-2762f2f47887', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '184.0', 'Y', NULL),
	('bcddb377-9770-596b-8c7f-429bad5473c6', 'ad36b12b-aedf-523c-9489-cf6b8c8aee83', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('c4bae54e-3c8c-5fd1-9ca5-6cd4a7637931', 'ad36b12b-aedf-523c-9489-cf6b8c8aee83', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('894de12a-96d9-51a4-9f9b-775d8f94f535', '3ea6043d-3cf1-5951-9e75-8b56dd171450', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '77.0', 'LG', NULL),
	('ca8f165e-f4d7-5881-9459-a6eba812a5b7', '3ea6043d-3cf1-5951-9e75-8b56dd171450', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '217.0', 'DG', NULL),
	('0960328e-ad3c-5c3d-a491-f0799c78b77f', '68da3754-b313-55c8-8d69-23a15de7ed99', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('45eb80fe-6bcb-5bb3-afb8-dda3c8ac8c7a', '68da3754-b313-55c8-8d69-23a15de7ed99', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('83a8afdf-edf4-52db-a0f6-bacf47aaacd6', '743b43af-32c2-5e60-ab5a-d86306e57eef', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('db0eee5c-ba7a-5e56-9626-d7bc5fe785bf', '743b43af-32c2-5e60-ab5a-d86306e57eef', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '232.0', 'DG', NULL),
	('949934a8-9fff-53fe-8425-1ba74d2224ed', '4769f74c-9759-5a76-8c40-bb455f32bd75', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('0a84e0fb-8280-5ec8-a475-7653550480c8', '4769f74c-9759-5a76-8c40-bb455f32bd75', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('4e27ca39-0eb3-5026-9d05-9d43aad4059c', '7d7d4805-f796-5aff-8846-b300832c01dd', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('225fdcfc-8eb5-5461-9663-fc3fd73ab49c', '7d7d4805-f796-5aff-8846-b300832c01dd', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('c4f856a7-378e-5ccf-b648-7858bc5c0905', 'b3657703-fce7-5f20-94e4-5c7ddbd6a6bf', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('3dfa9a66-4624-5503-a572-b637858b876f', 'b3657703-fce7-5f20-94e4-5c7ddbd6a6bf', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('43272228-4915-5b3a-ab0e-09a881f33614', '5e45a2bc-6e44-5e6f-a7cf-298cb8fba154', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('cad33be0-576d-52de-a682-7b7abae21b66', '5e45a2bc-6e44-5e6f-a7cf-298cb8fba154', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('3d6b5af0-d56a-5319-b02c-81d90692d14c', '6fe1c671-9620-59f9-8c5f-84cb6d757358', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('df33e27e-8949-5965-8353-a45dcfaf3841', '6fe1c671-9620-59f9-8c5f-84cb6d757358', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('92c314fb-d5d0-56ce-b1f4-e00d51bfeb78', '58f41989-a04b-5583-9983-c4d8c8e07bc4', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('9cf75136-d2de-5520-b80b-ec71ac74b4b7', '58f41989-a04b-5583-9983-c4d8c8e07bc4', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('e8546e8e-19e1-5e10-b599-048b6c87978c', '165ee1ec-cee9-53ac-95a7-3519558d9685', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('98903fca-33f5-5ba6-b81c-a9093e236468', '165ee1ec-cee9-53ac-95a7-3519558d9685', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('b88d4857-28a9-5621-bed9-8f0134fbe58e', 'a5979f34-1781-5439-a8fc-53f5029fa112', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('b1790ada-7045-56a5-866d-6b993769706b', 'a5979f34-1781-5439-a8fc-53f5029fa112', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('7f96e33b-5a8e-5872-a0a9-8505ef7ff787', 'd5994d23-db52-595e-a4c8-e3891f8c3085', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('d424a92b-9773-5ebd-8538-a18a024d9b33', 'd5994d23-db52-595e-a4c8-e3891f8c3085', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('803c7a6c-0004-5fca-87f2-e49bbb5c4a7f', '8c22b460-8776-5636-a997-3443f394e09b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('51a13061-e0ce-54fc-adcc-67346fb982ea', '8c22b460-8776-5636-a997-3443f394e09b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('4e880505-9a18-5854-ae93-90a882ff51d9', '0c7a070b-209a-5b6d-a45e-193303c43df6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('621e5991-49ea-5c0e-8c32-23498019970c', '0c7a070b-209a-5b6d-a45e-193303c43df6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('baa56d77-61a8-557f-81e4-931241f49ddd', 'b8f76b23-ef92-5487-afd3-21ee24a519ba', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('9ca1e7f1-f7cf-5e3d-8bef-37fcc311a3a2', 'b8f76b23-ef92-5487-afd3-21ee24a519ba', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('60e91cd4-f39d-583f-b1dc-e109156c8b50', 'c8540916-2253-5c15-9016-831523ea16f9', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('3efda8cb-bd5b-5b7f-b1fd-cf532b8ed716', 'c8540916-2253-5c15-9016-831523ea16f9', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '255.0', 'DG', NULL),
	('65d3fef8-83d8-58c6-9e29-ed2f240b2871', 'd11a9282-d781-5556-b510-5fdf7bc87d05', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('9839dad1-5039-551a-a67f-33dc91d912cd', 'd11a9282-d781-5556-b510-5fdf7bc87d05', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, NULL, NULL, NULL),
	('c6b13425-2a97-550f-a6ea-a26599d6fde8', '4420cbe9-768b-54e3-8621-fa69c9dda662', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('8b4f3254-9b88-5e8d-ae3b-1924110b6f00', '4420cbe9-768b-54e3-8621-fa69c9dda662', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('22d248a6-dd79-5d0b-a5cb-f6cbee98d3a0', '794e8f96-44a2-5d37-82da-4f293672c8e3', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('f9f571c4-5823-5a82-b282-c25262ebb982', '794e8f96-44a2-5d37-82da-4f293672c8e3', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '185.0', 'R', NULL),
	('08ce9438-a6e5-5806-b9d1-f7f5b90a3bea', '2dea8e6c-5b4a-5790-9afb-887e5ab047e6', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('27a14440-e057-5409-b473-a0ccc49896e9', '2dea8e6c-5b4a-5790-9afb-887e5ab047e6', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('57529d80-a43d-5b07-980e-1184e48c2c9d', '8e1bd6ec-ff78-5156-858a-6c0d95e4b9e2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('b95b806e-fac9-5346-8ce7-2570f9096591', '8e1bd6ec-ff78-5156-858a-6c0d95e4b9e2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('fc6b9a2d-5caa-52b5-88d1-5814774b9f68', '57eafbdb-8814-5d9d-b76d-bf9ee9ea9ff8', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('faddf491-33ed-5a2d-b421-dfbbfcd2e601', '57eafbdb-8814-5d9d-b76d-bf9ee9ea9ff8', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('3e51a0c0-a9a2-5323-a00a-dca60019e20a', '152fd81b-a1c2-5c8a-a109-0dfe86e306d0', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '83.0', 'DG', NULL),
	('d637084e-7369-5fb3-a7d5-ae314454f2b1', '152fd81b-a1c2-5c8a-a109-0dfe86e306d0', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '245.0', 'LG', NULL),
	('96ec0eb3-69c8-567c-8ff8-11a3489516ac', 'ebb7a3ee-13ee-5bcd-8134-2d2a0b062afa', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('49e65e51-3d81-50f6-bccf-b994fb09be50', 'ebb7a3ee-13ee-5bcd-8134-2d2a0b062afa', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('f485f254-f3fa-5ba5-b86f-754102cc6c4e', '4ced198c-ef0f-5d36-9ea8-80c60c81de24', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('55ef8397-e2ee-5fda-99cc-2867d7ff38d2', '4ced198c-ef0f-5d36-9ea8-80c60c81de24', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('ef0c9103-5924-5624-8eae-95a0e3cb9b2e', '18ae1d14-99b5-5a6d-8d31-5fb26c4d9cbb', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('cade066c-6d05-5c51-8f38-385643993497', '18ae1d14-99b5-5a6d-8d31-5fb26c4d9cbb', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('815e98d6-6ecc-50dc-991c-c5f52c13093f', '12d796dc-d2e0-5827-be11-eac649e2cc23', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('7a20798a-f53c-5cb9-9c20-23bf89c5ce4c', '12d796dc-d2e0-5827-be11-eac649e2cc23', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('a2705d88-f89a-58ce-b052-32655843501c', '393c1ae5-9cdc-551c-afa8-c4debb2f1be0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('5e2178b6-c6d8-51f7-9eee-f39effc65943', '393c1ae5-9cdc-551c-afa8-c4debb2f1be0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('19e214e1-f484-54f2-b8bd-0fa7e0edf999', 'daa8af07-55cb-5faa-b380-b6dcc221caf9', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('a408c9d9-7689-5e5a-a6eb-0c97db06d306', 'daa8af07-55cb-5faa-b380-b6dcc221caf9', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('077ba8de-49dc-5d5a-b1dd-fabfae92f6f2', 'fe573217-0fc2-5652-b744-1bbc6cb22cf7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('d3f45ccf-86d1-54c9-9ef1-06dda50728a3', 'fe573217-0fc2-5652-b744-1bbc6cb22cf7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('de0f863b-da8d-5d91-a096-92ed2538b73f', '048713b0-f46d-569c-9cc1-b7c0d1bfa47f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('8229de78-6dda-5525-9405-5aa2bd3eba2d', '048713b0-f46d-569c-9cc1-b7c0d1bfa47f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('53963202-5779-537b-a62d-5c07a6ae463b', '55af85f1-5729-5775-a489-6744a08bc801', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('32893e5b-57cb-56fa-9e86-b213f84d932c', '55af85f1-5729-5775-a489-6744a08bc801', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('835b7150-f056-5f0b-b030-f463ffdc6d2d', '38d51352-1b17-5294-bd4f-c8810d6519d4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('4303267c-cd63-5ae7-90d7-32188d3adbdf', '38d51352-1b17-5294-bd4f-c8810d6519d4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL) ON CONFLICT DO NOTHING;
INSERT INTO public.attribute_grade VALUES
	('16ad9c44-026a-5f92-8d81-d9d96cbc950a', '298a47ed-9d22-5f0f-b24a-a1978993d85a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('abe77878-c8e5-5d01-8f96-6c362b9a1f32', '298a47ed-9d22-5f0f-b24a-a1978993d85a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('0ce862a6-9cbb-58f2-a400-9e00e4729b84', 'ab15e9dc-7ead-5308-a00f-7ea06756acb0', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('7e0e5951-d755-526e-b267-b34911457de5', 'ab15e9dc-7ead-5308-a00f-7ea06756acb0', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('19f610c1-48f4-588d-8e2c-724f5178612c', 'f3debeda-2897-57e2-993a-4c7ff4cf1a61', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('cbbaa52e-b805-5fce-a09c-23f0cbf5fd77', 'f3debeda-2897-57e2-993a-4c7ff4cf1a61', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '197.0', 'LG', NULL),
	('b6bb6ded-ab9b-5a84-a260-8906561cb770', '4ac9cf56-bd89-5358-9bc5-7d8fffbb7489', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('68e6bce2-0140-5da7-835a-d18a191e4fac', '4ac9cf56-bd89-5358-9bc5-7d8fffbb7489', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('a9a2baed-a863-5a64-a602-1ed84ce8a07c', '2f48f810-29f8-5637-ae19-7a1023785319', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('59585ecf-1bfa-5ac1-952c-d8a9770cb513', '2f48f810-29f8-5637-ae19-7a1023785319', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '213.0', 'LG', NULL),
	('334f66a6-3670-5602-ac78-da649d1b7225', 'dece5008-430f-568f-9d83-b27e21b3e974', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('899ff681-ec28-51d9-bd7d-d3eb6bec4aaa', 'dece5008-430f-568f-9d83-b27e21b3e974', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('d6dd1be2-646c-5ac8-896a-99d054c40af8', 'd1d03fa3-0adb-59f8-aac0-39a503f8d14c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('671fbcdf-d1e7-5648-9c47-223c3aa0806d', 'd1d03fa3-0adb-59f8-aac0-39a503f8d14c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('9df0ae1e-73bb-5e00-8270-8404d64fa76e', '5f29f017-e6ea-5f3e-ab31-8f7570177aa7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('178b9535-f72a-590f-b773-ae817ff81b5e', '5f29f017-e6ea-5f3e-ab31-8f7570177aa7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('66b26344-45e6-576b-8e51-384aad68cbe7', 'aa9a195a-91b3-565c-956e-52b7b77c05e7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('94580a7d-91c6-5c46-98ff-3969692a17db', 'aa9a195a-91b3-565c-956e-52b7b77c05e7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('5aa7392d-3a9c-5c56-ac9f-681637d3a80e', '429b7653-4f5b-5074-b69b-84a44d6cf777', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('508547fd-6384-5a56-971a-e6a7b569d46b', '429b7653-4f5b-5074-b69b-84a44d6cf777', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('5b0c6e7b-417b-5ed7-8069-546af97b9bb9', '0a942524-84c0-55a6-9e03-4be986988091', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('91e373ce-86fa-5b56-a2f2-7d62ce46df1b', '0a942524-84c0-55a6-9e03-4be986988091', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('c7ea5b8c-97b0-519c-901c-5e82d6492e8b', '5b43709a-c98b-50e5-b984-013a949c110b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('188ebf00-1144-593b-8253-7deb5438047a', '5b43709a-c98b-50e5-b984-013a949c110b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('b4e1aa66-7356-5287-8871-a64b3cd07c7d', '076e9120-ba17-5dc1-9b99-74a6d41321ba', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('10d5ae4c-7750-598c-9a1b-bd72d6dad90a', '076e9120-ba17-5dc1-9b99-74a6d41321ba', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '184.0', 'Y', NULL),
	('5cbde3d6-f48b-51ea-8365-8f2e3f519730', 'aaa71972-e829-5893-b65b-4be80cb6622e', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('d5e8e66b-5c49-59af-a82a-c1afcbb00727', 'aaa71972-e829-5893-b65b-4be80cb6622e', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '219.0', 'DG', NULL),
	('914a68da-0c22-5124-be1c-4a8425f71519', 'c91f601b-cf83-568c-b30a-e2138fb17e9c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('67d655e5-8968-5b38-b7d6-c659c420939b', 'c91f601b-cf83-568c-b30a-e2138fb17e9c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('2a2ab08f-70d3-5153-ac72-cc32e9d2ea64', 'f04d9eda-a85b-5dde-aa17-a6143924a09f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('994f9bfe-78ea-5a0f-939e-b97bd01a79ba', 'f04d9eda-a85b-5dde-aa17-a6143924a09f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '218.0', 'DG', NULL),
	('ddae26e8-40bd-5338-bc66-6b10e20231a3', '275ecf2e-2108-5f1c-8afc-ae22c1eb321b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '70.0', 'R', NULL),
	('a098adaf-8798-59d4-b5db-2973d122b3c2', '275ecf2e-2108-5f1c-8afc-ae22c1eb321b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('7d4bc4e3-f544-5091-b8e3-78c780574722', '90822420-59bb-50f6-acd8-1e5c62a7dd8b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('6b0ab02d-41bb-5730-b0ae-5d0b006deb96', '90822420-59bb-50f6-acd8-1e5c62a7dd8b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('09200676-e5f1-5e80-9ad5-70842dffeb6b', '9931699e-e9d3-5cf7-84ce-99050c01215a', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('29b44e7b-c8fa-5505-a780-a76e5cc4494f', '9931699e-e9d3-5cf7-84ce-99050c01215a', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '202.0', 'Y', NULL),
	('6cf63831-f975-5680-b7aa-bbf626f823ed', 'c5da84cb-6bdd-5f46-a624-1bf0835481c2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('468b8d2e-8b69-59fc-a712-34cfea990868', 'c5da84cb-6bdd-5f46-a624-1bf0835481c2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('b6f19093-703c-5d41-a04c-67022eab6970', 'e76f4795-ce15-5574-b5ef-20d287d0e3b0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('fa88bf0c-5d49-59fe-ae54-fc9dc1145021', 'e76f4795-ce15-5574-b5ef-20d287d0e3b0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('e56b8f25-d7f8-5e39-9f40-fba828280759', 'bdd0a22c-5de7-5ff2-83d3-2e3f0cfdea9c', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '82.0', 'LG', NULL),
	('6ec7183e-0e4a-53a4-994a-bf7dc002357c', 'bdd0a22c-5de7-5ff2-83d3-2e3f0cfdea9c', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '230.0', 'Y', NULL),
	('0550b9c0-5383-5dd1-9c64-09034e12684d', '6ac73311-800f-523f-a7bb-4138871ed7be', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('d4e20ffd-cd76-5a73-842a-999370c88c97', '6ac73311-800f-523f-a7bb-4138871ed7be', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '193.0', 'LG', NULL),
	('533575cd-ba14-5dac-b9a2-b9897d91f429', '7f3b17f3-4c3c-5e70-969a-177ba7a52b3a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('32d39eef-25f7-52f5-bba1-36f37a6edc9e', '7f3b17f3-4c3c-5e70-969a-177ba7a52b3a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('96905814-4970-5e9c-bf39-524484ee96e1', '12a4021d-4dc9-57a1-9d53-78d44bb72519', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('866c5338-70bb-5ee5-91d0-78a205da1db6', '12a4021d-4dc9-57a1-9d53-78d44bb72519', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '199.0', 'LG', NULL),
	('4bbfdebe-0d0f-56b0-af21-c799fb75f6ec', '1b493ddd-70ab-56d8-bb39-6554dfeaf408', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('917685d0-d99a-5f16-9aa1-7ea231826031', '1b493ddd-70ab-56d8-bb39-6554dfeaf408', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '230.0', 'DG', NULL),
	('25265124-bd29-58c2-9a28-729ba14e8f4b', '4dedbd17-e490-58ca-a951-79534ae3dcc7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('840a04b9-0918-5793-87b8-b3c046ee222d', '4dedbd17-e490-58ca-a951-79534ae3dcc7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '192.0', 'LG', NULL),
	('b6839a5d-0fda-5d33-b0ed-e03ea5d6187f', 'fe5f46f9-02a8-55d0-a73b-d65caa6b84af', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '70.0', 'R', NULL),
	('4a991a69-1874-5a0b-b416-fbc5c488343f', 'fe5f46f9-02a8-55d0-a73b-d65caa6b84af', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '157.0', 'R', NULL),
	('9d76918b-1ee3-5a86-b1ec-7d5a50b6312c', '09a3f6fe-efe2-58dd-88e7-73cbf00a16da', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('24739e1d-8589-5d1d-968a-7b01ebe0ac04', '09a3f6fe-efe2-58dd-88e7-73cbf00a16da', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('d98493fb-835e-5a9f-aa67-56d66897d0a8', '087a4719-f0eb-52e1-985a-7a28881dd19b', 'bf4fa778-1dd7-51bd-8668-32e0b8808066', NULL, NULL, '77.0', 'DG', NULL),
	('bdb1e57e-0a99-526e-bb37-ad7eb0ea5795', '087a4719-f0eb-52e1-985a-7a28881dd19b', '9130b146-1bd3-5c1c-9212-988af2e7446e', NULL, NULL, '189.0', 'LG', NULL),
	('3edebcf5-3b89-5351-9eed-2d787e735980', '70173cda-44c7-529f-bd3c-bc74e4ccc530', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('e380c2ab-1157-5948-8663-d820115255f0', '70173cda-44c7-529f-bd3c-bc74e4ccc530', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '243.0', 'DG', NULL),
	('3dea4076-dd63-5312-9f54-69bfcb69e450', '43a6fc9f-4753-5a53-9604-d75f1fe8000b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('c2285f42-f9b7-5c3b-93b5-d46a9d041e07', '43a6fc9f-4753-5a53-9604-d75f1fe8000b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '243.0', 'DG', NULL),
	('18c47c3b-db21-5dd9-883b-802f82543f42', '39d5ee4e-877a-55c3-b15b-bcd9b285828c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('ede5fc6d-fe81-5a84-80fd-1141c0fbbe77', '39d5ee4e-877a-55c3-b15b-bcd9b285828c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '214.0', 'LG', NULL),
	('c88681b0-2b6d-53c3-9ca6-ea13ad98580f', 'ca06d2a8-da11-5a96-9c9e-09f962f349d3', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('71b293fd-cd72-5e1d-b8f6-db210cc1a62f', 'ca06d2a8-da11-5a96-9c9e-09f962f349d3', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('f540853f-6f9c-5086-a95a-2c35bb306f52', '9d0cd8e1-dffd-522b-ac7c-476593817e39', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('0d55f291-b712-53ba-9164-f372857665f9', '9d0cd8e1-dffd-522b-ac7c-476593817e39', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '239.0', 'DG', NULL),
	('c40b7a47-ad8f-5a86-b316-ff890745264d', '64f9c532-0c48-566b-ba8d-5ffc8d318327', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('608978c9-611c-5769-b611-f3e7d70326fb', '64f9c532-0c48-566b-ba8d-5ffc8d318327', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('a944cf00-98c8-5719-bdab-e6f58ed347e8', 'de0b151b-0603-54ad-b2e5-18c9bbb1dd36', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('8b433bc5-4468-5bad-ba89-88ce6487bca9', 'de0b151b-0603-54ad-b2e5-18c9bbb1dd36', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '164.0', 'R', NULL),
	('de961dda-86c1-55d3-afbc-a2785fdedeb7', 'a93d40c2-e5ba-5d79-bfac-3c2f564fd00b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('4be1387d-0851-55a7-a9d5-ba2fb299dadb', 'a93d40c2-e5ba-5d79-bfac-3c2f564fd00b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('0b262ab3-c338-5f71-944c-5eb8947e323f', '21087704-a71b-5f05-9645-ee24120ec139', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('5a0ccfcb-645f-58af-a0c8-1dd8bb581f0a', '21087704-a71b-5f05-9645-ee24120ec139', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('8ad8e3ca-554e-51d1-8f23-0fca45495f78', '8f08871a-f013-5ce9-8370-9374f24e4252', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('f582c98c-63da-5380-8704-3c8ab917eb7a', '8f08871a-f013-5ce9-8370-9374f24e4252', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('8db9c8f1-4315-5d89-9c84-300d0d1658ef', 'd0d9b245-768d-5fd8-a187-56fd8bc2d567', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('243564d0-532b-5627-807d-422b02a9c610', 'd0d9b245-768d-5fd8-a187-56fd8bc2d567', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('f1bde264-b6df-5fa5-9468-3ee040492dba', '761f107d-f412-509f-bf7c-767c4a49cea4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('abc07c61-16d0-5604-9671-0bc7d4633e88', '761f107d-f412-509f-bf7c-767c4a49cea4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '213.0', 'DG', NULL),
	('8b2d9669-3c68-5e04-b57e-c2ac520c8182', '133d3b56-847d-5392-bd6f-ecb1bda049a0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('cbb4ebfd-ab8a-5ec0-ab31-5ff5421e4acf', '133d3b56-847d-5392-bd6f-ecb1bda049a0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('dec5ae94-99b4-523a-b835-ba4530c5e490', '963ff4d2-5e82-5aa0-84ed-f1789854e405', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '84.0', 'DG', NULL),
	('a2a2cea0-2b6c-5052-b5dd-11783bfc4a2a', '963ff4d2-5e82-5aa0-84ed-f1789854e405', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '269.0', 'DG', NULL),
	('b1a992b5-0454-52f8-bacd-6492c9ca2111', 'd1ab167a-b3fe-55dd-94d5-7bea532ae0ad', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '83.0', 'DG', NULL),
	('f5b142a2-5c5b-53a3-9101-02996d5312e1', 'd1ab167a-b3fe-55dd-94d5-7bea532ae0ad', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '230.0', 'Y', NULL),
	('6a1b460e-eb72-57cd-93fd-ef0102cfa69e', 'ddb1911c-906f-5d70-8c74-eebe37cc5550', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('4ead3f4d-53b0-5fc5-adb6-7f2b94d4f548', 'ddb1911c-906f-5d70-8c74-eebe37cc5550', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('6f9cb880-bb64-59da-87e6-a26ac2ca97cc', 'd65dda01-90a8-59e0-b5bf-2b9ee91dd181', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('bcb54324-0e5b-5f2a-a01e-74b80c31696c', 'd65dda01-90a8-59e0-b5bf-2b9ee91dd181', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('530a8ebb-0352-5ad5-8dc6-81f2b6e912d3', '649fce71-f312-5f07-9560-d81531d5e99f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('aae645be-a2f5-5729-af7d-ac4eecb22e00', '649fce71-f312-5f07-9560-d81531d5e99f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('2016df6a-096b-5410-9221-33efd1cd01bc', 'ddf909a2-295a-54c7-9322-979aed5acb22', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('6e229f75-a868-5784-abc2-632960cd28bc', 'ddf909a2-295a-54c7-9322-979aed5acb22', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('fd334961-d88e-5644-a34b-6697cadade09', '314dcb5d-cbd8-518a-bf84-b5cf5c734ccb', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('3b8f8590-7cc1-5ff2-8273-a6685c01f8b8', '314dcb5d-cbd8-518a-bf84-b5cf5c734ccb', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('0ad0fc53-78e6-54ca-b0b2-8744dbd3ee68', 'c8b42182-990d-5ea8-9644-7eb09918c895', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('019a47ba-c65d-540b-9daa-d55cfd21faa4', 'c8b42182-990d-5ea8-9644-7eb09918c895', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('e3ff3a9b-4c28-59da-b2f2-8c038636726e', '114bd3ef-a238-5120-a327-c3b144cc66cc', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('765d76c7-e12d-5cb6-8cde-6f8e1ba23654', '114bd3ef-a238-5120-a327-c3b144cc66cc', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('8f6157d6-7d27-5f08-89fa-a3a06e3dc2c8', '428b1abd-48bb-50ff-bd47-493a14bfc1c0', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '82.0', 'LG', NULL),
	('ab2a07fa-af58-57b5-b6d4-e4d517cd220b', '428b1abd-48bb-50ff-bd47-493a14bfc1c0', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '240.0', 'LG', NULL),
	('2e2351fa-32ee-59ef-af27-99bcba7ac532', '1bc05cce-46dd-5ac9-8e29-cd3fe4e3e76f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('cf951f3c-bb0a-589a-8e49-21965fc6ae22', '1bc05cce-46dd-5ac9-8e29-cd3fe4e3e76f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('8206ab7f-8f43-539d-8999-de0969aaa8e7', 'd45b13e6-58fa-5968-9897-da2a585156fa', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('d9f9d12c-ba15-521d-b4a3-8de2aac1d0d5', 'd45b13e6-58fa-5968-9897-da2a585156fa', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('30116383-5258-57df-a73b-0003df008fa5', '3ecfe5f5-bd13-58fd-b133-6fb1b7313ed0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('51e0a757-2405-5d57-8a3e-d96d3571f514', '3ecfe5f5-bd13-58fd-b133-6fb1b7313ed0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '189.0', 'Y', NULL),
	('345cc6aa-2edd-514a-a7a3-ad8823704d99', '17205aac-76d1-5c53-8b29-e91164d14784', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('5dd08570-191a-5c7d-a468-bb89cabbbde7', '17205aac-76d1-5c53-8b29-e91164d14784', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('3ae517d1-0154-5b62-a9a9-a3ced57faacf', '0cd2bd5b-49fa-541e-a3d3-c5c15404b6c7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('38214fa4-754e-56e1-91ed-25f2f1085b53', '0cd2bd5b-49fa-541e-a3d3-c5c15404b6c7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('dbe86041-a07f-582f-bc52-a569fcc6c46b', '8b1adb21-812e-5577-942e-8c8c789bdf09', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('5e2bc400-f00d-596a-a59a-2b6b38bc1a78', '8b1adb21-812e-5577-942e-8c8c789bdf09', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '165.0', 'R', NULL),
	('32cf48ee-c0b9-5f2a-ab06-e50265db2008', 'dd9c301a-2d3c-59b7-b24b-5215205d1120', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('3aa319d1-c0f1-5986-b81c-9aa2f9b709db', 'dd9c301a-2d3c-59b7-b24b-5215205d1120', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '185.0', 'R', NULL),
	('6c311cfd-fbc8-572f-a6e7-8c0ccd294bda', '434b3e46-7d35-592b-9572-644b4dc33a76', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('d2f403ef-dd01-522b-a02c-346dc7bc0e09', '434b3e46-7d35-592b-9572-644b4dc33a76', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '238.0', 'DG', NULL),
	('5430c132-f8e4-50e7-b138-a4072b61d9c0', '5a610df1-32a6-53e1-a51e-0af90c2717c5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('9e5eabd4-2bae-5f55-a6cb-c78d06842805', '5a610df1-32a6-53e1-a51e-0af90c2717c5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '194.0', 'LG', NULL),
	('ab01f9aa-bb6b-527b-aa85-f5bed970d7f2', 'ad447f0c-80c8-5384-a1e9-28fbf462f67f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('80c1e822-fa8c-547c-aa1e-dac8d29c835c', 'ad447f0c-80c8-5384-a1e9-28fbf462f67f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('8ef0e778-12ff-5e8d-9e86-cd1d3f3fd341', '0918b346-baa7-5da6-97f0-97476bf0a0e7', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '82.0', 'LG', NULL),
	('5a092738-00d3-54c1-b5e3-5c663a9f1737', '0918b346-baa7-5da6-97f0-97476bf0a0e7', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '233.0', 'Y', NULL),
	('9bed00f3-5afe-5d7a-8fd6-77883fbcc8df', '71e2ee6c-b92e-53cb-b780-1280e6ab1421', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('b680011b-7a8c-523f-821b-9e329966e103', '71e2ee6c-b92e-53cb-b780-1280e6ab1421', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('55f88651-fecf-5849-ba77-5a5c2ed1ebf2', 'abbed48d-7890-5b5d-bd1d-071c02590aad', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('fbf7d543-aa18-5698-af06-2e99a7bddf30', 'abbed48d-7890-5b5d-bd1d-071c02590aad', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('857c6cce-570b-5e03-8af9-1b4c7b0c4849', '9497468a-67a6-513a-aa85-f42cdfc2341b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('2d2d08dc-b6ac-5005-815d-5b2400933e35', '9497468a-67a6-513a-aa85-f42cdfc2341b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('b0c5fb2c-3dfb-5317-bbd0-fd0d60db6e31', '8b1a61b7-4bbe-584e-b715-9fb6727ff50a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('e26a7374-22e3-5a30-8756-b9d892428a9c', '8b1a61b7-4bbe-584e-b715-9fb6727ff50a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('46521bbe-a8a1-57d1-bfc9-c6b3fad67d5e', 'ec910efe-89a0-5d45-b6bd-e5f789d63d66', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('cd3f73ce-bdef-5f25-a3a7-8dc88b93c6df', 'ec910efe-89a0-5d45-b6bd-e5f789d63d66', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('b1e9e85e-e663-5ec1-84cf-194bbb636012', 'efb80b56-095d-59da-ba77-451039eddd19', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('b6b9caa9-197e-5adb-bdca-20327881a137', 'efb80b56-095d-59da-ba77-451039eddd19', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('64db8ffd-2f29-507f-9a18-51cff0cb651d', 'ee46ff27-f693-574a-b41f-167ffbdd2081', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('68506e54-6e9c-5f35-92a3-40cfeb437391', 'ee46ff27-f693-574a-b41f-167ffbdd2081', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('7daf1fe1-6ed7-5d46-95a1-be74714b6b6d', 'c91b3cb5-3871-5a6a-be0f-a26b482e4406', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('6dbf6e0f-8388-581a-99fc-9f2ee2da12d4', 'c91b3cb5-3871-5a6a-be0f-a26b482e4406', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('dbe60efe-c715-5cd6-87e3-b7aa506948cc', '324facb1-f4ac-594d-bed7-ad5b6d91bad0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('183ef249-c64e-5969-b528-6e62575c5aac', '324facb1-f4ac-594d-bed7-ad5b6d91bad0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('ef9e7187-66a7-53a0-b52e-c5d568cb74b8', '606e4c3d-187e-50a0-970d-824ea555d519', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, NULL, NULL, NULL),
	('ab3d5cc2-022e-5b7a-a798-5eb913911313', '606e4c3d-187e-50a0-970d-824ea555d519', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, NULL, NULL, NULL),
	('0c440929-fd65-5533-8975-9be6d10d952e', '04279cbf-2527-5012-9301-fd65c76fbd13', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('2044f9dc-e052-5a6d-8866-b0416e4bb866', '04279cbf-2527-5012-9301-fd65c76fbd13', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('3d57299b-6ec0-5481-81eb-4e6d1315a348', '7b0da06f-102f-55f5-ad72-6d269d0825e8', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('5a3d2acd-35c3-5315-9dcd-23a91e7a01a9', '7b0da06f-102f-55f5-ad72-6d269d0825e8', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('a7bab4aa-8a1d-5be4-81af-f189d5e783b7', '4e411401-3c16-5c3a-81a5-f3b3353c2567', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('951becdb-6507-5e8d-a8cd-eb703c68895c', '4e411401-3c16-5c3a-81a5-f3b3353c2567', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('c6e26687-a4e3-58b1-a86e-a11942d2e7ad', '3300a364-02e6-556e-8386-3fb66b102993', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('52d7ddf0-549e-5e44-af86-b428c1fc1fd8', '3300a364-02e6-556e-8386-3fb66b102993', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '198.0', 'LG', NULL),
	('77bdd211-1ad8-5892-881b-42ff5eeacde4', '5fccac1d-8fa4-5ff7-a396-671281af9e9a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('70a00061-0ba8-5e52-b6ba-c88eeb8a8b69', '5fccac1d-8fa4-5ff7-a396-671281af9e9a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('84f23ed8-f63b-539a-92de-809f33555df5', '8f7c1c34-0ba4-5d09-acf3-dc2cac57c04f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('edb59eb9-6215-575b-8ca0-b14da60ed594', '8f7c1c34-0ba4-5d09-acf3-dc2cac57c04f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('0900fb61-0f68-563d-bc6b-a600bdec3d7e', 'af2374c3-2c0d-5b36-afcd-3afb2509ced6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('7e27d27d-ef22-5d43-8907-887482ee2d0a', 'af2374c3-2c0d-5b36-afcd-3afb2509ced6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('171fccf2-542c-51b2-8398-ee9bb363a235', 'd8bf9cd1-651b-531c-8faa-b239931763f2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('49c1b527-63ff-5d46-a507-a74f17d0198e', 'd8bf9cd1-651b-531c-8faa-b239931763f2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('b88d6917-df35-5948-b57f-376dde744559', '188aacfd-8e77-54f4-8889-b3164ae2a0c8', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('4ec8d097-f8dd-5b11-b333-68ab4b236e36', '188aacfd-8e77-54f4-8889-b3164ae2a0c8', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('41487e29-3aae-56bf-abba-7cf8c5bbc8c9', '4487b165-a3b7-50f8-9995-08ca921ed5da', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('95b470b0-5270-5bf4-b1dd-e091a418eb75', '4487b165-a3b7-50f8-9995-08ca921ed5da', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('20e2941a-8bc4-501a-b1e6-0feb87f44dca', '9e3ee6ef-a18f-5a32-889c-401c14252c09', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('038339bb-ea56-5fe7-9f21-b0e2dc93fcf9', '9e3ee6ef-a18f-5a32-889c-401c14252c09', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('746deef8-a53c-5e6d-ac9d-173f9fbfc853', '440d9b2d-9f4a-58cd-93d3-82d1374a21a2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('0b214808-18c4-50f8-834c-1cbd14122ffd', '440d9b2d-9f4a-58cd-93d3-82d1374a21a2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('3ca65997-89b5-5266-88ce-a7cd6db1276d', '22ce1580-c9c6-5ce0-9e81-5230626bf301', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('25ac9b66-cd52-58da-9d87-44eab622d255', '22ce1580-c9c6-5ce0-9e81-5230626bf301', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('fa3bf808-9fc9-5e74-a580-2c9cf4d6b8db', 'f2d6ebdf-a3be-5c32-8209-355026e2bd9b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('b7612557-8b5f-5032-a138-584021bb8b08', 'f2d6ebdf-a3be-5c32-8209-355026e2bd9b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('33fefc5e-d354-5a05-94fc-a68dd6466cee', '9d678ad5-cd14-52a8-9668-cafe03d14bd6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('ef7e9f8b-64c6-5eec-9395-c92c5c0ba726', '9d678ad5-cd14-52a8-9668-cafe03d14bd6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('a12975a9-d23b-5259-b038-df4c10c7f984', '8cc03f1f-45a8-5d5f-9de8-790ff617bb27', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('ea055567-a0c6-5e60-aae7-718ed1bf456e', '8cc03f1f-45a8-5d5f-9de8-790ff617bb27', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('94eab35b-6d8c-5c00-8c34-89dfd1421bf9', '1811e8df-f8b2-5949-83b4-0ebfef3c5f9e', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('0a521b8c-0833-5023-ad6f-59097b394010', '1811e8df-f8b2-5949-83b4-0ebfef3c5f9e', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('66f3ec5c-9419-53f7-a5ff-75e1f68b044a', '80d5ab38-1f94-5f86-bc99-7c1b182e7f49', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('e20e20cf-21bc-5a51-bd9b-236ad7c20f97', '80d5ab38-1f94-5f86-bc99-7c1b182e7f49', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '191.0', 'R', NULL),
	('893aa575-6c14-5f18-b7e7-2ccba374ad16', '1cc0cf7c-8a57-5e3d-954c-320a68f7daee', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('18140fb5-9f07-5fbf-a341-777f979ffce0', '1cc0cf7c-8a57-5e3d-954c-320a68f7daee', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '202.0', 'DG', NULL),
	('e86bfadd-0a45-5328-b577-911ffe2b1e31', 'e7569ced-4a9a-5982-b1ce-ba918f51143c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('162f3d31-97ef-5a71-9f86-c6259f8e3d49', 'e7569ced-4a9a-5982-b1ce-ba918f51143c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '212.0', 'DG', NULL),
	('025389da-dc7a-5658-802e-781758eb2577', 'b272431d-23f5-5ade-acb5-14c7f6d96666', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('50cc2f4f-59f0-51c2-a6b8-2d2e5fd97aca', 'b272431d-23f5-5ade-acb5-14c7f6d96666', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '181.0', 'Y', NULL),
	('27fbbdf9-82f8-5beb-9fbe-f823cefad0ca', '8a4e1655-3c1a-52d5-82e8-00a5420e215f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('874bf436-6df1-5422-9873-c6ab0989e8a1', '8a4e1655-3c1a-52d5-82e8-00a5420e215f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('6ee2fa08-e956-5723-addc-2ae22a88bda1', 'abd1c4d8-dff4-58f3-98e0-7e8fcfb55487', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('4c4777d8-fc01-579f-a680-a94337d99878', 'abd1c4d8-dff4-58f3-98e0-7e8fcfb55487', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('5f153031-30cb-5759-a837-3baa5417f1b3', '1788d350-505f-5bc8-baea-20bd2281fb56', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('7fc71ab7-0206-5dd6-98a6-1b1b97a138f9', '1788d350-505f-5bc8-baea-20bd2281fb56', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('247528f1-2f01-5ff0-aee1-f1ac0da8dda5', '5bec0514-8852-522d-95e4-327a82fb456f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('073a9d81-b423-5e4f-a959-56b31298ab7a', '5bec0514-8852-522d-95e4-327a82fb456f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('b6308eea-dff1-5e57-bfbc-060c4f963771', '49fd2065-3801-517d-b0e0-f6fc48582c7c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('bf964a9e-65c8-5a2f-a94b-682ec7e30b24', '49fd2065-3801-517d-b0e0-f6fc48582c7c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('daac9c53-9ce7-52ef-a5b3-daf039b944e2', 'f541e6e8-f24c-50ea-b110-2686fd37789e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('ba0e3be1-d120-5b4d-901c-ed48f1ad8441', 'f541e6e8-f24c-50ea-b110-2686fd37789e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('12b206ce-bcf0-5bf3-8daf-3f81444e8bf0', '1f472c11-b07b-546f-b751-7aae3208bb5a', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('1d9f04ed-1930-5124-bb2f-cc311f7bf850', '1f472c11-b07b-546f-b751-7aae3208bb5a', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('49ac8dbd-d129-5774-9c4b-6086d01c5670', '6841dc95-88d8-5025-9a8a-d8ab0b276b2f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('bf6b93d3-132d-569f-8860-704815502bd5', '6841dc95-88d8-5025-9a8a-d8ab0b276b2f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('3d883b10-4833-5904-8914-f4f74b417b78', '76cb1699-959b-5dab-b1de-2091b73453d7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('1af135fe-9110-5d9f-b719-1d146ff9ce25', '76cb1699-959b-5dab-b1de-2091b73453d7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('a6c37886-da14-565b-bb0a-94ac2f9b98ff', '5e470845-dc26-56dc-af50-98eee5a6d4d9', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('948a6d6c-3977-50fb-93ff-e48627a4fb2c', '5e470845-dc26-56dc-af50-98eee5a6d4d9', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '206.0', 'DG', NULL),
	('ac7a669e-33e5-568b-95db-e8f10402197d', '14f8dfdf-3f6f-58ed-8996-dcdab7fe73c7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('e36afcde-d77b-5bc7-95ac-1933227c2f19', '14f8dfdf-3f6f-58ed-8996-dcdab7fe73c7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('137ed023-de78-516c-ad11-ed574afe0489', '985228f1-c9f7-5175-be28-423ce1bb5101', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('10761d58-5cdb-5969-87f7-816544014c23', '985228f1-c9f7-5175-be28-423ce1bb5101', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('e1e1df7e-a86b-58d6-b952-cf98caa6b3cc', '7cc4c77a-133f-5bdf-8427-4208020da9ac', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('42dddfb2-fe00-50db-b88f-57e33d47880c', '7cc4c77a-133f-5bdf-8427-4208020da9ac', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('bd941b85-6de1-55bf-84a3-8fb3fd964d6b', '5aa4f70b-9a83-5c48-957e-5fbb10f982b1', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('ebafc20c-8cc6-51df-b386-134b05f215ec', '5aa4f70b-9a83-5c48-957e-5fbb10f982b1', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('3beb79ec-ec20-59ae-825b-8a938cc51190', 'be39a1f4-7942-5bde-8e1e-624a712ab1ea', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('5a8117ca-9f86-5290-b9c3-1472d2fe8b3d', 'be39a1f4-7942-5bde-8e1e-624a712ab1ea', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('2513e836-5084-5578-b6aa-65466c8c66a1', 'b999479b-426f-53fd-93d8-469f1a4e3433', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('ee2a71d2-eae1-51cc-aedc-d3ae904d08ed', 'b999479b-426f-53fd-93d8-469f1a4e3433', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('ecfdfe0f-879c-506b-ae2f-7382dd35898c', '00e75189-b4a0-57d9-befe-03805f3195d4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('bf586382-2d1c-5446-9441-20ee7b235ff4', '00e75189-b4a0-57d9-befe-03805f3195d4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('7f6dfdfc-f172-5dab-b04e-c6e961e89f7c', 'eca16b84-71ac-5000-aa76-613ee23aca11', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('a5b31099-a924-57de-af67-f30f84775860', 'eca16b84-71ac-5000-aa76-613ee23aca11', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('36f8b62e-05e4-5b7e-8c5f-72a935cbce2b', '3144859d-0618-5847-866f-4223e028061d', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('1860dbe2-fe74-5040-a4fc-d6e2e0e49a8d', '3144859d-0618-5847-866f-4223e028061d', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('d8db546a-4f11-5ed3-8d5b-d1d9a48db439', '8dd3a208-eadf-5f77-8396-8958462fd5e2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('7b68bfcf-8ffa-55e7-ab47-8cc541301c59', '8dd3a208-eadf-5f77-8396-8958462fd5e2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('5761b8b5-5fe5-56b4-9c6a-8418cd5937db', 'a5b8282b-eff1-5d37-a1ab-86139b7efbd8', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('1e55a78d-2116-568f-919f-b5667f35c823', 'a5b8282b-eff1-5d37-a1ab-86139b7efbd8', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('099a9b0c-7b2d-531a-ac51-dc107863e4b2', 'b43e7769-e920-537c-bc20-bd328f70cfc4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('46f5f9b3-9f93-59cb-b9e0-9fbd94bb7038', 'b43e7769-e920-537c-bc20-bd328f70cfc4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('36f9671f-8e99-58a6-9d24-c41e5e45cb90', 'b0db1cd4-6564-5897-baf3-c181f0f146e9', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('e34ced9f-8838-516e-8311-e02b909c29b6', 'b0db1cd4-6564-5897-baf3-c181f0f146e9', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('4c3de976-c17a-503b-b1cd-0de0ef55a527', 'bf937056-5caa-513c-8dfd-ae9d7df22d52', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('6cebd1ab-670d-5551-aa8e-9edc3e5b8fae', 'bf937056-5caa-513c-8dfd-ae9d7df22d52', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('73fb7431-984b-5331-9c07-7095cf48fafd', '3d301cfd-3693-5fbc-9e7e-9ebc0e1bd711', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '77.0', 'LG', NULL),
	('7f5b2930-e54c-59f8-9cdf-c2c6601d8ae6', '3d301cfd-3693-5fbc-9e7e-9ebc0e1bd711', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('27d94f94-2a33-573f-9858-3c8028235309', 'dd05e038-3c29-5e36-9afe-cfd6b38008da', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('d0228279-274d-516c-b38e-299630ecbcb3', 'dd05e038-3c29-5e36-9afe-cfd6b38008da', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('21ce15d0-4591-53fe-8884-dd82e54d2a6b', '9b40e600-78db-5168-b194-7fb600ca9093', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('d7d490b6-6608-5c8d-80d3-395fe01c20e1', '9b40e600-78db-5168-b194-7fb600ca9093', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('f91045e7-6c5a-5b0d-bf48-d30ced90cff4', 'd9931e43-4e32-5f65-8ef2-c7dd49a70189', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('bed0202a-a1ad-5405-8bd3-5823f8af0778', 'd9931e43-4e32-5f65-8ef2-c7dd49a70189', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('f1e15efe-7d1c-544c-8c27-c6a073e625b0', '71f9db76-cd16-5491-8276-820b51db5b46', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('df079a6b-cc98-5efd-94bb-50abd08365f3', '71f9db76-cd16-5491-8276-820b51db5b46', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('3a5141de-2733-5887-98cc-63f3d3e8fc9e', '8e34609e-88a3-50be-b51d-4a78f53fa848', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('eae90775-3823-5e49-8300-46e42d9872c3', '8e34609e-88a3-50be-b51d-4a78f53fa848', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('379a0139-278a-52d8-a689-89477b875fe9', '868d2b61-adb7-524c-914e-27b2d349237c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('79f0bb89-13f1-57bf-a682-87f4bc259ec1', '868d2b61-adb7-524c-914e-27b2d349237c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('57cd1bcd-8067-529b-a7ee-e0281e74eb89', '9ec4269c-9819-5660-873e-98871330acbb', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('008d3163-a915-5d7d-9777-4d40c8a657f1', '9ec4269c-9819-5660-873e-98871330acbb', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('2d432fe4-54a2-57ab-9e77-7cabf8ed6c5c', '0a5a0e61-899d-5022-b151-abc68a702dfc', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('1bbc0bb5-c4a2-5307-b6fc-4cce811395bd', '0a5a0e61-899d-5022-b151-abc68a702dfc', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '190.0', 'R', NULL),
	('389718b8-85df-5016-9f19-c288b5cfda6b', '00bfa0dd-f469-509a-b061-48ef6bf1a11d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '69.0', 'R', NULL),
	('17e162aa-a736-5c53-a3cb-d4ad08a545df', '00bfa0dd-f469-509a-b061-48ef6bf1a11d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('c4d40b31-fc89-58ce-9e02-89416a638e45', 'b9053826-c4e6-5a4e-9452-d18914a0a477', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('277d1624-a11c-5805-96b7-754e9cd2a022', 'b9053826-c4e6-5a4e-9452-d18914a0a477', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('5f2981bb-bad6-55d3-8d72-7a62c5ed6ca3', '44e612e1-7be2-56a6-915f-8fbdb11e5e02', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('bc93d4a4-8d9a-5786-be44-e1129915e25f', '44e612e1-7be2-56a6-915f-8fbdb11e5e02', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('53c5e1c5-083f-517b-a038-8ea2542d93e5', '7c834658-59a5-506d-a829-fe84f80902f7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('82c13bd3-e122-54a5-9aa0-0e27b774578d', '7c834658-59a5-506d-a829-fe84f80902f7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('1e7042f3-0433-5650-8139-4f3540b7e1fd', 'b952a63f-d0f1-5148-a7cf-f1c6282c78a5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '77.0', 'LG', NULL),
	('9d1f727b-42c8-5d44-aaa8-ffbd9032ae8a', 'b952a63f-d0f1-5148-a7cf-f1c6282c78a5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '185.0', 'R', NULL),
	('d1f54ec3-9a75-531f-b95f-68632d096cdd', '24d7d8e2-91e6-5232-8c0a-bb052db990a2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('bf5b1de1-9b6e-5bc6-80b8-0ca1e2d7c8a6', '24d7d8e2-91e6-5232-8c0a-bb052db990a2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('a268b8b0-0765-5a49-a66f-fb5bb24cab66', 'd5addb3b-1d01-57b3-981d-26d91bd87b78', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('45480285-423a-5842-bf17-95eeec593a6a', 'd5addb3b-1d01-57b3-981d-26d91bd87b78', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('f8ea5a32-e7e6-57fe-9906-81b0f1575a78', '2bc990cb-91e5-5498-8f5a-27699137d415', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('ec2a2b52-252c-5821-9e6a-e4658730ed24', '2bc990cb-91e5-5498-8f5a-27699137d415', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('caef2c26-03db-5e70-93c5-88f493d7d867', '48311cdb-659b-5fed-b5f3-de5c7f64440e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('176173c6-60cf-587d-9072-f84dcaed3561', '48311cdb-659b-5fed-b5f3-de5c7f64440e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('6826dc7e-39bd-55a2-9e64-57e8318ee253', '5bff01d7-1ad9-55dd-bf4c-1c9f62b49ee1', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('fce8fd2a-77f0-5eb7-a63b-e37e8c2543b9', '5bff01d7-1ad9-55dd-bf4c-1c9f62b49ee1', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('31ad398b-98ac-5a0e-bf58-2a048765452f', '57e26209-e9ae-5292-94ad-4d43ed4d4ed2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('2e1b00d0-8329-560e-a8d1-ac0af6954fde', '57e26209-e9ae-5292-94ad-4d43ed4d4ed2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('f489ea9c-7626-51bf-a1bf-b50d226389ff', '2fa437f9-14a8-5930-a81d-47d5ecf74d43', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('5f505584-99ca-5be2-a169-d4ff50d27db8', '2fa437f9-14a8-5930-a81d-47d5ecf74d43', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('1067ce48-60c2-5f17-8e4a-83c7e8fe6267', 'e2899075-dbbe-5fc0-8fb9-352eb8cb2021', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('f94f9970-1d12-5352-ad11-6216cde1b64d', 'e2899075-dbbe-5fc0-8fb9-352eb8cb2021', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('edce1629-4f94-51ca-91c6-0673157bc347', '4f58ee0d-4543-5dd3-b2ec-6973334dabd1', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, NULL, NULL, NULL),
	('d1820018-dc60-5374-a767-2b244ecbc787', '4f58ee0d-4543-5dd3-b2ec-6973334dabd1', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, NULL, NULL, NULL),
	('e9a86639-424b-5170-b764-40426d502cb1', 'fba74048-55b0-55ce-8811-8d0ff4e701b0', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('6aa06e9f-84ab-5fd2-b3c3-357af02ea28a', 'fba74048-55b0-55ce-8811-8d0ff4e701b0', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('17927448-dc90-50d8-9f56-d2bbc7f0501c', '0484e2b9-d638-556b-a25c-f6e0042f5f65', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('cbac2fef-0a2c-52d7-b95e-1cd4e37cc49a', '0484e2b9-d638-556b-a25c-f6e0042f5f65', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('5300bc7c-4ecd-5367-b65d-70191c1d31c4', 'e4e51787-716b-50e2-b560-7109adc55797', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('b6c65428-a0fc-5ac6-98fa-9316adc099c2', 'e4e51787-716b-50e2-b560-7109adc55797', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('2a23340b-c455-5fb0-a1c2-d5ee6a65f149', '2e5c122d-4faf-5daf-a9ec-11d94702d28f', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('2127f7c8-b004-553e-b41b-6cf054024516', '2e5c122d-4faf-5daf-a9ec-11d94702d28f', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('e6b8e06f-5631-52cb-bdc7-362bde745120', '97b29591-41ef-557b-8501-afc1d0712f20', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('be84d64c-c47c-5578-a6f1-21cd14cb2ae1', '97b29591-41ef-557b-8501-afc1d0712f20', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('e196126e-af96-5b2d-bd87-bcc5f6f75292', '5c93a9f7-46f2-54f4-873a-60282fc6eee7', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('d1455548-39b2-504c-8fe1-8e1a79f242a6', '5c93a9f7-46f2-54f4-873a-60282fc6eee7', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('69ed22d0-8210-524c-ae3d-1dd259db5661', '0bce6863-3f59-5f54-994c-ef3d1c4ce244', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('1330adef-6b05-59b6-b1e5-304847430bbf', '0bce6863-3f59-5f54-994c-ef3d1c4ce244', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('aa493fc6-44c5-5369-9394-ef718d81c759', '6377fd7a-f293-5fb1-993b-3f7801e39516', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('26a5e862-d0a6-53be-80ed-fe362f0abee3', '6377fd7a-f293-5fb1-993b-3f7801e39516', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('fb807b58-720d-5d8d-baeb-af50d9f4e2ba', 'e3f3f62a-fa30-5979-a989-566b4a87275e', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '84.0', 'DG', NULL),
	('5b9262be-a332-5f4f-a853-bef534cc0441', 'e3f3f62a-fa30-5979-a989-566b4a87275e', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '215.0', 'R', NULL),
	('86817277-2511-5e9a-8ba8-9dc173c5f249', 'fd999337-e2a6-5804-b605-5500a1eeef36', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '70.0', 'R', NULL),
	('c4849e69-9a28-556a-8b82-ea5cf8b830dd', 'fd999337-e2a6-5804-b605-5500a1eeef36', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('8906b678-bde7-5c7a-90fd-eb2935de76f7', '866ec21e-71aa-5ff2-b47a-2427a004e167', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('d5e07c73-5edc-507a-b263-62773ea677cc', '866ec21e-71aa-5ff2-b47a-2427a004e167', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('df0ed54c-4a22-5221-9865-6469f25fcfa7', '1bc05d2e-6418-5f28-a304-8f09fe01c611', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('0879e25c-fb6a-5424-a521-e2598a2cb2d8', '1bc05d2e-6418-5f28-a304-8f09fe01c611', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('17c26e2d-c6d7-52ec-8eb7-b92d800234b2', 'e9f65fbd-95d8-505b-901f-3aa08a537506', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('7d283175-61ef-5e1e-8bcf-b9e0b99e330c', 'e9f65fbd-95d8-505b-901f-3aa08a537506', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('1587f94f-dc96-57a0-a3c3-79e1794ea8bc', '150912f3-12ab-50cb-a4db-a2fc0eee3b1a', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('cb6a42d8-b49e-5584-ac55-4ee2c0e51377', '150912f3-12ab-50cb-a4db-a2fc0eee3b1a', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('9c19454b-70cc-5849-970a-b235ef5ee40a', 'b87f0d6b-72e1-5d84-a6e2-876ce4d4ee97', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('acca0be2-2dd5-52ec-8d82-da005d1efa5a', 'b87f0d6b-72e1-5d84-a6e2-876ce4d4ee97', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('ea058190-2890-54ad-a1cc-5d3e9de9dc16', '770c1f75-8bdb-541f-8efb-7e6e9c36da79', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('dc3eadd7-3281-5593-bf6f-b1c4953cccaa', '770c1f75-8bdb-541f-8efb-7e6e9c36da79', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('9d96b721-68b0-5dae-be9d-7c0916fec89f', '68c3e21f-4aeb-5583-b092-e6f00e286894', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('9be2e346-9682-56ff-9e7a-924f532bf22c', '68c3e21f-4aeb-5583-b092-e6f00e286894', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('a4576da6-7617-5ed2-93b4-f7ef33f4a13c', 'a6aaa1a9-2612-5e3b-84a4-85b04951e8f3', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('2b694d1c-b965-5c2f-b014-b24c2220c7cb', 'a6aaa1a9-2612-5e3b-84a4-85b04951e8f3', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('ac291224-7107-513f-b3d9-a5f45d4d87aa', 'dd2ee258-f7bb-52f5-918f-abcf8ac88bae', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('d76ba012-2839-521a-816c-06a14e8a0b29', 'dd2ee258-f7bb-52f5-918f-abcf8ac88bae', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('4b169e08-8216-5fde-a4cb-c34ab5bc9332', '51b2052a-ded5-52bf-ad6b-f047a19db53b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('9c5249f1-01fb-584e-9e0b-8df0dc19dfe0', '51b2052a-ded5-52bf-ad6b-f047a19db53b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('5c17e3b9-5260-5e2b-b14d-756a6ba83aa6', 'b611d767-ee8e-5f64-b0a6-1e8fee0db027', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('4183217a-9d73-54dc-b108-fdf6eaa84f6a', 'b611d767-ee8e-5f64-b0a6-1e8fee0db027', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '250.0', 'DG', NULL),
	('77a0947b-547d-5f01-bf24-cb608f7cfc9a', 'd569b35f-cab0-503b-8e0e-8414f9b04f31', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('7e75de40-870d-537d-8fac-b48ddf8dd9fd', 'd569b35f-cab0-503b-8e0e-8414f9b04f31', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('be2e78f3-99b3-5f46-8eca-2bad1194a387', '89f3de1c-1b8d-5a70-8147-68617d741e57', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('554c2cde-cd2f-5134-b6ce-379221741a6a', '89f3de1c-1b8d-5a70-8147-68617d741e57', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('3deb1051-8403-52be-be14-da583c4d030e', 'e89ae6e1-1aa0-52b1-886e-417b31b1905e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('7cd229b1-caf3-5216-9632-be11c31333df', 'e89ae6e1-1aa0-52b1-886e-417b31b1905e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('9676fc5a-dbca-5441-aabc-0a99b7dd9a2e', '95331e16-7304-57a5-93a2-c236af5d7f7d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('fe0c7f8b-87c3-5c71-a319-aed8e21e2909', '95331e16-7304-57a5-93a2-c236af5d7f7d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('4f38372e-83f0-545b-b742-9dfcae57cb01', '306deebf-562c-5a6d-9bde-dc9a10a986c9', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('62594ce4-6af6-5b56-9527-9dd37391f9a6', '306deebf-562c-5a6d-9bde-dc9a10a986c9', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('18f1b281-c835-502b-b9ef-a101ff7b43da', '1683b836-6a0f-5932-8bbb-04a734910f90', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('7685eeec-305a-5c5a-ad03-108c79da3b11', '1683b836-6a0f-5932-8bbb-04a734910f90', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('ec87b2c9-805a-5982-8cd5-c032894ae567', '0e7881fa-f4d7-5271-864a-1e6848d9a8d8', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('05e71b10-fe91-5259-945c-be514cd8c037', '0e7881fa-f4d7-5271-864a-1e6848d9a8d8', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('b3b9e3c8-24bb-5449-a477-0f4f18275269', 'd90718a6-d100-56dc-b017-00d18a5ddea8', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('4b703738-ae08-55f7-829c-d1df1c1476eb', 'd90718a6-d100-56dc-b017-00d18a5ddea8', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('fbc2a812-e73f-5d3b-8ae3-308395bba4e7', '3e4c3565-131d-551a-b5cb-2c85d1bb3019', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('6ca84f9b-7254-5e73-ab5f-36f9f809fe87', '3e4c3565-131d-551a-b5cb-2c85d1bb3019', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '255.0', 'DG', NULL),
	('e3ed926f-4d8e-54a4-8784-5f6dc6801113', 'afda4a41-76b3-5cf9-80ae-17052a38dbbd', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('237f185b-5068-50ac-8054-e14cf753fa4c', 'afda4a41-76b3-5cf9-80ae-17052a38dbbd', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('c164e63c-86ab-5f59-8417-3f31dea3a970', '0bf82a83-f240-5989-ba3b-c820a646ba10', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('250e37a7-d1ca-518a-9446-ccc7da81c02e', '0bf82a83-f240-5989-ba3b-c820a646ba10', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '240.0', 'DG', NULL),
	('5e527f6e-7763-5960-b060-f6f559b91ad2', 'bf0dfda0-1d15-583a-9797-037dfd9ae1e9', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('dab19254-ebd9-5ef7-86fb-14d523b939ae', 'bf0dfda0-1d15-583a-9797-037dfd9ae1e9', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('3ef88062-7584-58bb-a878-5d8fd3539abe', '74d79be1-7e71-514e-9f88-425cb646e126', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('59377168-9b1f-58ef-bae2-8677bdc73fb7', '74d79be1-7e71-514e-9f88-425cb646e126', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('baf7480b-8619-5de9-b58e-a814098761a8', 'dd49eb29-a9db-5249-955e-b915ec21ff06', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('bc28cea9-d423-5a51-9a1e-40cf81a4cc87', 'dd49eb29-a9db-5249-955e-b915ec21ff06', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('0aba2449-29e8-51a2-bd93-a47e55c28e4a', 'a1b41c07-8847-599e-b47d-40c905f60176', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('3e071a41-5adf-5b7e-858d-0d42782bb850', 'a1b41c07-8847-599e-b47d-40c905f60176', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('1cf1a9de-e2b9-581f-af27-d6005fd0546f', '81df608b-5b72-52d2-a9f9-83dc263cc9d3', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('b1ddc3f4-938d-53c0-9164-fdb6df4a0910', '81df608b-5b72-52d2-a9f9-83dc263cc9d3', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('939040f2-c064-50cf-9d00-c756598e0202', 'e5c8162c-4649-5131-8446-cf0d789bf4bc', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('4a99a4b4-e4f1-5b7c-a04d-03d74f166520', 'e5c8162c-4649-5131-8446-cf0d789bf4bc', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('5a0fb39e-fe0e-58ee-9555-02bbd69e2cba', '9b363db4-a538-58f6-b239-bcc61dd54ebd', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('e8dd2324-bd46-51e9-b498-293d26f35aef', '9b363db4-a538-58f6-b239-bcc61dd54ebd', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('71c49899-43f2-5704-8001-976f841e741f', '885a25db-210d-5a72-adf0-37865a5f5625', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('1b0d5a2f-c804-555e-b40c-c58d6254adbf', '885a25db-210d-5a72-adf0-37865a5f5625', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('b3e13943-04dd-5ee5-b42f-9880a9c7ce6e', '3e8cac1f-9f03-5ba0-a48d-612e1706dbc6', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('9e685612-709b-591c-b087-ce59f9dbafc0', '3e8cac1f-9f03-5ba0-a48d-612e1706dbc6', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '245.0', 'DG', NULL),
	('b7acc283-f869-5c0a-8c5f-5cea941fecb2', '73185114-6982-5cbd-9ee7-0439b5054885', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('9ad974bc-af24-5ca1-b003-d6c6e52ea770', '73185114-6982-5cbd-9ee7-0439b5054885', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('28df6274-aae0-5732-8f8d-b43fcc3ecb4b', 'a8641766-b3ef-561d-8824-a96e7a569571', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '80.0', 'DG', NULL),
	('43b7a67c-c2db-576d-84cd-20a5f6a2fa1e', 'a8641766-b3ef-561d-8824-a96e7a569571', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('f3ffd823-8204-5ff8-aa8a-83d0458fc5b7', '670fa4a3-9e4c-5724-8e22-3fa52ddc2f71', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('987b6d25-a34b-5bb3-a6a1-8618247f1e9b', '670fa4a3-9e4c-5724-8e22-3fa52ddc2f71', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('3413f524-7728-5b10-a0ed-949296083696', '61f47f9a-373c-5459-9154-f17c58e795ea', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('10d7fab0-e294-5a6d-a0d0-efcc17cc7970', '61f47f9a-373c-5459-9154-f17c58e795ea', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('851252d2-2b79-5c5a-a659-6485d55e15f2', 'aad0565e-e031-5217-a149-2fe2fb15e2d3', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('1f91e320-1f69-5aff-b997-f4e532c299c3', 'aad0565e-e031-5217-a149-2fe2fb15e2d3', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('bd372aa5-44ba-5fcb-b9b1-bbd73a033cdb', '0ab29c47-95ce-5232-9465-c5bd8f980d08', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('f8eddd28-40d8-5ff9-9a98-f56e52df5ea3', '0ab29c47-95ce-5232-9465-c5bd8f980d08', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('ecb50809-fa23-5ab8-b2b9-fd118d94e1aa', '382933ad-7943-545c-b66a-060f04483162', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('a7cfcad8-80d9-543c-ae36-6ce8e3a7b714', '382933ad-7943-545c-b66a-060f04483162', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('6f8d1f0d-16b8-5c50-96c7-4190c9d1772e', '153fbe63-9a88-5e98-a834-99b5c84e0069', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('81fb457e-2ba5-5dcc-bbc9-0805c1e25d0f', '153fbe63-9a88-5e98-a834-99b5c84e0069', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('e46d36d9-94d1-51ee-9c11-09f721fb933d', '9cf21507-a4ea-5232-ad65-f2e41a7009ce', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('76986611-27da-5b5f-a13d-7295568b16ab', '9cf21507-a4ea-5232-ad65-f2e41a7009ce', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('5a5f2301-69d1-571d-b6f4-2062dac3a236', '3f224a87-e595-5e4d-8ef1-f3a22ddbaab9', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('15659d5d-841b-58ad-8d0e-48f55e7b4646', '3f224a87-e595-5e4d-8ef1-f3a22ddbaab9', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('f0a02809-29c1-57f0-842d-2d77cbfa674d', '390298ef-c55a-5e79-9615-664508781150', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('6611ed39-ec0e-5a45-bdc6-ad96e831cc3f', '390298ef-c55a-5e79-9615-664508781150', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '225.0', 'DG', NULL),
	('772ecfac-fdc9-55ba-a8cd-7431c38a32ea', 'a0df649d-c859-586a-8794-add157f72708', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('fdb490cc-8ca0-596b-964a-1056b68dc3d0', 'a0df649d-c859-586a-8794-add157f72708', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('df87639d-4ce4-5fff-8c1a-51b94a67b51c', 'a07f9da6-b98b-5f1a-8844-517b2b6ac32d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('f67829e8-5cbd-5bbe-a5ff-786e0f6d83ae', 'a07f9da6-b98b-5f1a-8844-517b2b6ac32d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('897a89d7-3593-5681-8053-2556b479ac8d', 'fe7e7e56-06f4-5af9-bf99-3857e680cb65', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, NULL, NULL, NULL),
	('4c801570-6c9a-5a22-9360-6784b3416b1c', 'fe7e7e56-06f4-5af9-bf99-3857e680cb65', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, NULL, NULL, NULL),
	('82eec211-f5e2-5221-af69-cb7415967294', '3ed508ed-2da7-59a7-8276-84c055997ec9', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('24e1d6c8-1edc-50a9-a22a-66ec9704ddb9', '3ed508ed-2da7-59a7-8276-84c055997ec9', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('20177c52-4333-5d28-8747-a0ea55b5e9d0', '6d70c88b-93a0-5e57-99e9-4929a7d1839a', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('6a932cd2-a31d-5c56-8218-71fd1cb84c28', '6d70c88b-93a0-5e57-99e9-4929a7d1839a', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('62bb2a5a-f74b-5f3a-ad56-8b2c7a37e2a3', 'ed49fb5d-727b-53e9-8fc6-df5e49368c13', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('fbb67013-f56d-5ed0-93b7-4a4150172469', 'ed49fb5d-727b-53e9-8fc6-df5e49368c13', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('994447cb-2c9f-5a43-8662-53bf8176e908', '444cb8fe-6d6a-5f6d-8b81-591554421705', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '69.0', 'R', NULL),
	('7d12464c-d41a-50a3-880a-7eb9980a4569', '444cb8fe-6d6a-5f6d-8b81-591554421705', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '168.0', 'R', NULL),
	('c3b1e008-e968-555f-981e-84bc8c6e088b', '72ec4402-3152-525d-9345-70e9757d8ba0', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('432d50c6-bafc-531f-b28c-1ec5868d94a6', '72ec4402-3152-525d-9345-70e9757d8ba0', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('37311de1-7be9-5486-a3f2-bc35bea04e0f', '59a364c0-8c92-5fe1-9b88-3666020a8365', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('6719050b-3fed-526b-8a21-ca865448cda6', '59a364c0-8c92-5fe1-9b88-3666020a8365', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '230.0', 'DG', NULL),
	('feb16c91-d36c-5dd0-9b86-bb8967201a5c', 'c9e8bd71-0098-5790-8beb-2f86f68c3264', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('c2c6ea0a-8585-5076-88ba-e8b4d593b5b9', 'c9e8bd71-0098-5790-8beb-2f86f68c3264', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '198.0', 'LG', NULL),
	('8b239fa8-bd63-5a77-afb6-af32c2395ce7', 'c9813ed5-89e3-5d0d-a028-9bfe40b4556b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('3e173443-8d88-5cdd-82e5-cbe3d95aafc5', 'c9813ed5-89e3-5d0d-a028-9bfe40b4556b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('fac7e8e3-5169-5bbe-97e2-171e4e5d1136', '9c47df21-e997-577d-ae2c-e0c8c5b47d9b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('272fc37f-4566-50e4-ae6e-42f35356a2ad', '9c47df21-e997-577d-ae2c-e0c8c5b47d9b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('3ed2b713-34e7-5d53-a451-d89953151f73', '54d12513-b848-5446-a3ee-9c568f7b24cb', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('8b55cc23-fa3e-5dfd-88f5-9f2baba5761d', '54d12513-b848-5446-a3ee-9c568f7b24cb', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('432757ba-ff52-5888-a36b-81f592adea68', 'fbfe12f9-04ff-5b8b-946e-94d423063941', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('149fb745-f8ac-51a0-a152-f7c462ff18f4', 'fbfe12f9-04ff-5b8b-946e-94d423063941', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '220.0', 'DG', NULL),
	('18f0dcd0-6b2e-5afd-8429-9a4270f32c32', '0ce99b29-747b-51e7-acd2-0c9a3110f2ed', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('94850e26-6c7c-5e44-a300-038c193ae801', '0ce99b29-747b-51e7-acd2-0c9a3110f2ed', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '175.0', 'R', NULL),
	('9bff1763-7b4d-5d12-89e2-deddee8a0bd8', 'ef0ea3f5-9481-58dd-a11a-bfacbf62b2fd', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('09c23101-708c-5802-9cf1-8c192ff96a25', 'ef0ea3f5-9481-58dd-a11a-bfacbf62b2fd', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '172.0', 'R', NULL),
	('fbe0ad56-5a99-535a-9e9a-66d277817805', 'a56ba88e-dc8c-5577-803f-fd2f952e6b84', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '82.0', 'LG', NULL),
	('7f9fc781-b9f2-5408-a824-c6b841344c71', 'a56ba88e-dc8c-5577-803f-fd2f952e6b84', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '280.0', 'DG', NULL),
	('cb9800a5-2a7b-5b30-ad04-1791447641df', 'ec2f0671-579a-589e-9e5a-04fd8a269acf', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('109d2093-b882-5c55-9aee-e2c1bd0a28db', 'ec2f0671-579a-589e-9e5a-04fd8a269acf', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('793296bb-61d9-5a1d-8580-f44de29d6ace', '94b65e93-1d11-592d-a600-96bbf8b49592', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('17281de2-fa2d-5581-b178-76abe0f5876f', '94b65e93-1d11-592d-a600-96bbf8b49592', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('c4c325c9-659f-527f-9787-832e0c79fd93', '1d77d366-093e-57be-a928-f5958e98df16', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('9a0cf49b-36c3-5bd6-aa07-24309a72c204', '1d77d366-093e-57be-a928-f5958e98df16', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('026032c1-6c7d-518d-a3e6-d9d0d1184970', '9eedc62f-c5c4-58b7-9c44-c8c5ba913f2c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('b6823e20-d761-54c1-bb43-cd589152fcd6', '9eedc62f-c5c4-58b7-9c44-c8c5ba913f2c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '250.0', 'DG', NULL),
	('e814ba8a-7ce2-544a-9a6f-8deaeb0b4443', 'a00c43a2-0073-52e9-a103-a7f8728ce847', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('ae543459-2ddb-569e-8e40-0cc306c8f23e', 'a00c43a2-0073-52e9-a103-a7f8728ce847', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('1151418c-f0f7-5513-8bab-c62ff33ec52d', 'a111b071-93e6-57c5-b240-e4e56f9c5337', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '84.0', 'DG', NULL),
	('f9d6b56e-3c17-5379-bd4c-767fdbb8b4c6', 'a111b071-93e6-57c5-b240-e4e56f9c5337', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '250.0', 'DG', NULL),
	('01e15e24-ed0a-5265-8bf7-0549fb8de021', '58a70bd8-d1b1-5409-8ff8-7f7943e7f88e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('a626e390-4509-553e-86bc-ad94ef243b52', '58a70bd8-d1b1-5409-8ff8-7f7943e7f88e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('c26332aa-5591-50b9-b98d-5dc88b7ea260', 'd2ffd210-9bf3-5435-8581-abcfbbf59c28', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('d0b6f3d7-6cce-5d7c-ae15-881b0db714b2', 'd2ffd210-9bf3-5435-8581-abcfbbf59c28', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('66c06bbb-46ea-50af-9c05-a6dd1e0e8f6a', '150af5e9-a189-5a1c-a7a8-b9ae50c6f40c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('ef3192df-26d5-524a-9513-1fa8a5877321', '150af5e9-a189-5a1c-a7a8-b9ae50c6f40c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('16382a03-a22a-5414-bc86-5b16f7424f6e', '1f748fff-1163-532c-9084-23687dad2fe4', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('36779e4b-ec45-55aa-b14a-42529dd668d2', '1f748fff-1163-532c-9084-23687dad2fe4', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('81620520-b557-5d5a-a75d-e923cff8c6c4', '9e7552a0-4cd5-5a21-9368-77e107b47bbf', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('f81bc91b-3102-5825-af1f-18b214d13f51', '9e7552a0-4cd5-5a21-9368-77e107b47bbf', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('ac3e7ac8-23cf-58bf-b2ec-ac183d224529', '8b790ccc-f7dd-50c9-ac9e-cf332e42fe26', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('16e8cb74-f54c-5db8-9504-e468f2eda27a', '8b790ccc-f7dd-50c9-ac9e-cf332e42fe26', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('6e6bf418-3cf6-5133-8e85-ef1ec6d2086e', 'f94b6abc-ee98-5be1-9a5a-862ebac769ed', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('00269a71-e95b-509e-801c-b4c5491c41b2', 'f94b6abc-ee98-5be1-9a5a-862ebac769ed', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('9b3244ad-c59f-542b-906a-d8867f0db664', '08abd09d-72dd-5896-8ce8-da91a363fd62', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('744222fa-9968-5d66-a18b-26e3738ba823', '08abd09d-72dd-5896-8ce8-da91a363fd62', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('c8dd3c35-ac68-5b28-95b2-ab35f8398f6f', '661e80bf-39b4-56a1-aea6-bfa7d9a9b9a5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('da7539d0-6a40-5067-a82c-fbba20eac4cc', '661e80bf-39b4-56a1-aea6-bfa7d9a9b9a5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('5c69fc96-3101-5d3e-b038-968a4a4fdbc0', '7a0666f4-fc9e-55cc-a776-bdee4fd942f4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('802a97b1-d8db-5ef9-aa57-d1a2d78dd186', '7a0666f4-fc9e-55cc-a776-bdee4fd942f4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '165.0', 'R', NULL),
	('05884667-2d9b-5de3-bdf4-0597f8df76e6', '29cff5eb-5f88-5fe7-ad88-612bee0b9305', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('ae00478c-3263-5eda-ae49-5684af40e4bf', '29cff5eb-5f88-5fe7-ad88-612bee0b9305', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('92ec678f-5b97-55ce-9141-a39155dba1a7', '452712e5-7447-52f5-8b47-3db4284a51a6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('10a5bd34-e84f-563c-8af1-1d157de948ea', '452712e5-7447-52f5-8b47-3db4284a51a6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('c15258ec-0246-5165-97cb-34acb8920047', '4042e9be-9a91-5ce2-af17-2a5e46df01cc', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('754f96f1-6aaf-5585-88c3-a93842464d93', '4042e9be-9a91-5ce2-af17-2a5e46df01cc', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('ae73b251-b42e-5165-a338-14e040574dca', '0ffe14c2-06d9-58b5-bed4-3be8922c4cb5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('2b80e80a-3d24-52ef-918b-e8ba7ede4c0c', '0ffe14c2-06d9-58b5-bed4-3be8922c4cb5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('5256c19c-28b0-5467-a742-62c5801522ef', '3c3a3871-f9b4-5433-97f5-31adeb9a4629', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('aa34529a-e72a-5320-9194-cce88c7d1147', '3c3a3871-f9b4-5433-97f5-31adeb9a4629', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('a809b62d-5b77-59e8-8cc6-7a886337571b', 'c15b8c91-80b1-5f50-8b8e-efbdabe430f5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('c95e3424-8c92-58c0-a878-4d32cde71991', 'c15b8c91-80b1-5f50-8b8e-efbdabe430f5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '160.0', 'R', NULL),
	('55995ba8-7239-57e7-9604-0b41060fc361', 'c6a204ff-a260-5bab-add9-ff75db547211', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('97347cfc-f748-5101-ae7e-ee85fa4a49de', 'c6a204ff-a260-5bab-add9-ff75db547211', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('1467881a-ea8a-5a50-9ccc-b7e4a850f393', '8f8e1444-d7c2-5f45-b5bd-6a3bf7f61e18', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('66958356-fdba-524f-aea9-bf3d8c7de1d1', '8f8e1444-d7c2-5f45-b5bd-6a3bf7f61e18', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '250.0', 'DG', NULL),
	('0fb95312-637b-54ac-8979-8a1e3f0e34c6', '625aebb9-26d2-5ca9-838b-2f233761531e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('981eb1cd-8834-59d9-b1da-8d3ef0b7e26d', '625aebb9-26d2-5ca9-838b-2f233761531e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('08874f13-b17e-5405-b8dc-c511d2dc0119', 'ae5a4132-95c0-5776-b1b0-8c3476eb719a', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '79.0', 'Y', NULL),
	('2679f87d-005e-5996-a965-dbe6980aaa20', 'ae5a4132-95c0-5776-b1b0-8c3476eb719a', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '210.0', 'R', NULL),
	('dda01449-6b09-5c3f-b7c5-f85ad94e6897', 'f08f12c0-e6fa-58f3-b66d-f3598557a072', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('188a4187-e9cd-50cc-a131-1a9372811616', 'f08f12c0-e6fa-58f3-b66d-f3598557a072', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '225.0', 'Y', NULL),
	('1cb3bae5-8982-5ee8-ab02-879caf6c17bb', '58fbf7c9-42b2-5b7c-a457-566d1e278cc5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('c9bf7e31-b6c4-5f1a-b9a9-6c6554752775', '58fbf7c9-42b2-5b7c-a457-566d1e278cc5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '240.0', 'DG', NULL),
	('a4e68fc3-9e59-5fa2-9c2e-0f4d5d932862', 'f5ed35c4-7b51-5871-8564-893083c21c88', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('b86fa907-3cd7-5661-af67-91559a6fda42', 'f5ed35c4-7b51-5871-8564-893083c21c88', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '200.0', 'DG', NULL),
	('fb2cbc91-ee85-55f0-af6b-360419e7a32b', 'e12087a8-81d0-574a-8985-6c6068d710d4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('1bf35d1e-305e-56bb-9f53-836d0223a523', 'e12087a8-81d0-574a-8985-6c6068d710d4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('773949eb-746d-5b7a-830d-adbba27a8a64', 'dc1d42b2-c184-5b9f-a9dd-ad6b73e9084e', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('e3b70517-f033-5e11-83da-4d11cff6a96c', 'dc1d42b2-c184-5b9f-a9dd-ad6b73e9084e', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('de706f53-7631-53fd-bed9-7e310660eb60', 'f1607602-d227-592e-a911-3054701743ef', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('58dce2b3-b276-5027-95e3-b2c1f0ccb7ad', 'f1607602-d227-592e-a911-3054701743ef', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('796d4f04-8a82-57a1-8be7-a70d5fd4d8e4', '8c4b1728-ec26-534d-a65e-44cc5a7ca1e0', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('619d375a-fa96-561c-aaf2-034c1e402e74', '8c4b1728-ec26-534d-a65e-44cc5a7ca1e0', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('d424a3c8-44af-56fe-b7ae-9c89ea9fad26', 'ce2a4e46-bf5e-5123-84b1-11c2af568e33', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('5e991502-3694-531c-ae74-c945f4e27aac', 'ce2a4e46-bf5e-5123-84b1-11c2af568e33', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('ff93297f-6301-57c0-a26a-c8ce355b1800', '62ef868f-7208-5855-9709-32d2041bdb94', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '74.0', 'Y', NULL),
	('0f9093dd-7582-5f03-9097-b5fc6e6f6f3d', '62ef868f-7208-5855-9709-32d2041bdb94', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('c6724c97-e938-51a9-aa1a-72e732f0e4d8', 'c7f6bce0-215d-53b5-8e34-951a76e41801', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('156c4dd8-da34-543c-8e92-aa95d8ce9f39', 'c7f6bce0-215d-53b5-8e34-951a76e41801', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('5d7c8f5e-35d8-5d39-8432-6c2b4618fc2d', 'dccd0bc6-baee-5a7b-997a-596eff6176ee', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('89aec807-2984-5edd-9527-12058fbd3c33', 'dccd0bc6-baee-5a7b-997a-596eff6176ee', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('0a268948-bd80-5e56-b6f0-8de2fab39420', 'e12599e4-fc2d-5b41-bc86-8f4cd290e6ad', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('1329e573-7b45-5356-8e8a-dcbc9666acad', 'e12599e4-fc2d-5b41-bc86-8f4cd290e6ad', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('0057e988-d468-56cb-b6c0-fb09428adcd3', 'fe5fed0e-9a3a-52e4-9a77-23a67ecba25b', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('e0d5b334-7138-510a-83ec-2f018cec698e', 'fe5fed0e-9a3a-52e4-9a77-23a67ecba25b', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL) ON CONFLICT DO NOTHING;
INSERT INTO public.attribute_grade VALUES
	('4a028fad-00b5-5271-b0fc-1b2c28375a96', '95522c4d-fce7-5244-bbd6-c239fed00ae8', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('249fde1d-5a66-5ab8-8a8a-7bdb7fecafde', '95522c4d-fce7-5244-bbd6-c239fed00ae8', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('9cc340fa-8307-528e-89c4-38ed789831f2', '90f302c1-852d-55a6-893e-5ad8cf20c9d2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '71.0', 'R', NULL),
	('517f96df-3b4b-54e5-86af-d736546011e2', '90f302c1-852d-55a6-893e-5ad8cf20c9d2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('e3861a81-5c79-5c99-9a8c-18a153946736', '9e4ca190-b0f9-5492-8264-5ca81f5cd71c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('ffb11ce2-6b14-53a4-88be-bcb3b093f5b7', '9e4ca190-b0f9-5492-8264-5ca81f5cd71c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '245.0', 'DG', NULL),
	('c2e23ad0-30e2-51e4-9a65-afd4d25b3d25', '3cc9cd9b-5471-5c20-bdd8-a27c6627cc99', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('a507670d-679e-5319-b497-7994bae430c7', '3cc9cd9b-5471-5c20-bdd8-a27c6627cc99', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('776a28d3-9e8c-5789-b48f-ec6c822ddc1a', 'f4d8e160-ebc2-52e8-86f9-a3b98375a19c', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '83.0', 'DG', NULL),
	('7fe66d5b-712f-5395-9d71-e72505f2f90b', 'f4d8e160-ebc2-52e8-86f9-a3b98375a19c', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '235.0', 'LG', NULL),
	('eb801d3a-a8a1-5194-a086-f0ef673b2f7f', '15ccd3af-81a2-54d9-ad77-8cd8dff2e785', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('c7269ff5-4727-58bc-8d5e-37f074f1e5fb', '15ccd3af-81a2-54d9-ad77-8cd8dff2e785', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('4c2491dd-6883-5e4b-89c3-835882996bd0', '6e07b064-6cea-5ba3-987b-dd3792f8cb0d', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('c0b04fc6-9c1e-5258-b141-a3e27394584d', '6e07b064-6cea-5ba3-987b-dd3792f8cb0d', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '235.0', 'DG', NULL),
	('f7dcb5ed-6c78-53cb-9d0b-ed9600f22ea7', '1474fd7b-14cf-5739-aa00-e24195e86985', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('81917d89-5b97-5905-80b1-e00ae9038d10', '1474fd7b-14cf-5739-aa00-e24195e86985', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('1ab565b3-a5d5-5bee-854f-40224d6e257f', '1305fcae-300b-579e-ba5a-5c0e4b400bfc', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('e7b43da5-4401-5ae6-81a1-7b58914d1d79', '1305fcae-300b-579e-ba5a-5c0e4b400bfc', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('df0b5898-a126-53d9-ad72-f08e902af3d0', '86b95577-badc-5737-8e29-c31cb01ed1e5', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('82bf4602-d391-5f55-ae64-623589479f1a', '86b95577-badc-5737-8e29-c31cb01ed1e5', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('d2f27edd-b423-56f4-a476-e6cdce7e1fe2', '59c5e573-6e24-5042-a0fc-a253893a9a1f', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('9a9ea8aa-0dbf-5808-9252-081ab0d25c8f', '59c5e573-6e24-5042-a0fc-a253893a9a1f', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '210.0', 'LG', NULL),
	('dca593c9-a849-5e93-99a3-6e976bc6a60a', 'c66b1f64-d9be-5d3e-835b-944675831df6', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('badf497e-0f70-55df-9973-3b71bc6e743c', 'c66b1f64-d9be-5d3e-835b-944675831df6', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '165.0', 'R', NULL),
	('3dcf63dd-ce54-530c-8f94-833989be3c44', '2d1ffd7c-0865-5792-9080-8e7d586fb57c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('8b91851e-33ac-5ecd-8383-2983cc6f39a4', '2d1ffd7c-0865-5792-9080-8e7d586fb57c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '170.0', 'R', NULL),
	('8a0f70f5-1407-55fd-89e5-64e3054cb6f5', 'ef77f0a0-ae5d-5fd6-a931-c6d170a5646b', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('dcc45e26-8340-50e7-9713-8e1ab8d26c42', 'ef77f0a0-ae5d-5fd6-a931-c6d170a5646b', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '175.0', 'R', NULL),
	('8cefc500-5546-52e9-9e9b-7de284fa8ee4', '8b5c56c4-ebeb-5cf1-8402-020d7e72d45c', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('e0f598e6-f1f7-584f-9f06-161e1459b6bb', '8b5c56c4-ebeb-5cf1-8402-020d7e72d45c', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('920ee44b-da07-52ae-ae69-dd9c8b9376d4', '2d6e8595-fcea-5c01-8f5d-a9737f24b360', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '81.0', 'DG', NULL),
	('b2e12ce8-4d40-5bab-a305-cceb93c1700f', '2d6e8595-fcea-5c01-8f5d-a9737f24b360', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('2f90b195-3f27-54b7-b412-d35402aad1bb', '76a1b2a4-61d0-5d93-b59a-0bdba401655c', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('1d4537dc-fcbc-54be-9808-c7b51dc4be7b', '76a1b2a4-61d0-5d93-b59a-0bdba401655c', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('7a4e1a5b-1394-503e-80ae-4f9ef3a4b4f6', 'ae039a06-5fa0-5eea-8558-e99f8d817cef', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('c4460d93-351d-5e78-b504-38cee006f5ac', 'ae039a06-5fa0-5eea-8558-e99f8d817cef', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '255.0', 'DG', NULL),
	('2d2c00f8-f699-5783-b6f0-df96639da45c', 'feb5ec28-260a-5d31-999f-aaa3f82afd5a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('d2bab4d2-757e-5cef-9623-c4c7f94cf35a', 'feb5ec28-260a-5d31-999f-aaa3f82afd5a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('c4a1bb5f-5f0f-5a61-922c-42a993e11196', '4bd3ad65-d93f-5669-8ac3-7d2fbf5f7377', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('726b531b-3ad3-5b28-baf3-0a6c6dbe2caa', '4bd3ad65-d93f-5669-8ac3-7d2fbf5f7377', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('479015c6-cc33-533d-9d67-75f42e913faf', '75a594a2-b384-5382-b495-0cf2418cc797', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '76.0', 'LG', NULL),
	('66e6ef6b-bdc6-5693-a71b-b479e157c40d', '75a594a2-b384-5382-b495-0cf2418cc797', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('eebd6463-5f0b-5c52-a5d7-4dea52a09568', '256057a3-7fd9-591d-bd4e-6510c1e617ac', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '82.0', 'DG', NULL),
	('027a99a8-c149-5493-a518-2c81b2549b97', '256057a3-7fd9-591d-bd4e-6510c1e617ac', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('312f0c18-2b4c-5747-900d-2cc45bcfdec7', 'c94e7fdf-c52e-5f67-a397-cf740b0c6bab', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('10ed23e5-7ad8-5895-8d0e-9ba5fab92d17', 'c94e7fdf-c52e-5f67-a397-cf740b0c6bab', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('f9724140-05f0-5e6b-886c-1f0e499271f3', 'd1c9ebaa-bf7d-5b50-89af-0eb9c5b95e0a', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('3af20934-4a8d-574d-952f-2abfecc589b1', 'd1c9ebaa-bf7d-5b50-89af-0eb9c5b95e0a', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
	('056abec0-32a4-57ed-9856-0f014bd647e5', 'ef510008-817b-5929-a739-055df104eb0d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('60988213-bb7a-5a23-b951-d7626ca7f20a', 'ef510008-817b-5929-a739-055df104eb0d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '215.0', 'DG', NULL),
	('a76f4778-1ccb-550a-8a66-1e4815e58c02', '111c8432-c425-5e84-9dba-8eb549d19cc2', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '80.0', 'DG', NULL),
	('2e76b917-988d-5686-a296-d7222c00bf37', '111c8432-c425-5e84-9dba-8eb549d19cc2', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '205.0', 'LG', NULL),
	('2d74cf39-54a2-5709-baae-5a397c9e7c50', '88fa88aa-c0b3-57bb-928a-97cf325b9b82', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('2842b9e8-5a01-55ec-bcf3-5faf38da5c77', '88fa88aa-c0b3-57bb-928a-97cf325b9b82', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '240.0', 'DG', NULL),
	('41d5017d-a096-5bb9-b74f-9ec7165d6cd2', '95a122b9-9d48-57d5-ab04-41b82d8a8eb8', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '79.0', 'DG', NULL),
	('0e9bf54b-d189-5d00-b0e5-858767981893', '95a122b9-9d48-57d5-ab04-41b82d8a8eb8', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '225.0', 'DG', NULL),
	('9cd235fb-0f4d-54bb-8c62-971168fa2bad', '19455758-876b-5db6-a997-0b24ef5fbf90', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('87e20305-364c-5ecf-88c0-e371e5fb3aac', '19455758-876b-5db6-a997-0b24ef5fbf90', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '182.0', 'Y', NULL),
	('8638313f-a78c-5137-a39d-04fc954810f3', 'ec8ea5a8-3856-532e-8583-fadb239943f4', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('54dbf4d5-b810-59f1-bb30-b4f4ecc570c9', 'ec8ea5a8-3856-532e-8583-fadb239943f4', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('7e197243-b0b9-5e8c-8889-f572ad53269c', 'cfca5fc5-129f-54d7-b066-32b51c925132', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('a045c36c-b364-5204-8775-f02eca5bb192', 'cfca5fc5-129f-54d7-b066-32b51c925132', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('f4d415af-b898-582c-b1f4-3d3bde45ca0a', '87517441-f1c8-5a34-bf3a-15ec077b4e83', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '78.0', 'LG', NULL),
	('92a7444d-bcf0-546f-bdae-639324127bf8', '87517441-f1c8-5a34-bf3a-15ec077b4e83', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '195.0', 'Y', NULL),
	('a76142ea-ac18-59dc-88c2-74ae8101ad81', 'b8cee345-6cfc-556b-8674-68dacfad1903', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '81.0', 'DG', NULL),
	('8d63519b-84ce-57c4-b715-a7b69626b655', 'b8cee345-6cfc-556b-8674-68dacfad1903', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '215.0', 'DG', NULL),
	('16342dc6-5d5e-5799-8c07-2cbef237f47d', 'c0bec325-1993-5362-8db3-a903fb7e9b40', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '73.0', 'Y', NULL),
	('38768e4f-0eeb-5cfa-b95a-b574dd4e27ae', 'c0bec325-1993-5362-8db3-a903fb7e9b40', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('7d4eee43-430a-531f-8f2b-ba5a7de9f330', 'ebbb9ab4-826f-5758-85fc-d725be46597e', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '85.0', 'DG', NULL),
	('1beed730-36ec-591c-a6d9-bdef04caa01d', 'ebbb9ab4-826f-5758-85fc-d725be46597e', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '241.0', 'LG', NULL),
	('7c521b4a-d7d5-5ebe-91ff-d24efbf10b3f', '962e4649-39cb-5b2c-8de9-ec90f5e8b92e', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('a6cae289-c6a2-5665-bbc6-04d0e721cb51', '962e4649-39cb-5b2c-8de9-ec90f5e8b92e', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('515c07b8-6ccf-5e40-b07e-cd939bdabd84', '9fa243bd-d6eb-53db-8027-13237fbd5ce2', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('98e78dbb-8eb5-5af0-b977-c270e15decce', '9fa243bd-d6eb-53db-8027-13237fbd5ce2', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('2dd24e6c-0789-5850-9b33-bf651c62edeb', '17bf36ad-fba8-5720-bf90-d9064ed1944d', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('4fae665b-f279-51e4-b4b1-f08e2654dd37', '17bf36ad-fba8-5720-bf90-d9064ed1944d', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('6e8485f1-ca6c-5bc8-b2b2-97322711b745', '38a456da-1d18-5594-9173-bc800ea3c198', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '72.0', 'R', NULL),
	('44736b33-ec42-5489-a299-d725cef4ea5a', '38a456da-1d18-5594-9173-bc800ea3c198', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('e4841293-ce7b-59a9-a3b5-493bc11f42f9', '8e70171d-a017-5a0c-bbb7-492b6f6c76d1', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('4247d95f-fc4c-584d-bab6-b1b85ab1633a', '8e70171d-a017-5a0c-bbb7-492b6f6c76d1', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('5ac45b6a-9979-5885-b784-08ec6ee50c58', '8dddc432-d769-5108-9f52-07c27ac05a69', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('3b1c7f37-f697-56e4-ab35-02d2bb575669', '8dddc432-d769-5108-9f52-07c27ac05a69', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '205.0', 'DG', NULL),
	('a2558e30-fcf2-5766-a84c-012a7edad8a4', '0a4a6589-693d-5b1e-bb0b-efe82db16666', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '79.0', 'DG', NULL),
	('dbde350c-ce07-5f2c-b832-7a821044d9b8', '0a4a6589-693d-5b1e-bb0b-efe82db16666', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '220.0', 'DG', NULL),
	('45cf2e31-9f77-5691-acaf-319407955dd1', 'd2576f25-6e47-58fe-9b7a-aa4363ee08ba', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('b98e961f-581f-506c-91ac-542662d2fa32', 'd2576f25-6e47-58fe-9b7a-aa4363ee08ba', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('49ce765e-5493-5cae-b235-60d5db7b8bd4', '2e41c008-1648-57b6-b2b3-70af27bc0ad6', 'c595f8a5-ddf9-585c-b137-b73b833da085', NULL, NULL, '84.0', 'DG', NULL),
	('7ab141c0-d4ce-5ae3-bc08-0fa73f3b8802', '2e41c008-1648-57b6-b2b3-70af27bc0ad6', '6ff5b127-7ffa-5fcc-82c1-28428f721d25', NULL, NULL, '270.0', 'DG', NULL),
	('5ef351d0-7799-5cf3-ac31-c954accb92d6', '31d85c55-41e3-5316-99f4-f6580dc12470', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('823b9851-9fb5-511a-82a1-350eb18ffcd0', '31d85c55-41e3-5316-99f4-f6580dc12470', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '180.0', 'Y', NULL),
	('f9e2bbde-ec23-5bae-a843-2b6154e59797', '260a0f7c-f424-5b68-91d8-302ff6b410fa', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '84.0', 'DG', NULL),
	('e2108d57-7b57-5087-907f-84b9f2249d0a', '260a0f7c-f424-5b68-91d8-302ff6b410fa', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('c290d3b0-b500-59a1-833e-43bd53627f20', 'ed005fe3-7dae-55cd-8f7a-7673dbc16ad4', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('7296cc67-582b-5245-ade7-fecb7d712dc4', 'ed005fe3-7dae-55cd-8f7a-7673dbc16ad4', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('3f40014d-feaa-56ed-b8c8-f1ec28c3d5e9', 'de7aa144-4284-5038-812d-2d723f794fb3', '1e75bf24-b32e-54a8-98cb-7f7d95bc16a8', NULL, NULL, '83.0', 'DG', NULL),
	('15e21d48-d7ba-5f51-b627-2cb62dd2e154', 'de7aa144-4284-5038-812d-2d723f794fb3', '58a18bb2-5040-5660-8e4b-3bdebfef0d1a', NULL, NULL, '200.0', 'Y', NULL),
	('3647d8c7-e918-5408-ad1f-6a10b162b120', '32ac568f-4da6-5201-b8c8-af7052ca8cc5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('5c05271a-e3c7-5e9e-9950-60fc4c2ae016', '32ac568f-4da6-5201-b8c8-af7052ca8cc5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '195.0', 'LG', NULL),
	('78be4aec-0b05-5e7f-bbef-c9d7582b9bfe', 'a2248904-1ad9-557d-a3aa-20f213f12984', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '78.0', 'DG', NULL),
	('1825908e-818a-5f32-8c12-c4f255d25bf5', 'a2248904-1ad9-557d-a3aa-20f213f12984', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('3c498aa6-6dfe-54f1-88e6-62006dc1b663', 'dae87909-5d5b-58f5-8032-4355761ca8b5', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '77.0', 'DG', NULL),
	('18945a3c-ed16-5d22-aa69-141c7ed936e7', 'dae87909-5d5b-58f5-8032-4355761ca8b5', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '210.0', 'DG', NULL),
	('bb3b21d8-7a04-59ba-82a5-b708c875b243', '04f4c9c8-0475-596e-8e1f-3f1d0396b8a7', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('b9ee7df4-d7e7-5d02-91eb-99b036ab5f92', '04f4c9c8-0475-596e-8e1f-3f1d0396b8a7', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '190.0', 'LG', NULL),
	('06468732-2fee-580c-9dd2-a4b74e2f46e7', 'd37b2016-91e2-5b75-b0d3-da14f6e24435', '13b71f82-37ae-5198-ac5d-683ac4707910', NULL, NULL, '75.0', 'LG', NULL),
	('51b4a5ae-0582-5bb0-9d2d-e0e1dda0e345', 'd37b2016-91e2-5b75-b0d3-da14f6e24435', 'be9fe335-05a5-5821-9138-89a2102c2844', NULL, NULL, '185.0', 'Y', NULL),
