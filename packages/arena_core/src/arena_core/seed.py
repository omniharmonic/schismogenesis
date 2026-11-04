"""Seed loader: SEED-v4 plus the Slice 1 selection.

Niches are curated hypotheses and never mix with data-derived clusters. Loading is idempotent:
identical inputs add no rows at all, and changed inputs upsert by niche_id / landmark_id.
"""

import json
import pathlib
import re
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Connection, Engine, text

from arena_core.provenance import code_ref, inputs_hash, log_events

# Gate G0.3 plus later decisions. D-31.9 added bayeslord and D-31.12 added Alex Karp, neither in
# SEED-v4, so 817 becomes 819. D-31.12 also moved three seed landmarks in, so 53 slice landmarks
# becomes 58. D-31.18 (atlas expansion, Benjamin 2026-11-03) added 18 new voices and moved 7 more
# seed landmarks in: 819 becomes 837 and 58 becomes 83. D-31.20 (round 4, AI and the social
# contract, 2026-11-03) added 31 new voices and moved 11 more seed landmarks in: 837 becomes 868
# and 83 becomes 125; its gap round (4b) added 28 more and moved 3 in: 896 and 156. These
# stay literal so verify checks the data against the decision instead of against itself.
EXPECTED = {
    "niches": 234,
    "landmarks": 896,
    "slice niches": 15,
    "slice core niches": 8,
    "slice adjacent niches": 7,
    "slice landmarks": 156,
    "worldview core landmarks": 11,
    "landmarks hidden from public surfaces": 20,
    "flagged landmarks visible on public surfaces": 0,
    "landmarks without exactly one primary niche": 0,
    "primary role rows disagreeing with landmark": 0,
    "persons not public figures": 0,
    "excluded landmarks present": 0,
}
SECONDARY_WEIGHT = 0.5  # OPEN-4 default
DEFAULT_SECONDARY_ROLE = "bridger"
OUTSIDER_ALIAS = re.compile(r"outsider|critics|pejorative", re.IGNORECASE)
HANDLE = re.compile(r"@\w+")
PAREN_NAME = re.compile(r"\(([^)]+)\)\s*$")


class SeedError(ValueError):
    """The input files are inconsistent. Nothing was written."""


@dataclass
class LoadResult:
    skipped: bool
    created: int = 0
    updated: int = 0


def niche_aliases(aliases: list[str]) -> list[dict[str, str]]:
    return [
        {"text": alias, "kind": "outsider" if OUTSIDER_ALIAS.search(alias) else "self"}
        for alias in aliases
    ]


def person_aliases(record: dict[str, Any]) -> list[dict[str, str]]:
    found = []
    match = PAREN_NAME.search(record["name"])
    if match and record.get("record_type") == "person":
        found.append({"text": match[1], "kind": "stage", "source": "seed"})
    handle = HANDLE.search(str(record.get("platforms", {}).get("x", "")))
    if handle:
        found.append({"text": handle[0], "kind": "handle", "source": "seed"})
    return found


def resolve_niche_refs(names: list[str], lookup: dict[str, str], own_id: str) -> list[str]:
    """Seed cross-references are free text. Keep only exact matches; the rest stay in raw."""
    ids = {lookup[name.lower()] for name in names if name.lower() in lookup}
    return sorted(ids - {own_id})


def niche_lookup(niches: list[dict[str, Any]]) -> dict[str, str]:
    """Lowercased name or alias -> niche_id, leaving out anything two niches share."""
    seen: dict[str, set[str]] = {}
    for niche in niches:
        for label in [niche["name"], *niche["aliases"]]:
            seen.setdefault(label.lower(), set()).add(niche["niche_id"])
    return {label: next(iter(ids)) for label, ids in seen.items() if len(ids) == 1}


def merge_inputs(seed: dict[str, Any], slice_: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every landmark with slice fields applied, after checking the two files agree."""
    landmarks = {record["landmark_id"]: dict(record) for record in seed["landmarks"]}
    niche_ids = {niche["niche_id"] for niche in seed["niches"]}
    excluded = {record["landmark_id"] for record in seed["excluded_landmarks"]}

    unknown_niches = {n["niche_id"] for n in slice_["niches"]} - niche_ids
    if unknown_niches:
        raise SeedError(f"slice niches not in seed: {sorted(unknown_niches)}")
    for record in slice_["landmarks"]:
        landmark_id = record["landmark_id"]
        if landmark_id in excluded:
            raise SeedError(f"excluded landmark in slice: {landmark_id}")
        if landmark_id in landmarks:
            landmarks[landmark_id]["in_slice"] = "slice-1"
        elif record.get("added"):  # a landmark added by decision after the seed froze
            if record["primary_niche"] not in niche_ids:
                raise SeedError(f"{landmark_id}: unknown niche {record['primary_niche']}")
            landmarks[landmark_id] = {**record, "in_slice": "slice-1", "slice_addition": True}
        else:
            raise SeedError(f"slice landmark not in seed and not marked added: {landmark_id}")

    for landmark_id in slice_.get("worldview_core", []):
        if landmarks.get(landmark_id, {}).get("in_slice") != "slice-1":
            raise SeedError(f"worldview core landmark not in slice: {landmark_id}")
        landmarks[landmark_id]["worldview_core"] = True

    # Read both flag sources and take the union: a flag in either one hides the landmark.
    for flag in seed["flags_for_benjamin"]["landmarks"]:
        if flag["landmark_id"] not in landmarks:
            raise SeedError(f"flagged landmark not in seed: {flag['landmark_id']}")
        landmarks[flag["landmark_id"]]["flag_type"] = flag["type"]
    return list(landmarks.values())


def _niche_row(
    niche: dict[str, Any], lookup: dict[str, str], tiers: dict[str, str], version: str
) -> dict[str, Any]:
    own_id = niche["niche_id"]
    return {
        "niche_id": own_id,
        "name": niche["name"],
        "domain": niche["domain"],
        "cross_domains": niche["cross_domains"],
        "aliases": json.dumps(niche_aliases(niche["aliases"])),
        "description": niche["description"],
        "telos": niche["telos"],
        "sacred_values": json.dumps(niche["sacred_values"]),
        "existential_threats": json.dumps(niche["existential_threats"]),
        "combatants": resolve_niche_refs(niche["combatants"], lookup, own_id),
        "adjacent": resolve_niche_refs(niche["adjacent_niches"], lookup, own_id),
        "placement_prior": json.dumps(niche["placement"]),
        "slice_tier": tiers.get(own_id),
        "seed_version": version,
        "merged_from": niche["merged_from"],
        "raw": json.dumps(niche),
    }


def _landmark_row(record: dict[str, Any], version: str) -> dict[str, Any]:
    flagged = record.get("flag_type") is not None
    return {
        "landmark_id": record["landmark_id"],
        "name": record["name"],
        "person_aliases": json.dumps(person_aliases(record)),
        "primary_niche_id": record["primary_niche"],
        "role": record["role"],
        "platforms": json.dumps(record["platforms"]),
        "longform_output": record["longform_output"],
        "verification": record["verification"],
        "in_slice": record.get("in_slice"),
        "worldview_core": record.get("worldview_core", False),
        "flag_type": record.get("flag_type"),
        "public_surface_allowed": not flagged,
        # OD-30 default: verified-active, unflagged landmarks form the core panel.
        "panel_status": "core_panel"
        if record["verification"] == "verified-active" and not flagged
        else "newcomer",
        "gender": record.get("gender"),
        "seed_version": f"{version}+D-31.9" if record.get("slice_addition") else version,
        "raw": json.dumps(record),
    }


def _role_rows(record: dict[str, Any]) -> list[dict[str, Any]]:
    landmark_id = record["landmark_id"]
    rows = [
        {
            "landmark_id": landmark_id,
            "niche_id": record["primary_niche"],
            "role": record["role"],
            "is_primary": True,
            "weight": 1.0,
            "basis": "seed:primary",
        }
    ]
    explicit = record.get("secondary_roles", {})
    for niche_id in record.get("secondary_niches", []):
        rows.append(
            {
                "landmark_id": landmark_id,
                "niche_id": niche_id,
                "role": explicit.get(niche_id, DEFAULT_SECONDARY_ROLE),
                "is_primary": False,
                "weight": SECONDARY_WEIGHT,
                "basis": "seed:secondary_roles" if niche_id in explicit else "seed:default_role",
            }
        )
    return rows


UPSERT_NICHE = text("""
    INSERT INTO niche (niche_id, name, domain, cross_domains, aliases, description, telos,
      sacred_values, existential_threats, combatant_niche_ids, adjacent_niche_ids,
      placement_prior, slice_tier, seed_version, merged_from, raw)
    VALUES (:niche_id, :name, :domain, :cross_domains, CAST(:aliases AS jsonb), :description,
      :telos, CAST(:sacred_values AS jsonb), CAST(:existential_threats AS jsonb), :combatants,
      :adjacent, CAST(:placement_prior AS jsonb), :slice_tier, :seed_version, :merged_from,
      CAST(:raw AS jsonb))
    ON CONFLICT (niche_id) DO UPDATE SET name = EXCLUDED.name, domain = EXCLUDED.domain,
      cross_domains = EXCLUDED.cross_domains, aliases = EXCLUDED.aliases,
      description = EXCLUDED.description, telos = EXCLUDED.telos,
      sacred_values = EXCLUDED.sacred_values, existential_threats = EXCLUDED.existential_threats,
      combatant_niche_ids = EXCLUDED.combatant_niche_ids,
      adjacent_niche_ids = EXCLUDED.adjacent_niche_ids,
      placement_prior = EXCLUDED.placement_prior, slice_tier = EXCLUDED.slice_tier,
      seed_version = EXCLUDED.seed_version, merged_from = EXCLUDED.merged_from, raw = EXCLUDED.raw
""")
UPSERT_PERSON = text("""
    INSERT INTO person (person_id, display_name, aliases, is_public_figure)
    VALUES (:landmark_id, :name, CAST(:person_aliases AS jsonb), true)
    ON CONFLICT (person_id) DO UPDATE SET display_name = EXCLUDED.display_name,
      aliases = EXCLUDED.aliases
""")
# public_surface_allowed is ANDed on update, so a reload can hide someone but never expose them:
# a takedown or a re-flag survives. Sign-offs (OD-01, OD-02) are applied after loading.
UPSERT_LANDMARK = text("""
    INSERT INTO landmark (landmark_id, name, primary_niche_id, role, platforms, longform_output,
      verification, in_slice, worldview_core, flag_type, public_surface_allowed, panel_status,
      gender, seed_version, raw)
    VALUES (:landmark_id, :name, :primary_niche_id, :role, CAST(:platforms AS jsonb),
      :longform_output, :verification, :in_slice, :worldview_core, :flag_type,
      :public_surface_allowed, :panel_status, :gender, :seed_version, CAST(:raw AS jsonb))
    ON CONFLICT (landmark_id) DO UPDATE SET name = EXCLUDED.name,
      primary_niche_id = EXCLUDED.primary_niche_id, role = EXCLUDED.role,
      platforms = EXCLUDED.platforms, longform_output = EXCLUDED.longform_output,
      verification = EXCLUDED.verification, in_slice = EXCLUDED.in_slice,
      worldview_core = EXCLUDED.worldview_core,
      flag_type = EXCLUDED.flag_type,
      public_surface_allowed = landmark.public_surface_allowed AND EXCLUDED.public_surface_allowed,
      panel_status = EXCLUDED.panel_status, gender = EXCLUDED.gender,
      seed_version = EXCLUDED.seed_version, raw = EXCLUDED.raw
""")
UPSERT_ROLE = text("""
    INSERT INTO landmark_niche (landmark_id, niche_id, role, is_primary, weight, basis)
    VALUES (:landmark_id, :niche_id, :role, :is_primary, :weight, :basis)
    ON CONFLICT (landmark_id, niche_id, valid_from) DO UPDATE SET role = EXCLUDED.role,
      is_primary = EXCLUDED.is_primary, weight = EXCLUDED.weight, basis = EXCLUDED.basis,
      valid_to = NULL
""")


def _close_stale_roles(connection: Connection, roles: list[dict[str, Any]]) -> None:
    """End links the new seed dropped, first, so a changed primary cannot hit the one-primary
    index."""
    keep = {(role["landmark_id"], role["niche_id"], role["is_primary"]) for role in roles}
    current = connection.execute(
        text("SELECT landmark_id, niche_id, is_primary FROM landmark_niche WHERE valid_to IS NULL")
    ).all()
    stale = [
        {"landmark_id": row[0], "niche_id": row[1]} for row in current if tuple(row) not in keep
    ]
    if stale:
        connection.execute(
            text(
                "UPDATE landmark_niche SET valid_to = current_date "
                "WHERE landmark_id = :landmark_id AND niche_id = :niche_id AND valid_to IS NULL"
            ),
            stale,
        )


def load_seed(engine: Engine, seed_path: pathlib.Path, slice_path: pathlib.Path) -> LoadResult:
    seed_bytes, slice_bytes = seed_path.read_bytes(), slice_path.read_bytes()
    seed, slice_ = json.loads(seed_bytes), json.loads(slice_bytes)
    landmarks = merge_inputs(seed, slice_)  # validates before anything is written
    digest = inputs_hash(seed_bytes, slice_bytes)
    version = seed["meta"]["version"]

    with engine.begin() as connection:
        already = connection.execute(
            text(
                "SELECT 1 FROM stage_item WHERE item_type = 'seed' AND item_id = 'slice-1' "
                "AND stage = 'seed' AND inputs_hash = :digest AND status = 'done'"
            ),
            {"digest": digest},
        ).first()
        if already:
            return LoadResult(skipped=True)

        run_id = connection.execute(
            text(
                "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, params) "
                "VALUES ('seed', 'seed_load', 'manual', :code_ref, CAST(:params AS jsonb)) "
                "RETURNING run_id"
            ),
            {
                "code_ref": code_ref(),
                "params": json.dumps({"seed": seed_path.name, "slice": slice_path.name}),
            },
        ).scalar_one()

        lookup = niche_lookup(seed["niches"])
        tiers = {niche["niche_id"]: niche["tier"] for niche in slice_["niches"]}
        niche_rows = [_niche_row(n, lookup, tiers, version) for n in seed["niches"]]
        landmark_rows = [_landmark_row(record, version) for record in landmarks]
        role_rows = [row for record in landmarks for row in _role_rows(record)]

        known = {
            ("niche", row[0]): row[1]
            for row in connection.execute(text("SELECT niche_id, raw::text FROM niche"))
        } | {
            ("landmark", row[0]): row[1]
            for row in connection.execute(text("SELECT landmark_id, raw::text FROM landmark"))
        }
        previous_raw = {key: json.loads(value) for key, value in known.items()}

        connection.execute(UPSERT_NICHE, niche_rows)
        connection.execute(UPSERT_PERSON, landmark_rows)
        connection.execute(UPSERT_LANDMARK, landmark_rows)
        _close_stale_roles(connection, role_rows)
        connection.execute(UPSERT_ROLE, role_rows)

        events, created, updated = [], 0, 0
        entities = [("niche", row["niche_id"], row) for row in niche_rows] + [
            ("landmark", row["landmark_id"], row) for row in landmark_rows
        ]
        for entity_type, entity_id, row in entities:
            before = previous_raw.get((entity_type, entity_id))
            if before == json.loads(row["raw"]):
                continue
            change = "created" if before is None else "updated"
            created += before is None
            updated += before is not None
            events.append(
                {
                    "type": f"{entity_type}.seeded",
                    "actor_type": "pipeline",
                    "actor_id": str(run_id),
                    "entity_type": entity_type,
                    "entity_id": entity_id,
                    "payload": {"change": change, "seed_version": row["seed_version"]},
                    "run_id": run_id,
                }
            )
        log_events(connection, events)

        connection.execute(
            text(
                "INSERT INTO stage_item (item_type, item_id, stage, inputs_hash, run_id, status) "
                "VALUES ('seed', 'slice-1', 'seed', :digest, :run_id, 'done')"
            ),
            {"digest": digest, "run_id": run_id},
        )
        connection.execute(
            text(
                "UPDATE pipeline_run SET status = 'succeeded', finished_at = now(), "
                "stats = CAST(:stats AS jsonb) WHERE run_id = :run_id"
            ),
            {"run_id": run_id, "stats": json.dumps({"created": created, "updated": updated})},
        )
    return LoadResult(skipped=False, created=created, updated=updated)


VERIFY_QUERIES = {
    "niches": "SELECT count(*) FROM niche",
    "landmarks": "SELECT count(*) FROM landmark",
    "slice niches": "SELECT count(*) FROM niche WHERE slice_tier IS NOT NULL",
    "slice core niches": "SELECT count(*) FROM niche WHERE slice_tier = 'core'",
    "slice adjacent niches": "SELECT count(*) FROM niche WHERE slice_tier = 'adjacent'",
    "slice landmarks": "SELECT count(*) FROM landmark WHERE in_slice = 'slice-1'",
    "worldview core landmarks": "SELECT count(*) FROM landmark WHERE worldview_core",
    "landmarks hidden from public surfaces": (
        "SELECT count(*) FROM landmark WHERE NOT public_surface_allowed"
    ),
    "flagged landmarks visible on public surfaces": (
        "SELECT count(*) FROM landmark WHERE flag_type IS NOT NULL AND public_surface_allowed"
    ),
    "landmarks without exactly one primary niche": """
        SELECT count(*) FROM landmark l WHERE (SELECT count(*) FROM landmark_niche r
          WHERE r.landmark_id = l.landmark_id AND r.is_primary AND r.valid_to IS NULL) <> 1""",
    "primary role rows disagreeing with landmark": """
        SELECT count(*) FROM landmark_niche r JOIN landmark l USING (landmark_id)
        WHERE r.is_primary AND r.valid_to IS NULL
          AND (r.niche_id <> l.primary_niche_id OR r.role <> l.role)""",
    "persons not public figures": "SELECT count(*) FROM person WHERE NOT is_public_figure",
    "excluded landmarks present": "SELECT count(*) FROM landmark WHERE landmark_id = 'androgenic'",
}


def verify_seed(engine: Engine) -> list[tuple[str, int, int]]:
    """Return (check, expected, actual) for every gate check."""
    with engine.connect() as connection:
        return [
            (name, expected, connection.execute(text(VERIFY_QUERIES[name])).scalar_one())
            for name, expected in EXPECTED.items()
        ]
