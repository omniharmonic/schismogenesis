# antimemes.is

The front page for antimemes.is (https://antimemes.is), Benjamin Life's arts lab for dialogue across difference. It's one scrolling page that tells the story: mimetic contagion, then schismogenesis, then the scapegoat, then why the usual fixes fail, then anti-mimesis, the three instruments (SEE, MEET, MOVE), the first release (The Great AI Debate), the loop that connects them (see, meet, move, meta-consensus) and the rules.

The lab and The Great AI Debate (https://debate.antimemes.is) are one site in two places. Both share the top bar (the `anti+memes` wordmark), footer, colours and type set out in `docs/brand/BRAND.md`. A live graph of the real AI Futures map runs behind the page.

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
    img/              favicon.svg, icon-180.png, og.png (1200×630)
    robots.txt        allow all, points at the sitemap
    sitemap.xml       https://antimemes.is/
  deploy/vercel.json  clean URLs and security headers (copied next to the site by deploy.sh)
  deploy.sh           refresh data, assemble build/antimemes, deploy to production
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

## Links to the debate

The top of `site/js/site.js` holds the only copies of the cross-site links: `LAB_URL` (https://antimemes.is), `DEBATE_URL` (https://debate.antimemes.is) and a `CONFIG` of paths (survey `/`, atlas `/atlas`, thinkers `/people`, a thinker's profile `/people#<id>`, about `/about`, privacy `/privacy`). Any element with `data-link="survey"` (or `atlas`, `people`, `debate`, `about`, `privacy`, `lab`) gets its address from there. Links between the lab and the debate open in the same tab, because they are one site.

## The loop scene

`#loop` shows how the debate's map feeds the rest, drawn on the real graph: SEE (an example "you" marker in the largest school), MEET (a dashed path to the school whose centre is farthest away on the map), MOVE (the signed description coming back as bridging reputation) and meta-consensus (every school linked to every other, with the honest count of signed descriptions: 0). The school names come from the data. MEET and MOVE are labelled "Next" and "Coming" because they aren't built yet.

## Deploy

`apps/antimemes/deploy.sh` refreshes the data and deploys to production. It needs Benjamin's go-ahead. The private-preview password gate and the `noindex` header were removed for the public launch.

## Not done yet (needs Benjamin)

- Connecting the domain antimemes.is (and debate.antimemes.is for the debate) in Vercel.
- A "follow" link (newsletter, social handle or email). There's no public channel to point to yet, so the invitation only offers the survey and the Atlas.
- `img/og.png` is a 1200×630 screenshot of the hero with the bar's links swapped for "antimemes.is / First release: The Great AI Debate". To retake it, serve the site and screenshot it at 1200×630.
