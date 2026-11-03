"""SQL for rooms. Plain SQLAlchemy Core text queries against the 0009_rooms tables."""

import hashlib
import json
import secrets
import uuid

from sqlalchemy import Engine, text


def key_hash(key: str) -> bytes:
    return hashlib.sha256(key.encode()).digest()


class Store:
    def __init__(self, engine: Engine):
        self.engine = engine

    def ensure_room(self, slug: str, title: str, bundle: dict, config: dict | None = None) -> str:
        """Create the room if missing and make sure every anchor is an approved statement."""
        with self.engine.begin() as c:
            room = c.execute(text("SELECT room_id FROM room WHERE slug = :s"), {"s": slug}).scalar()
            if room is None:
                room = c.execute(
                    text(
                        "INSERT INTO room (slug, title, bundle_version, config) "
                        "VALUES (:s, :t, :v, CAST(:c AS jsonb)) RETURNING room_id"
                    ),
                    {"s": slug, "t": title, "v": bundle["version"], "c": json.dumps(config or {})},
                ).scalar()
            for anchor in bundle["anchors"]:
                c.execute(
                    text(
                        "INSERT INTO room_statement (room_id, text, origin, anchor_id, status) "
                        "VALUES (:r, :t, 'anchor', :a, 'approved') "
                        "ON CONFLICT (room_id, anchor_id) DO NOTHING"
                    ),
                    {"r": room, "t": anchor["text"], "a": anchor["id"]},
                )
        return str(room)

    def room(self, slug: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT room_id, slug, title, description, status, bundle_version, config "
                        "FROM room WHERE slug = :s"
                    ),
                    {"s": slug},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def counts(self, room_id, include_synthetic: bool = False) -> dict:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text("""SELECT
                  (SELECT count(*) FROM room_participant p WHERE p.room_id = :r AND (:syn OR NOT is_synthetic)) AS people,
                  (SELECT count(*) FROM room_statement s WHERE s.room_id = :r AND status = 'approved') AS statements,
                  (SELECT count(*) FROM room_vote v JOIN room_statement s USING (statement_id)
                    WHERE s.room_id = :r) AS votes"""),
                    {"r": room_id, "syn": include_synthetic},
                )
                .mappings()
                .one()
            )
        return dict(row)

    def join(
        self, room_id, key: str, handle: str | None, consent: str, synthetic: bool = False
    ) -> str:
        with self.engine.begin() as c:
            return str(
                c.execute(
                    text(
                        "INSERT INTO room_participant (room_id, key_hash, handle, consent_version, is_synthetic) "
                        "VALUES (:r, :k, :h, :c, :s) RETURNING participant_id"
                    ),
                    {"r": room_id, "k": key_hash(key), "h": handle, "c": consent, "s": synthetic},
                ).scalar()
            )

    def authenticate(self, room_id, participant: str, key: str) -> bool:
        try:
            uuid.UUID(participant)
        except ValueError:
            return False
        with self.engine.connect() as c:
            stored = c.execute(
                text(
                    "SELECT key_hash FROM room_participant WHERE participant_id = :p AND room_id = :r"
                ),
                {"p": participant, "r": room_id},
            ).scalar()
        return stored is not None and bytes(stored) == key_hash(key)

    def anchor_statements(self, room_id) -> dict[str, str]:
        with self.engine.connect() as c:
            rows = c.execute(
                text(
                    "SELECT anchor_id, statement_id FROM room_statement "
                    "WHERE room_id = :r AND origin = 'anchor'"
                ),
                {"r": room_id},
            ).all()
        return {a: str(s) for a, s in rows}

    def vote(self, participant: str, statement: str, vote: int) -> None:
        with self.engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO room_vote (participant_id, statement_id, vote) VALUES (:p, :s, :v) "
                    "ON CONFLICT (participant_id, statement_id) "
                    "DO UPDATE SET vote = EXCLUDED.vote, updated_at = now()"
                ),
                {"p": participant, "s": statement, "v": vote},
            )
            c.execute(
                text(
                    "INSERT INTO room_vote_event (participant_id, statement_id, vote) VALUES (:p, :s, :v)"
                ),
                {"p": participant, "s": statement, "v": vote},
            )

    def votes_bulk(self, rows: list[tuple[str, str, int]]) -> None:
        if not rows:
            return
        params = [{"p": p, "s": s, "v": v} for p, s, v in rows]
        with self.engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO room_vote (participant_id, statement_id, vote) VALUES (:p, :s, :v) "
                    "ON CONFLICT (participant_id, statement_id) "
                    "DO UPDATE SET vote = EXCLUDED.vote, updated_at = now()"
                ),
                params,
            )
            c.execute(
                text(
                    "INSERT INTO room_vote_event (participant_id, statement_id, vote) VALUES (:p, :s, :v)"
                ),
                params,
            )

    def statement_in_room(self, room_id, statement: str) -> bool:
        try:
            uuid.UUID(statement)
        except ValueError:
            return False
        with self.engine.connect() as c:
            return (
                c.execute(
                    text(
                        "SELECT 1 FROM room_statement WHERE statement_id = :s AND room_id = :r "
                        "AND status = 'approved'"
                    ),
                    {"s": statement, "r": room_id},
                ).first()
                is not None
            )

    def next_statements(self, room_id, participant: str, limit: int) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text("""SELECT s.statement_id, s.text, s.origin, s.anchor_id,
                          (SELECT count(*) FROM room_vote v WHERE v.statement_id = s.statement_id) AS seen
                        FROM room_statement s
                        WHERE s.room_id = :r AND s.status = 'approved'
                          AND NOT EXISTS (SELECT 1 FROM room_vote v
                                          WHERE v.statement_id = s.statement_id AND v.participant_id = :p)
                        ORDER BY seen, random() LIMIT :n"""),
                    {"r": room_id, "p": participant, "n": limit},
                )
                .mappings()
                .all()
            )
        return [{**dict(r), "statement_id": str(r["statement_id"])} for r in rows]

    def texts(self, room_id) -> list[str]:
        with self.engine.connect() as c:
            return [
                r[0]
                for r in c.execute(
                    text(
                        "SELECT text FROM room_statement WHERE room_id = :r AND status <> 'rejected'"
                    ),
                    {"r": room_id},
                )
            ]

    def statements_today(self, participant: str) -> int:
        with self.engine.connect() as c:
            return int(
                c.execute(
                    text(
                        "SELECT count(*) FROM room_statement WHERE author_id = :p "
                        "AND created_at > now() - interval '1 day'"
                    ),
                    {"p": participant},
                ).scalar()
                or 0
            )

    def add_statement(
        self,
        room_id,
        text_: str,
        author: str | None,
        origin: str = "participant",
        status: str = "pending",
    ) -> str:
        with self.engine.begin() as c:
            return str(
                c.execute(
                    text(
                        "INSERT INTO room_statement (room_id, text, origin, author_id, status) "
                        "VALUES (:r, :t, :o, :a, :st) RETURNING statement_id"
                    ),
                    {"r": room_id, "t": text_, "o": origin, "a": author, "st": status},
                ).scalar()
            )

    def approved_statements(self, room_id) -> dict[str, dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT statement_id, text, origin, anchor_id FROM room_statement "
                        "WHERE room_id = :r AND status = 'approved'"
                    ),
                    {"r": room_id},
                )
                .mappings()
                .all()
            )
        return {
            str(r["statement_id"]): {
                "text": r["text"],
                "origin": r["origin"],
                "anchor_id": r["anchor_id"],
            }
            for r in rows
        }

    def vote_rows(self, room_id) -> list[tuple[str, str, int, bool]]:
        with self.engine.connect() as c:
            rows = c.execute(
                text("""SELECT v.participant_id, v.statement_id, v.vote, p.is_synthetic
                        FROM room_vote v JOIN room_participant p USING (participant_id)
                        WHERE p.room_id = :r"""),
                {"r": room_id},
            ).all()
        return [(str(p), str(s), int(v), bool(syn)) for p, s, v, syn in rows]

    def vote_version(self, room_id) -> tuple:
        with self.engine.connect() as c:
            row = c.execute(
                text("""SELECT count(*), max(e.event_id) FROM room_vote_event e
                        JOIN room_participant p USING (participant_id) WHERE p.room_id = :r"""),
                {"r": room_id},
            ).one()
            moderated = c.execute(
                text("SELECT max(moderated_at) FROM room_statement WHERE room_id = :r"),
                {"r": room_id},
            ).scalar()
        return (row[0], row[1], str(moderated))

    def pending(self, room_id) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT statement_id, text, created_at FROM room_statement "
                        "WHERE room_id = :r AND status = 'pending' ORDER BY created_at"
                    ),
                    {"r": room_id},
                )
                .mappings()
                .all()
            )
        return [
            {
                "statement_id": str(r["statement_id"]),
                "text": r["text"],
                "created_at": r["created_at"].isoformat(),
            }
            for r in rows
        ]

    def moderate(self, room_id, statement: str, approve: bool, reason: str | None) -> bool:
        with self.engine.begin() as c:
            done = c.execute(
                text(
                    "UPDATE room_statement SET status = :st, reject_reason = :why, moderated_at = now() "
                    "WHERE statement_id = :s AND room_id = :r AND status = 'pending'"
                ),
                {
                    "st": "approved" if approve else "rejected",
                    "why": reason,
                    "s": statement,
                    "r": room_id,
                },
            )
        return done.rowcount == 1

    def add_dispute(self, person: str, anchor: str | None, body: str, contact: str | None) -> None:
        with self.engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO placement_dispute (person_id, anchor_id, body, contact) "
                    "VALUES (:p, :a, :b, :c)"
                ),
                {"p": person, "a": anchor, "b": body, "c": contact},
            )

    def disputes(self) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT dispute_id, person_id, anchor_id, body, contact, status, created_at "
                        "FROM placement_dispute ORDER BY created_at DESC LIMIT 200"
                    )
                )
                .mappings()
                .all()
            )
        return [
            {
                **dict(r),
                "dispute_id": str(r["dispute_id"]),
                "created_at": r["created_at"].isoformat(),
            }
            for r in rows
        ]

    def add_fairness(self, bundle_version: str, rating: int) -> None:
        with self.engine.begin() as c:
            c.execute(
                text("INSERT INTO fairness_rating (bundle_version, rating) VALUES (:v, :r)"),
                {"v": bundle_version, "r": rating},
            )

    def fairness(self) -> dict:
        with self.engine.connect() as c:
            n, mean = c.execute(text("SELECT count(*), avg(rating) FROM fairness_rating")).one()
        return {"count": int(n), "mean": None if mean is None else round(float(mean), 2)}

    # ---------- launch round: profiles, identity, cache, limits, counters ----------

    def add_check(
        self, kind: str, handle: str | None, challenge: str, verifier: str | None = None
    ) -> str:
        with self.engine.begin() as c:
            return str(
                c.execute(
                    text(
                        "INSERT INTO identity_check (kind, handle, challenge, code_verifier) "
                        "VALUES (:k, :h, :c, :v) RETURNING check_id"
                    ),
                    {"k": kind, "h": handle, "c": challenge, "v": verifier},
                ).scalar()
            )

    def get_check(self, check_id: str) -> dict | None:
        try:
            uuid.UUID(check_id)
        except ValueError:
            return None
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT * FROM identity_check WHERE check_id = :i "
                        "AND created_at > now() - interval '1 hour'"
                    ),
                    {"i": check_id},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def check_by_state(self, state: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT * FROM identity_check WHERE kind = 'x' AND challenge = :s "
                        "AND verified_at IS NULL AND created_at > now() - interval '15 minutes'"
                    ),
                    {"s": state},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def verify_check(
        self, check_id, handle: str, account_id: str, name: str, avatar: str | None
    ) -> None:
        with self.engine.begin() as c:
            c.execute(
                text(
                    "UPDATE identity_check SET verified_at = now(), handle = :h, account_id = :a, "
                    "display_name = :n, avatar_url = :av, code_verifier = NULL WHERE check_id = :i"
                ),
                {"i": check_id, "h": handle, "a": account_id, "n": name, "av": avatar},
            )

    def create_profile(self, row: dict) -> None:
        with self.engine.begin() as c:
            if row.get("check_id"):
                used = c.execute(
                    text(
                        "UPDATE identity_check SET used_at = now() WHERE check_id = :i "
                        "AND verified_at IS NOT NULL AND used_at IS NULL RETURNING check_id"
                    ),
                    {"i": row["check_id"]},
                ).first()
                if used is None:
                    raise ValueError("That verification has expired or was already used.")
                # one live profile per verified account: publishing again replaces the old one
                c.execute(
                    text("DELETE FROM profile WHERE identity = :k AND account_id = :a"),
                    {"k": row["identity"], "a": row["account_id"]},
                )
            c.execute(
                text("""INSERT INTO profile (code, edit_hash, identity, handle, display_name, avatar_url,
                          account_id, check_id, listed, include_answers, summary, answers, glyph,
                          bundle_version)
                        VALUES (:code, :edit_hash, :identity, :handle, :display_name, :avatar_url,
                          :account_id, :check_id, :listed, :include_answers, CAST(:summary AS jsonb),
                          CAST(:answers AS jsonb), CAST(:glyph AS jsonb), :bundle_version)"""),
                {
                    **row,
                    "summary": json.dumps(row["summary"]),
                    "glyph": json.dumps(row["glyph"]),
                    "answers": None if row["answers"] is None else json.dumps(row["answers"]),
                },
            )

    def profile(self, code: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT code, edit_hash, identity, handle, display_name, avatar_url, listed, "
                        "include_answers, summary, answers, glyph, bundle_version, created_at, hidden_at "
                        "FROM profile WHERE code = :c"
                    ),
                    {"c": code},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def update_profile(self, code: str, edit_key: str, listed: bool) -> bool:
        with self.engine.begin() as c:
            done = c.execute(
                text(
                    "UPDATE profile SET listed = :l, updated_at = now() "
                    "WHERE code = :c AND edit_hash = :h"
                ),
                {"l": listed, "c": code, "h": key_hash(edit_key)},
            )
        return done.rowcount == 1

    def delete_profile(self, code: str, edit_key: str) -> bool:
        with self.engine.begin() as c:
            done = c.execute(
                text("DELETE FROM profile WHERE code = :c AND edit_hash = :h"),
                {"c": code, "h": key_hash(edit_key)},
            )
        return done.rowcount == 1

    def hide_profile(self, code: str, hidden: bool) -> bool:
        with self.engine.begin() as c:
            done = c.execute(
                text(
                    "UPDATE profile SET hidden_at = CASE WHEN :h THEN now() ELSE NULL END "
                    "WHERE code = :c"
                ),
                {"h": hidden, "c": code},
            )
        return done.rowcount == 1

    def listed_profiles(self, limit: int = 200) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT code, identity, handle, display_name, avatar_url, summary, created_at "
                        "FROM profile WHERE listed AND hidden_at IS NULL AND identity <> 'anon' "
                        "ORDER BY created_at DESC LIMIT :n"
                    ),
                    {"n": limit},
                )
                .mappings()
                .all()
            )
        return [{**dict(r), "created_at": r["created_at"].isoformat()} for r in rows]

    def recent_profiles(self, limit: int = 50) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT code, identity, handle, display_name, listed, hidden_at, created_at "
                        "FROM profile ORDER BY created_at DESC LIMIT :n"
                    ),
                    {"n": limit},
                )
                .mappings()
                .all()
            )
        return [
            {
                **dict(r),
                "created_at": r["created_at"].isoformat(),
                "hidden_at": r["hidden_at"] and r["hidden_at"].isoformat(),
            }
            for r in rows
        ]

    def cached_report(self, room_id) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT version, report, personal, "
                        "extract(epoch FROM now() - computed_at) AS age FROM report_cache "
                        "WHERE room_id = :r"
                    ),
                    {"r": room_id},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def save_report(self, room_id, version: str, report: dict, personal: dict) -> None:
        with self.engine.begin() as c:
            c.execute(
                text("""INSERT INTO report_cache (room_id, version, report, personal, computed_at)
                        VALUES (:r, :v, CAST(:rep AS jsonb), CAST(:per AS jsonb), now())
                        ON CONFLICT (room_id) DO UPDATE SET version = EXCLUDED.version,
                          report = EXCLUDED.report, personal = EXCLUDED.personal,
                          computed_at = now()"""),
                {
                    "r": room_id,
                    "v": version,
                    "rep": json.dumps(report),
                    "per": json.dumps(personal),
                },
            )

    def try_report_lock(self, connection, room_id) -> bool:
        """A transaction-scoped advisory lock, so only one instance recomputes a room at a time."""
        key = int.from_bytes(hashlib.sha256(str(room_id).encode()).digest()[:8], "big", signed=True)
        return bool(
            connection.execute(text("SELECT pg_try_advisory_xact_lock(:k)"), {"k": key}).scalar()
        )

    def hit(self, bucket: str, limit: int, window_seconds: int) -> bool:
        """Record a hit; False when the bucket is over its limit for the window."""
        with self.engine.begin() as c:
            count = c.execute(
                text(
                    "SELECT count(*) FROM rate_hit WHERE bucket = :b "
                    "AND at > now() - make_interval(secs => :w)"
                ),
                {"b": bucket, "w": window_seconds},
            ).scalar()
            if (count or 0) >= limit:
                return False
            c.execute(text("INSERT INTO rate_hit (bucket) VALUES (:b)"), {"b": bucket})
            if secrets.randbelow(20) == 0:  # occasional cleanup of old hits
                c.execute(text("DELETE FROM rate_hit WHERE at < now() - interval '1 day'"))
        return True

    def count(self, name: str) -> None:
        with self.engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO daily_counter (name, n) VALUES (:n, 1) "
                    "ON CONFLICT (day, name) DO UPDATE SET n = daily_counter.n + 1"
                ),
                {"n": name},
            )

    def counters(self, days: int = 14) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT day, name, n FROM daily_counter WHERE day > current_date - :d "
                        "ORDER BY day DESC, name"
                    ),
                    {"d": days},
                )
                .mappings()
                .all()
            )
        return [{"day": r["day"].isoformat(), "name": r["name"], "n": int(r["n"])} for r in rows]

    def anchor_sheets(self, room_id, include_synthetic: bool = False) -> dict[str, dict[str, int]]:
        """Each participant's votes on the anchor statements; synthetic voters only in demo rooms."""
        with self.engine.connect() as c:
            rows = c.execute(
                text("""SELECT v.participant_id, s.anchor_id, v.vote
                        FROM room_vote v
                        JOIN room_statement s USING (statement_id)
                        JOIN room_participant p USING (participant_id)
                        WHERE s.room_id = :r AND s.anchor_id IS NOT NULL
                          AND (:syn OR NOT p.is_synthetic)"""),
                {"r": room_id, "syn": include_synthetic},
            ).all()
        sheets: dict[str, dict[str, int]] = {}
        for participant, anchor, vote in rows:
            sheets.setdefault(str(participant), {})[anchor] = int(vote)
        return sheets

    def visible_profiles(self) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(text("SELECT identity, summary FROM profile WHERE hidden_at IS NULL"))
                .mappings()
                .all()
            )
        return [dict(r) for r in rows]
