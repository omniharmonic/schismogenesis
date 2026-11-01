-- ===================================================================
-- 7. Map: cluster_snapshot, cluster, cluster_membership, crosswalk, lineage
-- ===================================================================
CREATE TABLE cluster_snapshot (                   -- the spine's Snapshot
  snapshot_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  public_id       text UNIQUE NOT NULL,           -- '2026-W48', '2026-11-27-d'
  horizon         snapshot_horizon NOT NULL,
  as_of           timestamptz NOT NULL,
  data_window     tstzrange NOT NULL,
  bank_version    int NOT NULL,
  panel_season    text NOT NULL,
  params          jsonb NOT NULL,                 -- clustering params, thresholds, seeds
  model_versions  jsonb NOT NULL,
  agent_free      boolean NOT NULL DEFAULT false, -- true for the re-fit without agent_provenance inputs
  parent_snapshot_id uuid REFERENCES cluster_snapshot(snapshot_id),
  validity        jsonb NOT NULL DEFAULT '{}',    -- silhouette, stability ARI, eye-test status
  status          text NOT NULL DEFAULT 'built' CHECK (status IN ('built','approved','published','withdrawn')),
  bundle_ref      text,                           -- path/URL of the published bundle
  bundle_sha256   text,
  run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
  model_name text NOT NULL DEFAULT 'code', model_version text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
);

CREATE TABLE cluster (
  cluster_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  local_index     int NOT NULL,
  label           text NOT NULL,                  -- provisional: best-aligned niche name
  label_status    text NOT NULL DEFAULT 'provisional' CHECK (label_status IN ('provisional','ratified')),
  n_landmarks     int NOT NULL, n_users int NOT NULL DEFAULT 0,
  centroid        real[] NOT NULL,                -- in the snapshot's 2-D layout space
  profile         halfvec(1024),                  -- mean proposition-embedding of affirmed propositions
  cohesion        real,
  UNIQUE (snapshot_id, local_index)
);

CREATE TABLE cluster_membership (
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  subject_type    text NOT NULL CHECK (subject_type IN ('landmark','user')),
  subject_id      text NOT NULL,
  cluster_id      uuid NOT NULL REFERENCES cluster(cluster_id),
  weight          real NOT NULL CHECK (weight BETWEEN 0 AND 1),    -- soft membership
  is_primary      boolean NOT NULL,
  coords          real[] NOT NULL,                -- 2-D position
  uncertainty     real NOT NULL,
  basis           text NOT NULL CHECK (basis IN ('content','reactions')),
  n_reactions     int,                            -- users only
  eligible_to_ratify boolean NOT NULL DEFAULT false,
  PRIMARY KEY (snapshot_id, subject_type, subject_id, cluster_id)
);
CREATE INDEX membership_cluster ON cluster_membership (cluster_id) WHERE is_primary;
CREATE INDEX membership_ratifiers ON cluster_membership (cluster_id) WHERE eligible_to_ratify;

CREATE TABLE niche_cluster_crosswalk (
  snapshot_id     uuid NOT NULL REFERENCES cluster_snapshot(snapshot_id),
  niche_id        text NOT NULL REFERENCES niche(niche_id),
  cluster_id      uuid NOT NULL REFERENCES cluster(cluster_id),
  share_of_niche_landmarks real NOT NULL,
  share_of_cluster real NOT NULL,
  jaccard         real NOT NULL,
  PRIMARY KEY (snapshot_id, niche_id, cluster_id)
);

CREATE TABLE cluster_lineage (
  from_cluster_id uuid NOT NULL REFERENCES cluster(cluster_id),
  to_cluster_id   uuid REFERENCES cluster(cluster_id),             -- null for 'fades'
  type            text NOT NULL CHECK (type IN ('continues','splits','merges','born','fades')),
  overlap         real NOT NULL, confidence real NOT NULL,
  computed_on     text NOT NULL DEFAULT 'core_panel',
  PRIMARY KEY (from_cluster_id, to_cluster_id)
);

