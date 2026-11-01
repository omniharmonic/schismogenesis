"""Ingest one written work as episode + transcript + paragraph segments (ADR-030)."""

import hashlib
import json
import pathlib
from dataclasses import dataclass

from arena_core.provenance import code_ref
from arena_core.storage import FileSourceStore
from sqlalchemy import Engine, text


@dataclass(frozen=True)
class WrittenWork:
    url: str
    title: str
    author_id: str
    published: str
    channel: str
    channel_platform: str = "website"
    format: str = "essay"
    authorship: str = "own_name"
    language: str = "en"


def paragraphs(body: str) -> list[str]:
    return [" ".join(part.split()) for part in body.split("\n\n") if part.strip()]


def ingest_written(
    engine: Engine, store: FileSourceStore, work: WrittenWork, path: pathlib.Path
) -> str:
    """Return the episode id. Ingesting the same URL again changes nothing."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).digest()
    with engine.begin() as connection:
        existing = connection.execute(
            text("SELECT episode_id FROM episode WHERE platform = :p AND external_id = :e"),
            {"p": work.channel_platform, "e": work.url},
        ).scalar_one_or_none()
        if existing:
            return str(existing)
        known = connection.execute(
            text("SELECT 1 FROM landmark WHERE landmark_id = :a"), {"a": work.author_id}
        ).first()
        if not known:
            raise ValueError(f"unknown landmark: {work.author_id}")

        version = code_ref()
        run_id = connection.execute(
            text(
                "INSERT INTO pipeline_run (stage, job_name, trigger, code_ref, params) "
                "VALUES ('S4', 'ingest_written', 'manual', :v, CAST(:p AS jsonb)) RETURNING run_id"
            ),
            {"v": version, "p": json.dumps({"url": work.url})},
        ).scalar_one()
        common = {"run": run_id, "v": version, "h": digest}
        channel_id = connection.execute(
            text("SELECT channel_id FROM channel WHERE platform = :p AND title = :t"),
            {"p": work.channel_platform, "t": work.channel},
        ).scalar_one_or_none()
        if channel_id is None:
            channel_id = connection.execute(
                text(
                    "INSERT INTO channel (platform, title, run_id, model_version, inputs_hash) "
                    "VALUES (:p, :t, :run, :v, :h) RETURNING channel_id"
                ),
                {**common, "p": work.channel_platform, "t": work.channel},
            ).scalar_one()
        episode_id = connection.execute(
            text(
                "INSERT INTO episode (channel_id, platform, external_id, url, title, published_at,"
                " language, format, authorship, transcript_status, discovered_via, run_id,"
                " stage, model_version, inputs_hash) VALUES (:c, :p, :u, :u, :t, :d, :l, :f, :a,"
                " 'fetched', CAST(:via AS jsonb), :run, 'S4', :v, :h) RETURNING episode_id"
            ),
            {
                **common,
                "c": channel_id,
                "p": work.channel_platform,
                "u": work.url,
                "t": work.title,
                "d": work.published,
                "l": work.language,
                "f": work.format,
                "a": work.authorship,
                "via": json.dumps([{"method": "manual"}]),
            },
        ).scalar_one()
        connection.execute(
            text(
                "INSERT INTO appearance (episode_id, person_id, mention_text, role, evidence,"
                " resolution_confidence, resolution_method, status, run_id, stage, model_name,"
                " model_version, inputs_hash) VALUES (:e, :a, :a, 'author', ARRAY['byline'], 1,"
                " 'manual', 'accepted', :run, 'S4', 'code', :v, :h)"
            ),
            {**common, "e": episode_id, "a": work.author_id},
        )
        transcript_id = connection.execute(
            text(
                "INSERT INTO transcript (episode_id, route, language, has_diarization,"
                " has_word_timestamps, storage_ref, rights_basis, run_id, stage, model_name,"
                " model_version, inputs_hash) VALUES (:e, 'written_source', :l, false, false,"
                " :ref, 'public_web', :run, 'S4', 'code', :v, :h) RETURNING transcript_id"
            ),
            {**common, "e": episode_id, "l": work.language, "ref": store.put(raw, ".txt")},
        ).scalar_one()
        connection.execute(
            text(
                "INSERT INTO private.segment (transcript_id, seq, text, person_id, speaker_kind,"
                " attribution_confidence, locator) VALUES (:t, :s, :x, :a, 'person', 1,"
                " CAST(:loc AS jsonb))"
            ),
            [
                {
                    "t": transcript_id,
                    "s": seq,
                    "x": body,
                    "a": work.author_id,
                    "loc": json.dumps({"paragraph": seq + 1}),
                }
                for seq, body in enumerate(paragraphs(raw.decode()))
            ],
        )
    return str(episode_id)
