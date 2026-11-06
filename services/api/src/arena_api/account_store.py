"""Database access for accounts (migration 0011_accounts)."""

from __future__ import annotations

import datetime
import json
import secrets
import uuid

from sqlalchemy import Engine, text

from arena_api.accounts import digest

SESSION_DAYS = 365
FLOW_MINUTES = 15
EMAIL_MINUTES = 15
EMAIL_ATTEMPTS = 5


class AccountStore:
    def __init__(self, engine: Engine):
        self.engine = engine

    # ---------- sessions

    def new_session(self, account_id: str) -> str:
        token = secrets.token_urlsafe(32)
        with self.engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO account_session (token_hash, account_id, expires_at) "
                    "VALUES (:t, :a, now() + make_interval(days => :d))"
                ),
                {"t": digest(token), "a": account_id, "d": SESSION_DAYS},
            )
        return token

    def session_account(self, token: str | None) -> str | None:
        if not token or len(token) > 100:
            return None
        with self.engine.begin() as c:
            row = c.execute(
                text(
                    "UPDATE account_session SET last_seen_at = now() "
                    "WHERE token_hash = :t AND expires_at > now() RETURNING account_id"
                ),
                {"t": digest(token)},
            ).first()
        return str(row[0]) if row else None

    def end_session(self, token: str | None) -> None:
        if token:
            with self.engine.begin() as c:
                c.execute(
                    text("DELETE FROM account_session WHERE token_hash = :t"), {"t": digest(token)}
                )

    # ---------- logins

    def sign_in(
        self,
        kind: str,
        subject: str,
        current: str | None,
        handle: str | None = None,
        name: str | None = None,
        avatar: str | None = None,
        details: dict | None = None,
    ) -> str:
        """The account this login belongs to. A new login joins the signed-in account, if any,
        or starts a new one. The provider's name and picture fill in what the account lacks."""
        with self.engine.begin() as c:
            row = c.execute(
                text("SELECT account_id FROM account_login WHERE kind = :k AND subject = :s"),
                {"k": kind, "s": subject},
            ).first()
            if row:
                account = str(row[0])
                c.execute(
                    text(
                        "UPDATE account_login SET handle = coalesce(:h, handle), "
                        "avatar_url = coalesce(:av, avatar_url), "
                        "details = coalesce(CAST(:d AS jsonb), details) "
                        "WHERE kind = :k AND subject = :s"
                    ),
                    {
                        "h": handle,
                        "av": avatar,
                        "k": kind,
                        "s": subject,
                        "d": json.dumps(details) if details else None,
                    },  # fmt: skip
                )
            else:
                account = current or str(
                    c.execute(
                        text("INSERT INTO account DEFAULT VALUES RETURNING account_id")
                    ).scalar()
                )
                c.execute(
                    text(
                        "INSERT INTO account_login "
                        "(kind, subject, account_id, handle, avatar_url, details) "
                        "VALUES (:k, :s, :a, :h, :av, CAST(:d AS jsonb))"
                    ),
                    {
                        "k": kind,
                        "s": subject,
                        "a": account,
                        "h": handle,
                        "av": avatar,
                        "d": json.dumps(details) if details else None,
                    },  # fmt: skip
                )
            if kind in ("bsky", "x"):
                # a social login refreshes the picture; the name only fills a blank
                c.execute(
                    text(
                        "UPDATE account SET avatar_url = coalesce(:av, avatar_url), "
                        "display_name = coalesce(display_name, :n), "
                        "bio = coalesce(bio, :b), updated_at = now() "
                        "WHERE account_id = :a"
                    ),
                    {
                        "av": avatar,
                        "n": (name or handle or "")[:80] or None,
                        "a": account,
                        "b": " ".join(((details or {}).get("description") or "").split())[:160]
                        or None,
                    },  # fmt: skip
                )
        return account

    def login_account(self, kind: str, subject: str) -> str | None:
        with self.engine.connect() as c:
            row = c.execute(
                text("SELECT account_id FROM account_login WHERE kind = :k AND subject = :s"),
                {"k": kind, "s": subject},
            ).first()
        return str(row[0]) if row else None

    def linked_participants(self, season: str) -> set[str]:
        with self.engine.connect() as c:
            rows = c.execute(
                text(
                    "SELECT participant_id FROM account_sheet "
                    "WHERE season = :s AND participant_id IS NOT NULL"
                ),
                {"s": season},
            ).all()
        return {str(r[0]) for r in rows}

    def account(self, account_id: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT account_id, display_name, avatar_url, bio, show_on_map, created_at "
                        "FROM account WHERE account_id = :a"
                    ),
                    {"a": account_id},
                )
                .mappings()
                .first()
            )
            if row is None:
                return None
            logins = (
                c.execute(
                    text(
                        "SELECT kind, handle FROM account_login WHERE account_id = :a "
                        "ORDER BY created_at"
                    ),
                    {"a": account_id},
                )
                .mappings()
                .all()
            )
        return {**dict(row), "logins": [dict(r) for r in logins]}

    def update_account(self, account_id: str, fields: dict) -> None:
        allowed = {k: v for k, v in fields.items() if k in ("display_name", "bio", "show_on_map")}
        if not allowed:
            return
        sets = ", ".join(f"{k} = :{k}" for k in allowed)
        with self.engine.begin() as c:
            c.execute(
                text(f"UPDATE account SET {sets}, updated_at = now() WHERE account_id = :a"),  # noqa: S608 (fixed keys)
                {**allowed, "a": account_id},
            )

    def delete_account(self, account_id: str) -> None:
        with self.engine.begin() as c:
            participants = [
                r[0]
                for r in c.execute(
                    text(
                        "SELECT participant_id FROM account_sheet "
                        "WHERE account_id = :a AND participant_id IS NOT NULL"
                    ),
                    {"a": account_id},
                ).all()
            ]
            for p in participants:  # their answers leave the public results too
                c.execute(text("DELETE FROM room_vote_event WHERE participant_id = :p"), {"p": p})
                c.execute(text("DELETE FROM room_vote WHERE participant_id = :p"), {"p": p})
            c.execute(text("DELETE FROM account WHERE account_id = :a"), {"a": account_id})

    # ---------- OAuth flows

    def put_flow(self, state: str, kind: str, data: dict) -> None:
        with self.engine.begin() as c:
            c.execute(
                text(
                    "INSERT INTO auth_flow (state, kind, data) VALUES (:s, :k, CAST(:d AS jsonb))"
                ),
                {"s": state, "k": kind, "d": json.dumps(data)},
            )
            if secrets.randbelow(20) == 0:
                c.execute(text("DELETE FROM auth_flow WHERE created_at < now() - interval '1 day'"))

    def take_flow(self, state: str, kind: str) -> dict | None:
        """A flow is used once: taking it deletes it."""
        with self.engine.begin() as c:
            row = c.execute(
                text(
                    "DELETE FROM auth_flow WHERE state = :s AND kind = :k "
                    "AND created_at > now() - make_interval(mins => :m) RETURNING data"
                ),
                {"s": state, "k": kind, "m": FLOW_MINUTES},
            ).first()
        return dict(row[0]) if row else None

    # ---------- email

    def new_email_token(self, email: str, token: str, code: str) -> None:
        with self.engine.begin() as c:
            c.execute(
                text("INSERT INTO email_token (token_hash, email, code_hash) VALUES (:t, :e, :c)"),
                {"t": digest(token), "e": email, "c": digest(f"{email}:{code}")},
            )

    def use_email_link(self, token: str) -> str | None:
        with self.engine.begin() as c:
            row = c.execute(
                text(
                    "UPDATE email_token SET used_at = now() "
                    "WHERE token_hash = :t AND used_at IS NULL "
                    "AND created_at > now() - make_interval(mins => :m) RETURNING email"
                ),
                {"t": digest(token), "m": EMAIL_MINUTES},
            ).first()
        return row[0] if row else None

    def use_email_code(self, email: str, code: str) -> bool:
        """True once for the right code; each wrong guess uses up one of five attempts."""
        with self.engine.begin() as c:
            row = c.execute(
                text(
                    "SELECT token_hash, code_hash FROM email_token WHERE email = :e "
                    "AND used_at IS NULL AND attempts < :n "
                    "AND created_at > now() - make_interval(mins => :m) "
                    "ORDER BY created_at DESC LIMIT 1 FOR UPDATE"
                ),
                {"e": email, "n": EMAIL_ATTEMPTS, "m": EMAIL_MINUTES},
            ).first()
            if row is None:
                return False
            if secrets.compare_digest(bytes(row[1]), digest(f"{email}:{code}")):
                c.execute(
                    text("UPDATE email_token SET used_at = now() WHERE token_hash = :t"),
                    {"t": row[0]},
                )
                return True
            c.execute(
                text("UPDATE email_token SET attempts = attempts + 1 WHERE token_hash = :t"),
                {"t": row[0]},
            )
            return False

    # ---------- answers

    def sheet(self, account_id: str, season: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT season, answers, updated_at, participant_id FROM account_sheet "
                        "WHERE account_id = :a AND season = :s"
                    ),
                    {"a": account_id, "s": season},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        return {
            "season": row["season"],
            "answers": row["answers"],
            "updated_at": row["updated_at"].isoformat(),
            "participant_id": row["participant_id"] and str(row["participant_id"]),
        }

    def save_sheet(
        self,
        account_id: str,
        season: str,
        answers: dict,
        where: tuple[float, float] | None,
        nearest: str | None,
        participant_id: str | None,
    ) -> None:
        x, y = where if where else (None, None)
        with self.engine.begin() as c:
            c.execute(
                text("""INSERT INTO account_sheet (account_id, season, answers, x, y, nearest,
                          participant_id)
                        VALUES (:a, :s, CAST(:ans AS jsonb), :x, :y, :n, :p)
                        ON CONFLICT (account_id, season) DO UPDATE SET answers = EXCLUDED.answers,
                          x = EXCLUDED.x, y = EXCLUDED.y, nearest = EXCLUDED.nearest,
                          participant_id = coalesce(EXCLUDED.participant_id,
                                                    account_sheet.participant_id),
                          updated_at = now()"""),
                {
                    "a": account_id,
                    "s": season,
                    "ans": json.dumps(answers),
                    "x": x,
                    "y": y,
                    "n": nearest,
                    "p": participant_id,
                },  # fmt: skip
            )

    def map_people(self, season: str, limit: int = 2000) -> list[dict]:
        """Everyone with a placed sheet this season. Name, picture and bio only for people who
        switched on show_on_map and have a picture from a Bluesky or X sign-in."""
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text("""SELECT s.x, s.y, s.nearest, a.show_on_map, a.display_name, a.bio,
                              a.avatar_url,
                              (SELECT l.handle FROM account_login l
                               WHERE l.account_id = a.account_id
                                 AND l.kind IN ('bsky','x') ORDER BY l.kind LIMIT 1) AS handle,
                              (SELECT l.kind FROM account_login l
                               WHERE l.account_id = a.account_id
                                 AND l.kind IN ('bsky','x') ORDER BY l.kind LIMIT 1) AS kind
                            FROM account_sheet s JOIN account a USING (account_id)
                            WHERE s.season = :s AND s.x IS NOT NULL
                            ORDER BY s.updated_at DESC LIMIT :n"""),
                    {"s": season, "n": limit},
                )
                .mappings()
                .all()
            )
        out = []
        for r in rows:
            point: dict = {"x": round(float(r["x"]), 2), "y": round(float(r["y"]), 2)}
            if r["show_on_map"] and r["avatar_url"] and r["handle"]:
                point |= {
                    "face": r["avatar_url"],
                    "name": r["display_name"] or r["handle"],
                    "handle": r["handle"],
                    "kind": r["kind"],
                    "bio": r["bio"] or "",
                    "nearest": r["nearest"],
                }
            out.append(point)
        out.sort(key=lambda p: "face" not in p)  # faces first
        return out

    def sheet_count(self, season: str) -> int:
        with self.engine.connect() as c:
            return int(
                c.execute(
                    text("SELECT count(*) FROM account_sheet WHERE season = :s AND x IS NOT NULL"),
                    {"s": season},
                ).scalar()
                or 0
            )


def iso(when: datetime.datetime | None) -> str | None:
    return when.isoformat() if when else None


class AccountPages(AccountStore):
    """Round 2: the account's public results page, its social details, its room statements,
    and camp-name proposals."""

    def socials(self, account_id: str) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text(
                        "SELECT kind, handle, details FROM account_login "
                        "WHERE account_id = :a AND kind IN ('bsky','x') ORDER BY created_at"
                    ),
                    {"a": account_id},
                )
                .mappings()
                .all()
            )
        out = []
        for r in rows:
            d = r["details"] or {}
            default = (f"https://bsky.app/profile/{r['handle']}" if r["kind"] == "bsky"
                       else f"https://x.com/{r['handle']}")  # fmt: skip
            out.append({
                "kind": r["kind"],
                "handle": r["handle"],
                "url": d.get("url") or default,
                "description": d.get("description", ""),
                "location": d.get("location", ""),
                "website": d.get("website", ""),
                "followers": d.get("followers"),
            })  # fmt: skip
        return out

    def owned_profile(self, account_id: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text("SELECT code, listed FROM profile WHERE owner_id = :a"),
                    {"a": account_id},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def put_owned_profile(self, account_id: str, row: dict) -> str:
        """Create or refresh the account's one public results page; the code never changes."""
        with self.engine.begin() as c:
            code = c.execute(
                text("SELECT code FROM profile WHERE owner_id = :a FOR UPDATE"),
                {"a": account_id},
            ).scalar()
            params = {**row, "owner": account_id, "summary": json.dumps(row["summary"]),
                      "glyph": json.dumps(row["glyph"])}  # fmt: skip
            if code:
                c.execute(
                    text("""UPDATE profile SET identity = :identity, handle = :handle,
                              display_name = :display_name, avatar_url = :avatar_url,
                              account_id = :account_id, listed = :listed,
                              summary = CAST(:summary AS jsonb), glyph = CAST(:glyph AS jsonb),
                              bundle_version = :bundle_version, updated_at = now()
                            WHERE owner_id = :owner"""),
                    params,
                )
                return str(code)
            c.execute(
                text("""INSERT INTO profile (code, edit_hash, identity, handle, display_name,
                          avatar_url, account_id, owner_id, listed, include_answers, summary,
                          glyph, bundle_version)
                        VALUES (:code, :edit_hash, :identity, :handle, :display_name, :avatar_url,
                          :account_id, :owner, :listed, false, CAST(:summary AS jsonb),
                          CAST(:glyph AS jsonb), :bundle_version)"""),
                params,
            )
            return row["code"]

    def delete_owned_profile(self, account_id: str) -> None:
        with self.engine.begin() as c:
            c.execute(text("DELETE FROM profile WHERE owner_id = :a"), {"a": account_id})

    def profile_owner_extras(self, code: str) -> dict | None:
        """Bio and socials for a results page that belongs to an account."""
        with self.engine.connect() as c:
            owner = c.execute(
                text("SELECT owner_id FROM profile WHERE code = :c"), {"c": code}
            ).scalar()
            if owner is None:
                return None
            bio = c.execute(
                text("SELECT bio FROM account WHERE account_id = :a"), {"a": owner}
            ).scalar()
        return {"bio": bio or "", "socials": self.socials(str(owner))}

    def statements_by(self, participant_id: str | None) -> list[dict]:
        if not participant_id:
            return []
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text("""SELECT s.statement_id, s.text, s.status, s.created_at,
                              count(*) FILTER (WHERE v.vote = 1) AS agree,
                              count(*) FILTER (WHERE v.vote = -1) AS disagree,
                              count(*) FILTER (WHERE v.vote = 0) AS pass
                            FROM room_statement s
                            LEFT JOIN room_vote v USING (statement_id)
                            WHERE s.author_id = :p
                            GROUP BY s.statement_id ORDER BY s.created_at DESC"""),
                    {"p": participant_id},
                )
                .mappings()
                .all()
            )
        return [
            {
                "statement_id": str(r["statement_id"]),
                "text": r["text"],
                "status": r["status"],
                "agree": int(r["agree"]),
                "disagree": int(r["disagree"]),
                "pass": int(r["pass"]),
            }
            for r in rows
        ]

    # ---------- camp names

    def camp_names(self, season: str, account_id: str | None) -> list[dict]:
        with self.engine.connect() as c:
            rows = (
                c.execute(
                    text("""SELECT n.name_id, n.node, n.name, n.status, n.created_at,
                              count(v.*) FILTER (WHERE v.up) AS up,
                              count(v.*) FILTER (WHERE NOT v.up) AS down,
                              bool_or(v.account_id = :me AND v.up) AS mine_up,
                              bool_or(v.account_id = :me AND NOT v.up) AS mine_down,
                              (n.account_id = :me) AS proposed_by_me
                            FROM camp_name n LEFT JOIN camp_name_vote v USING (name_id)
                            WHERE n.season = :s AND n.status <> 'declined'
                            GROUP BY n.name_id
                            ORDER BY n.node, count(v.*) FILTER (WHERE v.up) DESC, n.created_at"""),
                    {"s": season, "me": account_id},
                )
                .mappings()
                .all()
            )
        out = []
        for r in rows:
            mine = "up" if r["mine_up"] else "down" if r["mine_down"] else None
            out.append({"id": str(r["name_id"]), "node": r["node"], "name": r["name"],
                        "status": r["status"], "up": int(r["up"]), "down": int(r["down"]),
                        "my_vote": mine, "proposed_by_me": bool(r["proposed_by_me"])})  # fmt: skip
        return out

    def propose_camp_name(self, season: str, node: str, name: str, account_id: str) -> str:
        with self.engine.begin() as c:
            existing = c.execute(
                text(
                    "SELECT name_id FROM camp_name WHERE season = :s AND node = :n "
                    "AND lower(name) = lower(:name)"
                ),
                {"s": season, "n": node, "name": name},
            ).scalar()
            name_id = (
                existing
                or c.execute(
                    text(
                        "INSERT INTO camp_name (season, node, name, account_id) "
                        "VALUES (:s, :n, :name, :a) RETURNING name_id"
                    ),
                    {"s": season, "n": node, "name": name, "a": account_id},
                ).scalar()
            )
            c.execute(
                text(
                    "INSERT INTO camp_name_vote (name_id, account_id, up) VALUES (:i, :a, true) "
                    "ON CONFLICT (name_id, account_id) DO UPDATE SET up = true"
                ),
                {"i": name_id, "a": account_id},
            )
        return str(name_id)

    def camp_name(self, name_id: str) -> dict | None:
        try:
            uuid.UUID(name_id)
        except ValueError:
            return None
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT name_id, season, node, name, status FROM camp_name "
                        "WHERE name_id = :i"
                    ),  # fmt: skip
                    {"i": name_id},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def vote_camp_name(self, name_id: str, account_id: str, up: bool | None) -> None:
        with self.engine.begin() as c:
            if up is None:
                c.execute(
                    text("DELETE FROM camp_name_vote WHERE name_id = :i AND account_id = :a"),
                    {"i": name_id, "a": account_id},
                )
                return
            c.execute(
                text(
                    "INSERT INTO camp_name_vote (name_id, account_id, up) VALUES (:i, :a, :u) "
                    "ON CONFLICT (name_id, account_id) DO UPDATE SET up = EXCLUDED.up, "
                    "created_at = now()"
                ),
                {"i": name_id, "a": account_id, "u": up},
            )

    def decide_camp_name(self, name_id: str, accept: bool) -> bool:
        with self.engine.begin() as c:
            done = c.execute(
                text("UPDATE camp_name SET status = :st, decided_at = now() WHERE name_id = :i"),
                {"st": "accepted" if accept else "declined", "i": name_id},
            )
        return done.rowcount == 1

    def accepted_names(self, season: str) -> dict[str, str]:
        with self.engine.connect() as c:
            rows = c.execute(
                text(
                    "SELECT DISTINCT ON (node) node, name FROM camp_name "
                    "WHERE season = :s AND status = 'accepted' ORDER BY node, decided_at DESC"
                ),
                {"s": season},
            ).all()
        return {r[0]: r[1] for r in rows}

    def nearest_of(self, account_id: str, season: str) -> str | None:
        with self.engine.connect() as c:
            return c.execute(
                text("SELECT nearest FROM account_sheet WHERE account_id = :a AND season = :s"),
                {"a": account_id, "s": season},
            ).scalar()

    def primary_social(self, account_id: str) -> dict | None:
        with self.engine.connect() as c:
            row = (
                c.execute(
                    text(
                        "SELECT kind, subject, handle FROM account_login WHERE account_id = :a "
                        "AND kind IN ('bsky','x') ORDER BY created_at LIMIT 1"
                    ),
                    {"a": account_id},
                )
                .mappings()
                .first()
            )
        return dict(row) if row else None

    def rekey_participant(self, participant_id: str, key_hash: bytes) -> None:
        """Give the account's room entry a fresh key for this browser (older keys stop working)."""
        with self.engine.begin() as c:
            c.execute(
                text("UPDATE room_participant SET key_hash = :k WHERE participant_id = :p"),
                {"k": key_hash, "p": participant_id},
            )

    def link_participant(self, account_id: str, season: str, participant_id: str) -> None:
        with self.engine.begin() as c:
            c.execute(
                text("""INSERT INTO account_sheet (account_id, season, answers, participant_id)
                        VALUES (:a, :s, '{}'::jsonb, :p)
                        ON CONFLICT (account_id, season) DO UPDATE
                          SET participant_id = EXCLUDED.participant_id"""),
                {"a": account_id, "s": season, "p": participant_id},
            )
