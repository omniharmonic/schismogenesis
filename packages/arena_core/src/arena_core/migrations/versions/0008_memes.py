"""Memes and cited figures, and how each person uses them (ADR-034)."""

from alembic import op

revision = "0008_memes"
down_revision = "0007_claim_argument_role"


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE meme (
          meme_id      text PRIMARY KEY,
          kind         text NOT NULL CHECK (kind IN ('concept','figure')),
          label        text NOT NULL,
          gloss        text,
          family       text,
          origin       text,
          patterns     jsonb NOT NULL,
          run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
          model_name text NOT NULL, model_version text NOT NULL,
          prompt_id text, prompt_version text,
          created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL
        );
        CREATE TABLE meme_use (
          meme_id      text NOT NULL REFERENCES meme(meme_id),
          person_id    text NOT NULL REFERENCES person(person_id),
          uses         int NOT NULL,
          rate_per_10k real NOT NULL,
          first_year   int,
          works        text[] NOT NULL,
          stance       text NOT NULL CHECK (stance IN
                         ('embraces','attacks','engages','mentions','unclear')),
          confidence   text NOT NULL CHECK (confidence IN ('high','low')),
          note         text,
          run_id uuid NOT NULL REFERENCES pipeline_run(run_id), stage text NOT NULL DEFAULT 'S11',
          model_name text NOT NULL, model_version text NOT NULL,
          prompt_id text, prompt_version text,
          created_at timestamptz NOT NULL DEFAULT now(), inputs_hash bytea NOT NULL,
          PRIMARY KEY (meme_id, person_id)
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE meme_use; DROP TABLE meme")
