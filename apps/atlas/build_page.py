"""Pour atlas.json into the page template.

Usage: build_page.py <atlas.json> <output.html> [--full-document]
The artifact host adds the document skeleton, so --full-document is only for local browser tests.

When a fingerprint.json sits next to the output (the debate app's bundle), each person's portrait,
role and sharpest positions are taken from it for the faces and hover cards. Without one, the
page falls back to initials and the atlas's own text.
"""

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE / "atlas.tpl.html"
COPY = HERE / "copy.json"
# copy the page shows directly; the rest of the copy reaches it through build_atlas.py
PAGE_COPY = ("headline", "intro")


def cards(bundle: dict) -> dict:
    """Per person: face, role, initials and up to three positions, sharpest splits first.

    Mirrors hoverCardHTML in apps/arena/public/hovercard.js for a visitor with no answers.
    """
    out = {}
    for t in bundle.get("thinkers", []):
        tid = t["id"]
        rows = [
            (a, bundle["stances"][a["id"]][tid]["a"])
            for a in bundle.get("anchors", [])
            if tid in bundle.get("stances", {}).get(a["id"], {})
        ]
        rows.sort(key=lambda r: -(r[0].get("split_score") or 0))
        card = {
            "initials": t.get("initials"),
            "positions": [{"side": side, "text": a["text"]} for a, side in rows[:3]],
        }
        if not rows and bundle.get("voices", {}).get(tid):
            card["voices"] = [v["position"] for v in bundle["voices"][tid][:2]]
        for key in ("face", "role", "provisional", "between"):
            if t.get(key):
                card[key] = t[key]
        out[tid] = card
    return out


def main(data: str, output: str, *flags: str) -> None:
    atlas = json.loads(pathlib.Path(data).read_text())
    if COPY.exists():
        copy = json.loads(COPY.read_text())
        atlas.setdefault("copy", {}).update({k: copy[k] for k in PAGE_COPY if k in copy})
    bundle_path = pathlib.Path(output).parent / "fingerprint.json"
    people = cards(json.loads(bundle_path.read_text())) if bundle_path.exists() else {}

    def embed(obj: object) -> str:
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    page = (
        TEMPLATE.read_text().replace("/*ATLAS*/", embed(atlas)).replace("/*CARDS*/", embed(people))
    )
    if "--full-document" in flags:
        page = (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
            "</head><body>" + page + "</body></html>"
        )
    pathlib.Path(output).write_text(page)


if __name__ == "__main__":
    main(*sys.argv[1:])
