"""Labelled fake voters for demo rooms and tests. Never counted outside a demo room (PRD R14).

Three planted personas follow the bundle's camps on the anchor statements, with noise. Extra
statements plant one bridge (every persona agrees) and one divider (one persona against the rest),
so tests can check that the analysis finds what was planted.
"""

import numpy as np

DEMO_STATEMENTS = [
    ("bridge", "Labs should publish the results of their dangerous-capability evaluations."),
    ("divider", "Open-weight frontier models should be legal to release without a licence."),
    ("bridge", "People should be told when they are talking to an AI rather than a human."),
    ("mixed", "The US government should build its own frontier AI capacity."),
]


def persona_stances(bundle: dict) -> dict[str, dict[str, int]]:
    """Camp id -> anchor id -> stance, from the camp majority, else a fixed coin per anchor."""
    out: dict[str, dict[str, int]] = {}
    for n, camp in enumerate(bundle["camps"]):
        stances = {}
        for k, anchor in enumerate(bundle["anchors"]):
            entry = bundle["stances"][anchor["id"]]
            total = sum(entry[m]["a"] for m in camp["members"] if m in entry)
            stances[anchor["id"]] = (
                (1 if total > 0 else -1) if total else (1 if (n + k) % 2 else -1)
            )
        out[camp["id"]] = stances
    return out


def synthetic_votes(
    bundle: dict,
    extra: dict[str, str],
    n: int = 120,
    seed: int = 7,
    noise: float = 0.15,
    coverage: float = 0.75,
) -> tuple[list[tuple[str, str, int]], dict[str, str]]:
    """Rows of (participant, statement, vote) and each synthetic participant's persona.

    `extra` maps statement id -> planted kind ('bridge', 'divider' or 'mixed').
    `anchor statement ids` are the anchor ids themselves; callers map them to room ids.
    """
    random = np.random.default_rng(seed)
    personas = persona_stances(bundle)
    names = sorted(personas)
    rows: list[tuple[str, str, int]] = []
    membership: dict[str, str] = {}
    for i in range(n):
        persona = names[i % len(names)]
        participant = f"synthetic-{i:03d}"
        membership[participant] = persona
        plan = dict(personas[persona])
        for statement, kind in extra.items():
            if kind == "bridge":
                plan[statement] = 1
            elif kind == "divider":
                plan[statement] = 1 if persona == names[0] else -1
            else:
                plan[statement] = 1 if random.random() < 0.5 else -1
        for statement, stance in plan.items():
            if random.random() > coverage:
                continue
            roll = random.random()
            vote = 0 if roll < 0.08 else (-stance if roll < 0.08 + noise else stance)
            rows.append((participant, statement, int(vote)))
    return rows, membership
