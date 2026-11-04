"""Fetch and clean the texts for a source list into data/texts/<key>.txt (never committed).

Usage: uv run --with trafilatura --with pypdf python scripts/fetch_texts.py <sources.json>
       [--only-missing] [--only key,key,...] [--max-words N] [--min-words N]
Extraction is deterministic (trafilatura), so quotes can be checked against the text exactly.
Pages over MAX_WORDS keep their most AI-relevant paragraphs, in their original order.
Polite: one request every two seconds, an honest user agent, and failures are logged, not retried.
"""

import json
import pathlib
import re
import sys
import time
import urllib.request

import trafilatura

MAX_WORDS = 4000
TEXTS = pathlib.Path("data/texts")
LOG = TEXTS / "fetch-log.json"
AGENT = "DialogosResearch/1.0 (public-interest research; contact via omniharmonic on GitHub)"
TOPIC = re.compile(
    r"\b(AI|A\.I\.|AGI|artificial intelligence|superintelligen\w*|machine learning|model|LLMs?|"
    r"alignment|automation|robot\w*|compute|chips?|algorithm\w*|intelligence|technolog\w*|"
    r"regulat\w*|safety|risk|labou?r|jobs?|workers?)\b",
    re.I,
)


def trim(text: str, limit: int = MAX_WORDS) -> str:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    words = sum(len(p.split()) for p in paragraphs)
    if words <= limit:
        return "\n\n".join(paragraphs)
    scored = sorted(
        range(len(paragraphs)),
        key=lambda i: -len(TOPIC.findall(paragraphs[i])) / max(len(paragraphs[i].split()), 20),
    )
    keep, total = set(), 0
    for i in scored:
        n = len(paragraphs[i].split())
        if total + n > limit:
            continue
        keep.add(i)
        total += n
    return "\n\n".join(paragraphs[i] for i in sorted(keep))


def readable(url: str) -> str:
    """LessWrong pages are built by script in the browser; its static mirror has the same text."""
    for host in ("https://www.lesswrong.com/", "https://lesswrong.com/"):
        if url.startswith(host):
            return "https://www.greaterwrong.com/" + url[len(host) :]
    return url


def pdf_text(data: bytes) -> str:
    """Text of a PDF, page by page in order (deterministic, like the HTML extraction)."""
    import io

    from pypdf import PdfReader

    pages = [page.extract_text() or "" for page in PdfReader(io.BytesIO(data)).pages]
    # rejoin lines a PDF breaks mid-sentence, keep blank-line paragraph breaks
    text = "\n\n".join(pages)
    return "\n\n".join(" ".join(p.split()) for p in text.split("\n\n") if p.strip())


def fetch(url: str) -> str | None:
    request = urllib.request.Request(readable(url), headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 (listed sources)
        kind = response.headers.get("Content-Type", "")
        if "pdf" in kind:
            return pdf_text(response.read())
        if "html" not in kind and "text" not in kind:
            raise ValueError(f"not a web page ({kind})")
        html = response.read().decode("utf-8", errors="replace")
    return trafilatura.extract(
        html, include_comments=False, include_tables=False, favor_recall=True
    )


def main(sources: str, *flags: str) -> None:
    TEXTS.mkdir(parents=True, exist_ok=True)
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    limit = int(flags[flags.index("--max-words") + 1]) if "--max-words" in flags else MAX_WORDS
    floor = int(flags[flags.index("--min-words") + 1]) if "--min-words" in flags else 300
    only = set(flags[flags.index("--only") + 1].split(",")) if "--only" in flags else None
    for work in json.loads(pathlib.Path(sources).read_text())["works"]:
        path = TEXTS / f"{work['key']}.txt"
        if path.exists() and "--only-missing" in flags:
            continue
        if (only is not None and work["key"] not in only) or work.get("duplicate_of"):
            continue
        try:
            text = fetch(work["url"])
            if not text or len(text.split()) < floor:
                raise ValueError(f"too little text ({len((text or '').split())} words)")
            path.write_text(trim(text, limit) + "\n")
            log[work["key"]] = {
                "ok": True,
                "words": len(path.read_text().split()),
                "url": work["url"],
            }
        except Exception as error:  # every failure is recorded for a person to look at
            log[work["key"]] = {"ok": False, "error": str(error)[:200], "url": work["url"]}
        print(work["key"], "ok" if log[work["key"]]["ok"] else log[work["key"]]["error"])
        LOG.write_text(json.dumps(log, indent=1))
        time.sleep(2)


if __name__ == "__main__":
    main(*sys.argv[1:])
