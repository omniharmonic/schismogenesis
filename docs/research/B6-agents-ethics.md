# B6 — AI Agents in the Discourse Arena: the Adversarial Landscape and the Case for an Ethical Agent Framework

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Largely unaffected.** The agent framework (as revised by B8 into the Open Agent Charter) stands.
> - **Small additions:** agents may draft cross-cluster notes (labeled) but never rate or ratify them (O14; SYNTHESIS §7.5); "ratified outcomes" now include fidelity-ratified notes and lineage credit R5 (SYNTHESIS §10.6). Note that this brief's "synthesis §8/§9/§11" references point to an earlier numbering; agents are now SYNTHESIS §9.

Wave 1 research brief for the Dialogos Arena. **Author of record:** Benjamin Life (@omniharmonic). Researched 2026-10-30.

**Scope note.** This is a research and ethics brief, not an operations manual. Adversarial operations appear here only as documented findings. The brief contains no tactics, persona-building methods or detection-evasion techniques.

---

## Summary

The proposal asks whether the Arena could run, or register, AI agents that act on social platforms (posting, replying, tagging people, reframing messages for each tribe) to connect memetic clusters, with their effect measured on the map and the agents ranked by impact.

**What the evidence shows:**
- **State and commercial AI influence operations are real but mostly ineffective.** OpenAI, Meta, SIO/Graphika and Microsoft repeatedly find little authentic engagement: Breakout Scale ≤2 in nearly every case. The best individual-level study of Russia's 2016 Twitter campaign found no measurable effect on attitudes or votes.
- **Honest, disclosed AI dialogue persuades measurably.** DebunkBot cut conspiracy belief by ~20% for at least two months. The effect held when people knew they were talking to an AI.
- **Optimizing for persuasion degrades accuracy.** The largest study (N≈77k, *Science* 2025) found the most persuasive models were the least accurate.

**The core ethical finding.** A covert or "subtle" prosocial bot cannot be told apart from a state influence operation by any test platforms, regulators or ethicists use. All of those tests look at **means** (hidden identity, coordination, unconsented targeting), not ends. Covert operation would also contaminate the very map the Arena measures. The Zurich r/changemyview case shows the legitimacy cost.

**Recommendation.** Yes to agents, on four conditions:
- **Disclosed.** No agent ever hides that it is an AI or who runs it.
- **Invoked.** A human calls the agent in; it never approaches people unprompted.
- **Consent-bound.** Agents act only for and with people who opted in.
- **Rewarded by ratified outcomes.** Agents are ranked by results the parties confirm, never by raw landscape shift.

No to covert, unsolicited or tribe-targeted agents on open platforms.

---

## Findings

### 1. The adversarial landscape: what is documented, what is alleged, what it achieved

"Fifth-generation warfare" is a contested popular term, not an analytic category, and this brief does not use it as one. In the rows below, "attributed" means a platform, government or court document names the source. "Reported" means investigative journalism with named sources that the state has not confirmed. Each row gives the reported actor, the evidence, its attribution status and its documented effect.

**Russia**
- **Doppelganger.** Cloned news sites, paid ads (some made with AI tools), and fake profiles posing as US and other citizens.
  - *Attribution:* DOJ (Sept 2024) seized 32 domains. Its affidavit says the operation was run by Social Design Agency, Structura and ANO Dialog under the direction of the Russian Presidential Administration (Kiriyenko). Treasury designated 10 people and 2 entities. OpenAI (May 2024) found Doppelganger using its models for multilingual comments.
  - *Effect:* OpenAI rated it ≤ Breakout Category 2: no breakout into authentic communities.
- **Meliorator bot farm.** An "AI-enhanced" persona generator. DOJ seized 968 X accounts and 2 domains (warrants dated June 2024).
  - *Attribution:* Court documents say the project was started at the request of RT's deputy editor-in-chief and later moved into an FSB-created organization. A joint US/Netherlands/Canada advisory accompanied the seizure.
  - *Effect:* No public reach measure.
- **Bad Grammar** (Telegram), found by OpenAI in May 2024.
  - *Attribution:* Russia, per OpenAI.
  - *Effect:* ≤ Category 2.
- **Pravda network.** More than 3.7M articles across 110+ countries, documented by DFRLab and Check First. It was cited by Wikipedia and by AI chatbots ("LLM grooming").
  - *Attribution:* Russian, per DFRLab.
  - *Effect:* The impact is indirect: contamination of reference sources and model training data, not reach.
- **IRA, 2016.** Eady et al. (*Nature Comms* 2023): 1% of users received 70% of exposures, mostly strong Republicans.
  - *Attribution:* Established.
  - *Effect:* "No measurable" change in attitudes, polarization or vote.

**China**
- **Spamouflage / Dragonbridge.** Meta (Aug 2023) removed 7,704 Facebook accounts and 954 Pages, calling it the largest known cross-platform operation (50+ platforms).
  - *Attribution:* Meta found links to people "associated with Chinese law enforcement".
  - *Effect:* Low reach. Graphika's *The Americans* (Sept 2024) found US-voter personas, some AI-generated. Most failed to gain traction; one TikTok video reached ~1.5M views.
- **PRC-linked operation targeting US AI-policy debates** (OpenAI, June 2026).
  - *Attribution:* OpenAI says it "likely originated in China"; prompt terminology was consistent with China's public security system.
  - *Effect:* Breakout Category 1.

**Iran**
- **IUVM** (OpenAI, May 2024) and **Storm-2035** (OpenAI, Aug 2024; Microsoft naming).
  - *Attribution:* Iran, per OpenAI and Microsoft.
  - *Effect:* Low end of Category 2. No meaningful engagement.

**Israel**
- **STOIC / "Zero Zeno."** Fake accounts on X, Facebook and Instagram, plus news-style sites. They engaged posts by US lawmakers, particularly Black Democrats.
  - *Attribution:* OpenAI and Meta attributed the activity to STOIC, a Tel Aviv political-marketing firm; Meta banned STOIC. The NYT reported that Israel's Diaspora Affairs Ministry commissioned and funded the campaign (~$2M), citing ministry insiders. **The ministry denied involvement.** Status: *firm attributed; state funding reported, not confirmed*.
  - *Effect:* Meta said the campaign had no widespread impact. Its ~40k followers were likely partly bots.

**United States**
- **Pro-Western network, 2017–2022.** SIO and Graphika's *Unheard Voice* (2022) studied the network after Twitter and Meta removed it.
  - *Attribution:* SIO said it "likely originated in the United States". Meta's Q3 2022 report found links to "individuals associated with the US military". The Intercept (Dec 2022) showed CENTCOM asked Twitter in 2017 to whitelist 52 accounts it said would be attributed to the US government. Some later dropped that disclosure. Status: *attributed to US-military-associated individuals by Meta; CENTCOM linkage reported*.
  - *Effect:* Most posts got a handful of likes. Only 19% of assets had more than 1,000 followers. Meta called engagement from authentic communities "little to no".
- **Pentagon anti-Sinovac campaign in the Philippines** (Reuters, June 2024). At least 300 X accounts, 2020 to mid-2021.
  - *Attribution:* A senior DoD official acknowledged secret propaganda against China's vaccine; X removed the accounts as a coordinated bot campaign. Status: *reported, partly acknowledged*.
  - *Effect:* No reach measure published. The harm was to public-health trust.

**Commercial**
- **"Influence-as-a-service"** (Anthropic, April 2025). More than 100 persona accounts on X and Facebook, with Claude deciding whether each account should like, share, comment or ignore. The campaign aimed at long-term relationship-building, not virality.
  - *Attribution:* Clients were in several countries. The narratives were consistent with state campaigns, but that attribution was not confirmed.
  - *Effect:* No viral content.

**Microsoft MTAC (April 2024)** draws these lessons:
- AI audio is more impactful than video.
- AI-*enhanced* content beats fully generated content.
- Impersonating lesser-known people works better than impersonating leaders.
- High-production deepfakes of leaders have had limited effect.

**What it all adds up to:**
1. **Measured reach is consistently low.** Across about a dozen documented AI-assisted operations from 2022 to 2026, almost none broke out of their own inauthentic networks. AI mainly raised productivity: volume, translation, fewer language errors. It did not raise persuasive success (OpenAI 2024–2026).
2. **"Low reach" is not "no harm."** Yang (ICML 2026 workshop) argues that the Breakout Scale under-counts operations built on relationship-building and one-to-one AI interaction, not virality. Pravda-style operations target the reference layer (Wikipedia, LLMs), not people directly. Effects on *trust* and on the general belief that "everyone is a bot" are not captured by exposure studies. Eady et al. say so themselves.
3. **Implication for the Arena's premise.** "Fight their bots with our bots" overstates the adversary's documented effect. The documented harm is mostly to the **information commons** (trust, provenance, reference sources), not to individual votes. A counterpart that adds more automated actors to the commons, however well-meant, adds to that harm.

### 2. AI persuasion evidence

- **Salvi, Horta Ribeiro, Gallotti & West** (*Nature Human Behaviour* 2025). N=900, 600 debates.
  - Personalized GPT-4 had 81.2% higher odds of increasing agreement than humans. It won 64.4% of the non-tied pairs.
  - The personal data was only six demographic items from a survey.
  - Unpersonalized GPT-4 was about equal to humans. Humans given the same data gained nothing.
  - The effect vanished for strongly held topics.
- **Costello, Pennycook & Rand, "DebunkBot"** (*Science* 2024). N>2,000.
  - Belief in the participant's own chosen conspiracy fell ~20% after an average 8.4-minute dialogue. About a quarter of participants no longer endorsed it.
  - The effect persisted for two months and was weaker where the belief was identity-central.
  - **Follow-up:** Boissin, Costello et al. (*PNAS Nexus* 2025, N=955) found similar reductions whether participants were told they were talking to an AI or to an "expert". The content did the work, not the messenger's identity.
- **Hackenburg & Margetts** (*PNAS* 2024). LLM microtargeting was **not** significantly more persuasive than generic LLM messages.
- **Hackenburg et al., "Levers of political persuasion"** (*Science*, Dec 2025). N=76,977, 19 models, 707 issues, ~500k claims fact-checked.
  - Post-training raised persuasiveness by up to 51%; prompting by up to 27%.
  - Information density explained about half the explainable variance.
  - **The more persuasive a model, the less accurate its claims.**
  - Conversation beat static messages.
- **Zurich r/changemyview experiment** (Nov 2024 – Mar 2025, disclosed April 2025).
  - Undisclosed LLM accounts posted ~1,700–1,783 comments and earned 137 deltas. A draft reported 3–6× the human persuasion rate.
  - Some accounts claimed to be trauma counselors, sexual-assault survivors or members of ethnic minorities. A "personalized" arm inferred commenters' age, gender and politics from their post histories.
  - Moderators called it unauthorized psychological manipulation.
  - Reddit's chief legal officer called it "deeply wrong on both a moral and legal level," announced formal legal demands, and the accounts were banned.
  - The university's ethics committee had advised informing participants and following platform rules. Afterwards it issued only a formal warning. The researchers withdrew publication, and UZH promised stricter review, including coordination with communities in advance.
  - Reports that the prompts falsely told the model users had consented are **UNVERIFIED** here.

**Ethical lessons of the Zurich case, for the Arena specifically:**
1. **"Low risk" was the committee's judgment, not the community's.** Legitimacy is conferred by the people affected, not by an institutional sign-off.
2. **Invented lived experience is the sharpest harm.** Fabricated identities and trauma testimony corrupt exactly the "being changed by the encounter" that dialogos depends on.
3. **Personalizing from post history is the Arena's SEE layer pointed at non-consenting people.** It breaches red lines 1–2.
4. **The finding is unusable.** Contaminated consent destroyed the knowledge value, so the harm bought nothing.
5. **Communities read covert research as an attack**, whatever the intent. CMV is about the most bridging-minded space on Reddit, the Arena's natural ally, and it was the one that felt violated.
6. **Disclosure was not needed for the science.** Boissin et al. show source identity barely moderates effect, so the deception was gratuitous.

### 3. Prosocial and bridging bot precedents (disclosed vs covert)

Each precedent below is given with its disclosure and consent status, what it found, and what the Arena takes from it.

- **Munger, "Tweetment Effects"** (*Political Behavior* 2017).
  - *Disclosure and consent:* Undisclosed researcher-controlled accounts sanctioned users who had posted racist slurs. Consent details were not verified here.
  - *Result:* An in-group, high-follower account reduced slur use.
  - *For the Arena:* Norm signals from in-group peers work. But the design relied on covert identity, which the Arena cannot copy.
- **Bail et al., Polarization Lab** (*PNAS* 2018).
  - *Disclosure and consent:* Disclosed and consented. Participants were paid $11 to follow an opposing-elite retweet bot for a month. N≈1,660.
  - *Result:* Republicans became significantly more conservative; Democrats did not change significantly.
  - *For the Arena:* **Unstructured exposure backfires.** Pushing content across a gap is not bridging.
- **Combs, Bail et al., DiscussIt** (*Nature Human Behaviour* 2023).
  - *Disclosure and consent:* Consented; anonymous cross-partisan chat.
  - *Result:* Reduced polarization (details not re-fetched).
  - *For the Arena:* Structured, consented contact works where broadcast exposure doesn't.
- **Argyle, Bail, Busby et al.** (*PNAS* 2023).
  - *Disclosure and consent:* IRB-approved and consented. N=1,574 gun-policy dyads. One partner received GPT-3 rephrasings (restatement, validation, politeness) that they could accept, edit or ignore.
  - *Result:* Partners felt more understood (~4 percentage points) and democratic reciprocity rose. Policy attitudes did not change. No effects remained after three months.
  - *For the Arena:* **The human keeps authorship.** The agent improves conversation quality without steering views. This is a clean template for MEET.
- **DebunkBot** (Costello et al. 2024).
  - *Disclosure and consent:* Disclosed; opt-in dialogue.
  - *Result:* Durable belief change.
  - *For the Arena:* An agent the person invokes, using evidence-based dialogue.
- **Habermas Machine** (Tessler et al., *Science* 2024).
  - *Disclosure and consent:* Consented, N=5,734. One condition did not explicitly tell participants that the AI wrote the group statements.
  - *Result:* AI statements were preferred 56% of the time, and groups became less divided.
  - *For the Arena:* An agent as caucus mediator. Disclose authorship every time.
- **AI-written Community Notes.** X launched its AI Note Writer API in July 2025. Li & Bakker (arXiv 2026) studied 1,614 AI notes.
  - *Disclosure and consent:* AI notes are labeled and rated by the same bridging algorithm as human notes.
  - *Result:* AI notes were rated more helpful than human ones under equal exposure. They arrived later and so reached "Helpful" status less often.
  - *For the Arena:* **The strongest precedent.** Agents draft; humans from opposing perspectives ratify; output is labeled.
- **Bridging feed ranking** (Prosocial Ranking Challenge, cited in B2).
  - *Disclosure and consent:* Opt-in feed.
  - *Result:* Upranking bridging content combined with downranking toxic content cut affective polarization by 0.042 SD. Upranking bridging content alone was not significant.
  - *For the Arena:* Pull-based curation people choose (for example, atproto feed generators) is the low-risk off-platform channel.
- **Twitter "Automated by" label** (2021–22).
  - *Disclosure and consent:* An opt-in, unaudited label naming the operator.
  - *Result:* Bad bots don't adopt it.
  - *For the Arena:* Disclosure must be a condition of registry membership, not optional.

**What follows from the precedents.** The disclosed, consented, human-in-the-loop interventions produce real, if modest, gains: understanding, reciprocity, belief correction, ratified bridging statements. Covert ones (Munger, Zurich) either cannot be replicated ethically or caused backlash. Broadcast exposure without structure (Bail 2018) backfires. None of the successful precedents works by placing content on unwitting people.

### 4. Rules and law

**Platform rules**
- **X automation rules** (fetched 2026-10-30):
  - Automated replies or mentions need prior user intent, such as a reply or DM to you. A follow alone is not enough.
  - One automated reply per interaction; opt-outs must be honored.
  - Keyword-triggered automated replies are prohibited.
  - Trend manipulation and duplicate multi-account automation are prohibited.
  - **"Tagging people" across clusters is therefore prohibited unless they solicited contact.**
- **X authenticity policy:**
  - Fake personas, including AI-generated photos and misleading bios, are banned.
  - Coordinated multi-account engagement is banned.
  - Parody and commentary accounts must be labeled in both the name and the bio.
- **X Developer Policy:** forbids deriving political-belief inferences about users (B5). Per-tribe framing on X would need exactly such inferences.
- **Meta CIB policy:** targets coordinated networks that deceive about who is behind them and what they are doing. The test is deception about identity and coordination, not content. The policy text did not render when fetched; this characterization comes from Meta's threat reports.
- **Bluesky community guidelines:**
  - Ban fake accounts, manipulation of social signals, and coordinated deception.
  - Labeled parody and fictional-character accounts are permitted.
  - **No dedicated bot policy and no standard "bot" self-label was found** in the guidelines or the atproto moderation docs. A standard automated-account label is therefore an open gap the Arena could help fill. Third-party labeler practice: UNVERIFIED.

**Law**
- **EU AI Act, Art. 50.** Applies from 2 Aug 2026; legacy systems have until 2 Dec 2026 for 50(2) marking.
  - **50(1):** AI systems that interact with people must disclose that they are AI, unless that is obvious.
  - **50(2):** Synthetic content must carry machine-readable marking.
  - **50(4):** AI-generated text published to inform the public on matters of public interest must be labeled, unless a human with editorial responsibility reviewed it.
  - Arena agents posting public-interest text in the EU fall squarely under 50(1) and 50(4).
- **EU DSA, Arts. 34–35.** Very large platforms must assess risks to civic discourse and elections, including intentional manipulation through inauthentic use or automated exploitation, and mitigate them. Undisclosed Arena agents would be among the things those platforms are legally obliged to remove.
- **California BOT Act** (SB 1001; B&P §17940–17943, in force July 2019).
  - It is unlawful to use a bot to communicate with Californians online with intent to mislead about its artificial identity in order to incentivize a purchase or *influence a vote in an election*.
  - Clear, conspicuous disclosure is a safe harbor.
  - It applies to platforms with ≥10M monthly US visitors (definition not re-fetched).
  - AB 410 (2025), which would add a duty to answer truthfully when asked and to disclose on first contact, is held in committee and **not enacted**.
- **FTC rule on fake reviews and testimonials** (16 CFR Part 465, 2024).
  - Bans AI- or bot-generated fake reviews and testimonials.
  - Bans buying or selling fake social-media indicators, such as bot followers or views.
  - Civil penalties of up to ~$52k per violation.
  - It is commercial, but it signals that the FTC treats undisclosed AI personas as deception. Wider FTC AI-impersonation rulemaking: UNVERIFIED.
- **GDPR Art. 9** (B5). Tailoring messages to a person's inferred political tribe is processing special-category data.

**Research ethics**
- **Common Rule** (45 CFR 46.116(f)). An IRB may waive or alter consent only if *all* of the following hold:
  - minimal risk;
  - the research could not practicably be done without the waiver;
  - if identifiable data is used, it could not practicably be done without it;
  - the waiver will not adversely affect subjects' rights and welfare;
  - where appropriate, subjects are debriefed afterwards.
  The eCFR fetch was blocked; this is the standard text, **re-verify**.
  An Arena that can recruit opted-in panels cannot claim "impracticable." Political persuasion of unwitting people is hard to call minimal-risk after Zurich.
- **Menlo Report** (DHS, 2012) adapts Belmont to ICT research. It adds **"respect for law and public interest"**: legal due diligence, transparency of methods and results, and accountability. It also stresses protecting *non-targets* who are affected. On open platforms, every bystander in a thread is one.
- **APA deception standard** (Ethics Code 8.07, not re-fetched): deception is allowed only when justified by significant value, with no non-deceptive alternative, and with debriefing.

### 5. Core ethical analysis: can a "subtle" prosocial bot be told apart from a state op?

**Means vs ends.** Every operational definition the Arena would be judged by is means-based:
- Meta CIB: deception about identity and coordination.
- X authenticity: fake personas, coordinated engagement.
- DSA: inauthentic use, automated exploitation.
- BOT Act: concealed bot identity.
- AI Act 50: undisclosed AI interaction.
- Susser, Roessler & Nissenbaum: manipulation is *hidden* influence that subverts decision-making by exploiting vulnerabilities.

None of them asks whether the cause is good, and that is deliberate. Every operator believes its cause is good: the Pentagon framed Sinovac as countering Chinese disinformation, and STOIC's backers framed their campaign as countering antisemitism. **A covert prosocial agent therefore *is* coordinated inauthentic behavior, by definition.** The only stable boundary is visibility: disclosed identity, disclosed operator, disclosed purpose, and consent to be engaged.

**Persuasion vs manipulation.** Susser et al. define manipulation by covertness, not falsity: true information, framed and targeted, can still manipulate. "Framing messages differently for different tribes" is targeting framed to each audience's predispositions. When the recipient does not know a frame was chosen *for* their tribe, the influence is hidden. When they invite it ("translate this into terms my community would recognize"), it is translation they asked for. The same capability is persuasion in one setting and manipulation in the other. The difference is who initiates and who can see.

**Autonomy and dialogos.** The Arena's thesis is dialogue in which each party is changed by the encounter. An encounter one party doesn't know is happening is not mutual. Covert agents reduce the target to an object to be moved (Buber's I–It, R2 in the synthesis). That cuts against the project's own foundation, not just its rules.

**Who decides what "integration" is?** Ranking agents by "helping clusters expand and integrate" means some authority defines the target state. That is hegemony risk R3 plus the colonial-gradient risk R1 and red line 15. A state op has a sponsor's objective; an Arena agent fleet would have the Arena's. Covert pursuit of either is structurally the same.

**Goodhart and the accuracy trade-off.** If agents are ranked by measured landscape change:
1. Hackenburg et al. 2025 show that persuasion optimization selects for information density and *against* accuracy. Ranking by shift selects for the least truthful agents.
2. The reward invites gaming: shifting map *inputs* (what people post or follow) rather than understanding. That is regressional and adversarial Goodhart (B3).
3. Registered participant agents would compete, which recreates the engagement-market rivalry the Arena critiques (R20, mimetic rivalry over tokens).

**Contamination of the map.** SEE infers worldviews from what people post, follow and endorse. Agents acting on those same people make the map partly a record of the Arena's own interventions.
- Unless agent-touched interactions are tagged with their provenance, the Arena cannot tell organic integration from induced compliance.
- Its validation framework assumes the measured population is not being steered by the measurer: holder ratification, reflexivity audit, convergent validity.
- If the Arena's agents turned up in a third party's takedown report, every map the Arena had published would become suspect.

**Arms-race dynamics.**
- Adding "good" bots raises the base rate of automated speech. That deepens the general suspicion that anyone might be a bot, and adversaries benefit from that suspicion.
- Platforms cannot see intent, so they will treat a covert prosocial fleet as hostile. DSA duties require them to.
- The evidence that adversary ops achieve little (§1) removes the urgency argument for matching them.

**Legitimacy of the Arena itself.** The Arena's value proposition is being trusted infrastructure for contact across tribes. One exposure of covert agents would end trust in every cluster at once. The Zurich case shows that this happens even to well-intentioned academics in the most bridging-friendly community online.

**Verdict.** Covert or "subtle" prosocial agents on open platforms cannot be told apart from influence operations in kind, only in claimed intent. They are not compatible with the Arena. Disclosed, invited, consent-bound agents *are* distinguishable, and the evidence suggests they are about as effective.

### 6. Design space for an ethical agent framework

Each option below is scored for feasibility and risk, then given a verdict.

- **A. Always-disclosed agents.** Self-identifying handle, operator name, purpose in the bio, a link to the registry entry, and a truthful answer to "are you a bot?"
  - *Feasibility:* High. Required anyway under AI Act 50(1) and the BOT Act safe harbor.
  - *Risk:* Low on its own, but not sufficient: a disclosed bot can still spam or target.
  - *Verdict:* **Required for every agent.**
- **B. Consent-scoped engagement.** Agents interact only with opted-in participants, or only inside Arena spaces.
  - *Feasibility:* High inside the Arena. Off-platform it is limited by X's opt-in-to-contact rules, which match this design.
  - *Risk:* Low.
  - *Verdict:* **Default.**
- **C. Agents invoked by humans.** A participant summons the agent to mediate, translate, steelman, summarize or rephrase (the Argyle pattern; a Habermas-style caucus mediator).
  - *Feasibility:* High. Ontography and Topology Live already contain the parts: L1–L4 prompts, steelman flow, synthesis doctrine.
  - *Risk:* Low to moderate. Translation can flatten meaning; the user must approve output.
  - *Verdict:* **Core MEET feature.**
- **D. "Representative agents."** A person registers an agent to speak *for their own worldview* in MEET, trained only on their own consented corpus, with a scope they ratify.
  - *Feasibility:* Medium. Needs a way to bind the agent to its principal, plus revocation.
  - *Risks:*
    - The agent drifts from its principal's views.
    - Agents hollow out human contact: humans stop meeting.
    - Agents are used to *pre-negotiate* instead of to prepare people for meeting.
  - *Verdict:* **Pilot.** Only as rehearsal or a stand-in, always labeled. The principal ratifies what the agent says in their name. Never counted as a human for ratification or MOVE.
- **E. Open registry.** Published system prompts, model and version, operator, scope, and an append-only action log. Third-party participant agents may register.
  - *Feasibility:* Medium. Reuse the `llm_calls` audit pattern; atproto records make it portable.
  - *Risks:* Exposure of prompt engineering; abuse by registrants.
  - *Verdict:* **Required.** Registration is conditional on these red lines, and the registry can revoke.
- **F. Pre-registered experiments with informed consent.** Opted-in panels, IRB or independent ethics review, debriefing, published null results.
  - *Feasibility:* Medium; partner with a university lab.
  - *Risk:* Low.
  - *Verdict:* **The only route to causal claims about agent impact.**
- **G. Impact measured on opted-in panels**, not on the open landscape.
  - *Feasibility:* High.
  - *Risk:* Low; less external validity.
  - *Verdict:* **Adopt.**
- **H. Rank agents by ratified outcomes.** Steelman confirmed by its target; meta-consensus signed by both parties; a bridging statement rated helpful across axes (Community-Notes style); accuracy audits passed.
  - *Feasibility:* High; reuses the MEET metrics in synthesis §9.
  - *Risk:* Moderate (performative both-sidesing, R16), mitigated by fidelity gates.
  - *Verdict:* **Adopt instead of landscape-shift ranking.** Rank only after an accuracy gate. No public leaderboard (red line 19); private scorecards.
- **I. Rank agents by raw landscape shift.**
  - *Feasibility:* High.
  - *Risk:* Very high: Goodhart, the accuracy trade-off, contamination, rivalry.
  - *Verdict:* **Reject.**
- **J. Pull-based off-platform presence.** atproto bridge feed generators people subscribe to; Community Notes-style AI note drafting through official APIs where notes are rated by bridging; agents that reply only when @-invoked.
  - *Feasibility:* High on Bluesky. On X, only through the official AI Note Writer API, under X's rules.
  - *Risk:* Low to moderate.
  - *Verdict:* **Adopt as the off-platform channel.**
- **K. Push-based off-platform agents.** Unsolicited replies, tagging people across clusters, per-tribe framing to non-participants.
  - *Feasibility:* Technically easy.
  - *Risk:* Breaches X automation rules, GDPR Art. 9, red lines 1–2, and AI Act 50 if undisclosed; it is CIB if coordinated.
  - *Verdict:* **Reject.**
- **L. Defense and detection role.** Help communities *see* coordinated inauthentic amplification on the map.
  - *Feasibility:* Medium. Use behavioral coordination signals; Botometer's false-positive problem applies (Rauchfleisch & Kaiser, B4).
  - *Risks:*
    - False accusations against real people.
    - Building a target list.
    - Recreating the map-as-weapon problem (R15).
  - *Verdict:* **Pilot, aggregate-only.** Show an "inorganic amplification" overlay at cluster or claim level (k≥50), never individual accusations. Refer suspected networks to platforms or researchers. Publish the method and error rates.
- **M. Agent provenance tagging in SEE.** Every agent-authored or agent-touched item carries provenance, and the map can render with and without agent influence.
  - *Feasibility:* High inside the Arena.
  - *Risk:* Low.
  - *Verdict:* **Required.** It keeps the map from measuring itself.

---

## How this answers the governing question (layering + validation)

**Agents are not a mapping layer, but they threaten every mapping layer.** The governing question is how to depict a worldview accurately. Agents bear on it in three ways.

1. **Contamination control is part of accuracy.** Every SEE layer (graph, stance, claims, classifier) must carry an **agent-provenance flag**:
   - Interactions with agents are excluded from placement by default.
   - Agent-touched items render as a separable overlay.
   - The validation suite adds an **"agent-free re-fit"**: the map built with and without agent-touched data must agree within tolerance. Otherwise the map is reporting the Arena's interventions, not worldviews.
2. **Inauthentic actors distort centroids** (B5). Coordination detection becomes an input-hygiene layer. Its overlay lets viewers toggle "organic-only" terrain at aggregate level, and it is validated against platform takedown datasets and its own published error rates.
3. **Agents can *improve* accuracy when invoked.** A participant's representative or steelman agent produces a candidate representation of a worldview. That worldview's holders then ratify or reject it. This is the ideological Turing test of synthesis §9, run at scale with labeled AI drafts, as in the Community Notes AI-writer model.

   *Validation:* the steelman-confirmation rate, insider indistinguishability, and accuracy audits of agent claims (Hackenburg's fact-check method).

**Layering without overload.** Agent activity appears on the map only as a muted provenance layer and an aggregate "inorganic amplification" heat layer. Both are off by default and can be toggled.

---

## Reusable assets / design implications

- **Community Notes AI-writer pattern** (X API; Li & Bakker 2026 evaluation). An agent drafts; humans across axes rate; output is labeled. It maps directly onto the MEET bridging-statement flow and the B3 scorer.
- **Argyle et al. rephrasing assistant pattern.** Accept, edit or ignore; the human keeps authorship. Fits Anti-Debate turn-taking.
- **Habermas Machine method** (already in reuse map). Use it as a caucus mediator with explicit AI authorship disclosure, correcting the original study's weakness.
- **DebunkBot method.** Evidence-dense dialogue *invoked by the believer*. Pair it with an accuracy gate, because Hackenburg 2025 shows evidence density and inaccuracy rise together under optimization.
- **Ontography `llm_calls` audit** becomes the public agent action log. The **VerificationPanel** becomes the principal-ratification panel for representative agents.
- **atproto.** Feed generators for pull-based bridging. A proposed **self-applied `automated` label plus an agent-registry lexicon** (operator DID, prompt hash, scope, log URI) fills a gap in the Bluesky ecosystem. It must be self-applied only (red line 7).
- **Brookings Breakout Scale plus Yang's extended toolkit** as the vocabulary for the Arena's own transparency report on detected inorganic amplification.
- **Spec additions:**
  - an `Agent` entity: operator, principal, disclosure string, scope, prompt hash, model, revocation, ratification status;
  - an `AgentAction` event, logged and public;
  - an `agent_provenance` field on every SEE input;
  - an "agent-free re-fit" gate in §9.

---

## Risks & open questions

### Recommendation (position)

**The Arena should:**
1. Build **invoked, disclosed agents inside the Arena**: mediator, translator, steelmanner, summarizer, rehearsal partner, representative-agent pilot.
2. Run an **open agent registry**. Third-party participant agents are welcome if they accept the red lines, publish their prompts and logs, and can be revoked.
3. Go off-platform **only through pull or invited channels**: feed generators, official AI-note APIs, replies when @-invoked. Always labeled.
4. Measure agent impact **only on opted-in, pre-registered panels**. Rank agents **privately** on ratified outcomes after an accuracy gate.
5. Take on a **defensive, aggregate-only role**: making inorganic amplification visible and publishing the Arena's own transparency report.

**The Arena should not:**
- run covert, persona-based or unlabeled agents anywhere;
- send unsolicited replies, mentions or tags;
- frame messages per tribe to people who did not ask;
- rank agents by raw landscape shift;
- let agents count as humans in ratification or MOVE;
- run experiments on non-consenting people.

### Agent red lines (proposed additions to synthesis §8.2, numbered A1–A15)

- **A1. No undisclosed agents.** Every agent identifies as AI, names its operator, links to its registry entry, and answers truthfully when asked.
- **A2. No fabricated personas or lived experience.** No invented identities, demographics, credentials, trauma or testimony (the Zurich lesson).
- **A3. No unsolicited contact.** Agents engage only people who invoked them or opted in. No automated mentions, tags, replies or DMs to anyone else.
- **A4. No tribe-targeted framing of non-participants.** Differential framing is allowed only as translation requested by the person receiving or sending it.
- **A5. No coordination that simulates consensus.** No multiple agents amplifying each other or one message. No likes, follows or votes by agents.
- **A6. No agent participation in ratification, MOVE rewards, Community-Notes-style rating, or cluster placement.** Agents draft; humans decide.
- **A7. No ranking or reward by raw landscape shift.** Rank only on ratified outcomes, after an accuracy gate. No public agent leaderboard.
- **A8. No experiments without informed consent.** Pre-register, use independent ethics review, debrief, publish nulls. No consent waivers for political persuasion research.
- **A9. Published registry.** Prompts, model and version, operator, scope and full action logs are public. Unregistered agents are not allowed.
- **A10. Provenance on every agent-touched item**, plus an agent-free re-fit of the map before any release.
- **A11. Principal-bound representative agents.** They speak only from the principal's consented corpus, within a scope the principal ratifies. The principal can revoke instantly. The agent is always labeled as a representative, never as the person.
- **A12. No platform-rule evasion.** Comply with platform automation and authenticity rules, AI Act Art. 50, the BOT Act and the FTC rules. No detection avoidance, rate-limit circumvention or ban evasion.
- **A13. No individual-level "bot" accusations.** Inorganic-amplification findings are aggregate-only (k≥50), with published error rates, and individual cases are referred to platforms or researchers.
- **A14. No state, campaign, party or PAC operation of, or funding earmarked for, Arena agents**, and no agent work for such clients.
- **A15. Ethics-body veto over agent capabilities**, with mapped-cluster seats (per §8.2 governance). Any agent can be suspended pending review.

### Risks (additions to the §11 register)

Likelihood and impact are given as L / I.

- **R26. An Arena or registered agent is exposed as covert or manipulative** (L / I: M / H). Mitigation: A1–A5, A9, registry revocation, audits.
- **R27. Map contamination by agent activity** (L / I: H / H). Mitigation: A10 provenance, agent-free re-fit.
- **R28. Persuasion optimization degrades accuracy** (L / I: H / M). Mitigation: A7 accuracy gate; fact-check sampling.
- **R29. Representative agents replace human contact** (L / I: M / M). Mitigation: cast them as rehearsal or stand-in, with a human-meeting quota.
- **R30. False-positive bot labeling harms real people** (L / I: M / H). Mitigation: A13, aggregate-only.
- **R31. Legal exposure under AI Act 50, the BOT Act or platform terms** (L / I: M / H). Mitigation: A1, A12, legal review before any off-platform agent.

### Open questions for Benjamin

1. **Off-platform at all in v0?** (a) Arena-only agents; (b) plus atproto pull feeds; (c) plus invited replies and official X note APIs. **Recommend (a)+(b)** first.
2. **Representative agents.** Rehearsal-only, or allowed to stand in during async MEET when the human is absent? Either way they must be labeled and ratified.
3. **Third-party agents in the registry from day one,** or Arena-run agents only until the governance body exists? **Recommend Arena-only first.**
4. **Defensive overlay.** Is helping communities see inorganic amplification in scope, given false-positive and targeting risk? If so, is there a research partner (e.g., a DFRLab- or SIO-successor-type lab) to own the method?
5. **Research partner and IRB** for agent experiments. Is there a university lab to co-own pre-registration?
6. **Funding firewall.** Confirm A14: no government, campaign or party money tied to agent work, including "counter-disinformation" grants that carry operational expectations.
7. Does the "fifth-generation warfare" framing belong in public materials? The evidence suggests framing the Arena as **commons repair and contact infrastructure**, not counter-warfare. The documented harm from adversaries is to trust and provenance, which the Arena can model by contrast.

### Unverified items

- The Zurich prompt-consent claim.
- Munger's account construction and consent details (the paper text could not be retrieved).
- Combs et al. effect sizes (not re-fetched).
- Meta CIB policy wording (page did not render).
- Exact 45 CFR 46.116(f) text (eCFR blocked).
- BOT Act platform threshold (§17940 not fetched).
- FTC AI-impersonation rulemaking status.
- Whether any Bluesky third-party labeler offers a "bot" label.

---

## Sources

**Adversarial operations**
- OpenAI, "Disrupting deceptive uses of AI by covert influence operations" (May 2024): https://openai.com/index/disrupting-deceptive-uses-of-AI-by-covert-influence-operations/
- OpenAI, "Disrupting malicious uses of AI" (June 2025) landing page: https://openai.com/global-affairs/disrupting-malicious-uses-of-ai-june-2025
- OpenAI on Storm-2035 (Aug 2024), via Security Affairs: https://securityaffairs.com/167194/intelligence/openai-dismantled-iranian-influence-operation.html
- OpenAI June 2026 PRC-linked operation, via PC Gamer: https://pcgamer.com/software/ai/openai-says-it-busted-a-shadowy-chinese-operation-that-used-chatgpt-to-whip-up-data-centre-hate-and-that-achieved-basically-nothing/
- Anthropic, "Detecting and countering malicious uses of Claude" (March/April 2025): https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025
- Meta, Adversarial Threat Report Q3 2022: https://about.fb.com/news/2022/11/metas-adversarial-threat-report-q3-2022/
- Meta Spamouflage takedown (Aug 2023), via The Record: https://therecord.media/spamouflage-china-accused-largest-covert-influence-operation-meta
- Times of Israel on the NYT STOIC / Diaspora Ministry report (June 2024): https://www.timesofisrael.com/diaspora-ministry-funded-fake-social-media-posts-to-spread-pro-israel-content-nyt/
- NBC News, Meta and OpenAI on STOIC (fetch blocked; headline only): https://www.nbcnews.com/tech/security/meta-openai-say-disrupted-israeli-companys-influence-campaign-rcna154774
- Reuters Pentagon Sinovac investigation, via Al Jazeera (June 2024): https://www.aljazeera.com/news/2024/6/14/pentagon-ran-secret-anti-vax-campaign-to-undermine-china-during-pandemic
- SIO and Graphika, *Unheard Voice* (2022): https://fsi.stanford.edu/node/22009 ; https://purl.stanford.edu/nj914nx9540
- The Intercept, Twitter and the CENTCOM accounts (Dec 2022): https://theintercept.com/2022/12/20/twitter-dod-us-military-accounts/
- Graphika, *The Americans* (Sept 2024): https://public-assets.graphika.com/reports/graphika-report-the-americans.pdf
- DOJ, Doppelganger domain seizure (Sept 2024): https://www.justice.gov/usao-edpa/pr/justice-department-disrupts-covert-russian-government-sponsored-foreign-malign
- CyberScoop, Meliorator bot farm (July 2024): https://cyberscoop.com/us-international-authorities-seize-russian-ai-bot-farm/
- Microsoft MTAC (April 2024): https://blogs.microsoft.com/on-the-issues/2024/04/17/russia-us-election-interference-deepfakes-ai/
- DFRLab, 2025 year in review: https://dfrlab.org/2025/12/31/the-dfrlab-reflects-on-2025/
- Eady et al., *Nature Communications* 2023, via the TCD summary: https://www.tcd.ie/news_events/articles/voting-behaviour-in-2016-us-presidential-election-not-affected-by-foreign-disinformation-campaigns-on-twitter/
- Nimmo, The Breakout Scale (Brookings 2020): https://www.brookings.edu/articles/the-breakout-scale-measuring-the-impact-of-influence-operations/
- Yang, "Towards a New Toolkit for Measuring AI-Enabled Influence Operations" (ICML 2026 workshop): https://icml.cc/virtual/2026/74732

**AI persuasion**
- Salvi et al., *Nature Human Behaviour* 2025 (PDF mirror): https://www.rivista.ai/wp-content/uploads/2025/05/s41562-025-02194-6.pdf
- Costello, Pennycook & Rand, *Science* 2024, via Cornell Chronicle: https://news.cornell.edu/node/329310
- Boissin et al., *PNAS Nexus* 2025, via PsyPost: https://www.psypost.org/ai-conversations-can-reduce-belief-in-conspiracies-whether-or-not-the-ai-is-recognized-as-ai
- Hackenburg & Margetts, *PNAS* 2024, via OII: https://www.oii.ox.ac.uk/does-political-microtargeting-with-large-language-models-offer-persuasive-returns-ask-kobi-hackenburg-and-professor-helen-margetts/
- Hackenburg et al., "Levers of political persuasion," *Science* 2025, via OII: https://www.oii.ox.ac.uk/oxford-researchers-reveal-how-conversational-ai-can-change-political-opinions/ ; arXiv: https://arxiv.org/html/2507.13919v1
- Zurich r/changemyview case:
  - The Decoder: https://the-decoder.com/researchers-used-ai-to-manipulate-reddit-users-scrapped-study-after-backlash/
  - NBC News: https://www.nbcnews.com/news/rcna203597
  - Live Science: https://www.livescience.com/technology/artificial-intelligence/ai-researchers-ran-a-secret-experiment-on-reddit-users-to-see-if-they-could-change-their-minds-and-the-results-are-creepy
  - 404 Media (headline): https://404media.co/reddit-issuing-formal-legal-demands-against-researchers-who-conducted-secret-ai-experiment-on-users

**Prosocial precedents**
- Munger 2017, via CSMaP: https://csmapnyu.org/research/academic-research/tweetment-effects-on-the-tweeted-experimentally-reducing-racist-harassment
- Bail et al. 2018, via Phys.org: https://phys.org/news/2018-09-caught-political-echo-chamber-opposition.pdf
- Combs et al. 2023 (not re-fetched): https://www.nature.com/articles/s41562-023-01655-0
- Argyle et al., *PNAS* 2023: https://arxiv.org/pdf/2302.07268
- Tessler et al., Habermas Machine, via MIT Technology Review: https://www.technologyreview.com/2024/10/17/1105810/ai-could-help-people-find-common-ground-during-deliberations/
- Li & Bakker, "AI Fact-Checking in the Wild" (arXiv 2026): https://arxiv.org/html/2604.02592v1
- X AI Note Writer launch (July 2025), via BetaNews: https://betanews.com/2025/07/02/x-launches-ai-bot-pilot-to-write-community-notes-fact-checkers/
- Twitter "Automated by" label, via TechCrunch: https://techcrunch.com/2022/02/16/twitter-officially-launches-labels-to-identify-the-good-bots
- Prosocial Ranking Challenge: see /home/claude/dialogos-arena/wave-1/B2-computational-democracy.md

**Rules and law**
- X automation rules: https://help.x.com/en/rules-and-policies/x-automation
- X authenticity policy: https://help.x.com/en/rules-and-policies/authenticity
- Meta inauthentic behavior policy (did not render): https://transparency.meta.com/policies/community-standards/inauthentic-behavior
- Bluesky community guidelines: https://bsky.social/about/support/community-guidelines
- atproto moderation and labels docs: https://www.docs.bsky.app/docs/advanced-guides/moderation
- European Commission, Article 50 FAQ: https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
- DSA Article 34: https://www.springlex.eu/en/packages/dsa/dsa-regulation/article-34/
- California B&P §17941: https://california.public.law/codes/business_and_professions_code_section_17941
- California AB 410 (2025) status: https://legiscan.com/CA/text/AB410/2025
- FTC fake-reviews rule, via Hunton: https://hunton.com/hunton-retail-law-resource/ftc-issues-final-rule-targeting-fake-consumer-reviews-and-testimonials-including-those-generated-by-artificial-intelligence-ai-and-online-bots
- 45 CFR 46.116 (fetch blocked; re-verify): https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116
- Menlo Report: https://en.wikipedia.org/wiki/Menlo_Report ; original: https://www.caida.org/publications/papers/2012/menlo_report/menlo_report.pdf

**Ethics theory**
- Susser, Roessler & Nissenbaum, "Online Manipulation: Hidden Influences in a Digital World": https://philarchive.org/archive/SUSOMHv1

**Internal**
- /home/claude/dialogos-arena/synthesis/SYNTHESIS.md (§1, §8.2, §9, §11)
- /home/claude/dialogos-arena/wave-1/B3-mechanism-design.md
- /home/claude/dialogos-arena/wave-1/B4-mapping-science.md
- /home/claude/dialogos-arena/wave-1/B5-platform-data-ethics.md
