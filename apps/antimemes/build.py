#!/usr/bin/env python3
"""Refresh the anti-memes.is site data from the live Fingerprint bundle.

Reads   apps/arena/public/fingerprint.json   (the current AI Futures map)
        apps/arena/public/faces/<id>.jpg      (portraits)
        seed/SEED-v4.json                     (held-out landmark list, safety check)
Writes  apps/antimemes/site/map-data.json     (people, links, schools: first paint)
        apps/antimemes/site/map-quotes.json   (quotes and source links: loaded lazily)
        apps/antimemes/site/faces/<id>.jpg    (only portraits that have a credit)

Run from anywhere:  python3 apps/antimemes/build.py
Safe to re-run; it rebuilds both outputs from scratch each time.
Nothing here invents content: every name, quote, link and label comes from the bundle.
"""

from __future__ import annotations

import json
import shutil
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BUNDLE = REPO / "apps/arena/public/fingerprint.json"
FACES_SRC = REPO / "apps/arena/public/faces"
SEED = REPO / "seed/SEED-v4.json"
SITE = HERE / "site"
OUT = SITE / "map-data.json"  # people, links, schools, statements: needed for first paint
OUT_QUOTES = SITE / "map-quotes.json"  # stances with quotes and voices: loaded after first paint
FACES_OUT = SITE / "faces"

MIN_SHARED = 4  # statements two people must both have a stance on before we draw a link
LINKS_PER_NODE = 3  # strongest kin links kept per person
MIN_KIN = 0.34  # agreement score (-1..1) a kin link needs


def held_out_ids() -> set[str]:
    """Landmarks flagged for Benjamin's review. They must never appear on the public site."""
    if not SEED.exists():
        return set()
    flags = json.loads(SEED.read_text()).get("flags_for_benjamin", {})
    ids = set()
    for key in ("landmarks", "conflict_flags"):
        for item in flags.get(key, []) or []:
            if item.get("landmark_id"):
                ids.add(item["landmark_id"])
    return ids


def main() -> int:
    data = json.loads(BUNDLE.read_text())
    blocked = held_out_ids()

    thinkers = [t for t in data["thinkers"] if t["id"] not in blocked]
    dropped = [t["id"] for t in data["thinkers"] if t["id"] in blocked]
    if dropped:
        print(
            f"warning: removed held-out landmarks from the bundle copy: {dropped}", file=sys.stderr
        )
    ids = {t["id"] for t in thinkers}

    credits = data.get("faces", {}) or {}

    # Portraits: copy only those with a recorded credit, so every image shown is credited.
    if FACES_OUT.exists():
        shutil.rmtree(FACES_OUT)
    FACES_OUT.mkdir(parents=True)
    people = []
    for t in thinkers:
        face = None
        src = FACES_SRC / f"{t['id']}.jpg"
        if t["id"] in credits and src.exists():
            shutil.copy2(src, FACES_OUT / src.name)
            face = f"faces/{src.name}"
        people.append(
            {
                "id": t["id"],
                "name": t["name"],
                "initials": t.get("initials") or "".join(w[0] for w in t["name"].split()[:2]),
                "school": t.get("school"),
                "between": t.get("between"),
                "path": t.get("path"),
                "x": t.get("x", 0.0),
                "y": t.get("y", 0.0),
                "face": face,
                "provisional": bool(t.get("provisional")),
            }
        )

    # Stances, compact: {statement_id: {person_id: [agree(+1/-1), quote, url, work]}}
    stances = {}
    for sid, row in data["stances"].items():
        stances[sid] = {
            pid: [s["a"], s.get("q", ""), s.get("url", ""), s.get("work", "")]
            for pid, s in row.items()
            if pid in ids
        }

    # Kin links: share of agreements on statements both people took a side on.
    by_person: dict[str, dict[str, int]] = {pid: {} for pid in ids}
    for sid, row in stances.items():
        for pid, s in row.items():
            by_person[pid][sid] = s[0]
    pair_score = {}
    for a, b in combinations(sorted(ids), 2):
        shared = by_person[a].keys() & by_person[b].keys()
        if len(shared) < MIN_SHARED:
            continue
        score = sum(by_person[a][s] * by_person[b][s] for s in shared) / len(shared)
        pair_score[(a, b)] = (round(score, 3), len(shared))
    links = {}
    for pid in ids:
        mine = [
            ((a, b), v) for (a, b), v in pair_score.items() if pid in (a, b) and v[0] >= MIN_KIN
        ]
        mine.sort(key=lambda kv: (-kv[1][0], -kv[1][1]))
        for (a, b), (score, n) in mine[:LINKS_PER_NODE]:
            links[(a, b)] = {"s": a, "t": b, "w": score, "n": n}
    # Rival links: strongest disagreements, used for the schismogenesis scene.
    rivals = sorted(
        ((k, v) for k, v in pair_score.items() if v[0] <= -0.5 and v[1] >= MIN_SHARED),
        key=lambda kv: (kv[1][0], -kv[1][1]),
    )[:60]

    # Voices: first short position line per person (used in the dossier panel).
    voices = {}
    for pid, items in (data.get("voices") or {}).items():
        if pid in ids and items:
            voices[pid] = [
                {
                    "position": v.get("position", ""),
                    "quote": v.get("quote", ""),
                    "url": v.get("url", ""),
                    "work": v.get("work", ""),
                }
                for v in items[:3]
            ]

    nodes = data["tree"]["nodes"]
    schools = []
    for rid in data["tree"]["roots"]:
        n = nodes[rid]
        schools.append(
            {
                "id": rid,
                "label": n["label"],
                "note": n.get("note", ""),
                "members": [m for m in n.get("members", []) if m in ids],
                "children": [
                    {"id": c, "label": nodes[c]["label"], "note": nodes[c].get("note", "")}
                    for c in n.get("children", [])
                    if c in nodes
                ],
            }
        )

    out = {
        "source": "apps/arena/public/fingerprint.json",
        "bundle_version": data.get("version"),
        "season": data.get("season"),
        "atlas_version": data.get("atlas_version"),
        "sets": data.get("sets", []),
        "statements": [
            {"id": a["id"], "set": a["set"], "layer": a["layer"], "text": a["text"]}
            for a in data["anchors"]
        ],
        "people": people,
        "links": list(links.values()),
        "rivals": [{"s": a, "t": b, "w": v[0], "n": v[1]} for (a, b), v in rivals],
        "schools": schools,
        "camps": [
            {"label": c["label"], "members": [m for m in c["members"] if m in ids]}
            for c in data.get("camps", [])
        ],
        "notes": data.get("notes", []),
        "credits": {pid: credits[pid] for pid in ids if pid in credits},
    }
    # Who took which side, without quotes, so the split board can draw before quotes arrive.
    out["sides"] = {sid: {pid: s[0] for pid, s in row.items()} for sid, row in stances.items()}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    OUT_QUOTES.write_text(
        json.dumps(
            {"stances": stances, "voices": voices}, ensure_ascii=False, separators=(",", ":")
        )
    )
    n_faces = sum(1 for p in people if p["face"])
    n_stances = sum(len(v) for v in stances.values())
    n_links, n_rivals = len(out["links"]), len(out["rivals"])
    print(f"wrote {OUT.relative_to(REPO)} and {OUT_QUOTES.name}: {len(people)} people,")
    print(f"  {len(out['statements'])} statements, {n_stances} stances, {n_links} kin links,")
    print(f"  {n_rivals} rival links, {n_faces} portraits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
