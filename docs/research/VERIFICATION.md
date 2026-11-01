# Dialogos Arena: Verification of SYNTHESIS.md

**Author of record:** Benjamin Life (@omniharmonic). **Checked:** 2026-10-30 by an independent checker (not the author of the synthesis).

## A. Fidelity to briefs (§1 findings and figures)

All ten §1 findings trace to the cited briefs. Spot-checked figures and their sources were all consistent:

| Figure | Brief | Result |
|---|---|---|
| Silhouette −0.009 | A2 | Match |
| 4/3/6/1% overlap; 60-pair cap | A1 | Match |
| "I love X" / "I hate X" (Ghafouri) | B4 | Match |
| 212.9M ratings; 71.5% → 11.7% | B2, B4 | Match |
| Habermas 6–9 pp; 56/44 | B2 | Match |
| GG22 27 donors / 23 clustered / $0 | B3 | Match |
| CCN Climate 60–70% | B3 | Match |
| 32 of 38 rounds, ~$4M of $4.5M; "~89%" | B3 | Match |
| −0.042 SD (bridging + downrank toxic) | B2, B4 | Match |
| 10.7% with <10 ratings | B5 | Match |
| Deep Funding jurors 63–89% | B3 | Match |
| 10–20% friction loss | B3 | Match |
| Bluesky ~10.4M MAU; $15k LD / 1M posts; 3M reads cap | B5 | Match |
| Jev ~$0.05/user, ~$400 per 10^7 posts × 20 Q; $10k 2-hop ego; $1 owned | B4, B5 | Match |
| Atlas 58 ontologies, two axes; Lightfoot ~30% | A5 | Match |
| QUALITY gates 0.97 / 0.92 / etc.; 4/4 Ball × Kokotajlo; 0.93 dedup | A1, A3 | Match |

No fidelity edits were needed.

## B. External fact checks

| # | Claim | Source reached | Result | Edit |
|---|---|---|---|---|
| 1 | X Developer Policy forbids deriving/inferring political affiliation or beliefs; aggregate carve-out | docs.x.com/developer-terms/restricted-use-cases (primary) | **Confirmed.** "Never derive or infer, or store derived or inferred…" includes "Political affiliation or beliefs"; aggregate analysis that stores no personal data is permitted. | None |
| 2 | Jev (TypeSafe AI) launch, pricing, signup pause | aiweekly.co, gradually.ai, explainx.ai, aiprofitboardroom (secondary; no TypeSafe primary reached) | Launch on 2026-09-15 and the price of $0.042/M input tokens are **confirmed** (secondary sources only). "Signups paused" is **UNVERIFIED and contested**. One source says the waitlist was removed on 2026-09-21. Another (opentweet.io) says the direct API is still waitlisted, with Vercel, OpenRouter and Cloudflare gateways open. B4 reports a pause on 2026-09-22. | Changed the definite "signups paused" wording to "access status conflicting (UNVERIFIED)" in 3 places in SYNTHESIS.md (§5.1 S1 row, §10 reuse row, §12 Q7) and in the Jev bibliography note in both files |
| 3 | Andreou & Sirivianos 2026, second axis | arXiv 2609.21496 abstract page (primary) | **Confirmed**: second axis largely independent of left/right, interpreted (by authors) as institutional trust; 212,900,053 ratings; 71.5% → 11.7%; third axis lowers RMSE only 0.0008. | None |
| 4 | COCM: Miller, Kanich & Weyl, arXiv 2509.18343; 32 of 38 rounds | arxiv.org/html/2509.18343v1 (primary); arxiv.org/abs page blocked by permission timeout | **Confirmed** 38 rounds / ~$4.5M, 32 used CO-QF or hybrid / ~$4M; EAAMO '25. Author order is Miller, **Weyl & Kanich**. Abstract calls 89% an "adoption rate" (32/38 = 84%, so the synthesis's funds-share reading is plausible but not stated by the paper). Round-manager preference confirmed ("all interviewees felt CO-QF was an improvement"). | Fixed author order (both files); added a clause to §7.2 noting the abstract's "adoption rate" wording |
| 5 | Habermas Machine (Science 2024) preference result | Science paper PDF (rivista.ai mirror) and MIT Technology Review | **Confirmed** 56% vs 44%. Agreement gains were 8.6 / 9.3 / 5.9 pp across cohorts ("about eight percentage points"), so "6–9 pp" is right; they came from the whole AI-mediated deliberation, not the critique step alone. | Clarified §6.4 wording |
| 6 | Limberg & Barnes (2018); Lightfoot "The Liminal Web" | Medium original; Second Renaissance wiki; syscoi.com repost | **Confirmed**: Medium, 2018-09-14, 33 tribes, 9 dimensions (the Medium byline itself reads "Limberger"). Lightfoot 2021-11-18, modified 2023-04-14; "at least thirty percent" heuristic confirmed. | None |
| 7 | CJEU C-252/21 on special-category data | FRA case page; DLA Piper (secondary) | **Confirmed**: linking off-platform activity to an account is Art. 9 processing where it reveals a special category; mere visits are not "manifestly made public"; clicks/entries qualify only with prior explicit choice to make data public. Judgment 2023-07-04. The page does not name political opinion specifically (it covers all Art. 9(1) categories). C-446/21 not re-checked (**UNVERIFIED** in this pass). | None |
| 8 | Milli et al. NeurIPS 2024 bridging result | neurips.cc/virtual/2024/99058 (primary) | **Confirmed with a correction**: it is a **Pluralistic Alignment Workshop** poster, not a main-track paper; 70M Facebook URLs; naive bridging pushes down controversial topics. | Added "Pluralistic Alignment Workshop" in §7.3 and in the bibliography (both files) |

## C. Remaining UNVERIFIED after this pass

- Jev's current access status: secondary sources conflict, and no TypeSafe primary source was reached.
- arxiv.org/abs/2509.18343 (permission timed out). The HTML version was used instead.
- CJEU C-446/21 detail.
- All items already marked UNVERIFIED in the synthesis were not re-checked unless listed above.

## D. B6 integration (2026-10-30)

Brief B6 (AI agents and ethics) was integrated into SYNTHESIS.md as a new §8 "AGENTS: an ethical agent layer". Later sections were renumbered: Data and ethics is now §9, Validation §10, Reuse §11, Risks §12, Open questions §13, Spec checklist §14 and Bibliography §15. The section references in the table in B above use the old numbers. Other changes: finding 11 in §1; agent red lines A1–A15 in §9.2; three validation rows in §10; one reuse row in §11; risks R26–R31 in §12; questions Q16–Q22 in §13; spec 16 in §14; and bibliography section I (both files).

**B6 was not independently fact-checked beyond its own UNVERIFIED flags**, which are carried forward. The exceptions are the three spot checks below.

| # | Claim (as in B6 and §8) | Source reached | Result | Edit |
|---|---|---|---|---|
| 1 | Zurich r/changemyview: undisclosed LLM accounts; ~1,783 comments; 137 deltas; 3–6× human rate in draft; personas including a trauma counselor and an assault survivor; Reddit CLO "deeply wrong on both a moral and legal level" and formal legal demands; ethics committee had advised informing participants, issued a formal warning and promised stricter review; researchers chose not to publish | The Decoder; NBC News; The Register; eWeek; Wikipedia (secondary; no primary paper reached) | **Confirmed.** The Decoder gives 1,783 comments, 137 deltas, and rates of 17–18% vs a ~3% human baseline. NBC confirms the CLO quote, the legal demands, the ethics committee's advice and stricter review, and the decision not to publish. The Register and NBC confirm the personas. Note: NBC says "more than 1,000 comments"; the university initially said publication was proportionate, and the researchers later withdrew it. | None |
| 2 | Costello, Pennycook & Rand, *Science* 2024 (DebunkBot): ~20% reduction, ~8.4-minute dialogue, ~1 in 4 no longer endorsed, lasted ≥2 months, N>2,000 | Cornell Chronicle (2024-09-12; secondary press release) | **Confirmed** on every figure. | None |
| 3 | Eady et al., *Nature Communications* 2023: 1% of users received 70% of exposures, mostly strong Republicans; no measurable change in attitudes, polarization or vote | Trinity College Dublin release (secondary; the paper was published 2023-01-09) | **Confirmed.** Strong Republicans saw roughly nine times as many posts as Democrats or Independents. | None |

No SYNTHESIS.md edits were needed from these checks. Every other figure from B6 (Breakout ratings, Salvi 81.2%, Hackenburg 51% and N=76,977, Argyle ~4 pp, Meta 7,704 accounts, DOJ 968 accounts, and others) is carried forward **unchecked**.

## E. B7 and B8 integration (2026-10-30)

Briefs B7 (Girard, hyperstition and the mimetic state machine) and B8 (open agents, registries, token incentives and strategy markets) were integrated into SYNTHESIS.md:
- **Header** now cites B1–B8.
- **§1** finding 11 revised to the Open Agent Charter (open presence, invited contact, directional-shift audit); new findings 12 (integration game / state machine) and 13 (the Girardian design principle).
- **§2** four new reframe rows.
- **§8** revised: the B6 pull-only framework replaced by the Open Agent Charter O1–O15, with a binding/bond/slashing table; B6's registry, provenance flags, agent-free re-fit, ratified-outcome ranking and detection role retained.
- **New §9 "THE INTEGRATION GAME: a mimetic state machine"** (§9.1–9.10). Later sections renumbered: Data and ethics is now §10, Validation §11, Reuse §12, Risks §13, Open questions §14, Spec checklist §15, Bibliography §16. Internal cross-references were updated. Section numbers cited in tables B and D above use the older numbering.
- **§10.2** adds a reconciliation table: A3 is superseded for presence (retained for contact), A4 is narrowed to allow openly labeled multi-framing, and all other A-lines are retained.
- **§11** adds 11 validation rows; **§12** four reuse rows and an expanded build-new list; **§13** risks R32–R43 (R20 and R26–R31 updated); **§14** Q16 revised and Q23–Q30 added (Q23: confirm Jake Hartnell's position wording with him); **§15** spec 16 renamed Open Agent Charter Spec and spec 17 Integration Game / State Machine Spec added, plus three pre-spec actions; **§16** bibliography sections J (B7) and K (B8), in both SYNTHESIS.md and BIBLIOGRAPHY.md.

B7 and B8 were not independently fact-checked beyond their own UNVERIFIED flags, which are carried forward. The exceptions are the three spot checks below.

| # | Claim (as in B7/B8) | Source reached | Result | Edit |
|---|---|---|---|---|
| 1 | X automation rules: automated replies or mentions require prior user intent; a follow is not enough; keyword-triggered replies banned; unsolicited mass mentions are abuse; one reply per interaction; opt-outs honored; no automated likes; no duplicative accounts [B8] | help.x.com/en/rules-and-policies/x-automation (primary) | **Confirmed** on every element. The rule's wording is that users must "have requested or have clearly indicated an intent on X to be contacted by you" (examples: replying to your post, DMing you); following "is not a sufficient indication of user intent." | Quoted the intent wording in §8.2; no substantive change |
| 2 | ERC-8004 "Trustless Agents" is a Draft ERC, created 2025-08-13 by De Rossi, Crapis, Ellis and Reppel; three registries (identity, reputation, validation); states that Sybil attacks are possible [B8] | eips.ethereum.org/EIPS/eip-8004 (primary) | **Confirmed**: Status Draft, Standards Track ERC, created 2025-08-13, same four authors, same three registries; Security Considerations: "Sybil attacks are possible, inflating the reputation of fake agents." Mainnet registration counts (100k+) remain **UNVERIFIED**. | None |
| 3 | Broockman, Kalla & Westwood (*AJPS* 2022) and Voelkel et al. (*Science* 2024) megastudy [B7] | Yale ISPS abstract page (primary abstract); Stanford Sociology summary, HKS abstract page and Kellogg summary (author-institution pages) | **Broockman: confirmed with one narrowing.** Five experiments, N = 12,341; affective polarization substantially reduced; no evidence of effects on endorsing norm violations or accountability; effects only on general interpersonal attitudes. The abstract lists opposition to compromise among the outcomes it examined but reports no separate compromise finding, so B7's "support for compromise" is folded into the general null. **Voelkel: confirmed with a correction.** 32,059 participants; 25 interventions; 23 of 25 significantly reduced partisan animosity; "several" reduced support for undemocratic practices; effects sustained over two-week follow-ups. Correction: the **most effective treatments differed by outcome**. For animosity they were relatable out-partisans and shared identities. For anti-democratic attitudes they were correcting misperceptions of rival partisans' views and highlighting the threat of democratic collapse. B7's list ("shared identity, empathy and correcting misperceptions … among the most effective") blurred the two. The abstract does not say whether the same treatments moved both outcomes. | §9.10 states the outcome-specific finding and drops "support for compromise"; §1 finding 13 cites both papers without overclaiming |

**Remaining UNVERIFIED from B7/B8** (carried forward, not re-checked): ERC-8004 mainnet date and counts; universal availability of X's automated-account label; Bluesky community agent labels and lexicons; Farcaster's post-acquisition agent policy; Olas slashing; legal status of prize tournaments; detectability of slow persuasion drift; ITT discrimination for distant clusters; MacKenzie typology; Callon; Rossetti & Cazabet taxonomy; Flache et al. abstract; Esteban–Ray index; Dupuy's fixed-point formalism; the Irish referendum percentage; the Paris hair-dryer detail; the speaker identity of "Michael"; the author list of the 26-country meta-perception replication; Jake Hartnell's preferred characterization (to confirm with him, Q23). Every other B7/B8 figure (Polymarket ~25% wash trading, RetroPGF 3 967/1,594, Bittensor correlations, Virtuals counts, Metaculus vs Manifold Brier, IEM 74% of 964, Mastroianni 902/746, and others) is carried forward **unchecked**.
