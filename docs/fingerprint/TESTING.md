# Testing the AI Futures Fingerprint

For Benjamin. Everything runs on your machine. Nothing is public.

## Start it

```
ARENA_ADMIN_TOKEN=pick-a-long-secret-of-24-characters make app
```

Then open http://localhost:8800. Stop it with Ctrl+C. The admin page is http://localhost:8800/admin.html; use the same token there.

## What to try (about 20 minutes)

1. **The full run, on your phone if you can** (or a narrow browser window). Answer as yourself.
   - When you finish, the story plays: your print, your neighbourhood, your top match in their own words, the plot twist, your furthest, the camps, your rarest take, the map, and a share slide. Tap the right side to go on and the left to go back.
   - On any slide, try "Save this slide". On a phone it opens the share sheet with the image.
2. **Get a share link.**
   - Choose Anonymous and "Create my link". Open "View my page".
   - Copy the link and paste it into a new post on X or Bluesky, without posting. Locally the preview card won't load, because those sites can't reach your laptop. It will once the site is live.
   - Go back and try "Make a new link" and "Delete this link".
3. **Bluesky verification (real).** In the share sheet choose "My Bluesky account", enter your handle, post the code, and press "I've posted it". Then publish with "list me" ticked and open http://localhost:8800/people. Afterwards, delete the page from the share sheet and delete your Bluesky post.
4. **The room.** Open http://localhost:8800/?room=demo and join from the end of your result.
   - The report now shows:
     - "You in the room": your group, how rare your votes are, and your rarest take;
     - a picture of the room with the 27 thinkers placed inside it;
     - how stable the groups are;
     - bridges that must clear an uncertainty check.
   - The demo room's voters are fake, and a banner says so.
5. **Try to break it.**
   - Answer everything "Unsure". It should refuse to place you.
   - Write a room statement with an @handle or a link. It should be refused with a reason.

## What to look for and tell me
- Does the story make you want to share it? Which slide would you post?
- Any statement whose wording leans toward one camp. This matters most before launch.
- Any thinker who seems misread.
- Whether the name "AI Futures Fingerprint" works.

## Known limits
- Six thinkers can't be compared yet, because there are too few of their stated positions on these statements: Sacks, Weyl, Balaji, Musk, Scott Alexander, and sometimes Crawford.
- X sign-in is built but switched off until there's an X developer app (see `docs/runbooks/fingerprint-deploy.md`).
- Room identity is a random key in your browser, so clearing it lets someone vote again.
