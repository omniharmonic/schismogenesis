# Lifeworld Atlas: expansion candidates (draft)

**Status:** draft, awaiting Benjamin Life's approval. Research only: nothing has been fetched, ingested or published, and no one has been contacted.
**Prepared:** 2026-11-03, for Benjamin Life (@omniharmonic).
**Data file:** `seed/drafts/AI-FUTURES-SOURCES-v2-DRAFT.json`. It uses the same work format as `seed/AI-FUTURES-SOURCES.json`, plus a `people` list and a few extra fields: `verified_reachable`, `deliverable`, `coauthors` and `note`.

## At a glance

- **Deepening:** 24 new works for the 8 thinly read thinkers (3 each).
- **Widening:** 29 proposed new voices, each with 3 works (87 works).
- **Total:** 111 works. 102 of them were opened (HTTP 200, page title matches). The other 9 are marked `verified_reachable: false`, either because the check was blocked or because the page was not opened.
- **Excerpts:** every `excerpt` is empty, because no page text was read.
- **Seed overlap:** 11 of the proposed voices are already in `SEED-v4.json` as landmarks: zvi-mowshowitz, holly-elmore, bernie-sanders, meredith-whittaker, brian-merchant, ed-zitron, paul-kingsnorth, gary-marcus, dwarkesh-patel, venkatesh-rao and noah-smith. Their ids are reused.
- **Exclusions:** none of the 20 flagged ids and none of the 27 current atlas people are proposed.

## Deepening: what was added

| Thinker | New works | Weak spots |
|---|---|---|
| David Sacks | X thread on the AI Action Plan (Jul 2025); "Goldilocks" X post (Aug 2025); a16z podcast (Nov 2025) | Few long texts exist. The thread is read through a third-party mirror. The x.com post was not opened. |
| E. Glen Weyl | "The Real Dangers of Generative AI" (J. of Democracy, 2024); *Plurality* (open book, 2024); "AI Is an Ideology, Not a Technology" (Wired, 2020, with Jaron Lanier) | The Wired piece is older than the 2023+ preference. His Dec 2025 superintelligence lecture was found only in news coverage. |
| Balaji Srinivasan | a16z podcast on AI, politics and war (2025); "Too Fake to Tell" (2023); "The Purpose of Technology" (2020) | Third pick is weak: general, pre-2023, and the page was not opened. His AI views live mostly on X. |
| Elon Musk | Economist interview transcript (2026); Isaacson interview transcript; Lex Fridman #438 (2024) | Two of these are third-party transcripts (Singju Post). |
| Scott Alexander | "Why Not Slow AI Progress?"; "Most Technologies Aren't Races"; "Introducing AI 2027" | — |
| Jason Crawford | "In defense of slop"; "As we may vibe"; "AI is already 10x-ing academic research" | Content not read. The byline on the third post was not checked. |
| William MacAskill | "Preparing for the Intelligence Explosion"; 80,000 Hours interview (2025); "The importance of AI character" (2026) | Two of the three are co-written. |
| Audrey Tang | Jakarta Post op-ed (2025); Berlin Freedom Conference transcript (2025); Right Livelihood Lecture transcript (2025) | — |

## Widening: proposed voices by camp

### AI safety and EA
- **Zvi Mowshowitz.** The scene's most-read weekly AI digest, written from a "working doomer" point of view.
- **Helen Toner.** A governance researcher who links safety worries to a pro-dynamism framing.
- **Yoshua Bengio.** A top ML scientist arguing for catastrophic-risk caution. He chairs the International AI Safety Report.
- **Geoffrey Hinton.** A Nobel laureate whose takeover warnings moved mainstream opinion.
- **Holly Elmore (PauseAI US).** Grassroots pause activism, and criticism of EA from inside the safety camp.
- **Leopold Aschenbrenner.** "Situational Awareness": AGI by 2027, race with China, lock down the labs. It sits between safety and acceleration.

### e/acc and techno-optimists
- **Noah Smith.** An economist-blogger who makes the optimist case on jobs. Many of his posts are paywalled.
- **Andrej Karpathy and Dwarkesh Patel** are optimist-leaning builders and posters (listed below).
- Garry Tan was considered and left out: no long-form essays were found, only X posts.

### d/acc, pluralist and democratic AI
- **Divya Siddarth (Collective Intelligence Project).** Puts public input into AI models through alignment assemblies.
- **Alondra Nelson.** Rights-based democratic AI governance (also listed under policy).

### Frontier lab leaders
- **Demis Hassabis (Google DeepMind).** Science-first, "cautious optimism".
- **Mustafa Suleyman (Microsoft AI).** Argues against AI that seems conscious, and for "humanist superintelligence".
- **Mark Zuckerberg (Meta).** Made the open-weights case, then moved to "personal superintelligence".
- **Jack Clark (Anthropic).** "Technological optimism and appropriate fear". His essay is one side of the Sacks feud.

### AI-ethics and labour critics
- **Meredith Whittaker (Signal).** Treats AI as a product of surveillance capitalism, and argues that AI agents break privacy.
- **Brian Merchant.** Neo-Luddite labour reporting on AI job losses and the backlash against AI.

### Policy, both parties
- **Dean W. Ball (right).** A former White House adviser who helped write the 2025 AI Action Plan.
- **Samuel Hammond (right).** Argues that AGI will remake the state ("AI and Leviathan").
- **Alondra Nelson (Democratic).** Led the Biden "Blueprint for an AI Bill of Rights".
- **Bernie Sanders (left-populist).** Frames AI as oligarchs against workers. Proposes a robot tax and a 32-hour week.

### Economists
- **Daron Acemoglu.** Expects small macroeconomic gains from AI, and wants AI steered to help workers rather than replace them.
- **Anton Korinek.** Models what economic policy must do if AGI makes human labour obsolete.

### Religious and humanist critics
- **Pope Leo XIV.** Wrote the AI encyclical *Magnifica Humanitas* (2026).
- **Paul Kingsnorth.** An Orthodox Christian critique of "the Machine".

### "Normal technology" and hype sceptics
- **Arvind Narayanan (with Sayash Kapoor).** "AI as Normal Technology".
- **Gary Marcus.** Argues that LLMs can't reason, and that regulation is needed anyway.
- **Yann LeCun.** Says LLMs are a dead end for human-level AI, and that doom talk serves regulatory capture.
- **Ed Zitron.** Argues that AI is a financial bubble.

### Builders and posters central on X / TPOT
- **Andrej Karpathy.** A hands-on builder explaining what models are actually like.
- **Dwarkesh Patel.** The main long-form interviewer for the scene, and an essayist on timelines.
- **Venkatesh Rao.** TPOT's own idiom: AI as a camera, not an engine, and against "hyperanthropomorphism".

## Flags for Benjamin (conflicts of interest and checks)
- **Jack Clark.** Anthropic co-founder. Anthropic makes the model that built this list. This is a direct conflict of interest.
- **Divya Siddarth.** CIP partnered with Anthropic on "Collective Constitutional AI" (2023). Her field is also yours (civic tech / deliberation), so she may be in your network.
- **Anton Korinek.** Reportedly sits on Anthropic's Economic Advisory Council. Not verified.
- **Holly Elmore.** Several recent posts attack Anthropic by name. This is not a conflict, but an outside check would confirm her views are summarised fairly.
- **Paul Kingsnorth.** Mostly paywalled, and based in the UK/Ireland (US-centrality check).
- **Arvind Narayanan.** Most of his work is co-written with Sayash Kapoor. You may want to add Kapoor too.
- **Noah Smith.** His recent AI posts are paywalled.

## Problems and unverified items
- **Not opened (HTTP 403):** these are listed by web search but the automated check was blocked. Sanders's HELP report PDF and a sanders.senate.gov page; the Ford School video of Alondra Nelson; LeCun's OpenReview paper; Whittaker's "Steep Cost of Capture"; Acemoglu's Boston Review forum; Korinek's IMF F&D piece. The IMF URL was written from memory.
- **Not opened for other reasons:** the x.com URL for Sacks's August 2025 post (found through a blog repost and press coverage), and Balaji's "The Purpose of Technology" (taken from the balajis.com archive listing).
- **Dates:** some were written from memory rather than read off the page; each work's `note` says which. Two Singju Post dates are page dates, not air dates.
- **Thin long-form for central X figures:** Sacks, Balaji and Musk say most of what they say on X and podcasts. Their picks are weaker than the rest.
- **Nelson and Sanders:** no strong own-byline essays were found. Their lists lean on a government document or staff report and on an interview or op-ed.
- **Pseudonymous posters left out:** roon and janus/repligate are central in TPOT but pseudonymous. I left them out to respect privacy; it is your call.

## Camps that are still thin after this list
- **Forecasters.** Only Aschenbrenner, plus Kokotajlo already in the atlas. There is no Metaculus or superforecaster voice yet, such as Eli Lifland or Philip Tetlock.
- **e/acc proper.** Beyond Verdon and Andreessen, no X-native accelerationist with long-form writing was found. Garry Tan and similar figures post rather than write.
- **Religious voices beyond Catholic and Orthodox Christian.** No evangelical, Jewish, Muslim or Buddhist voices on AI yet.
- **Right-populist critics.** Hawley and Vance are already in. Still missing are the War Room / Steve Bannon / Joe Allen strand of anti-transhumanism; Joe Allen is in the seed.
- **Organised labour and creators.** Unions (for example Sara Nelson and Shawn Fain, both in the seed) and artists (Karla Ortiz, in the seed) are not yet represented in their own words.
- **AI welfare and consciousness researchers.** Only Suleyman touches it, and from the sceptical side.
- **Non-US and Global South voices.** The list is still very US- and UK-centred.
