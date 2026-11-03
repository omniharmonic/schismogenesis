# Deploying the AI Futures Fingerprint

For Benjamin, or whoever runs the launch. Nothing here has been done yet. Each step that makes something public, or that costs money, needs Benjamin's yes first.

## What runs in production
- **One web container** (`infra/arena/Dockerfile`, about 800 MB). It serves the pages, the API and the share images. No GPU and no paid API.
- **One Postgres database.** Neon's free tier works. Use a **separate production branch or project**, not the dev database, which holds the synthetic demo voters.

## 1. Choose a host (Benjamin)
Any container host works. Prices change, so check current pricing before choosing.
- **Fly.io, Render or Railway:** an always-on small container, usually a few dollars a month. This is the simplest choice.
- **Google Cloud Run:** scales to zero and has a free tier, but needs a Google Cloud billing account.
- **Vercel:** possible in principle (Python functions), but this app's scientific libraries are large. Check Vercel's current function size limit before choosing it.

Claude's recommendation: Fly.io or Render, with Neon for the database.

## 2. Create the production database
1. In Neon, create a project or branch called `fingerprint-prod`, and copy its connection string.
2. Apply the schema from your machine:
   ```
   ARENA_DATABASE_URL='postgresql://…prod…' make migrate
   ARENA_DATABASE_URL='postgresql://…prod…' uv run python scripts/rooms.py ensure
   ```
   Never run `scripts/rooms.py demo` against production. The demo room's fake voters belong only in dev.

## 3. Set the secrets on the host

| Variable | Value |
|---|---|
| `ARENA_DATABASE_URL` | the production connection string |
| `ARENA_ADMIN_TOKEN` | a random string of 32+ characters (`python -c "import secrets; print(secrets.token_urlsafe(32))"`); keep it in a password manager |
| `ARENA_PUBLIC_URL` | `https://your-domain` (used in share links and preview cards) |
| `ARENA_X_CLIENT_ID`, `ARENA_X_CLIENT_SECRET` | only if X sign-in is on (step 5) |
| `ARENA_CLIENT_IP_HEADER` | the header your host sets to the visitor's real address: `Fly-Client-IP` on Fly.io, `CF-Connecting-IP` behind Cloudflare. Without it, the app counts one proxy hop from the right of `X-Forwarded-For`; set `ARENA_PROXY_HOPS` if there are more. Rate limits depend on this being right. |

Also cap request bodies at 64 KB at the host or proxy if it allows (the app enforces this too).

The image already sets `ARENA_ENV=production`, `ARENA_TRUST_PROXY=1` and port 8080. In production the app refuses to start without a strong admin token.

## 4. Deploy and check
1. Build and push with the host's own tool, for example `fly deploy --dockerfile infra/arena/Dockerfile`.
2. Open `https://your-domain/api/health`. It should return `{"ok": true, …}`.
3. Take the fingerprint once on a phone, publish an anonymous link, and paste it into X's and Bluesky's composers to see the preview card. Then delete the link.
4. Open `/admin.html`, load it with the admin token, and check the daily counts appear.

## 5. X sign-in (optional)
1. At developer.x.com, create a project and app, and switch on OAuth 2.0 as a "Web App".
2. Callback URL: `https://your-domain/auth/x/callback`. Website: `https://your-domain`.
3. Scopes are read-only (`users.read tweet.read`); we only read name, handle and picture.
4. Put the client ID and secret into the host's secrets and redeploy. The X option then appears in the share sheet.
5. Confirm the X API tier you're on allows "Sign in with X" before announcing it.

## 6. Domain
Point the domain at the host (each host documents its DNS records), then set `ARENA_PUBLIC_URL` to match.

## Day to day
- **Moderation:** `/admin.html`. Approve or reject room statements, read misreading reports, and hide profiles.
- **Counts:** the admin page shows daily totals for starts, finishes, shares and publishes.
- **Load:** `make load-test` checks a 10,000-person room locally (about 9 seconds on an idle laptop). Reports are cached and recomputed at most once a minute per room.
- **Rolling back:** redeploy the previous image. Migrations only add tables, so older images keep working.
