-- ===================================================================
-- 0. Extensions, schemas, enums
-- ===================================================================
CREATE EXTENSION IF NOT EXISTS vector;        -- pgvector >= 0.7 (halfvec)
CREATE EXTENSION IF NOT EXISTS pg_trgm;       -- fuzzy alias search
CREATE EXTENSION IF NOT EXISTS citext;
CREATE SCHEMA IF NOT EXISTS private;          -- transcript text; not granted to arena_public

CREATE TYPE stance_source      AS ENUM ('stated','implied_by_act','inferred');
CREATE TYPE stance_value       AS ENUM ('affirm','reject','conditional','steelman_only');
CREATE TYPE tl_attitude        AS ENUM ('accepts','rejects','suspends','accepts_conditionally','accepts_for_argument');
CREATE TYPE stance_strength    AS ENUM ('tentative','leaning','confident','certain');
CREATE TYPE layer              AS ENUM ('ontological','epistemic','axiological','empirical','praxis');
CREATE TYPE relation_type      AS ENUM ('supports','contradicts','depends_on','reframes');
CREATE TYPE item_status        AS ENUM ('live_provisional','operator_approved','released','canonical',
                                        'participant_confirmed','participant_contested','rejected','retracted');
CREATE TYPE appearance_role    AS ENUM ('host','co_host','guest','panelist','moderator','debater','clip_subject');
CREATE TYPE mention_type       AS ENUM ('present','discussed_only','clip_only');
CREATE TYPE reaction_vote      AS ENUM ('agree','disagree','pass');
CREATE TYPE contribution_kind  AS ENUM ('note','steelman','synthesis');
CREATE TYPE synthesis_subtype  AS ENUM ('bridge_proposal','better_question','clean_disagreement');
CREATE TYPE helpfulness        AS ENUM ('helpful','somewhat','not_helpful');
CREATE TYPE snapshot_horizon   AS ENUM ('daily','weekly','monthly');
CREATE TYPE actor_kind         AS ENUM ('person','agent');
CREATE TYPE run_status         AS ENUM ('running','succeeded','failed','partial','cancelled');

