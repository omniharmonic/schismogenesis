# Deploying the AI Futures Fingerprint (Vercel and Neon)

Benjamin chose Vercel and Neon on 2026-11-03 (D-31.18). This is what is live, and how to change it.

## What's live
- **Site:** https://dialogos-fingerprint.vercel.app, from the Vercel project `dialogos-fingerprint` on the team "omniharmonic's projects".
  - A Python function (FastAPI) serves the pages, API and share images.
  - It's pinned to the `iad1` region, next to the database.
- **Database:** Neon project `dialogos-fingerprint` (id `super-haze-94320885`, region aws-us-east-1), reached through the pooled connection.
  - It holds only real data; the dev project `schismogenesis` holds the synthetic demo voters.
  - Migrations are at `0010_profiles`, and the room `ai-futures` is set up with the 24 season-1 statements.
- **Launch gate:** while `ARENA_SITE_PASSWORD` is set, every page shows a small password page. A correct password sets a 30-day cookie; basic auth also still works for scripts. A password page is used because some browsers, such as Dia, never show the basic-auth prompt. `/api/health` stays open for monitoring. The password is in `.env.production` on Benjamin's machine.

## Secrets
They're kept in `.env.production`, which is git-ignored and never committed. They're also set in Vercel for production and preview.

| Variable | Purpose |
|---|---|
| `ARENA_DATABASE_URL` | Neon pooled connection string |
| `ARENA_ADMIN_TOKEN` | admin page token (`/admin.html`) |
| `ARENA_RATE_SALT` | shared secret, so rate limits hold across instances |
| `ARENA_PUBLIC_URL` | `https://dialogos-fingerprint.vercel.app`, or the custom domain once set |
| `ARENA_SITE_PASSWORD` | the pre-launch gate; **delete this variable to launch** |
| `ARENA_TURNSTILE_SITE_KEY`, `ARENA_TURNSTILE_SECRET` | bot protection, which switches on when both are set (step below) |
| `ARENA_X_CLIENT_ID`, `ARENA_X_CLIENT_SECRET` | optional "Sign in with X" |

## Redeploy after changes
```
uv run python scripts/build_vercel.py          # assembles build/vercel (web app only)
cd build/vercel && vercel deploy --prod --yes --scope omniharmonics-projects
```
`build/vercel` keeps its `.vercel` link between builds. Schema changes come first: run `ARENA_DATABASE_URL=… make migrate` against production, then deploy.

## Switch on bot protection (Cloudflare Turnstile): about 2 minutes, Benjamin
1. In a Cloudflare account of your choice, go to Turnstile → Add widget.
   - Name: Dialogos.
   - Hostnames: `dialogos-fingerprint.vercel.app`, plus the custom domain when you have one.
   - Mode: "Managed".
2. Copy the site key and the secret key.
3. In the project folder:
   ```
   cd build/vercel
   vercel env add ARENA_TURNSTILE_SITE_KEY production   # paste the site key
   vercel env add ARENA_TURNSTILE_SECRET production     # paste the secret
   vercel deploy --prod --yes --scope omniharmonics-projects
   ```
   Joining, publishing, verifying, writing statements and reporting misreadings then need a passing check. Most people never see it.

## Launch
1. Set the custom domain in Vercel, update `ARENA_PUBLIC_URL`, and add the domain to the Turnstile widget.
2. Remove the gate: `vercel env rm ARENA_SITE_PASSWORD production`, then redeploy.
3. Check from a phone:
   - take it once;
   - publish an anonymous link and paste it into X's composer to see the preview card;
   - delete the link.

## Day to day
- **Admin:** `/admin.html` with `ARENA_ADMIN_TOKEN`. Moderation, misreading reports, profiles and daily counts.
- **Errors:** Vercel → project → Logs, or the Vercel MCP `get_runtime_errors`.
- **Rolling back:** in Vercel, promote the previous deployment. Migrations only add tables, so older deployments keep working.
- **Container alternative:** `infra/arena/Dockerfile` still builds the same app for any container host.
