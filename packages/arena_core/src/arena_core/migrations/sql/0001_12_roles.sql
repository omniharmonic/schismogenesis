-- ===================================================================
-- 12. Roles
-- ===================================================================
CREATE ROLE arena_api        NOLOGIN;  -- read public tables, write human tables
CREATE ROLE arena_worker     NOLOGIN;  -- read all, write derived
CREATE ROLE arena_operator_ro NOLOGIN; -- SELECT on ops.* views only
GRANT USAGE ON SCHEMA private TO arena_worker;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA private TO arena_worker;
REVOKE ALL ON SCHEMA private FROM arena_api, arena_operator_ro;
