# antimemes.is brand system (2026-11-05)

**Domain correction:** the registered domain is **antimemes.is** (no hyphen). Lab: https://antimemes.is. Debate: https://debate.antimemes.is. The wordmark can still read `antimemes`.

One site, one visual language, one sub-brand. Owner: Benjamin Life (@omniharmonic). Never OpenCivics. The word "Dialogos" is retired from everything a visitor can see (page titles, headers, meta, share cards, About, emails). Internal code names (package names, `dialogos-fingerprint` Vercel project) can stay.

## Architecture
- **antimemes.is**: the lab. The scroll story, the idea, the instruments, the rules.
- **debate.antimemes.is**: **The Great AI Debate**, the first release. The survey, results, thinkers, profiles, statements, the 3D Lifeworld Atlas, About, privacy.
- They are one site in two places. Every page on both carries the same top bar: the antimemes wordmark at left (`antimemes`, one word in Anton, no symbol) linking to https://antimemes.is, then on debate pages a slash and the sub-brand "The Great AI Debate" linking to the debate home. Same footer on both: "antimemes.is, an arts lab by Benjamin Life", links to the lab, the debate, About/method, privacy, portrait credits.
- Links between them are absolute and live in one config constant per app (`LAB_URL = "https://antimemes.is"`, `DEBATE_URL = "https://debate.antimemes.is"`).

## Ground and type (shared, from the lab)
- Dark first, everywhere: ground `#121820`, ground-2 `#19212b`, panel `#161d26`, rule `#2b3644`, rule-2 `#3a4757`, ink `#dde4eb`, ink-2 `#9aa7b6`, ink-3 `#6f7c8c`. A light theme may remain for the debate as an option, but the default and all screenshots/OG cards are dark.
- Type: Newsreader (argument, headlines, body), IBM Plex Sans Condensed (UI, labels, data readouts), Anton only for meme moments and the wordmark. No other faces.
- Two signals with fixed meaning across both: `--heat #ff5468` = rivalry, contagion, "unlike you"/disagreement-as-heat; `--recog #8fb0ff` = recognition, understanding, links, focus rings.
- Four camp colours (data encoding only, same everywhere, camp order c1..c4): `#e2b14a`, `#4cc2ae`, `#c08cf0`, `#e6dfcf`; ungrouped `#6e7b8b`.
- Ops-console furniture used sparingly: hairline corner brackets on framed panels, small Plex readouts (tabular numerals), crosshair on the graph. No neon glows, no gradients as decoration.

## The Great AI Debate sub-brand (keeps its identity)
- Name: "The Great AI Debate". Subtitle where needed: "Where do you stand on AI's future?". The fingerprint/glyph artwork and the Wrapped-style results story stay; they are its signature.
- Its own accent for agree/disagree marks: agree `#43c3a3`, disagree `#f06a9b`, unsure `#7d8796` (already the debate's dark palette). Agreement shading on the map uses these. Everything else uses the shared ground, type and signals.
- Wordmark lockup: `antimemes / The Great AI Debate`.

## The graph (the shared signature)
The live force graph from the lab home page is the house visual: real faces as round nodes ringed in camp colour, hairline links where published words agree, gentle gravity that settles, drag to pull a face, hover/tap for the hover card, crosshair + readout. The results map, the thinkers map and the 3D atlas all use this language so moving between them feels like zooming into one instrument. Respect prefers-reduced-motion (settled, static layout).

## The throughline (say it everywhere, briefly)
Mimesis makes us copy each other's enemies; schismogenesis splits us; the lab's answer is anti-mimesis: meeting difference without imitating or fighting it, measured by meta-consensus (each side can describe the other in terms the other would sign).
- **SEE**: The Great AI Debate maps the memetic landscape of AI from public figures' own words. Your answers place you on that map. (This is the first instrument.)
- **MEET**: from your map, the next step is to read the strongest version of a camp you're far from, and later write descriptions of other camps that they would sign (steelmen, anti-debates).
- **MOVE**: descriptions the described side signs earn bridging reputation, Community-Notes style; agents get a separate board and never ratify.
The debate's results page ends with this handoff ("You've seen the map. Now meet the far side.") pointing back to the lab, and the lab's debate section explains how the map feeds MEET and MOVE. Never claim MEET/MOVE features exist if they don't: say "next" or "coming".

## Copy rules
Plain, sharp, sentence case, no lorem ipsum, no fabricated numbers, no all-caps labels except Anton meme moments. Public figures only from their own public words; quotes ≤280 chars with links; a dispute route stays visible.
