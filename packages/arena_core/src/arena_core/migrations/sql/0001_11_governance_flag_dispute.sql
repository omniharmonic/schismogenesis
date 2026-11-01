-- ===================================================================
-- 11. Governance: flag (dispute)
-- ===================================================================
CREATE TABLE flag (
  flag_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  raised_by_type  text NOT NULL CHECK (raised_by_type IN ('user','landmark','operator','rights_holder','admin')),
  raised_by_id    text NOT NULL,
  kind            text NOT NULL CHECK (kind IN ('thats_not_me','placement_dispute','landmark_annotation','anchor_misattribution',
                     'proposition_unfaithful','niche_label_dispute','takedown','harassment','coordinated_rating','privacy')),
  target_type     text NOT NULL,                  -- claim | proposition | stance | landmark | contribution | episode | cluster
  target_id       text NOT NULL,
  text            text NOT NULL,
  state           text NOT NULL DEFAULT 'open' CHECK (state IN ('open','triaged','accepted','rejected','annotated','withdrawn')),
  sla_due_at      timestamptz NOT NULL,
  public_annotation text,                         -- landmark annotation shown beside a placement
  resolution      text, resolved_by text, resolved_at timestamptz,
  label_example_id uuid,                          -- every accepted correction becomes a gold-style example
  created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX flag_open ON flag (state, sla_due_at) WHERE state IN ('open','triaged');

