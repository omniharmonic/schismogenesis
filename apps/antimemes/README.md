# anti-memes.is

The front page for anti-memes.is, Benjamin Life's arts lab for dialogue across difference. It's one scrolling page that tells the story: mimetic contagion, then schismogenesis, then the scapegoat, then why the usual fixes fail, then anti-mimesis, the three instruments (SEE, MEET, MOVE), the first release (The Great AI Debate) and the rules. A live graph of the real AI Futures map runs behind the page.

It's a static site with no framework and no build step. It uses no third-party scripts, and the fonts are hosted in the site folder.

## Layout

```
apps/antimemes/
  build.py            refreshes the map data and portraits from the Fingerprint bundle
  site/
    index.html        the page
    css/site.css      design tokens and layout
    js/site.js        graph, scroll scenes, entity panel, split board (vanilla JS)
    map-data.json     people, links, schools, statements (generated; loads first)
    map-quotes.json   stances with quotes and source links (generated; loads when idle)
    faces/            portraits, only those with a recorded credit (generated)
    fonts/            Anton, IBM Plex Sans Condensed, Newsreader (SIL OFL)
    img/              favicon.svg, icon-180.png, og.png
```

File names avoid words that ad blockers block, such as `fingerprint` or `analytics`.

## Refresh the data

The map is being enlarged elsewhere. To pick up the current bundle, run:

```
python3 apps/antimemes/build.py
```

The script reads `apps/arena/public/fingerprint.json` and `apps/arena/public/faces/`. It drops any landmark listed in `seed/SEED-v4.json` → `flags_for_benjamin` as a safety check. Then it rewrites `map-data.json`, `map-quotes.json` and `faces/`.

Every name, quote, link, school label and portrait credit comes from the bundle; the page invents nothing. The scenes adapt to the data:
- The split scene picks the statement that divides the map most evenly.
- The contagion scene spreads outward from the best-connected person, along real agreement links.
- The plural scene groups people by the schools at the top of the bundle's tree.

## Preview locally

```
python3 -m http.server 8811 --directory apps/antimemes/site
```

Then open http://localhost:8811.

## Links to change later

The top of `site/js/site.js` holds one `CONFIG` object:
- `debateBase` is currently https://dialogos-fingerprint.vercel.app.
- `surveyPath` and `atlasPath` are added to that address.

When the debate moves to a subdomain, change `debateBase` there. The `og:image` URL in `index.html` already assumes https://anti-memes.is.

## Not done yet (needs Benjamin)

- Deployment and connecting the domain. Nothing has been published.
- A "follow" link (newsletter, social handle or email). There's no public channel to point to yet, so the invitation only offers the survey and the Atlas.
- `img/og.png` is a screenshot of the hero. To retake it, serve the site and screenshot it at 1200×630.
