# Testing the AI Futures Fingerprint

For Benjamin. Everything runs on your machine. Nothing is public.

## Start it

```
make app
```

Then open http://localhost:8800. Stop it with Ctrl+C.

- To moderate statements, start it with a token: `ARENA_ADMIN_TOKEN=pick-something make app`, then open http://localhost:8800/admin.html and paste the same token.
- The demo room already holds 120 labelled synthetic voters. To recreate it on a fresh database, run `make demo-room`.

## What to try (about 15 minutes)

1. **Take it for real** at http://localhost:8800. Answer as yourself.
   - Afterwards ask: did "Closest to the …" feel fair? Was the "Where you break from your neighbours" section the interesting part? Would you share the card?
2. **Try to break it.**
   - Answer everything "Unsure". You should get "Not enough to place you yet".
   - Answer only five statements, then press "See result now". You should get the same.
3. **Read the quote mirror.** Open a few statements and check the quotes against their links. If something is misread, use "Report a misreading". Your report lands in the admin page.
4. **Join a room.**
   - The demo room is at http://localhost:8800/?room=demo. Take the fingerprint there and press "Add my answers to the live room". Most voters there are fake (a banner says so), so the report is full: groups, bridges, common ground and splits.
   - The real room is plain http://localhost:8800. It will say "Groups appear after 10 people…" until real people join. That is correct behaviour.
5. **Write a statement** in the room.
   - Try one with an @handle or a link; it should be refused with a reason.
   - In the real room, a good one waits for moderation. Approve it from the admin page.
6. **Check privacy yourself (optional).** In your browser's developer tools, open the Network tab. Until you press "Add my answers to the live room", the page only loads its own files and fonts.

## What to look for and tell me
- Any statement whose wording feels slanted toward one camp. This matters most; a blind slant review is the next step before anyone else sees it.
- Any thinker who seems misplaced on a statement.
- Whether 24 statements feels too long or too short.
- Whether the name "AI Futures Fingerprint" works.

## Known limits in this build
- Six thinkers can't be compared yet, because the atlas has too few of their stated positions on these statements: Sacks, Weyl, Balaji, Musk, Scott Alexander, and (depending on answers) Crawford. The reveal names them. Reading more of their work fixes this.
- Room identity is a random key in your browser. Clearing it lets someone vote again. That's fine for a private test and not for a public launch.
- The demo and real rooms live in the dev database on Neon (free tier). The demo room's synthetic voters are flagged and never counted outside the demo room.
