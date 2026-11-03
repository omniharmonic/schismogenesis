# AI Futures Fingerprint: launch round

Owner: Benjamin Life. Drafted by Claude, 2026-11-02, from Benjamin's direction of the same day:
"make it even more robust to prep for a real launch… a serious thinkers version of spotify wrapped… are we doing proper polis-style clustering? can we do any better data analysis on the backend? allow someone to publish their profile to the site if they want? anonymous or with their twitter/bsky handle / pfp?… get ready to ship it to production."

This extends `01-PRD.md`, `02-ARCHITECTURE.md` and `03-IMPLEMENTATION-PLAN.md`. Where they conflict, this file wins for the launch.

## Status (2026-11-03)
L1 to L5 are built and pass `make ci`. Deployment (L6) waits on Benjamin's decisions in section 5.
- Done:
  - the Wrapped story, with savable story images;
  - share links with server-drawn preview cards;
  - anonymous and verified Bluesky profiles;
  - X sign-in, built but off until an X app exists;
  - the `/people` directory;
  - the analysis upgrades;
  - "You in the room";
  - thinkers placed in the room;
  - the Postgres report cache and rate limits;
  - security headers;
  - self-hosted fonts;
  - About and Privacy pages;
  - counters;
  - a production container image, built and smoke-tested;
  - the deploy runbook (`docs/runbooks/fingerprint-deploy.md`).
- Not done:
  - Cloudflare Turnstile. It isn't wired in; add it if bots show up.
  - The blind slant review of the 24 statements.
- Changed from the plan: the 10,000-person speed check runs with `make load-test`, not in CI, because a timed test fails whenever the machine is busy.

## 1. Product: what changes

### 1.1 The reveal becomes "Wrapped"
- After the last answer, a full-screen story plays: one idea per slide. Tapping or pressing a key moves it on, and there are progress bars at the top. Each slide has a "Save this slide" button that makes a 1080×1920 story image.
- The slides, in order:
  1. **Your print.** The ridge pattern is drawn from your answers and animates in.
  2. **Your neighbourhood.** "Closest to the Long-term stewards."
  3. **Your top match.** The thinker, the agreement count, and one of their real quotes on a statement you agreed on.
  4. **Plot twist.** Your strongest cross-cutting line: where you side against your neighbourhood, and with whom.
  5. **Your furthest.** The thinker you agree with least, with their quote on your biggest disagreement.
  6. **Where the camps split from you.** e/acc, AI safety/EA and d/acc, each with its deepest split layer.
  7. **Your rarest take.** The statement where the fewest thinkers, and the fewest room participants once you've joined, stand with you.
  8. **The map.** You, tethered to your three nearest thinkers.
  9. **Share.** A landscape card (1200×675) and a story card. The share sheet uses the phone's own sharing where it exists, plus links that open a post on X or Bluesky with the text filled in and a link.
- After the story, the full detailed reveal stays below, as it is now: quote mirror, camps table, fairness rating and dispute.

### 1.2 Share links and public profiles (opt-in)
- "Get a share link" publishes a profile at `/p/<code>`. Its preview image is drawn by the server, so posts on X and Bluesky show the card.
- **What gets published.** The person picks one, and sees a preview before anything is sent:
  - **Result only** (default): home school, nearest and furthest three with counts, signature lines and camp splits. Signature lines reveal those few answers, and the preview says so. The ridge pattern on a result-only profile is drawn with the statement order scrambled per profile, so it can't be read back into answers.
  - **Result and answers:** also shows how they answered each statement, which lets others compare with them.
- **How they appear:**
  - **Anonymous:** a generated name, e.g. "Fingerprint K7Q2".
  - **Bluesky:** verified. They post a one-time code from their account, and we check it through Bluesky's free public API, which also gives their display name and picture.
  - **X:** verified through "Sign in with X" (OAuth 2.0). This needs an X developer app (Benjamin to create; the free tier should cover sign-in, to be confirmed before it's switched on). Until then the X option is hidden.
  - Unverified handles are never shown. A viral page that lets anyone post "@someone is closest to X" invites impersonation.
- **Control.** The publisher's browser keeps a private edit key. With it they can change visibility or delete the profile at any time. Deletion removes the row; it doesn't just hide it.
- **The public directory.** `/people` lists only verified, listed profiles, and shows them as dots on the thinker map. The publisher chooses "listed" or "link only", and link only is the default. Admin can hide any profile.
- Profiles count only as self-reported results: the page says "Result as computed in their browser".

### 1.3 Rooms after joining
- The "You in the room" section adds:
  - how rare your overall pattern is (percentile among room participants);
  - your rarest take in the room;
  - the room groups that agree with you most and least;
  - where each thinker would sit in the room.

## 2. Analysis: are we doing proper Polis, and what's better

What we did in round 1 was close to Polis but simplified. For the launch:

1. **Polis's two-stage clustering.** Polis first makes up to 100 small "base clusters" of participants, then groups those into 2 to 5 opinion groups, choosing the number by silhouette. This makes groups stable as rooms grow into the thousands. We now do the same. A participant counts once they have voted on min(7, number of statements).
2. **Group stability.** The report bootstraps the statements 20 times, on up to 1,000 sampled participants, and measures how often the same groups come back (mean adjusted Rand index). Groups are labelled "clear" (≥ 0.8), "tentative" (0.5 to 0.8) or not shown (< 0.5).
3. **Bridging with uncertainty.** Community Notes guards against noisy notes with extra uncertainty checks. We bootstrap participants 20 times and require the lower 10th percentile of neutral agreement to be ≥ 0.65, as well as the point value ≥ 0.75.
4. **Fast and vectorised.** The matrix-factorisation fit is rewritten so a room of 10,000 people and 200 statements reports in seconds. A load test pins this.
5. **Thinkers placed in the room.** Each thinker is treated as a participant who voted only on the anchor statements, and projected into the room's own Polis space (not used to fit it). The room report can then show the room's groups and the 27 thinkers on one picture. This links the room space to the map, as the vision asked.
6. **Per-person measures, shown only to that person:** rarity (mean disagreement with everyone else, as a percentile), rarest take, and nearest and furthest group.
7. **Report caching.** Reports are stored in Postgres and recomputed at most once a minute per room, so a viral spike doesn't recompute on every page load.

## 3. Production

- **Hosting (Benjamin's decision).** Claude's recommendation is Vercel (Python on Fluid Compute) plus Neon Postgres, using a separate production branch. Both have free tiers he already uses. A Dockerfile is also provided, so any container host works.
  - Nothing is deployed until Benjamin says yes.
  - No paid plan is taken without asking.
- **Robustness:**
  - Rate limits move from memory to Postgres, so they work across instances.
  - Request size limits.
  - Strict security headers and a content security policy.
  - The admin token is required in production.
  - A health endpoint.
  - Migrations run as a separate step, never at startup.
- **Pages:** About and method, Privacy, and a "how we read the thinkers" note, all linked from the footer.
- **Measurement without tracking:** daily counters only (starts, finishes, story completed, shares by channel, joins, publishes). No IDs, no cookies, no third-party analytics.
- **Bot defence:** optional Cloudflare Turnstile on join and publish, switched on by setting keys. It's off by default.

## 4. Plan

| Stage | Work | Done when |
|---|---|---|
| L1 | Analysis: base clusters, stability, bootstrapped bridges, vectorised fit, thinkers in room space, per-person measures | Tests for each, plus a 10,000 × 200 load test under 10 s locally |
| L2 | Storage: profiles, verification, report cache, rate limits, counters (migration 0010) | API tests, including a mocked Bluesky check |
| L3 | Profiles: publish, edit and delete, the `/p/<code>` page with server-drawn preview image, `/people` directory | Browser test: publish, view, delete |
| L4 | Wrapped story and share sheet | Browser test at 390 px and 1280 px, light and dark; images save |
| L5 | Production hardening, pages, deploy config, runbook | `make ci`, plus a production-mode smoke test |
| L6 | Benjamin's yes: hosting, domain, X app, then deploy | Live URL |

## 5. Decisions for Benjamin
1. Hosting: Vercel plus Neon (recommended), or another host.
2. Domain name.
3. Create an X developer app, if X sign-in should be on at launch.
4. Whether `/people` (the public directory) launches on day one, or after a week of link-only profiles.
