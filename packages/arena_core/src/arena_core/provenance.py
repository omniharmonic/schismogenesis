"""Provenance helpers (spine §5) and the append-only event log."""

import hashlib
import json
import subprocess
from typing import Any

from sqlalchemy import Connection, text


def inputs_hash(*parts: bytes) -> bytes:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(hashlib.sha256(part).digest())
    return digest.digest()


def code_ref() -> str:
    """Git sha of the running code, or 'unknown' outside a checkout."""
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def log_events(connection: Connection, events: list[dict[str, Any]]) -> None:
    """Append events. Each dict needs type, actor_type, actor_id, entity_type, entity_id,
    payload and run_id."""
    if events:
        connection.execute(
            text(
                "INSERT INTO event_log "
                "(type, actor_type, actor_id, entity_type, entity_id, payload, run_id) "
                "VALUES (:type, :actor_type, :actor_id, :entity_type, :entity_id, "
                "CAST(:payload AS jsonb), :run_id)"
            ),
            [{**event, "payload": json.dumps(event["payload"])} for event in events],
        )
