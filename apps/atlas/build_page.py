"""Pour atlas.json into the page template.

Usage: build_page.py <atlas.json> <output.html> [--full-document]
The artifact host adds the document skeleton, so --full-document is only for local browser tests.
"""

import json
import pathlib
import sys

TEMPLATE = pathlib.Path(__file__).parent / "atlas.tpl.html"


def main(data: str, output: str, *flags: str) -> None:
    atlas = json.dumps(json.loads(pathlib.Path(data).read_text()), ensure_ascii=False)
    page = TEMPLATE.read_text().replace("/*ATLAS*/", atlas.replace("</", "<\\/"))
    if "--full-document" in flags:
        page = (
            '<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'
            + page
            + "</body></html>"
        )
    pathlib.Path(output).write_text(page)


if __name__ == "__main__":
    main(*sys.argv[1:])
