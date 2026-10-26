-- =====================================================================
--  Role (Step 1) — PostgreSQL schema
--  Spec: Impact on Winning, Model Math Update v9.1 (2 Oct 2026)
--
--  Layers:
--    1. Reference      : teams, players, games
--    2. Raw inputs     : possessions (on-floor fives), player_season_counts,
--                        torvik_player_season
--    3. Derived        : player_season_possessions, national_assist_share
--                        (empty after seeding; your pipeline computes them)
--    4. Config         : model_constants
--    5. Outputs        : player_onfloor_shares, player_group_scores,
--                        role_placement
--    6. Dummy only     : dummy_truth  (hidden archetype used to generate data)
-- =====================================================================

DROP SCHEMA IF EXISTS role CASCADE;
CREATE SCHEMA role;
SET search_path TO role;

-- ---------------------------------------------------------------------
-- 1. REFERENCE
-- ---------------------------------------------------------------------

CREATE TABLE teams (
    team_id        INTEGER      NOT NULL,
    season         SMALLINT     NOT NULL,
    team_name      TEXT         NOT NULL,
    conference_id  INTEGER,                      -- NULL = not D1 that season
    PRIMARY KEY (team_id, season)
);

CREATE TABLE players (
    player_id      INTEGER      PRIMARY KEY,
    player_name    TEXT         NOT NULL
);

CREATE TABLE games (
    game_id        BIGINT       PRIMARY KEY,
    season         SMALLINT     NOT NULL,
    game_date      DATE         NOT NULL,
    home_team_id   INTEGER      NOT NULL,
    away_team_id   INTEGER      NOT NULL,
    season_type    SMALLINT     NOT NULL,        -- 2 = regular season (the only one Role reads)
    tournament_id  INTEGER,                      -- NOT NULL = conf. tournament / March → excluded
    has_shot_tags  BOOLEAN      NOT NULL DEFAULT FALSE  -- 2026 ESPN tagged feed (~64% of games)
);
CREATE INDEX ON games (season);

-- ---------------------------------------------------------------------
-- 2. RAW INPUTS
-- ---------------------------------------------------------------------

-- One row per possession, both fives.  Input three (teammate shares) and
-- possession counts come from here.
CREATE TABLE possessions (
    game_id        BIGINT       NOT NULL REFERENCES games(game_id),
    possession_no  INTEGER      NOT NULL,
    season         SMALLINT     NOT NULL,
    off_team_id    INTEGER      NOT NULL,
    def_team_id    INTEGER      NOT NULL,
    off_p1 INTEGER, off_p2 INTEGER, off_p3 INTEGER, off_p4 INTEGER, off_p5 INTEGER,
    def_p1 INTEGER, def_p2 INTEGER, def_p3 INTEGER, def_p4 INTEGER, def_p5 INTEGER,
    garbage_time   BOOLEAN      NOT NULL DEFAULT FALSE,
    PRIMARY KEY (game_id, possession_no)
);
CREATE INDEX ON possessions (season);

-- Input one: counted behaviours per player-season (counts only, never rates).
-- 2026-only tagged columns are NULL in earlier seasons.
CREATE TABLE player_season_counts (
    player_id          INTEGER   NOT NULL REFERENCES players(player_id),
    season             SMALLINT  NOT NULL,
    team_id            INTEGER   NOT NULL,
    -- possessions on the floor are NOT here: computed from `possessions`
    -- into player_season_possessions by the pipeline

    -- available every season
    assists            INTEGER   NOT NULL,
    ast_to_three       INTEGER   NOT NULL,
    ast_to_rim         INTEGER   NOT NULL,
    ft_trips           INTEGER   NOT NULL,
    transition_fga     INTEGER   NOT NULL,
    steals             INTEGER   NOT NULL,
    blocks             INTEGER   NOT NULL,
    drb                INTEGER   NOT NULL,
    orb                INTEGER   NOT NULL,
    putbacks           INTEGER   NOT NULL,

    -- shots by zone (for assisted share and derived play types)
    fga_rim            INTEGER   NOT NULL,
    fgm_rim            INTEGER   NOT NULL,
    fgm_rim_ast        INTEGER   NOT NULL,
    fga_mid            INTEGER   NOT NULL,
    fgm_mid            INTEGER   NOT NULL,
    fgm_mid_ast        INTEGER   NOT NULL,
    fga_three          INTEGER   NOT NULL,
    fgm_three          INTEGER   NOT NULL,
    fgm_three_ast      INTEGER   NOT NULL,

    -- 2026 tagged play types (NULL before 2026)
    driving_layups     INTEGER,
    pullups_2          INTEGER,
    pullup_range_2s    INTEGER,
    floaters           INTEGER,
    pullups_3          INTEGER,
    plain_rim_fga      INTEGER,
    plain_rim_fgm      INTEGER,
    plain_rim_fgm_ast  INTEGER,
    tip_ins            INTEGER,
    hooks_turnarounds  INTEGER,
    alley_oops         INTEGER,                  -- stored, in no group yet

    PRIMARY KEY (player_id, season),
    CHECK (fgm_rim   <= fga_rim   AND fgm_rim_ast   <= fgm_rim),
    CHECK (fgm_mid   <= fga_mid   AND fgm_mid_ast   <= fgm_mid),
    CHECK (fgm_three <= fga_three AND fgm_three_ast <= fgm_three),
    CHECK (ast_to_three + ast_to_rim <= assists),
    CHECK (putbacks <= fga_rim)
);

-- Torvik attributes per player-season
CREATE TABLE torvik_player_season (
    player_id       INTEGER   NOT NULL REFERENCES players(player_id),
    season          SMALLINT  NOT NULL,
    team_id         INTEGER   NOT NULL,
    height_in       NUMERIC(4,1),               -- NULL = unknown (passes both guardrails)
    min_pct         NUMERIC(5,2) NOT NULL,      -- qualified needs >= 40
    usage           NUMERIC(5,2) NOT NULL,
    three_pa_share  NUMERIC(5,4) NOT NULL,      -- 3PA / FGA, 0–1
    PRIMARY KEY (player_id, season)
);

-- ---------------------------------------------------------------------
-- 3. DERIVED  (empty after seeding — the Python pipeline fills these)
-- ---------------------------------------------------------------------

-- Possessions on the floor per player-season.
--   from possessions JOIN games, where season_type = 2, tournament_id IS NULL,
--   NOT garbage_time; tagged_off_poss = offensive poss in games with has_shot_tags
CREATE TABLE player_season_possessions (
    player_id        INTEGER   NOT NULL,
    season           SMALLINT  NOT NULL,
    team_id          INTEGER   NOT NULL,
    off_poss         INTEGER   NOT NULL,
    def_poss         INTEGER   NOT NULL,
    tagged_off_poss  INTEGER,                    -- 2026 only, NULL before
    PRIMARY KEY (player_id, season)
);

-- National assisted share by zone, the shrink target (a = (ast + 5n)/(makes + 5))
--   ast_share = sum(fgm_<zone>_ast) / sum(fgm_<zone>) over player_season_counts
CREATE TABLE national_assist_share (
    season     SMALLINT  NOT NULL,
    zone       TEXT      NOT NULL CHECK (zone IN ('rim','mid','three')),
    ast_share  NUMERIC(6,4) NOT NULL,
    PRIMARY KEY (season, zone)
);

-- ---------------------------------------------------------------------
-- 4. CONFIG
-- ---------------------------------------------------------------------

CREATE TABLE model_constants (
    spec_version  TEXT     NOT NULL,
    key           TEXT     NOT NULL,
    value         NUMERIC  NOT NULL,
    note          TEXT,
    PRIMARY KEY (spec_version, key)
);

INSERT INTO model_constants (spec_version, key, value, note) VALUES
('9.1','MIN_PCT_QUALIFIED',   40,    'Torvik minutes % for qualified'),
('9.1','MIN_POSS',            300,   'offensive possessions for qualified / read'),
('9.1','PREV_SEASON_WEIGHT',  0.5,   'ROLE_DEF_PREV_W, established players'),
('9.1','SHRINK_K',            5,     'assisted-share shrink over 5 makes'),
('9.1','SHARE_MIN_POSS',      200,   'min possessions for lead/inside shares'),
('9.1','SHARE_MIN_READS',     4,     '4 of the 5 on his side need a read'),
('9.1','SHARE_THRESHOLD',     0.50,  'lead / inside / front cut'),
('9.1','DEF_CLOSE',           0.10,  'close-call gap'),
('9.1','H_WING',              77,    '6''5"'),
('9.1','H_67',                79,    '6''7"'),
('9.1','H_GUARD_MAX',         80,    '6''8"'),
('9.1','THREE_SHARE_SPEC',    0.60,  'shooting rule: 60%+ shots are threes'),
('9.1','DRB_PCTL_HIGH',       0.60,  'shooting rule 1'),
('9.1','DRB_PCTL_LOW',        0.50,  'shooting rule 2'),
('9.1','STEAL_SHOOT_MARGIN',  0.05,  'shooting rule 5');

-- ---------------------------------------------------------------------
-- 5. OUTPUTS  (written by the Python pipeline)
-- ---------------------------------------------------------------------

-- Input three result
CREATE TABLE player_onfloor_shares (
    player_id     INTEGER   NOT NULL,
    season        SMALLINT  NOT NULL,
    valid_poss    INTEGER   NOT NULL,           -- possessions with 4+ reads on his side
    lead          NUMERIC(5,4),                 -- NULL = missing (< 200 valid poss)
    lead2         NUMERIC(5,4),
    inside        NUMERIC(5,4),
    inside2       NUMERIC(5,4),
    front         NUMERIC(5,4),
    PRIMARY KEY (player_id, season)
);

-- Stage A–B result, one row per player-season-group
CREATE TABLE player_group_scores (
    player_id     INTEGER   NOT NULL,
    season        SMALLINT  NOT NULL,
    group_name    TEXT      NOT NULL CHECK (group_name IN
                  ('creation','self_creation','shooting','steals',
                   'def_glass','blocks','inside')),
    sample        TEXT      NOT NULL DEFAULT 'current'
                  CHECK (sample IN ('current','three_season')),
    raw_score     NUMERIC(6,4),
    group_score   NUMERIC(6,4),
    proposed_role TEXT,
    PRIMARY KEY (player_id, season, group_name, sample)
);

-- Final Role output + audit trail
CREATE TABLE role_placement (
    player_id         INTEGER   NOT NULL,
    season            SMALLINT  NOT NULL,
    primary_role      TEXT      NOT NULL,
    secondary_role    TEXT,
    family            TEXT      NOT NULL CHECK (family IN ('Guards','Wings','Bigs')),
    confidence        TEXT      NOT NULL CHECK (confidence IN ('normal','low')),
    fallback          BOOLEAN   NOT NULL DEFAULT FALSE,
    rules_mode        TEXT      NOT NULL CHECK (rules_mode IN ('full','coarse')),
    pooled_off_poss   INTEGER,
    winning_group     TEXT,
    top3_groups       JSONB,                    -- [{"group":..,"score":..,"role":..}, ...]
    decided_by        TEXT,                     -- 'clear' | 'creator' | 'interior' | 'length' | 'larger_sample' | 'volume' | 'fallback'
    top4_play_types   JSONB,                    -- [{"play_type":..,"pctl":..}, ...]
    lead              NUMERIC(5,4),
    inside            NUMERIC(5,4),
    spec_version      TEXT      NOT NULL DEFAULT '9.1',
    computed_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (player_id, season, spec_version)
);

-- ---------------------------------------------------------------------
-- 6. DUMMY ONLY — the archetype each dummy player was generated from.
--    Use it to sanity-check your pipeline; drop it for real data.
-- ---------------------------------------------------------------------
CREATE TABLE dummy_truth (
    player_id   INTEGER   NOT NULL,
    season      SMALLINT  NOT NULL,
    archetype   TEXT      NOT NULL,
    PRIMARY KEY (player_id, season)
);
