# Accounts and the people map (The Great AI Debate) — design, 2026-11-05

Owner: Benjamin Life. Approved in chat 2026-11-05 ("Let's build! Love your other proposals").

## Why
Benjamin won't share the Debate widely until people can (1) come back and change their answers on
any device, (2) put their name and picture on the map if they want, and (3) see at a glance where
the crowd sits against the experts. Today "remembering you" is only localStorage.

## Decisions (Benjamin's, 2026-11-05)
- Sign in four ways: **Bluesky** (real atproto OAuth), **X** (OAuth 2.0, Benjamin creates the X app),
  **email** (magic link plus a 6-digit code, sent through his Resend account), **private key** (a
  long key the browser's password manager saves; no email needed). All four reach one account.
- People on the public map as **individual dots**, but **faces first**: people who signed in with
  Bluesky/X and chose to be shown appear as their profile picture, drawn on top and larger; everyone
  else is a small plain dot behind them, so the map stays beautiful.
- The account is site-wide (antimemes), so future anti-debates add to the same profile; answers are
  stored per season.

## Calls Claude made (check these)
- Email sender is `antimemes <signin@omniharmonic.com>`: Resend's plan is at its 10-domain limit, so
  antimemes.is couldn't be added. Swap `ARENA_MAIL_FROM` once a domain slot is free.
- Sessions are an httpOnly, Secure, SameSite=Lax cookie (`am_session`, 1 year); state-changing
  requests also check the Origin header.
- Anonymous dots appear only once at least 10 people have added answers (the existing MIN_CELL).
  A dot's position comes from the person's three nearest thinkers, never from anything identifying.
- Nothing about a person is public unless they switch on "Show me on the map"; a face needs a
  Bluesky or X sign-in (that's where the picture comes from). Deleting the account deletes its
  logins, sessions, answers, room votes link and published profile.
- Every account sheet also feeds the existing public results (it is joined to the `ai-futures` room
  as a participant, and its votes are updated when answers change), so results stay one source.

## Data (migration 0011_accounts)
- `account(account_id uuid pk, display_name text ≤80, avatar_url text, bio text ≤160,
  show_on_map bool default false, created_at, updated_at)`
- `account_login(kind in ('bsky','x','email','key'), subject text, account_id fk, handle text,
  created_at, pk(kind, subject))` — bsky: DID; x: user id; email: lower-cased address; key: sha256 hex.
- `account_session(token_hash bytea pk, account_id fk, created_at, last_seen_at, expires_at)`
- `auth_flow(state text pk, kind text, data jsonb, created_at)` — OAuth state, PKCE, DPoP key; 15 min.
- `email_token(token_hash bytea pk, email text, code_hash bytea, attempts int, created_at, used_at)`
- `account_sheet(account_id fk, season text, answers jsonb, x real, y real, nearest text,
  participant_id uuid, updated_at, pk(account_id, season))`

## API contract (JSON; cookie auth; all under debate.antimemes.is)
- `GET /api/me` → `{"account": null}` or `{"account": {"display_name", "avatar_url", "bio",
  "show_on_map", "logins": [{"kind","handle"}], "sheet": {"season","answers","updated_at"} | null}}`
- `PATCH /api/me` body `{"display_name"?, "bio"?, "show_on_map"?}` → `{"ok": true}`
- `PUT /api/me/answers` body `{"answers": {anchor: -1|0|1}}` → `{"ok": true, "position": {x,y}|null}`
  (server recomputes position and nearest thinker; also updates the room votes)
- `DELETE /api/me` → deletes everything; clears cookie.
- `POST /api/auth/logout` → clears the session.
- `POST /api/auth/key/new` → `{"key": "am-xxxx-…"}` creates an anonymous account (or adds a key to the
  signed-in one) and signs in. The key is shown once.
- `POST /api/auth/key` body `{"key"}` → signs in.
- `POST /api/auth/email/start` body `{"email"}` → sends link + code; `{"ok": true}` always.
- `POST /api/auth/email/code` body `{"email","code"}` → signs in. `GET /auth/email?t=…` → signs in, 302 `/#signed-in`.
- `GET /auth/bsky/start?handle=…` → 302 to the person's Bluesky authorisation server.
  `GET /auth/bsky/callback` → signs in, 302 `/#signed-in` (or `/#signin=failed`).
- `GET /auth/x/start?next=account` and `/auth/x/callback` → same, for X (existing share-verify flow kept).
- Signing in while already signed in **adds** that login to the current account (link accounts).
- `GET /api/map/people` → `{"min_cell":10,"count":n,"people":[{"x","y","face"?,"name"?,"handle"?,
  "kind"?,"bio"?,"nearest"?}]}` — faces first; anonymous entries carry only x, y. Empty `people`
  below min_cell (count still given). CDN-cached for a minute.

## Screens
- **Account** (`/account.html`, nav item "You"): sign-in choices when signed out; when signed in,
  picture/name/bio, "Show me on the map" switch (with a face when a Bluesky/X login exists), linked
  logins with "add another way in", "Change my answers" (back into the survey with saved answers),
  sign out, delete account.
- **After the story / on results**: a "Save your answers" panel with the four ways in; on sign-in the
  local answers are uploaded. When signed in, answers save automatically as they change.
- **Returning visitor**: `app.js` asks `/api/me`; saved answers win over an empty local copy.
- **Map** (results page and Thinkers page): a three-way switch "Thinkers / People / Both". People are
  drawn in the same coordinates as thinkers: faces (round, small camp-neutral ring) on top, dots
  (3px, muted) beneath; hover card shows name, @handle, bio and nearest thinker for faces.
- **Gap**: results page opens with "Where the crowd and the experts split most" (top statements by
  |public agree share − thinkers agree share|), above the existing sections.

## Not now
Passkeys; email as a public identity; following/notifications; moderation tooling beyond the
existing admin hide.
