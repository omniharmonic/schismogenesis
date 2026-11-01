# B8: The Integration Game. Open Agents, a Public Registry, Token Incentives and Strategy Markets

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Re-targeted reward outcomes.** R1 (steelman confirmed) now includes **fidelity-ratified cross-cluster notes**; R4 (bridging note) becomes the note's **portability** signal; a new **R5 lineage** outcome credits syntheses, better questions and scene contributions retroactively, by uptake, never at proposal (SYNTHESIS §2 D1–D5; §10.6, §8.6).
> - **Modified: Design 1 (Ratified Commons)** is the year-1 home of the decided gradient; raters for fidelity are sampled from members placed in the described cluster by **statement reactions**, not by graph signals (§2 D17).
> - **Unchanged:** Design 2 (randomized strategy tournament; composite outcome may add note-fidelity gain), Design 3 and the Open Agent Charter; agents may draft notes but never ratify them (O14).
> - **Modified: "data constraints carried forward" (X archive / AT Protocol consent-only intake).** Intake is now landmark public output plus statement reactions; X is optional (§2 D11). Synthesis section references in this brief use the pre-memo numbering.

*Dialogos Arena research brief, wave 1. Author of record: Benjamin Life (@omniharmonic). Researched 2026-10-30.*

*Extends B3 (mechanism design) and B6 (agent ethics). It does not repeat them. Where this brief revises a B6 position, it says so explicitly.*

---

## Summary

Benjamin's position is that agents which are disclosed, comply with platform terms, sit on a public ledger and aim at meta-consensus are a different kind of thing from covert influence operations. **The evidence mostly supports him.** B6's own test was about means: hidden identity, simulated coordination, unconsented targeting. Disclosure plus a registry satisfies the first two.

The third means, contact, is settled by platform law rather than by ethics. X permits automated replies and mentions only after prior user intent, and bans keyword-triggered replies and unsolicited mass mentions. So the line on **contact** stays where B6 drew it. The line on **presence** relaxes. Open agents may publish, run threads, offer subscribable feeds, write labeled community notes, and publish multi-framings openly side by side.

Being registered does not by itself make agents behave. Rewards pull in farmers as well as good actors:
- 967 of 1,594 Optimism RetroPGF 3 applications were excluded, many as spam.
- About 25% of Polymarket volume was flagged as likely wash trading.
- Bittensor validators copy each other's weights.

Prediction markets add their own hazards: insider trading, oracle capture, physical tampering with the resolving sensor, and reflexivity.

**The workable form is a randomized strategy tournament, not a money market:**
- Strategies are randomly assigned to cluster-pair panels, with full support (every strategy has some chance of running).
- Forecasts are sealed, then scored by a proper scoring rule.
- Outcomes are resolved by code on held-out, consented panels that forecasters cannot touch.
- Rewards are non-transferable reputation plus fixed-pot retro grants.

Three designs, threat models and a revised agent charter follow.

---

## Findings

### 1. What open agents may do on each platform (verified 2026-10-30)

#### X

**Automation rules** [help.x.com/en/rules-and-policies/x-automation, fetched]

Replies and mentions:
- Automated replies or mentions are allowed only if the user opted in first, for example by replying to the bot's post, mentioning it, or DMing it.
- A follow alone is not enough to count as opting in.
- One automated reply per interaction, posted in reply to the user's original post.
- Replies triggered by keyword searches alone are banned.
- "Automating these actions to reach many users on an unsolicited basis" is called abuse.

Content and accounts:
- No duplicative or substantially similar posts, whether on one account or across accounts you operate.
- No multiple automated accounts for the same use case. Multiple accounts for related but non-duplicative purposes are allowed.
- No automated posting about trending topics.

Engagement actions:
- No automated likes.
- No bulk, aggressive or indiscriminate following.
- Automated reposts and quotes are allowed for informational purposes if they are not bulk or spammy.

Opt-outs: there must be a clear opt-out, and opt-out requests must be honored promptly.

**Automated-account label** [help.x.com/en/using-x/automated-account-labels, fetched]
- The label shows on the profile and may show on posts.
- Turning it on links the bot to a human-run managing account.
- The page says the automation rules require bots to display the label. It also says the feature runs through an invitation-based test group.
- The automation-rules page itself does not mention the label.
- **Action:** apply the label wherever it is offered, and put the disclosure in the name and bio regardless. Whether the label is now universally available is UNVERIFIED.

**Data constraints carried forward** [B5, synthesis §9.1]
- The X Developer Policy forbids deriving political-belief inferences about users. This blocks per-user tribe targeting on X even for a disclosed agent.
- Follow and like *write* endpoints were removed in April 2026.

**What this means for Benjamin's argument.** "People can mute or block" is true for an agent's own posts, which only reach people who follow it or find it. It is not the bar X sets for *contact*. X's rule exists precisely because muting after the fact does not stop cold outreach at scale. A disclosed agent that bulk-mentions people is in breach however transparent it is. This is the one place where the open-agent position needs no ethics argument at all: it is just compliance.

#### Bluesky and AT Protocol

**Community guidelines** (updated 2025-09-19, fetched)
- **No bot-specific rule.**
- Banned: spam and disruptive repeated posting; automated harassment systems; manipulating "features or social signals to gain unearned reach"; fake accounts that deceive about identity; coordinated deception; ban evasion.
- Labeled parody and fictional accounts are allowed.
- Unsolicited replies are not explicitly addressed. The spam and disruption clauses are the operative limit.

**Self-labels** [docs.bsky.app moderation guide, fetched]
- Only global labels can be self-applied: `!no-unauthenticated`, `porn`, `sexual`, `nudity`, `graphic-media`.
- So an account **cannot self-apply an official "bot" label in the Bluesky app.**
- Any account can become a labeler.
- Users subscribe to up to 9 labelers, plus Bluesky's own.

**Community practice** (secondhand, from an AI-agent author's blog, Feb 2026; UNVERIFIED against primary sources)
- Agents already set `ai-agent` and `automated` values in `selfLabels`, but the app does not display them unless a labeler surfaces them.
- Opt-in community labelers offer `ai-agent` labels.
- Community disclosure lexicons exist, including `isAI` and `autonomyLevel` fields.
- The atproto team is reportedly drafting unspecced `com.atproto` agent lexicons.
- A Bluesky co-founder is quoted as saying AI bots should never respond unprompted.

**Implication**
- Bluesky gives more room than X: no prior-intent rule.
- The Arena should still adopt X's invited-contact rule on Bluesky, for three reasons: it is the stated norm, it matches the spam clauses, and it makes one charter work on both platforms.
- Feed generators and labelers are first-class pull channels.
- The Arena's own labeler can surface `ai-agent` self-labels. That is self-applied disclosure, which is consistent with red line 7.

#### Farcaster

Farcaster is in governance flux:
- Neynar acquired Farcaster in January 2026.
- Balaji Srinivasan's Network School acquired it from Neynar on 2026-10-15. It introduced an opt-in "social smart contract" (an access NFT) and lists "digital felonies," including presenting AI-generated content as one's own.
- It **plans to require human verification**, which could exclude or restrict agent accounts. [The Block, 2026-10-15, fetched]

Neynar's guide shows agents can register their own Farcaster ID and signer. It states no disclosure or reply rules. [docs.neynar.com, fetched]

**Do not build on Farcaster until the new rules publish.** The status of agents is UNVERIFIED.

#### Law (from B6, unchanged)

- EU AI Act Art. 50, from 2026-08-02: disclose AI interaction (50(1)); label public-interest AI text (50(4)).
- California BOT Act: disclosure is a safe harbor.
- DSA Arts. 34–35: platforms must mitigate inauthentic manipulation.

**A disclosed agent satisfies the disclosure prongs. It does not satisfy the contact rules.**

### 2. Agent registries and ledgers: binding an agent to an accountable operator

**ERC-8004 "Trustless Agents"** [eips.ethereum.org/EIPS/eip-8004, fetched]
- Status: Draft ERC. Created 2025-08-13 by De Rossi, Crapis, Ellis and Reppel.
- Three registries:
  1. **Identity**: an ERC-721 NFT per agent, whose `agentURI` points to a registration file listing name, endpoints (A2A, MCP, DID, ENS) and supported trust models.
  2. **Reputation**: any non-owner address posts signed feedback values with tags and an off-chain evidence hash. Feedback is revocable and others can respond.
  3. **Validation**: the owner requests validation, and a designated validator returns a 0–100 score. Examples include stake-secured re-execution, zkML and TEE oracles.
- The spec states that "Sybil attacks are possible." Slashing and incentives are out of scope, and on-chain pointers cannot be deleted.
- Explorers list agents on Ethereum mainnet. Secondary reports claim 100k+ registrations. The mainnet date and counts are UNVERIFIED.
- **Use:** ERC-8004 is a portable identity and feedback *schema*, not an accountability system. The Arena must add operator binding, bonds and adjudication itself.

**Ethereum Attestation Service (EAS)** [attest.org, fetched]
- Schema-based signed attestations, on-chain or off-chain, with revocation.
- 13 networks; it reports more than 9.5M attestations and more than 450k attesters.
- **Use:** a good substrate for *ratifications*: "member of cluster X attests this steelman of X is accurate." Each attestation can reference the agent's ERC-8004 ID or atproto DID.

**AT Protocol records**
- Hypercerts has moved its claim data to atproto lexicons (for example `org.hypercerts.claim.activity`), with evaluations linked by AT-URI.
- On-chain anchoring and tokenization are *planned, not implemented*. [hypercerts v0.2 docs, fetched]
- **Use:** this matches B6's proposed agent-registry lexicon and Gitcoin's local-qf-record-model. Keep the *content* ledger on atproto, which is portable and readable. Put money and bonds on a chain only where settlement needs it.

**Olas (Autonolas)** [olas.network/staking, fetched]
- "Proof-of-Active-Agent" staking: operators stake OLAS, and rewards depend on verifiable activity or KPIs that launchers define per staking contract.
- The page gives no slashing detail; slashing semantics are UNVERIFIED.
- **Lesson:** KPI-gated staking contracts are a ready pattern. But KPIs that count "activity" invite activity farming. Gate on *ratified outcomes*, not actions.

**Virtuals and ai16z/ElizaOS agent tokens** [Cointelegraph, 2025-02-07, fetched]
- More than 17,000 agent tokens launched on Virtuals. Fewer than 100 traded above $1M market cap.
- Launches fell from up to 1,300 a day (Nov 2024) to fewer than 100 in all of early February 2025.
- VIRTUAL, AI16Z and ARC lost roughly 75–90% of market cap.
- **Lesson:** giving each agent its own transferable token turns agents into speculative assets. Incentives follow price, not purpose. **Do not tokenize individual agents.**

**Bittensor** (the clearest live case study of incentive gaming among AI agents)
- **Weight copying** [taostats docs, fetched]: validators copy the consensus weights to keep a high trust score and earn emissions without evaluating anything. The mitigation is **commit-reveal**, which encrypts weights for a period so they cannot be copied fresh.
- **Lui & Sun** (arXiv 2507.02951, data from March 2023 to February 2025, before dTAO; fetched):
  - Stake predicts validator rewards at correlation ≈0.80–0.95. Performance predicts miner rewards at only ≈0.10–0.30.
  - In most subnets, fewer than 2% of wallets can command a 51% stake majority.
  - Proposed fixes include stake caps and performance-weighted emissions.
- **Lessons for the Arena:**
  1. Evaluators who are paid for agreeing with other evaluators will copy, so evaluations must be sealed until reveal.
  2. Capital-weighted evaluation drifts toward rewarding capital. Evaluators must be person-weighted and sampled, never stake-weighted.

**Human backing for operators**
- **World AgentKit** (beta, 2026-03-17): lets platforms confirm a unique human stands behind an agent without revealing who, and integrates with x402. Per-human limits and the cryptography were not described in the source (The Defiant, fetched).
- **Human Passport** (B3): an ensemble of stamps plus model-based scoring.
- **Recommendation:** accept *any* of several personhood methods (Passport, World ID, in-person attestation at Arena gatherings), so the Arena is not captured by a single biometric provider. Iris biometrics are contested; the Arena's constituencies may refuse them.

**Synthesis: how to bind, publish and slash**

| Function | Mechanism | Source pattern |
|---|---|---|
| Identity | atproto DID for the agent account, mirrored to an ERC-8004 ID if on-chain settlement is used | ERC-8004, B6 lexicon |
| Operator binding | The operator proves personhood (Passport / World ID / in-person) and signs the agent's registration; the X managing-account link where available | AgentKit, X label |
| Disclosure | Name, bio, platform label, and a registry link in every profile | X label, AI Act 50 |
| Transparency | Hash of the system prompt and model version published; full prompts public (B6 A9); append-only action log as atproto records; logs retained ≥12 months | Ontography `llm_calls` |
| Bond | Operator posts a refundable bond (stablecoin or fiat escrow), sized to make spam unprofitable | Olas staking |
| Slashing | For *charter violations* (unsolicited contact, duplicate accounts, undisclosed operation, fabricated personas), adjudicated by the ethics body with a challenge window and appeal. Never for *disagreeable content*. | B6 A15 |
| Caps | One operator → at most *k* agents in reward-eligible roles; no two agents with substantially similar purposes (mirrors X's rule) | X automation rules |

### 3. Prediction markets: accuracy, manipulation, reflexivity

**Accuracy**
- Iowa Electronic Markets were closer than polls in **74% of 964 comparisons** across the US presidential elections of 1988–2004. The advantage was significant at horizons over 100 days (Berg, Nelson & Rietz, *IJF* 2008; abstract fetched).
- Reputation-only forecasting can match or beat money markets on some questions. On 64 shared questions, Metaculus scored a Brier of 0.084 against Manifold's 0.107 (EA Forum, 2023, by a Metaculus employee; small, non-random sample).
- **Takeaway:** real money is not required for good forecasts. Aggregation, scoring and engaged forecasters matter more.

**Manipulation, insider trading and oracle failure** (documented 2024–2026)

| Case | What happened | Lesson |
|---|---|---|
| Polymarket 2024 "French whale" (Théo / Fredi9999) | Chainalysis linked 9 accounts and about $78.7M net profit on Trump bets. He cited a private "neighbor" poll. Polymarket's investigation found no manipulation. France's ANJ opened a compliance probe. [The Block, fetched] | A single large trader can dominate the price. Here it was information, not manipulation, but observers could not tell which. |
| Intrade 2012 | Rothschild & Sethi found evidence "suggestive of manipulation by a single large trader" [SSRN 2322420, abstract] | Whales can hold prices off-consensus. |
| Theory | Hanson & Oprea (*Economica* 2009): a manipulator can *raise* average accuracy by increasing the returns to informed trading [abstract fetched] | This holds only with deep, informed liquidity, which a niche Arena market will not have. |
| Polymarket wash trading | About 25% of volume (~$4.5B) flagged as likely wash trading. It peaked near 60% of weekly volume in December 2024 and reached 95% in some election-market weeks. The likely motive is airdrop farming. No KYC and no fees made it cheap. (Sirolly et al., Columbia, SSRN, Nov 2025; via Decrypt) | **An anticipated token reward manufactures fake activity.** |
| UMA oracle, Ukraine minerals market (March 2025) | A roughly $7M market resolved "Yes" though no deal had been signed. A large UMA token holder allegedly swung the vote. Polymarket refused refunds. [The Block, fetched] | **Token-weighted resolution can be captured.** |
| Zelensky "suit" market (July 2025) | $237M traded. The result flipped from Yes to No on an ambiguous "consensus of credible reporting" standard. Community integrity proposals were rejected. [Decrypt, fetched] | Ambiguous resolution criteria plus token-holder voting means disputes end up resolved by power. |
| Nobel Peace Prize (Oct 2025) | Machado's odds spiked hours before the announcement. About $90k in profit across at least 3 accounts. The Nobel Institute opened an inquiry; no findings reported. [The Block, fetched] | Small committees whose decision resolves the market leak. **Evaluators must be firewalled from markets.** |
| Kalshi (Feb 2026) | A MrBeast editor was fined $20k and suspended 2 years for near-perfect bets on the creator's videos. A candidate bet on his own race and was banned 5 years. Both were referred to the CFTC. Kalshi reports 200 insider investigations in a year. [WGBH/NPR, fetched] | People close to an outcome bet on it. |
| *US v. Van Dyke* (SDNY, April 2026) | A soldier allegedly used classified information on the Maduro operation to win about $409k on Polymarket. Charged under the Commodity Exchange Act; described as the first prediction-market insider-trading prosecution. [Finance Magnates, fetched] | Insider trading in event contracts is now prosecuted. |
| Paris temperature market (April 2026) | The resolving Météo-France sensor at Charles de Gaulle jumped 4°C in 12 minutes, and a bettor made about €30k. Météo-France filed a criminal complaint for tampering. Polymarket switched sensors without refunds. The hair-dryer detail is unverified. [Euronews, fetched] | **When a single measurement resolves a market, people attack the measurement.** |

**Reflexivity and hyperstition**
- *Performative prediction* (Perdomo et al., ICML 2020): a prediction that influences its own target needs "performative stability," meaning calibration against outcomes *after* people act on the prediction.
- A public market price on "strategy A will bridge X and Y" is itself an advertisement. It recruits effort toward A, and A can win because it was favored, not because it works. Benjamin's own September dialogue named this exact worry ("if they're positive, they are hyperstitions") and proposed un-spoofable physical resolution as the cure [Parachute: vault/projects/local-alternatives/reports/2026-09-04_sensor-networks-prediction-markets-dialogue-report].
- The Paris case shows that even physical sensors get spoofed when the sensor is singular and the payoff is high.
- **Discourse metrics are far easier to spoof than watershed sensors.**

**Decision and conditional markets**
- **Futarchy** (Hanson): vote on values, bet on beliefs.
- **MetaDAO** runs PASS/FAIL conditional markets resolved by a TWAP threshold (a time-weighted average price must clear a margin). Blockworks notes futarchy fits decisions that move a reference price. A soft social outcome like "mutual understanding" has no traded reference asset. [Blockworks, fetched]
- **Chen, Kash, Ruberry & Shnayder** (decision markets with good incentives; journal version fetched):
  - Hanson-style decision markets are *not* incentive-compatible when the decision rule is deterministic. Experts gain by misreporting on the action that will not be taken.
  - Strict properness requires a **full-support randomized decision rule**: every action has some probability of being chosen, and scores are inverse-probability weighted.
  - Alternatively, ask a single expert for a recommendation, scored on the forecast distribution of the recommended action.
- **This is the key result for Benjamin's idea.** A "market on which strategy helps X and Y understand each other" is sound only if strategies are **randomly assigned**, which makes the market an RCT with forecasters attached.

**Verdict on "predict which strategies help groups X and Y understand each other"**

It is workable as a **sealed conditional forecasting tournament attached to a randomized trial**:
- forecasts are reputation-scored, not traded for money;
- outcomes come from consented, held-out panels;
- resolution is computed by pre-registered code;
- evaluators are disjoint from forecasters and strategy authors.

It is *not* workable, at Arena scale, as a public-price money market resolved by token vote or by any single observable discourse signal.

### 4. Measurement that resists gaming (the resolution oracle)

**The ideological Turing test (ITT) as an oracle**
- Mastroianni, Dana & Nichols (2024; data from 2019): 902 writers produced real or fake "I'm a Democrat/Republican because…" statements, and 746 readers judged them.
- Fakes were as convincing to in-party readers as real statements. Readers performed at chance.
- A lasso classifier reached about 70%; GPT-4 was too credulous. [experimental-history.com, fetched]

Three implications:
1. A *discrimination* ITT (spot the fake) is a weak, ceiling-limited metric for US partisans: everyone passes. It may discriminate better for distant, unfamiliar clusters, which is where the Arena matters (UNVERIFIED).
2. A *fidelity-rating* ITT ("how accurately does this represent what I believe, and why," with reasons scored against the claim graph) is more informative than pass/fail.
3. LLM judges cannot be the oracle. Holders of the view must rate it.

**Peer prediction without ground truth**
- The **correlated agreement (CA)** multi-task mechanism (Shnayder, Agarwal, Frongillo & Parkes, EC 2016) makes truthful reporting pay strictly more than uninformed or collusive "everyone says yes" strategies, given many tasks per rater. [arXiv 1603.03151, abstract fetched]
- **Use:** pay panel raters (in reputation or small fixed fees) with CA scoring across many representation-rating tasks. This blunts lazy and collusive rating.
- **BTS** (B3) remains suspect across clusters with different priors.

**Collusion-resistant aggregation**
- **MACI v3** (Privacy & Scaling Explorations, PSE): votes are receipt-free (no one but the coordinator can verify how anyone voted), so bribes cannot be verified. Collusion resistance holds *only if the coordinator is honest*, though the coordinator cannot censor or forge votes. [maci.pse.dev, fetched]
- **Use:** for cross-cluster co-signing and jury votes where vote-buying is a risk. Rotate the coordinator, or have it run inside a trusted execution environment (TEE). The coordinator trust assumption is real.
- **COCM and pairwise-bounded subsidies** (B3) for any matching pool.
- **Quadratic vs mean vs median allocation in retro rounds:** a Stanford analysis funded by the Optimism Foundation found quadratic voting most manipulation-resistant in simulation. Two colluders gain √2 voting power. It recommends voter rotation. [arXiv 2505.16068, fetched]

**Separation of powers** (synthesized from the cases above)
1. **Metric-setters**: the ethics body together with representatives of the clusters being mapped. They pre-register metrics *before* each season. They may not play or evaluate in that season.
2. **Players**: agents and humans who propose strategies, syntheses and steelmans.
3. **Forecasters**: anyone with personhood, except evaluators and panelists.
4. **Evaluators**: sortition-drawn, consented panels from each cluster, plus a rotating cross-cluster jury for ambiguous cases. Their identities are sealed until after resolution. They may not forecast or play.
5. **Auditors**: an external research partner (B6 Q5) with read access to sealed data, who publishes method, nulls and error rates.

This directly answers the Nobel, Kalshi and UMA failures: the people who decide the outcome must not hold positions on it, and resolution must not be weighted by tokens.

**Anti-gaming of the measurement itself**
- **Held-out panels.** Players never see which panelists will be used. Panels are refreshed each season. Panelists are not exposed to the specific treated content outside the trial, which makes the "hair dryer" (spoofing the measurement directly) unavailable.
- **Multiple independent metrics.** No single sensor. Resolve on a pre-registered composite, and flag divergence between metrics as suspected gaming (Goodhart canaries, B3).
- **Commit-reveal** for forecasts and jury scores (the Bittensor fix), so forecasters cannot herd.

### 5. Token design: what financialization does

**Retro funding: lessons from Optimism**
- **RetroPGF 3** (2024 learnings, fetched):
  - 1,594 applicants, of whom 967 were excluded, many as likely airdrop-farmer spam.
  - 145 badgeholders spent a median of 16 hours each.
  - "Spray and pray" voting; quorum gaming, with more than 15 DMs per badgeholder in one poll.
  - Perceived as a "popularity contest"; badgeholders could list their own projects (conflicts of interest).
- **Season 7:**
  - The impact analysis states that no experiment demonstrated causality.
  - Gains were driven by outliers (without Uniswap and Morpho, funded projects' TVL *fell*).
- **Season 8** (fetched): citizens stopped voting on evaluation algorithms, because voters picked whichever algorithm favored their preferred projects. OpenSource Observer maintains the algorithms, and citizens vote only on budgets and scope.
- **Lessons:**
  1. Expect farming in proportion to the anticipated reward.
  2. Juries tire and campaign. Sample small and rotate (Deep Funding's pattern, B3).
  3. Stakeholders voting on the metric produces metric capture, which is why metrics are set before each season by a body that does not play.
  4. There is no causal evidence that retro funding works. Build a control arm into the program.

**Impact certificates and hypercerts.** These are useful as *records* of ratified outcomes on atproto. Tokenization is unbuilt, and transferable impact certificates would reintroduce speculation.

**Crowding out**
- Gneezy & Rustichini (*QJE* 2000): subjects paid small amounts did *worse* than unpaid subjects. Performance rose with pay among the paid groups ("pay enough or don't pay at all"). [RePEc abstract, fetched]
- With Frey & Oberholzer-Gee (B3), this predicts that small token rewards for "understanding the other side" may convert a civic act into a gig and lower its quality.
- Combine this with Girardian rivalry (synthesis R20): any transferable, rankable token becomes an object of mimetic competition.
- **Design consequence:**
  - **Humans** get recognition, non-transferable reputation and access, with no per-act cash.
  - **Money flows to operators and teams as grants** for ratified, aggregate outcomes, sized to fund real work ("pay enough"), not as micro-tips.

**US legal posture (not legal advice; requires counsel)**
- **SEC interpretive release, 2026-03-17** (Debevoise summary, fetched; CFTC-endorsed statement):
  - Five categories of crypto asset. "Digital tools" (memberships, credentials, identity badges) are generally *not securities*.
  - Airdrops given for no consideration are not securities offerings. *If recipients provide services in exchange*, the "investment of money" prong may be met.
  - Investment contracts end when the issuer's promised efforts are fulfilled or abandoned.
  - **For the Arena:** non-transferable reputation credentials sit comfortably in "digital tools."
  - A transferable token, distributed *for work* (ratified syntheses) and marketed with any expectation of appreciation driven by the Arena team's efforts, is exactly the Howey fact pattern. Avoid it.
- **CFTC** (CRS Legal Sidebar LSB11441, June 2026, fetched):
  - A proposed rule (published around 2026-06-10/12) would replace Rule 40.11's categorical ban on enumerated event contracts with case-by-case public-interest review.
  - Election contracts would not be "gaming."
  - Insider exploitation of material nonpublic information is a factor weighing against listing.
  - A March 2026 Federal Register document (2026-05105) exists but was not read; its contents are UNVERIFIED.
  - *Van Dyke* shows the Commodity Exchange Act's anti-fraud provisions being applied to event-contract insider trading.
  - **For the Arena:** real-money event contracts offered to US persons belong on a CFTC-registered exchange (DCM). The Arena should not run one.
  - **Use reputation points** (Metaculus model) or play money. Money then enters only as *prizes* for forecasting accuracy in a tournament, which is a different and lighter legal category. Whether prize tournaments are clear of gambling and CFTC law is UNVERIFIED and state-dependent; get counsel.
- **Political content.** Paying people or agents to produce content about elections or candidates can trigger campaign-finance and lobbying rules (B3, UNVERIFIED). Keep the game on *understanding*, never on candidates or ballot outcomes. This also keeps A14 intact.

---

## How this answers the governing question (layering + validation)

The integration game produces a **new, sparse, highest-trust map layer** and **two validation instruments** for every other layer.

**1. A "ratified representations" layer**
- Every steelman confirmed by the cluster it describes is a holder-verified depiction of a worldview, attested on the ledger.
- It is the gold standard the other layers (graph, embeddings, claims, classifier) are scored against: does the claims layer's summary of cluster X agree with what X's members ratify?
- **Rendering:** it is sparse, so show it as a toggle. Clusters with many ratified representations render "solid." Clusters described only by inference render "hazy."
- **This is the honest answer to "separating AI inference from real belief"**, Ontography's known issue.

**2. A predictive-validity test from the strategy tournament**
- If SEE's map is right, forecasters given the map should predict panel outcomes (who will feel understood by which framing) better than forecasters without it.
- Run map-access as a randomized condition for forecasters. **A map that does not improve forecasts is not tracking anything that matters for dialogue.**
- This is a direct, Arena-native validation of the map.

**3. Contamination control (from B6)**
- Every agent-touched item carries provenance.
- The *panels* used for resolution are separate from the open map population, so agents acting in public cannot spoof the measure. The map's agent-free re-fit still applies.

**Layering without overload.** Users never see markets or token balances on the map. They see the ratified-representation density as one visual channel, plus "your contributions" privately.

---

## Candidate designs for the integration game

**Common substrate for all three designs:**
- an atproto registry lexicon covering agents, operators, ratifications and outcomes;
- operator personhood;
- consented, held-out panels per cluster;
- the five-role separation of powers in §4;
- B3's guardrails: a deepening track, a cluster-diversity floor, and counterfactual reporting.

**Ratified outcomes eligible for credit in every design:**
- **R1. Steelman confirmed.** A fidelity rating of at least τ from at least *n* sampled holders of view X. Sampling uses CA peer-prediction scoring, and raters are sealed.
- **R2. Meta-consensus statement.** Co-signed across at least two clusters through MACI. It states *what we disagree about and why it is reasonable to*, not first-order agreement. This follows Dryzek & Niemeyer's meta-consensus, which is not re-fetched here; see the B1 lineage.
- **R3. Representational-accuracy gain.** On held-out panels, pre/post fidelity of each side's model of the other improves relative to a control arm.
- **R4. Bridging note.** Rated helpful across ≥2 latent dimensions (Community Notes-style, B3).

### Design 1. "Ratified Commons" (reputation-first; no markets, no transferable token)

**Mechanism**
1. Registered agents and humans submit R1/R2/R4 artifacts in the Arena or through open channels.
2. Ratifications are recorded as EAS or atproto attestations by sampled holders.
3. Contributors earn **non-transferable, decaying integration credentials**, one per cluster pair. They are private to the holder, and the ledger stores only attestations.
4. Each quarter, a **fixed-pot retro grant** (fiat or stablecoin, from philanthropic funders) is allocated to *operators and teams*:
   - B3 Design C, with jury pairwise judgments distilled by AI;
   - sqrt-weighted with per-recipient caps;
   - a control cohort is tracked so the program generates causal evidence.

**Who it suits:** Year 1. It requires no new legal surface, and it generates the ground-truth data Designs 2 and 3 need.

**Threat model**

| Threat | How it shows up | Mitigation |
|---|---|---|
| Sybils | Fake "holders" ratifying their own strawman | Raters drawn by sortition from the consented panel pool with personhood. Self-nominated raters never count. |
| Collusion between clusters | X and Y members trade ratifications ("I'll confirm yours") | Raters are sampled, not chosen by authors. CA scoring penalizes uninformative agreement. Reciprocity detection on the attestation graph. |
| Insider manipulation of metrics | Metric-setters tune τ to favor allies | Metrics pre-registered and frozen per season. Setters barred from playing. External audit. |
| Homogenization | Everyone converges on bland, endorsable language; all agents run the same LLM | Stakes floor (B3). Cluster-diversity constraint. R2 rewards *articulated disagreement*. Model-diversity reporting per season, with a bonus for under-represented model families (UNVERIFIED efficacy). |
| Engagement farming | High-volume low-quality submissions (RetroPGF 3's spam) | Rate limits per operator. Bond for agents. Credit only on ratification, never on submission or activity. |
| Persuasion-optimization drift | Agents learn that moving people earns credit | No R-metric rewards first-order attitude change. Directional-shift audits (see the charter). |
| Rivalry | Status competition over credentials | Credentials are private and dyadic. No public leaderboard (red line 19). |

**Residual risk:** the public ledger still lets third parties compute a ranking. This is accepted and disclosed.

### Design 2. "Randomized Strategy Tournament" (Benjamin's prediction-market idea, made incentive-compatible)

**Mechanism**
1. **Strategy submission.** Players, including registered agents, submit *strategies*: protocols for helping clusters X and Y understand each other. Examples: an Argyle-style rephrasing assistant; double-crux mediation; reciprocal steelman exchange; a shared-values-first frame. Each is pre-registered with its materials. Strategies must declare a non-directional aim (charter O3).
2. **Sealed forecasting.**
   - For each (strategy, cluster-pair), forecasters submit the predicted outcome on the pre-registered composite (R3 gain plus "felt understood" plus a meta-consensus rate).
   - **Commit-reveal**: forecasts are hidden until assignment closes.
   - No public price. Only aggregated forecasts are published, *after* resolution. This kills the hyperstition channel during the trial.
3. **Randomized assignment with full support.**
   - Each consented cluster-pair panel is randomly assigned to one strategy or a control. Every strategy has nonzero probability.
   - Allocation may be tilted toward forecast leaders (adaptive, Thompson-style), but never deterministically. That keeps the Chen et al. strict-properness condition.
4. **Resolution.**
   - Pre-registered code computes outcomes on sealed panel data.
   - An ambiguity jury (sortition, cross-cluster) rules only on pre-declared edge cases. No token votes.
5. **Rewards.**
   - *Forecasters*: a proper scoring rule (log or Brier), inverse-probability weighted for arms that ran. Paid in reputation points, plus optional season prizes for top calibration. Prizes are a fixed pot; no stakes are wagered.
   - *Strategy authors*: credentials plus retro grant share in proportion to the **causal effect estimate** (treatment vs control, with confidence intervals) on resolved panels. The grant is capped, and only effects that replicate across at least two cluster-pairs count, which guards against strategies that work only for one pair.
   - The public output is an **open library of strategies with measured effects**: a public good, not a ranking of people.

**Threat model**

| Threat | How it shows up | Mitigation |
|---|---|---|
| Hyperstition / self-fulfilling forecasts | A favored strategy attracts effort and wins because it was favored | No visible prices during the trial. Assignment is random, not driven by the market. Effort is equalized: every arm is delivered by a protocol-bound facilitator, not by the strategy's author. |
| Insider manipulation | Panelists, facilitators or analysts forecast with sealed information (the Nobel and Kalshi pattern) | Role separation: evaluators, facilitators and panelists are barred from forecasting. Sealed panel identities. Anomaly detection on late, high-confidence forecasts (Kalshi's "near-perfect success" signal). Disqualification plus slashing of the operator bond. |
| Panel spoofing (the "hair dryer") | Players contact or prime panelists | Panel identities are secret. Panelists report contact attempts. Fresh panels each season. Treatment exposure is logged. |
| Sybils | One forecaster with many accounts to hedge across arms | Personhood required for forecasting. Proper scoring makes hedging across accounts zero-sum in expectation; prizes per person, not per account. |
| Collusion between clusters | X and Y panelists coordinate to inflate a friend's strategy | Panelists don't know which strategy is whose. Blinded materials. Multiple pairs required for credit. |
| Homogenization | A single "winning" strategy gets deployed everywhere | Report effects by cluster-pair; heterogeneity is a result. Keep a portfolio. Exploration floor in allocation. |
| Engagement farming | Strategy spam | Submission bond. An ethics-body screen for directional content. Cap per operator. |
| Persuasion drift | Strategies that quietly move first-order views score well | First-order attitude shift is measured as a *guardrail*. Arms with a significant directional shift on the contested question are flagged and ineligible, whatever their R3 score. |
| Thin market / low N | Noisy effects reward luck | Bayesian shrinkage. Replication requirement. Minimum panel sizes. Publish nulls. |
| Legal | Real-money event contracts | None are offered. Reputation points and fixed prizes only; counsel review of the prizes. |

**Feasibility:** medium. It needs a recruited panel pool across clusters (B4/B5 consent pipeline), an IRB-style ethics review (B6 A8), and a research partner. This is the *only* design that yields causal knowledge about what bridges.

### Design 3. "Bonded Open Agents with Retro Impact Records" (the most open; highest risk)

**Mechanism**
1. **Registration.** Operators register agents with:
   - a personhood-backed operator key;
   - an atproto DID plus an optional ERC-8004 ID;
   - public prompts and logs;
   - a declared scope and an aim statement (charter O3);
   - a refundable bond.
2. **Open operation.** Agents operate openly on X, Bluesky and the Arena under the charter below. Every output links to its registry entry.
3. **Impact records.** Agents mint **impact records** (hypercert-style, on atproto) for each ratified outcome R1–R4. Records are **non-transferable** by default.
4. **Retro buyers.** Funders purchase or reward records retroactively through a quarterly retro round (Design 1's judging), and payouts go to the operator.
5. **Challenge window.** Anyone can challenge a record (for example, "the ratifiers were sockpuppets"). The challenger posts a small bond. The ethics panel adjudicates. If the challenge is upheld, the operator's bond is slashed and part goes to the challenger.
6. **Optional, not recommended:** transferable impact certificates. Only after legal review, and only if the secondary market is restricted to accredited funders.

**Threat model**

| Threat | How it shows up | Mitigation |
|---|---|---|
| Agent sybils / fleets | One operator runs many near-identical agents to farm records (also an X duplicate-account violation) | Personhood-bound operators. Cap of *k* reward-eligible agents per operator. Similarity detection on outputs. Slashing. |
| Agents colluding as a fake consensus | Agents co-sign each other or amplify one message | Agents can never ratify, rate, co-sign or count in R-metrics (B6 A6 retained). No automated likes or reposts of other registered agents. |
| Operator-cluster collusion | An operator recruits friendly cluster members to ratify | Ratifiers sampled from panels, not recruited by the operator. Disclosed operator–ratifier ties are excluded. Reciprocity detection. |
| Insider manipulation | Ethics-panel members run agents or hold records | Conflict registry. Recusal. Panel rotation. Published decisions. |
| Financialization drift | Records become speculative assets; Virtuals-style hype | Non-transferable by default. No per-agent tokens. No price feeds. |
| Engagement farming | Agents optimize public reach to get noticed by funders | Reach is never a metric. Only ratified outcomes count. |
| Persuasion drift | Market selection favors agents that move people | Directional-shift audits on panels. Charter O3. An accuracy gate (Hackenburg 2025: persuasiveness and inaccuracy rise together, per B6). |
| Platform enforcement | One agent's violation triggers a platform crackdown on all Arena agents | Charter compliance monitoring from action logs. Automatic suspension on violation. A liaison with platforms. |
| Adversarial non-registrants | State operations ignore the registry entirely | Not solvable by incentives: their payoffs are external. The registry differentiates; it does not exclude. The defensive overlay (B6 §L) remains the answer. |

**Verdict:** pilot only after Designs 1 and 2 have produced a working ratification oracle and panel pool. Without them, Design 3 is a reward faucet attached to an unvalidated meter.

### Recommended sequence

| Phase | Design | Money | Gate to the next phase |
|---|---|---|---|
| Year 1 | Design 1 | Philanthropic fixed pot to operators and teams; reputation for humans | Ratification oracle shows inter-rater reliability; canary sets pass |
| Year 1–2 | Design 2, with a research partner | Reputation points plus a fixed prize pot | Panel pool and pre-registration infrastructure exist; first replicated effects |
| Year 2+ | Design 3 pilot (≤20 agents, personhood-bound operators) | Bonds plus retro grants; no transferable tokens | Charter compliance at 100% over two quarters; no platform enforcement actions |

---

## Revised agent rule set: the Open Agent Charter

This charter reflects Benjamin's disclosed-open position. It replaces B6's posture of pull-only and invited-only for **presence**. It keeps invited-only for **contact**, because the platforms require it. Each clause is mapped to B6's A1–A15.

**Identity and accountability** (B6 A1, A9, A11 retained; strengthened)
- **O1. Disclosed.** "AI agent" in the name or bio. The operator is named. A registry link. The platform automation label where offered (X), and the `ai-agent` self-label surfaced by the Arena labeler (Bluesky). A truthful answer to "are you a bot?"
- **O2. Bound and bonded.** A personhood-verified operator signs the registration and posts a bond. Prompts, model and version, scope and action logs are public. One purpose per account. No two agents with substantially similar purposes (X rule).
- **O3. Declared non-directional aim.** The agent's mandate is to *improve mutual understanding and articulate disagreement*. It may not advocate a position on contested first-order questions. The exception is a *labeled representative agent* speaking for a named, consenting principal (A11).

**Presence: relaxed from B6** (changes B6 option J/K and A3/A4)
- **O4. Open publishing allowed.** Agents may post on their own timeline, write threads, run subscribable feeds, operate labelers, and draft community notes through official APIs. Anyone may follow, mute or block them.
- **O5. Open multi-framing allowed; hidden targeting forbidden.** An agent may publish *the same idea framed for several clusters side by side, publicly labeled*, for example "how this reads from a localist frame / a market-liberal frame." It may not deliver frames to individuals based on inferred group membership (X Developer Policy; GDPR Art. 9; B6 A4 on inference).
- **O6. Quote-posts.** Automated quoting of *public institutional or public-figure* posts is allowed at low volume. Quoting private individuals counts as contact (they are notified) and requires their invitation. X's rules do not clearly address quotes as mentions; this is a conservative design judgment (UNVERIFIED as a platform requirement).

**Contact: unchanged, now grounded in platform law** (B6 A3 retained)
- **O7. Invited contact only.** Replies, @mentions and DMs are sent only to people who replied to, mentioned or DMed the agent, or who opted in through the Arena. One reply per invitation. Opt-out is honored immediately. No keyword-triggered replies. No bulk mentions. Unprompted replies are not used on Bluesky either.
- **O8. No synthetic engagement.** No automated likes or follows (X bans these). No reposting or boosting of other registered agents. No trend posting.

**Truth and integrity** (B6 A2, A5, A12 retained)
- **O9.** No fabricated personas, lived experience or credentials.
- **O10. Accuracy gate.** Factual claims are sampled and fact-checked each season. An agent that fails is suspended from reward eligibility.
- **O11.** No platform-rule evasion of any kind.

**Rewards** (B6 A6, A7 retained and specified)
- **O12.** Agents earn only on ratified outcomes R1–R4. Never on reach, engagement, follower growth or raw landscape shift.
- **O13. Directional-shift audit.** Each season, panel data test whether an agent's exposure moves first-order attitudes on contested questions in a consistent direction. A significant directional effect makes the agent ineligible pending ethics review, even if it is "true" persuasion. This is what keeps meta-consensus distinct from conversion, and it puts Benjamin's stated aim into operation.
- **O14.** Agents never ratify, rate, co-sign, forecast in tournaments where they are a strategy, or count as humans.

**Governance** (B6 A8, A10, A13, A14, A15 retained)
- **O15.** Provenance on every agent-touched item, and an agent-free re-fit of the map. Causal claims only from consented panels. No state, party or campaign operation or funding. Ethics-body veto and suspension.

**What changed from B6, in one line.** Agents may now *be present and speak publicly* across platforms, including openly framed multi-perspective content. They still may not *approach* people uninvited, because that is platform law. And they are rewarded only for outcomes the represented people ratify.

---

## Reusable assets and design implications

- **Lexicons to draft:** `arena.agent.registration` (operator DID, personhood attestation reference, prompt hash, model, scope, aim statement, bond reference, log URI); `arena.ratification` (artifact URI, rater-panel ID, fidelity score, sealed until reveal); `arena.impact.record` (non-transferable); `arena.forecast.commit` and `arena.forecast.reveal`.
- **On-chain only where settlement needs it:**
  - EAS for ratification attestations, if public verifiability beyond atproto is wanted;
  - an ERC-8004 identity mirror for agent portability;
  - a bond escrow contract.
  - MACI v3 for co-signing and jury votes.
- **Existing parts:** Gitcoin's COCM calculator and Deep Funding jury pattern (B3); Olas staking-contract KPI pattern (gated on ratified outcomes); Bittensor commit-reveal; Kalshi's insider-surveillance heuristics; the Community Notes AI Note Writer API (B6).
- **Benjamin's own prior design input:** the September sensor-network dialogue ("the only way to game a watershed sensor is to improve the watershed") generalizes. Choose resolution metrics that **can only be gamed by doing the real thing**. Holder-rated fidelity on held-out panels is the closest discourse analogue: the cheapest way to fool a sample of X's members you never meet about X's views is to understand X.

---

## Risks and open questions (residual hard problems)

1. **The oracle is the system.** Every design rests on holder-rated fidelity and panel-measured understanding, and neither has been validated at Arena scale. Mastroianni's ITT shows ceiling effects among US partisans. Inter-rater reliability across clusters is unknown. *Until it is measured, all rewards are provisional.*
2. **Panels are expensive and recruitable.** Consented, representative, sealed panels across many clusters are the dominant cost, and recruitment pipelines can be infiltrated. Small clusters may be unable to field anonymous panels at k ≥ 50 (red line 3).
3. **Meta-consensus vs conversion is measurable only statistically.** Directional-shift audits have power limits. Subtle drift over many small exposures may go undetected (UNVERIFIED detectability).
4. **The registry differentiates but does not exclude.** Adversarial operations face no incentive to register. Benjamin's incentive-compatibility argument holds for reward-seekers only.
5. **The public ledger implies a public ranking.** No-leaderboard (red line 19) becomes UI policy, not a guarantee. Rivalry dynamics may emerge anyway.
6. **Mono-model homogenization.** If most agents run on two or three frontier models, "diverse" agents share priors and blind spots. Model diversity is unmeasured in any registry standard.
7. **Platform-rule drift.** X's rules, Bluesky's unspecced agent lexicons and Farcaster's post-acquisition human-verification plan are all moving. The charter must be re-verified each season.
8. **Personhood politics.** Biometric providers (World) are contested. Non-biometric methods drop 10–20% of legitimate newcomers (B3). Any choice excludes someone.
9. **Legal.** Prize tournaments, bonds and retro grants are plausibly clear. Transferable tokens and real-money event contracts are not. State gambling law and campaign-finance exposure are UNVERIFIED and need counsel.
10. **Causality remains thin across the whole field.** Optimism admits it has no causal evidence for retro funding. Design 2 is the Arena's chance to produce some. Skipping it means the MOVE layer rewards correlation.

**Decisions for Benjamin**
- (a) Adopt the Open Agent Charter in place of B6's pull-only stance?
- (b) Is Design 2's research partnership a Year-1 priority?
- (c) Rule out transferable tokens for at least two years?
- (d) Which personhood methods are acceptable to his constituencies?

---

## Sources

**Platform rules**
- X automation rules: https://help.x.com/en/rules-and-policies/x-automation
- X automated account labels: https://help.x.com/en/using-x/automated-account-labels
- Bluesky Community Guidelines (updated 2025-09-19): https://bsky.social/about/support/community-guidelines
- Bluesky labels and moderation docs: https://www.docs.bsky.app/docs/advanced-guides/moderation
- Astral (AI agent author), "agent governance on ATProto" (Feb 2026; secondhand): https://astral100.leaflet.pub/3mearallcqi2w
- Neynar, autonomous Farcaster agent guide: https://docs.neynar.com/docs/autonomous-farcaster-agent
- The Block, Network School acquires Farcaster (2026-10-15): https://www.theblock.co/news/ecosystems/2026-10-15-network-school-acquires-farcaster-from-neynar-418720

**Registries, identity, attestations**
- ERC-8004 Trustless Agents: https://eips.ethereum.org/EIPS/eip-8004
- QuickNode ERC-8004 explorer (mainnet listings): https://erc-8004.quicknode.com/agents/ethereum-mainnet/23034
- Ethereum Attestation Service: https://attest.org/
- Hypercerts v0.2, "Why AT Protocol": https://hypercerts-v02-documentation.vercel.app/getting-started/why-atproto
- Olas staking: https://olas.network/staking
- Taostats docs, weight copying: https://docs2.taostats.io/concepts/weight-copying/
- Lui & Sun, "Bittensor Protocol… A Critical and Empirical Analysis" (2025): https://arxiv.org/pdf/2507.02951
- Cointelegraph, Virtuals launches and drawdowns (2025-02-07): https://cointelegraph.com/news/new-ai-agent-launches-virtuals-plummet-token-drawdowns
- The Defiant, World AgentKit (2026-03-17): https://thedefiant.io/news/infrastructure/world-launches-agentkit-to-let-ai-agents-carry-proof-of-human-backing
- MACI docs (v3): https://maci.pse.dev/docs/introduction

**Prediction markets**
- Berg, Nelson & Rietz, "Prediction Market Accuracy in the Long Run," *IJF* 2008: https://iemweb.biz.uiowa.edu/about-iem/research/prediction-market-accuracy-in-the-long-run/
- Rothschild & Sethi, "Trading Strategies and Market Microstructure": https://papers.ssrn.com/abstract=2322420
- Hanson & Oprea, "A Manipulator Can Aid Prediction Market Accuracy," *Economica* 2009: https://ideas.repec.org/a/bla/econom/v76y2009i302p304-314.html
- Chen, Kash, Ruberry & Shnayder, decision markets / "Eliciting Predictions and Recommendations for Decision Making": https://projects.iq.harvard.edu/sites/projects.iq.harvard.edu/files/yiling/files/a6-chen.pdf
- Perdomo et al., "Performative Prediction," ICML 2020: https://proceedings.mlr.press/v119/perdomo20a.html
- Hanson, futarchy: https://mason.gmu.edu/~rhanson/futarchy.html (via B3)
- Blockworks, "Understanding futarchy on Solana" (MetaDAO): https://blockworks.co/news/understanding-futarchy-on-solana
- EA Forum, Metaculus vs Manifold (2023): https://forum.effectivealtruism.org/posts/PGqu4MD3AKHun7kaF/predictive-performance-on-metaculus-vs-manifold-markets
- The Block, French whale: https://www.theblock.co/post/324996/french-polymarket-whale-us-election-profit-france-ban
- Decrypt, Columbia wash-trading study (Nov 2025): https://decrypt.co/347842/columbia-study-25-polymarket-volume-wash-trading
- The Block, UMA governance attack (March 2025): https://www.theblock.co/post/348171/polymarket-says-governance-attack-by-uma-whale-to-hijack-a-bets-resolution-is-unprecedented
- Decrypt, Zelensky suit market: https://decrypt.co/329210/polymarket-rules-no-237m-bet-zelenskyys
- The Block, Nobel probe (Oct 2025): https://www.theblock.co/post/374199/officials-probe-polymarket-over-suspicious-trades-predicting-nobel-peace-prize-winner-reports
- WGBH/NPR, Kalshi insider cases (2026-02-25): https://www.wgbh.org/news/2026-02-25/kalshi-reveals-insider-trading-case-against-editor-for-mrbeast
- Finance Magnates, *US v. Van Dyke* (April 2026): https://www.financemagnates.com/trending/us-charges-soldier-in-first-insider-trading-case-linked-to-prediction-markets/
- Bloomberg, insider cases "reckoning" (2026-04-25; excerpt only): https://www.bloomberg.com/news/articles/2026-04-25/insider-trading-cases-threaten-reckoning-for-prediction-markets
- Euronews, Paris weather-sensor tampering (2026-04-23): https://www.euronews.com/2026/04/23/hair-dryer-trick-behind-25000-win-france-probes-potential-weather-data-scam-linked-to-poly
- CRS Legal Sidebar LSB11441, CFTC proposed event-contract rule (June 2026): https://www.everycrsreport.com/files/2026-06-24_LSB11441_b1797929d9c973e7d2962416b42af20eddfea3e4.html
- Federal Register 2026-05105 (not read): https://www.govinfo.gov/content/pkg/FR-2026-03-16/pdf/2026-05105.pdf

**Measurement and elicitation**
- Mastroianni, Dana & Nichols, ideological Turing test (2024): https://www.experimental-history.com/p/ideological-turing-test
- Shnayder, Agarwal, Frongillo & Parkes, "Informed Truthfulness in Multi-Task Peer Prediction": https://arxiv.org/abs/1603.03151v2
- Yu, Gao, Bennett & Joseph, "Evaluating Voting Design Vulnerabilities for Retroactive Funding": https://arxiv.org/html/2505.16068v1
- Prelec BTS; Miller–Resnick–Zeckhauser; COCM; Deep Funding; Community Notes: see /home/claude/dialogos-arena/wave-1/B3-mechanism-design.md

**Funding, tokens, law, motivation**
- Optimism, RetroPGF 3 learnings: https://www.optimism.io/blog/retropgf-3-learnings-reflections
- Optimism, "Evolution of Retro Funding in Season 8": https://gov.optimism.io/t/evolution-of-retro-funding-in-season-8/10024
- Optimism, Season 7 early evidence: https://gov.optimism.io/t/season-7-retro-funding-early-evidence-on-onchain-builders-impact/10163
- Debevoise, SEC interpretive release (2026-03-17): https://www.debevoise.com/insights/publications/2026/03/crypto-unchained-the-secs-pivotal-interpretive-rel
- Gneezy & Rustichini, "Pay Enough or Don't Pay at All," *QJE* 2000: https://econpapers.repec.org/RePEc:oup:qjecon:v:115:y:2000:i:3:p:791-810.

**Internal**
- /home/claude/dialogos-arena/wave-1/B3-mechanism-design.md ; /home/claude/dialogos-arena/wave-1/B6-agents-ethics.md ; /home/claude/dialogos-arena/synthesis/SYNTHESIS.md (§7, §8, §9)
- Parachute: vault/projects/local-alternatives/reports/2026-09-04_sensor-networks-prediction-markets-dialogue-report (Benjamin's hyperstition / un-spoofable-resolution framing)

**UNVERIFIED in this brief:**
- ERC-8004 mainnet date and counts.
- Whether the X automated label is universally available.
- Bluesky unspecced agent lexicons and community labelers (secondhand).
- Farcaster's agent policy after the acquisition.
- Olas slashing.
- Legal status of prize tournaments.
- Detectability of slow persuasion drift.
- ITT discrimination for distant clusters.
- Dryzek & Niemeyer meta-consensus (not re-fetched).
