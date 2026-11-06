# Accounts round 2: your results, sharing, the next step, camp names, scale, brand — 2026-11-05

Owner: Benjamin Life. From his notes after X and Bluesky sign-in went live (2026-11-05).

## What he asked for
1. Your own results are nearly impossible to find again. The You tab gets a side navigation:
   **Your results** and **Settings**. The results page gets an easy "find me".
2. Share your results to X and Bluesky, when they're first made and any time after.
3. Pull more of your X / Bluesky profile so it feels like your actual profile.
4. On your first results, the map still says "You", and if you're signed in it shows your picture
   there, so you feel you're among the thinkers.
5. Lab landing page: drop the "anyone will do" text (let the animation tell it); drop the glitch /
   3D text effects; drop the block-letter See / Meet / Move keys; a cleaner wordmark, closer to
   Palantir but still internet-culture; copy rooted in theory (Girard, Bateson, Habermas) that makes
   clear your Debate answers are themselves part of the process; a brand that can grow from AI
   policy to the whole pop-culture memetic landscape.
6. Hold people's hand to the next step: after seeing yourself on the map, add statements; the
   reward is agreement across clusters. An MVP must exist for launch.
7. Ready for volume: stress test, and a map that still reads with thousands of people (density,
   clusters you can zoom into).
8. Naming camps: in-house for now, but verified people in a cluster can propose a name for it,
   share it with others in their cluster, vote, and suggest alternatives. A communicative reason
   space in Habermas's sense.

## Calls Claude made (check these)
- **One public results page per account**, at the existing `/p/<code>` address, kept up to date as
  answers change (the code stays the same). It shows the account's picture, name, bio and social
  links. It is created the first time someone shares or switches on "Show me on the map", never
  silently. Anonymous share links keep working as before.
- **Sharing** uses each network's own compose page (x.com/intent/post and bsky.app/intent/compose)
  with the results link; the link's preview card is the existing fingerprint card. No posting on
  anyone's behalf, no extra permissions.
- **Profile details** we already may read: X `description, location, url, verified,
  public_metrics, created_at`; Bluesky `description, banner, followersCount`. The provider bio fills
  the account bio only when the account has none.
- **Next step MVP** = the existing live room (people add statements, vote, Polis groups, Community
  Notes-style bridging), made account-aware: signed-in people join with their account, statements
  they write show on their results page with how many groups agreed, and a "Bridges" board ranks
  statements by cross-group agreement with their authors' names (if the author shows themselves).
  Agents never ratify; moderation stays with Benjamin (existing admin page).
- **Camp names**: a person may propose and vote on names only for the camp and school their own
  nearest thinker sits in, and only with a Bluesky or X sign-in (one account, one vote per
  proposal). Proposals show to others in that cluster with vote counts; Benjamin ratifies from the
  admin page; nothing renames on the public map until he does.
- **Scale**: below 400 people, dots and faces as now. Above it, the people layer becomes a density
  field (hex bins shaded by count) with faces of people who show themselves on top; zooming or
  selecting a camp opens that area at full detail. The server bins positions, so the payload stays
  small. Load test: synthetic 50k sheets for results, people map and account writes.
- **Wordmark**: three directions are shown to Benjamin to pick; until he picks, the current mark
  stays but loses its glitch and 3D effects.

## API additions
- `GET /api/me` adds `profile: {code, url, listed} | null` and `socials: [{kind, handle, url,
  description, location, website, followers, banner?}]`.
- `PUT /api/me/profile` body `{summary, glyph, listed}` (summary and glyph as for POST
  /api/profiles) → `{code, url}`; same code on every call. Uses the account's picture, name, bio and
  its Bluesky/X handle (first found) as identity; anonymous accounts publish as anon.
- `DELETE /api/me/profile` → removes the public page.
- `GET /api/profiles/{code}` adds `bio`, `socials` (public fields only) for account profiles.
- Room: `POST /api/rooms/{slug}/join` accepts a signed-in session in place of a key; `GET
  /api/me/statements` → statements I wrote, with status and bridging measures.
- Camp names: `GET /api/camps/names` (proposals with votes, for my cluster when signed in),
  `POST /api/camps/{node}/names` `{name}`, `POST /api/camps/names/{id}/vote` `{up: bool}`; admin
  `POST /api/admin/camps/names/{id}` `{accept: bool}`.
- `GET /api/map/people?bins=1` → hex-binned counts plus faces, when large.
