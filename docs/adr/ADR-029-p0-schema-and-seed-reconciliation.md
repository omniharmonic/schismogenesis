# ADR-029: P0 schema and seed reconciliation

Status: accepted for P0, pending Benjamin's review at the P0 gate. Date: 2026-10-31.

## Context
Building P0 from the docs exposed places where they disagree with each other or with the data.
`0001_initial` stays a verbatim copy of 08a §A1 and §A1.1, and a test enforces that. Everything
below lives in `0002_reconcile` or in the seed loader, so each deviation is reviewable by itself.

## Decisions
1. **Landmark counts are 818 and 54, not 817 and 53.** D-31.9 added bayeslord to the slice file but
   not to SEED-v4. The decisions log outranks the Plan and Architecture, so `arena seed verify`
   expects 818 and 54. Docs 08 §12.1, 09 §4.0 (G0.3) and SPINE §8 still show the old numbers.
2. **Six tables and one schema were missing.** SPINE §10.3 names `rate_bucket`, `gpu_window`,
   `admin_approval` and schema `ops`, and 08 defines them, but §A1 omits them, so `0002` adds them.
   `gold_item`, `gold_label` and `gold_adjudication` have no definition anywhere; they wait for
   P2-W1-01, which owns them. The Plan's note that they are "already in `0001_initial`" is wrong.
3. **Two constraint defects are fixed.** `cluster_lineage`'s primary key forced `to_cluster_id` to
   NOT NULL, which made `fades` rows impossible although §A1 says that column is null for them.
   `proposition_relation`'s UNIQUE let duplicates through because bank-scope rows have a null
   `episode_id`. Both now use unique indexes with NULLS NOT DISTINCT.
4. **Provenance.** `chunk`, `encounter`, `statement` and `cluster_snapshot` gain the spine's
   `prompt_id` and `prompt_version`. Eight tables (`cluster`, `cluster_membership`,
   `niche_cluster_crosswalk`, `cluster_lineage`, `live_question_proposition`,
   `contribution_score`, `reputation_score`, `understanding_cell`) carry provenance only through
   their parent snapshot or scoring run, as 08a designs them. A test lists them explicitly, and
   every new table must be classified. Strictly, spine §5 says "every derived row", so this is a
   question for the gate.
5. **Secondary niche roles.** 107 of 137 secondary links have no role in the seed. They load as
   `bridger`, the most common explicit value (21 of 30), at weight 0.5, with
   `basis = 'seed:default_role'` so they can be found and corrected. This touches OD-04.
6. **`panel_status` follows the OD-30 default:** verified-active and unflagged landmarks are
   `core_panel`; the rest are `newcomer`.
7. **Reloads can hide, never expose.** On update, `public_surface_allowed` is the old value AND the
   new one. A takedown survives a reload. The cost is that a sign-off under OD-01 or OD-02 must be
   applied after any reload that re-flags someone, which is the safe direction.
8. **Free-text niche references.** Seed `combatants` and `adjacent_niches` are names, not ids. Only
   exact, unambiguous name or alias matches become ids; the full text stays in `niche.raw`.

## Environment notes
- Host port 5544, because 5432 and 5433 are in use on the dev Mac.
- MinIO is not in compose: `minio/minio` is denied on Docker Hub, including `latest`, and neither
  tag tried on quay.io exists (checked 2026-10-31). SPINE §10.8 expects an object store, and P1
  transcript storage needs one, so the replacement is an open decision.
- WAL archiving waits for P4, because the pgvector image has no pgbackrest.
