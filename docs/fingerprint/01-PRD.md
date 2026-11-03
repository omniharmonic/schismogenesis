# AI Futures Fingerprint: product requirements

Owner: Benjamin Life (@omniharmonic). Drafted by Claude for Benjamin, 2026-11-02.
Status: adopted direction (Benjamin, 2026-11-02: "let's produce a scoped implementation plan… scope it to appeal to the EA / e/acc / d/acc TPOT subcultures… nail the fingerprint… best in class meme map, real polis-style community note infra… not full citizen assembly scale"). Details below are Claude's calls unless marked as his.

Related: `docs/vision/2026-11-02-holistic-vision-draft.md` (the long vision), `02-ARCHITECTURE.md`, `03-IMPLEMENTATION-PLAN.md`, ADR-036.

## 1. In one paragraph

A web app where someone from the AI-and-society conversation on X (EA, AI safety, e/acc, d/acc, the wider "TPOT" scene) answers about 24 short statements about AI and the future, with no names attached. Then they see which of 27 public thinkers they actually agree with, quote by quote, where they sit on a map of worldviews, and where they break from their own side. They can share a card of the result, then join a live room. In the room everyone votes on statements, including ones other participants write. The room shows its own opinion groups the way Polis does, and the statements that win across groups the way Community Notes does.

## 2. Why this, why now

- The people in this scene already sort themselves by labels (e/acc, doomer, d/acc, EA). They argue about where the lines are. A tool that shows where you *actually* sit, using real quotes, feeds an urge they already have.
- Benjamin's goal for Dialogos is meta-consensus: sides able to describe each other in terms the other side would sign. The fingerprint is the front door, and the room is the first small, real instance of that.
- We already have the hard part: a checked structure of 360 ideas held by 27 thinkers, each holding backed by a quote of 280 characters or fewer with a link (the Lifeworld Atlas).

## 3. Who it is for

**Primary:** people active in the AI futures conversation on X and Substack who identify with, or argue against, e/acc, EA or AI safety, d/acc, or the pluralist and progress-studies crowds. They are online, quick to share, sceptical of quizzes, and alert to bias. They will test whether it was rigged.

**Secondary:** journalists, researchers and community organisers in the same conversation, who want to see the room's structure.

**Not now:** the general public, citizen assemblies, other policy topics, minors (age gate: 18+).

## 4. What success looks like

| Measure | Target for the private beta |
|---|---|
| Complete the fingerprint, out of those who start | ≥ 60% |
| Share or copy the result, out of those who finish | ≥ 15% |
| Join the room, out of those who finish | ≥ 30% |
| Votes per room participant | median ≥ 20 |
| Participant-written statements approved | ≥ 1 per 15 participants |
| Bridging statements found (pass the bar with ≥ 2 groups present) | ≥ 3 per room of 100 |
| "Was this fair to you?" rating of the reveal | ≥ 3.5 of 5 on average |
| Reports that a thinker's placement is wrong | each one answered within 7 days |

Anti-goals, which count as failure even if the numbers look good:
- It reads as a personality quiz that tells you which tribe you belong to. Results must show splits and cross-cutting views, not just a label.
- A side can say it was rigged and be right: slanted wording, an unbalanced statement set, or one camp's thinkers quoted better.
- Answers can be tied back to a person without their choice.
- Engagement comes from outrage: the room rewards the most divisive statements.

## 5. The experience, step by step

### 5.1 Landing
- Headline, written by Claude for Benjamin to revise: "Where do you actually sit on AI's future?" Below it: "Answer 24 statements. Names stay hidden until the end. Then see which of 27 thinkers you agree with, in their own words."
- Shows the camps by name (e/acc, AI safety, d/acc, pluralists, critics, progress studies) and faces or initials of the thinkers. It must not suggest which answer is "right".
- 18+ confirmation. One line on privacy: "Your answers stay in your browser unless you choose to join the room."

### 5.2 Answering
- 24 statements in 3 sets of 8: **what AI is**, **what we know and value**, **what to do**. They follow the atlas layers, so the order runs from roots to action.
- Each statement is one card with four buttons: Agree, Disagree, Unsure, Skip. Keyboard shortcuts on desktop (A, D, U, S). Thumb-sized on phones.
- No names or quotes while answering. That is the Quote Mirror rule: the user reacts to the idea, not the person.
- A progress bar. After each set, one teaser line, e.g. "So far you're closer to the Long-term stewards than to the Builders." No names yet.
- Users can go back and change an answer.

### 5.3 The reveal (the fingerprint)
In this order:
1. **Your nearest thinkers.** The top 3, each with agreement on shared statements ("You agree with Vitalik Buterin on 9 of 11"). Also the 3 furthest.
2. **Where you sit.** A 2D map of the 27 thinkers, grouped into the atlas schools, with you placed among the thinkers you agree with most. It's labelled as approximate.
3. **Your signature.** The 2 or 3 statements where you break with your nearest school and side with a different one: "You're with the Builders on most things, but you agree with the AI risk rationalists that capable AI won't care about us by default." This is the cross-cutting line, and the most shareable part.
4. **Your splits with the camps.** For e/acc, AI safety/EA and d/acc, the layers where you agree and split, from roots to action, and the deepest layer where you split. This reuses the atlas fork profile.
5. **Quote mirror.** For each statement you answered, which thinkers' own words agree or disagree, each quote 280 characters or fewer with a link to the source.
6. **Share card.** A downloadable image and a copyable text with your top 3, your school neighbourhood, your signature line and a mini map. It shows no individual answers beyond what the user picks.
7. **Fair to you?** A 1 to 5 rating, plus "Report a placement" next to each thinker, which leads to the dispute form.
8. **Honesty notes.** These are always visible: "Thinkers are read by machine from about 3 public works each. None has reviewed this. Agreement counts only statements where we found a stated position."

### 5.4 The room (Polis-style, with Community Notes bridging)
- The user opts in with one button: "Add my answers to the live room." Only then does anything leave the browser. They get a random participant ID, stored in their browser. A handle is optional and self-declared.
- **Vote:** the 24 anchor statements, plus approved statements from participants, served with the least-voted first. Agree, Disagree or Pass.
- **Write:** one statement at a time, 140 characters or fewer. A writing tip reads: "Write something that people who disagree with you might also agree with." Statements wait for moderation before anyone sees them.
- **Room report**, which updates as votes arrive:
  - **Opinion groups**, Polis style: participants clustered on their votes, with a 2D view and the statements that set each group apart. Shown only once at least 10 participants have each cast at least 7 votes.
  - **Bridges**, Community Notes style: statements rated well by people on both sides of the room's main split. These need at least 5 raters and a high base score with low dependence on side. This is the headline of the report.
  - **Common ground**, Polis group-informed consensus: statements every group leans to agree with.
  - **Live splits:** statements that divide the room most.
  - **How the room maps to the thinkers:** each opinion group's nearest thinkers, based on its votes on the anchor statements.
  - **You:** your group, and which bridges you voted for.
- The report never names individual participants.

### 5.5 The map
- The full 3D Lifeworld Atlas is available at `/atlas`, and the user's position is passed in from their own browser. The 2D map in the reveal is the light version for phones.

### 5.6 Moderation and disputes
- Benjamin, or someone he names, approves or rejects participant statements in an admin view. It's protected by a token held only by the operator. Rejection reasons: duplicate, not a statement, abuse, off-topic, identifies a private person.
- Placement disputes from anyone, including the thinkers themselves, go to a queue the operator answers.

## 6. Requirements

### Must have (beta)
- R1. Statement set: 24 anchors chosen by code from the atlas ideas where thinkers stand on both sides. It's balanced across the three layer sets and across the camps (rule in architecture §4). The selection is recorded and reproducible.
- R2. Neutral wording: each anchor's text is the atlas's neutral proposition. Any edit for readability is reviewed blind by two readers for slant (eval E-F1).
- R3. All scoring for the fingerprint runs in the browser. Without opt-in, the server receives no answers. Since the launch round it also receives anonymous daily counts (such as "started" or "shared"), with no IDs and no cookies (04-LAUNCH.md section 3).
- R4. Agreement with a thinker counts only statements where that thinker has a stated (not inferred) position. Results show the count, and a thinker needs at least 3 shared statements to be ranked.
- R5. The reveal includes splits and at least one cross-cutting line whenever the data supports one. A user is never shown as a pure member of one camp without showing where they depart from it.
- R6. Quotes are 280 characters or fewer, each with a link. No full texts.
- R7. Room voting: one live vote per participant per statement, which they can change. Analysis covers the latest votes only.
- R8. Room analysis: Polis PCA and k-means groups with representative statements; Community Notes matrix factorisation for bridges; group-informed consensus; divisiveness. Each step has a minimum-data rule, and below it the report says "not enough votes yet" instead of guessing.
- R9. Participant statements are moderated before display. 140-character limit. They can't contain @handles, links or emails.
- R10. Admin view for moderation and disputes, behind a token.
- R11. Share card as PNG and text, generated in the browser.
- R12. Accessible: keyboard operable, readable contrast in light and dark, usable at 360px width.
- R13. Only the 27 atlas thinkers appear. None of the 20 flagged landmarks appear anywhere.
- R14. A synthetic demo mode for local testing fills a room with clearly labelled fake voters, so the report can be seen working. It can never run against a production database.

### Should have (soon after)
- R15. 3D atlas overlay of "you".
- R16. "Would they sign this?" notes: participants rate the app's one-line description of each school, Community Notes style. Descriptions that people *inside* the school rate as fair are marked as signed by that school. This is the first real meta-consensus signal.
- R17. Optional X sign-in, so handles are real and a person can't easily vote twice.
- R18. Statement suggestions from a local model ("a bridge between group A and B might be…"). These are agent-written and labelled. Agents never ratify.
- R19. Weekly round cadence with a published Record of Understanding.

### Won't have now
- Citizen-assembly-scale deliberation, other topics, payments, public individual profiles, AI agents voting, any paid API.

## 7. Safety and fairness tests (before Benjamin shares a link)
- S1. Balance: across 1,000 random answer sheets, each school is the top match about as often as its share of thinkers would predict (no school above 2× or below 0.5× its fair share). Synthetic test.
- S2. A real-world self-test: Benjamin and at least two people from different camps take it and say whether their result was fair.
- S3. No answer leaves the browser before opt-in (network check in the browser).
- S4. With all answers "Unsure", the reveal says "not enough answers" rather than placing anyone.
- S5. Participant text with a handle, link or email is refused.
- S6. The demo seed refuses to run when the database is not a local or test database.

## 8. Open points for Benjamin
1. The name. Working title: "AI Futures Fingerprint", inside Dialogos.
2. Whether the reveal shows thinkers' photos (rights) or initials (Claude's default: initials).
3. Who moderates participant statements during the beta.
4. Hosting for the beta (a public URL is outward-facing, so it needs his yes). Locally it runs with one command.
5. Whether to add the 3 to 5 TPOT-native voices the atlas lacks (for example a d/acc builder or an EA org voice) before launch. It would need new extraction.
