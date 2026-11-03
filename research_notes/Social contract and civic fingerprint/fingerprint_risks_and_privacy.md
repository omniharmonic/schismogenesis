# Risks of holding civic or ideological fingerprints, and privacy-preserving designs (as of November 2026)

**Status of these notes.** This is research, not legal advice. Items marked **[LEGAL REVIEW]** need a lawyer before anyone relies on them.

**Scope.** This file adds to `docs/research/B5-platform-data-ethics.md` and `docs/research/B6-agents-ethics.md` and does not repeat them. Those files already cover GDPR Art. 9 case law, the EU political-ad regulation (TTPA), scraping law, the basic Cambridge Analytica lesson, and agent red lines A1–A15.

**Evidence limits.**
- The session's web search budget ran out partway through. The last searches (China, Tea, 23andMe) did not run, and some later gaps were filled only by direct fetches of known URLs.
- Many law firm and vendor pages reached me only through search summaries, so I treat them as secondary. The items read directly from statute or primary text are Minnesota, Texas (2023 enrolled bill), Virginia, the California AG FAQ, GDPR Arts. 3 and 27, the Common Rule, and AI Act Art. 5 and Annex III.
- The numbered tests below were run for this memo on public data. They are illustrative and not peer-reviewed.

---

## Precedent harm: what has gone wrong with political-profile data

### Takeaway
I found no documented breach of a political quiz or survey site. The harm record comes from neighbouring cases: quiz data reused for targeting, modelled voter files left exposed, donor lists mapped for harassment, leaky trackers on voting-advice tools, and small "safe space" apps breached. The closest live threat in the US in 2026 is legal compulsion, not hackers: government demands to unmask critics.

### Cited Findings

**Quiz-to-targeting**
- Kogan's personality app "thisisyourdigitallife" captured around 87 million profiles, licensed to Cambridge Analytica under an agreement dated 4 June 2014; the estimate rose from about 50 million — [Medium summary of ICO investigation](https://medium.com/lawyers-lunchbox/information-commissioners-office-investigates-cambridge-analytica-6d8a9ad4146e) (secondary).
- The FTC found app users were falsely told it would not collect names or identifiable information, when it collected Facebook User IDs. The order requires deleting the information collected — [FTC](https://www.ftc.gov/news-events/news/press-releases/2019/12/ftc-issues-opinion-order-against-cambridge-analytica-deceiving-consumers-about-collection-facebook).
- Facial analysis study: Kosinski (2021) used 1,085,795 people. A database summary gives 68% average out-of-sample accuracy for political orientation, 69% after controls, versus 66% for a five-factor personality test — [DOAJ](https://doaj.org/article/e21ee1866fda470b95ee95b9e2fb0d67). Press coverage says 72% — [PsyPost](https://www.psypost.org/2021/03/facial-recognition-technology-can-predict-a-persons-political-orientation-with-72-accuracy-59888). These figures conflict; check the [paper](https://link.springer.com/content/pdf/10.1038/s41598-020-79310-1.pdf). Method critics exist — [The Debrief](https://thedebrief.org/disturbing-study-says-facial-recognition-can-determine-political-affiliation/).

**Voting-advice tools (VAAs)**
- In a study of 11 Finnish VAAs from the 2023 parliamentary election, 7 leaked sensitive information about users' political opinions to third parties — [Springer, "Leaky Democracy"](https://link.springer.com/chapter/10.1007/978-981-97-1313-4_30) (abstract via search; full text blocked).

**Voter-file brokers**
- The L2 database (2015) exposed addresses, names, political preferences and issue opinions such as gun control, likely through a misconfiguration — [FedScoop](https://fedscoop.com/exposed-u-s-voter-database-poses-extreme-danger-researcher-says/).
- An RNC contractor (2016–17) exposed data on nearly 200 million potential voters, with modelled positions on 46 issues — [UpGuard](https://www.upguard.com/breaches/the-rnc-files); [The Hill](https://thehill.com/policy/cybersecurity/338383-data-on-198-million-us-voters-left-exposed-to-the-internet-by-rnc-data/).

**Political ad targeting**
- Meta stopped political, electoral and social-issue ads in the EU from October 2025, blaming the TTPA's rules and uncertainty — [Meta](https://about.fb.com/news/2025/07/ending-political-electoral-and-social-issue-advertising-in-the-eu/).

**Donor lists and doxxing**
- Eightmaps placed California Prop 8 donor names on a Google map — [Next City](https://nextcity.org/daily/entry/mapping-proposition-8). Reported harm ranged from angry emails to death threats, as described by an advocacy source — [Heritage](https://www.heritage.org/marriage-and-family/report/the-price-prop-8).
- *Americans for Prosperity v. Bonta* (2021, 6–3) struck down California's donor-disclosure rule on associational grounds — [Campaign Legal Center](https://campaignlegal.org/index%2Ephp/cases-actions/americans-prosperity-foundation-v-bonta); [Cato](https://cato.org/supreme-court-review/2020-2021/americans-prosperity-foundation-v-bonta-first-amendment-sensitive).

**State compulsion (live in 2026)**
- DHS reportedly sent hundreds of administrative subpoenas for names, emails and phone numbers behind accounts critical of ICE. Google, Meta, Reddit and Discord were reported recipients. No judge reviews these first. Some users were notified and had 10–14 days to contest — [NYT reprint](https://www.hawaiitribune-herald.com/2026/02/14/nation-world-news/homeland-security-wants-social-media-sites-to-expose-anti-ice-accounts/?nonamp=1). The ACLU and others have sued for records — [Reason](https://reason.com/2026/04/24/civil-liberties-groups-sue-for-information-on-ices-speech-chilling-subpoenas/); [Inquirer](https://www.inquirer.com/news/pennsylvania/ice-foia-lawsuit-aclu-subpoenas-social-media-dhs-20260420.html). The extent of company compliance is unclear across sources.

**Social credit**
- There is no central individual social credit score in China. The national system mainly covers companies. Point-scoring comes from local pilots such as Rongcheng, and residents there were later allowed to opt out — [MIT Technology Review](https://www.technologyreview.com/2022/11/22/1063605/china-announced-a-new-social-credit-law-what-does-it-mean/).

**Worldcoin / World**
- Brazil banned it in January 2025 over paying for iris scans. The Philippines ordered a halt in October 2025. Thailand ordered a halt and deletion in November 2025 — [Rest of World](https://restofworld.org/2026/sam-altman-worldcoin-zoom-tinder-partnerships/); [ID Tech](https://idtechwire.com/thailand-orders-worldcoin-to-halt-iris-scans-and-delete-biometric-data/).
- Bavaria's regulator ordered deletion of non-compliant data in December 2024 — [CryptoNews](https://cryptonews.com/news/german-watchdog-orders-worldcoin-to-delete-non-compliant-data-citing-gdpr-violations/). Kenya: deletion after a High Court ruling — [CryptoNews.net](https://cryptonews.net/news/legal/32319750/) (crypto trade press; verify against regulators).

**Small-app breach analogue**
- The Tea app leaked about 72,000 images, then a later leak exposed 1.1 million private messages including talk of infidelity and abortion. The sources disagree on some figures — [Wikipedia](https://en.wikipedia.org/wiki/Tea_(app)).

### Inferences
- **The Cambridge Analytica pattern is a promise broken by the database key.** "We don't collect identifiable data" failed because of a user ID. Any Dialogos claim of "anonymous" must survive the same test.
- **A voting-advice tool's server is not its only leak.** Third-party scripts are enough, so a fingerprint page should load no third-party scripts at all.
- **The voter file is an existing join table.** It already holds modelled issue positions on most US adults, so an attacker could compare leaked answer vectors against it. This linkage is my reasoning; I found no documented case.
- **The China parallel is misused if read as "a score that rules everyone."** The real lesson is narrower: moral behaviour turned into a reusable public number. That applies to MOVE more than to the fingerprint.
- **Payment taints consent.** Brazil's objection to paying for iris scans suggests that rewards in MOVE should never be consideration for handing over a fingerprint.

### Gaps
- No breach of a quiz-style political site found (Pew, iSideWith, Political Compass and the like). Absence of reports is not proof of absence.
- Could not read iSideWith's privacy policy (two guessed URLs returned 404), nor Pew's data practices or Wahl-O-Mat's (bpb page did not cover it). Their data handling is **unverified**. No DPA action on Wahl-O-Mat or Stemwijzer was found.
- **myPersonality:** I recall a 2018 report of exposed credentials giving access to about 3 million users' data, but could not verify it. Do not cite without a source.
- *NAACP v. Alabama* was not confirmed in these searches, though it is the foundational case to ask a lawyer about.
- 23andMe's bankruptcy (data as a sale asset) could not be verified: the search budget ended and the FTC URL I tried returned 404. It is the right precedent to check for acquisition risk.

---

## Law: what practically hits a small US-based project

### Takeaway
A small project below 35,000–100,000 users, or a nonprofit in the right states, escapes most US state privacy statutes on paper. The state lists I could read do not name political opinions. They do name "religious beliefs", and California names "philosophical beliefs", so a worldview quiz can trip them anyway. Three things apply regardless of size: honesty in privacy claims, minors rules (Colorado's has no size threshold), and GDPR if the project targets people in the EU. **[LEGAL REVIEW]** on all of it.

### Cited Findings

**How many states.** 24 states have comprehensive laws if Florida's narrow one is counted. Alabama, Louisiana, Oklahoma and Vermont were enacted in 2026 — [MultiState](https://www.multistate.us/insider/2026/10/28/twenty-four-states-now-have-comprehensive-consumer-privacy-laws).

| Law | Threshold | Nonprofit | Sensitive list includes political opinion? | Source quality |
|---|---|---|---|---|
| California CCPA/CPRA | For-profit; over $25M revenue, or buy/sell/share 100k+ residents, or 50%+ revenue from sales | "Generally does not apply" | No, but "religious or philosophical beliefs" yes; one chart disagrees | [CA AG](https://oag.ca.gov/privacy/ccpa); [Hogan Lovells](https://www.hlc.com/en/publications/cpra-countdown-new-compliance-obligations-and-challenges-around-sensitive-personal-information); conflict: [NatLawReview](https://natlawreview.com/article/updated-colorado-what-considered-sensitive-personal-information) |
| Colorado CPA | 100k consumers a year, or sale revenue plus 25k | Secondary sources: no exemption | B5 says no; statute text unreadable here | [CO bill summary](https://leg.colorado.gov/bills/sb21-190); [Wiley](https://wiley.law/alert-New-State-Privacy-Laws-May-Apply-to-Nonprofit-Organizations); [Venable](https://www.venable.com/insights/publications/2023/10/what-nonprofits-need-to-know-about-state) |
| Virginia | 100k, or 25k plus over 50% sale revenue | Exempt | Not checked here | [Va. Code](https://law.lis.virginia.gov/vacode/title59.1/chapter53/section59.1-576/) |
| Texas TDPSA | No numeric test; anyone offering services used by Texans unless SBA small business | Exempt | No; lists "religious beliefs" | [HB 4 enrolled](https://capitol.texas.gov/tlodocs/88R/billtext/html/HB00004F.htm) |
| Minnesota | 100k, or 25k plus over 25% sale revenue | No general exemption | No; lists "religious beliefs" | [Minn. Stat. ch. 325M](https://www.revisor.mn.gov/statutes/cite/325M/full) |
| Maryland | 35k, or 10k plus over 20% sale revenue | Not checked | Sources list religious beliefs, not political | [Constangy](https://constangy.com/constangy-cyber-advisor/maryland-online-data-privacy-act-is-broader-stricter-and-more-easily-triggered-than-many-state-privacy-laws); [Enzuzo](https://www.enzuzo.com/blog/maryland-online-data-privacy-act) |
| Vermont (2026) | 35k; 3,000 for sensitive data or sale | One search summary says no blanket exemption; source not pinned down | Not checked | [MultiState](https://www.multistate.us/insider/2026/10/28/twenty-four-states-now-have-comprehensive-consumer-privacy-laws) (thresholds only) |
| Alabama (2026) | 25k, under-500-employee exemption unless selling | Not checked | Not checked | [MultiState](https://www.multistate.us/insider/2026/10/28/twenty-four-states-now-have-comprehensive-consumer-privacy-laws) |

- **Small-business traps:** even SBA small businesses may not sell sensitive data without consent in [Texas (541.107)](https://capitol.texas.gov/tlodocs/88R/billtext/html/HB00004F.htm) and [Minnesota (325M.17)](https://www.revisor.mn.gov/statutes/cite/325M/full).
- **Connecticut:** vendor sources claim any sensitive-data processing triggers the law regardless of volume, but sources conflict on the sale trigger — [Clym](https://www.clym.io/blog/us-privacy-law-comparison-map); [Consently](https://consently.net/blog/us-state-privacy-laws). **[LEGAL REVIEW]**: if true, this is the lowest bar.
- **Maryland:** sensitive data may be processed only where "strictly necessary" for a requested service; whether consent can cure a sale is disputed — [Constangy](https://constangy.com/constangy-cyber-advisor/maryland-online-data-privacy-act-is-broader-stricter-and-more-easily-triggered-than-many-state-privacy-laws).
- **Colorado inferences:** rules require consent for sensitive data inferences, with a narrow draft exception (delete in 12 hours, no sale). Final text unconfirmed — [Fox Rothschild on the 2022 draft](https://www.foxrothschild.com/publications/colorado-issues-draft-rules-to-supplement-privacy-law); [LexBlog](https://www.lexblog.com/?p=2278668). **[LEGAL REVIEW]**.
- **Minnesota profiling:** consumers may opt out of "profiling in furtherance of automated decisions that produce legal effects" — [statute](https://www.revisor.mn.gov/statutes/cite/325M/full).

**Minors.**
- Colorado SB 24-041 took effect 1 October 2025. It reportedly applies regardless of revenue or processing thresholds, to services that know or wilfully disregard that a user is a minor — [Colorado General Assembly](https://leg.colorado.gov/bills/sb24-041); [Mondaq](https://www.mondaq.com/unitedstates/privacy-protection/1686116/colorado-tightens-rules-on-minors-online-dataare-you-ready-for-october-1).
- COPPA's amended rule took effect June 2025, with compliance due 22 April 2026. It covers child-directed services and those with actual knowledge of under-13 users — [Federal Register](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule); [Mondaq](https://webiis10.mondaq.com/unitedstates/privacy-protection/1790866/coppas-amended-rule-is-now-in-full-effect-what-operators-need-to-know). One source puts the penalty at $53,088 per violation — [BBB Programs](https://bbbprograms.org/media/insights/blog/coppa-amended).

**GDPR reach.**
- Applies to non-EU controllers offering services to, or monitoring, people in the Union — [Art. 3(2)](https://gdpr-info.eu/art-3-gdpr/).
- Such a controller needs an EU representative unless processing is occasional, excludes large-scale special-category data, and is low risk — [Art. 27](https://gdpr-info.eu/art-27-gdpr/).

**Research rules.** The Common Rule covers research conducted, supported or regulated by a federal agency — [45 CFR 46.101](https://www.law.cornell.edu/cfr/text/45/46.101). An independent, unfunded project is outside it by default.

**Data broker rules.** California defines a broker as selling data on consumers with whom it has no direct relationship. Fees are $6,000 a year and DROP deletion cycles began 1 August 2026 — [CPPA](https://cppa.ca.gov/data_brokers/).

**AI Act reach.** See the behavioural-harms section below.

### Inferences
- **"Revealing" is the trap word.** A question set on meaning, God, family or dignity can reveal religious belief, health, or sexuality. State statutes catch this even where "political opinion" is missing. Fix by screening question items, or treat the whole fingerprint as sensitive.
- **A nonprofit form helps in Texas, Virginia and California, but not in Colorado or Minnesota.** Benjamin is in Colorado, so the home-state law gives no nonprofit shelter. Thresholds probably do until 100,000 users, if the project is "conducting business" there. **[LEGAL REVIEW]**
- **If people choose to take the quiz, and nothing is sold, the broker rules should not apply** because the project has a direct relationship. Selling or licensing fingerprints to anyone would change that.
- **"No minors" needs a real mechanism, not just a policy.** Asking age creates "actual knowledge". A neutral 18+ self-declaration, checked on the device and never sent, seems the lowest-data approach. **[LEGAL REVIEW]** on whether a client-side gate is adequate.
- **Device-only fingerprints may shrink the controller's role** under GDPR and state laws, but the rating and credential data still count. Do not assume "client-side" means out of scope. **[LEGAL REVIEW]**
- **IRB not applying is not a free pass.** The ethics are unchanged, and any university partner or journal brings it back. A voluntary independent ethics review would be cheap and credible.

**What a lawyer should answer first (ordered):**
1. Does a fingerprint count as sensitive data under Colorado, Connecticut, Maryland, Minnesota and Vermont law?
2. Does a US site accessible from Europe "offer services" to the EU, and can launch be restricted to avoid this?
3. How does the entity form (nonprofit or LLC) change coverage?
4. Does a public MOVE score create defamation, FCRA-like or AI Act social-scoring exposure?
5. How should the project respond to subpoenas, and what must it say about them to users?
6. Is the age mechanism adequate?

### Gaps
- Whether **any** of the 24 state laws names political opinions was not exhaustively checked. I read Minnesota and Texas directly; neither does.
- Colorado statute text would not parse. Final Colorado Rule 6.10 not confirmed. Colorado minors rule approval not confirmed.
- Oregon, Delaware and Minnesota nonprofit treatment conflicted across sources; Minnesota is resolved by the statute (only an insurance-fraud nonprofit carve-out).
- State age-verification and app-store laws in 2026 were not reached.
- Not sourced here: FTC jurisdiction over nonprofits, state breach-notification duties, certificates of confidentiality, AAPOR survey norms, and whether data the project holds on landmarks triggers different rules.

---

## Re-identification: is a 40-answer fingerprint uniquely identifying?

### Takeaway
Yes. In real public opinion data, about 95–100% of people who answered the same 40 items had a vector nobody else shared, and that was with only three answer options. Uniqueness is not the same as a name, but it means a fingerprint is a stable key: anyone with some of the answers can find the rest. Calling stored answer vectors "anonymous" would be false, and this conclusion does not depend on how polarized people are.

### Cited Findings

**The classic results**
- Sweeney: up to 87% of the US population identifiable by 5-digit ZIP, gender and date of birth — [Wikipedia summary](https://en.wikipedia.org/wiki/Data_re-identification).
- de Montjoye et al.: four low-resolution location points uniquely identified 95% of 1.5 million phone users — [same source](https://en.wikipedia.org/wiki/Data_re-identification).
- Rocher, Hendrickx and de Montjoye (2019): model estimates 99.98% of Americans would be correctly re-identified in any dataset using 15 demographic attributes, and heavily sampled datasets are unlikely to meet GDPR's anonymisation standard — [Imperial repository](https://spiral.imperial.ac.uk/entities/publication/c2c69dc9-aa21-45e6-a107-42b20300a205); [press release](https://www.eurekalert.org/news-releases/779013). This is a model estimate about demographics, not attitudes.
- Narayanan and Shmatikov: an attacker knowing "only a little bit" found subscribers in the Netflix data of about 500,000, exposing apparent political preferences — [arXiv](https://arxiv.org/abs/cs/0610105).
- Survey panels: more collected variables make respondents more likely to be singled out by response pattern alone. Such survey-specific work is rare compared with register or medical data — [arXiv 1404.1808](https://arxiv.org/pdf/1404.1808).

**Test run for this memo: public Polis vote data.** Source: [compdemocracy/openData](https://github.com/compdemocracy/openData). All data is CC BY and described as "anonymous human expressions" — [README](https://raw.githubusercontent.com/compdemocracy/openData/master/README.md).

Method: took each conversation's 10, 20, 30 and 40 most-answered items, kept participants who answered all of them, and counted vectors nobody else in that subset shared. Pass counts as an answer. Options are agree, disagree, pass. Only aggregates were computed; no attempt was made to identify anyone. The youth policing dataset was deliberately excluded.

| Conversation | People with all 40 | Unique at 10 | at 20 | at 30 | at 40 |
|---|---|---|---|---|---|
| march-on | 2,008 | 6.7% | 39.9% | 92.8% | 99.4% |
| vtaiwan.uberx | 349 | 47.9% | 90.1% | 93.8% | 94.6% |
| bowling-green | 332 | 46.5% | 85.5% | 92.6% | 96.4% |
| canadian-electoral-reform | 49 | 78.3% | 97.0% | 96.1% | 100% |
| brexit-consensus | 32 | 53.7% | 93.8% | 100% | 100% |

Row sample size shrinks as items increase (for example march-on: 4,476 at 10 items). Small groups make uniqueness easier. March-on is the most informative row, because it has the biggest n and the most lopsided answers, and it still reaches 99.4%. Pairs agreed on 41–64% of items on average.

Marginal entropy over those 40 items summed to about 37–56 bits. That is an upper bound, since it ignores correlation between answers. The US adult population needs about 28 bits to single out one person.

**Simulation, also run for this memo.** 300,000 synthetic people, 5-point items, driven by 2 or 5 hidden opinion factors plus noise:

| Hidden factors, strength | Unique at 10 items | 15 | 20 | 40 |
|---|---|---|---|---|
| 2, moderate (0.5) | 76.9% | 99.95% | 100% | 100% |
| 2, strong (0.7) | 56.6% | 99.6% | 100% | 100% |
| 2, very strong (0.85) | 25.7% | 92.3% | 99.35% | 100% |
| 5, strong (0.7) | 64.7% | 99.9% | 100% | 100% |

Simulated data is not real opinion. A real population has clumps (for example, straight party-line answerers), so a few people would be less unique than this.

### Inferences
- **The number that matters is about 15–30 answers, not 40.** In the simulation, about 15–20 5-point answers make nearly everyone unique among 300,000 people; in the Polis data, three-option answers get there by about 30. So trimming 40 items to 25 does not make the data safer. Only going near 10 items lowers uniqueness much (roughly 7–78% in these tests), and that may hurt placement. Item count should be set for placement quality, and protection must come from not storing the vector.
- **Unique does not equal named.** Three linkage paths would turn it into a name:
  - a partner, colleague or employer who knows or can guess some answers;
  - a person's public posts, turned into predicted answers by an LLM;
  - the same person taking a similar quiz elsewhere, or retaking this one, which joins sessions.
- **Noise-tolerant matching should be assumed.** Netflix shows fuzzy matches work, so small answer changes will not break linkage.
- **Never store demographics beside answers.** ZIP, birth date and gender alone reach 87% with no opinions at all.
- **Publishing a Polis-style vote matrix would release a reversible key.** This is not an accusation about Polis, whose participants join for a single topic. A durable, cross-topic 40-item worldview vector is a different and riskier object.

### Gaps
- No published study found that measures uniqueness or re-identification specifically for political attitude vectors at population scale. My test is small-sample. A proper answer needs a large panel with the actual question set.
- Test-retest drift for attitude fingerprints was not measured, so how long a fingerprint stays a usable key is unknown.

---

## Inference attacks: reconstructing answers and proving membership

### Takeaway
A coarse cluster label gives away only a modest amount about any one answer: about 6–9 points above a simple guess on contested datasets, and about zero on lopsided ones. So publishing a coarse label is far safer than publishing a vector, but it is not free, and the label is the harm on its own terms. The real leaks are small clusters, stable IDs, and the fact of being in the dataset at all.

### Cited Findings

**Test run for this memo, same Polis data.** Method: split items at random in half, cluster people using one half (k-means, k = 2, 3, 4, 6), assign held-out people to a cluster, then guess their other half using their cluster's most common answers. Compare to guessing each item's overall majority. One random split per k, so read these as rough.

| Conversation | n | Guess from cluster (held-out) | Plain majority guess | Gain |
|---|---|---|---|---|
| bowling-green | 332 | 60–64% | 51–54% | about +9 points |
| vtaiwan.uberx | 349 | 67–75% | 60–68% | about +6.5 to +9 points |
| march-on | 2,008 | 71–77% | 71–77% | about 0 to +1 |
| canadian-electoral-reform | 49 | 69–74% | 70–75% | about −2 to +1 (too small) |
| brexit-consensus | 32 | 68–72% | 67–74% | about −2 to +1 (too small) |

**Membership inference.** An attacker with a record and black-box model access can infer whether that record was in the training data — [Shokri et al.](https://arxiv.org/abs/1610.05820).

**Community Notes publishes per-person data.** Its public files carry a permanent participant ID on every rating, "stable even if the user changes their username/handle". The enrolment file includes `modelingGroup` for each user — [Community Notes docs](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/download-data.md).

### Inferences
- **Copying Community Notes' open data release would publish each rater's cluster under a permanent ID.** The whole note-rating history would also act as a fingerprint. This one design habit would defeat most other protections, so publish note-level aggregates only.
- **Finer output leaks more.** I did not test exact map coordinates, but a person's dot on a map is a compressed copy of their votes, so coordinates should stay on the device.
- **Small clusters break the label.** In a cluster of a few people, the label both identifies and reveals. Set a floor, for example no cluster displayed or stored below a large minimum size. Choosing the number needs testing.
- **Being in the dataset is itself sensitive.** A worldview project attracts people with reasons to care. A list of who signed up is a targeting list even with no answers attached. Treat account emails and phone hashes as sensitive, and avoid the list if possible.
- **A model shipped to the browser can leak the people who trained it.** Cluster centres from small seed panels could reveal them. Train on large groups, or use public landmarks and synthetic anchors.

### Gaps
- Did not test coordinates, repeated label release over time (where changes in label leak more), or attribute inference with demographics added.
- Did not find a Polis-specific privacy analysis.

---

## Privacy-preserving designs: what a tiny team can do, and what fits per-rater scoring

### Takeaway
The best design is simple and cheap: compute the fingerprint on the person's device and never send it. Local differential privacy, multi-party aggregation and MACI are real but mostly wrong for this stage. The hard constraint is scoring: matrix factorization needs a stable rater × note table. The resolution is to let the scorer work from ratings under seasonal pseudonyms, with only a coarse, optional viewpoint attestation, and never to pass the fingerprint to the server.

### Cited Findings

**Client-side examples and tools**
- zkPassport reads a passport chip and creates proofs on the phone, revealing only requested facts such as `over_18` or `unique`, plus a per-app nullifier. It says it stores no user data — [zkPassport](https://zkpassport.id/) (vendor claim).
- Semaphore: identity, Merkle-tree group, zero-knowledge membership proof, and nullifier to block double-signalling. JavaScript libraries create identities and proofs off-chain — [Semaphore docs](https://docs.semaphore.pse.dev/). On-chain contracts manage groups and verify proofs in the documented setup. Its site says it works for Web2 and Web3 — [semaphore.pse.dev](https://semaphore.pse.dev/). Whether a blockchain-free deployment is practical was not tested.
- W3C Verifiable Credentials 2.0 has been a Recommendation since 15 May 2025. It defines holder, issuer and verifier, plus selective and unlinkable disclosure formats including bbs-2023 and SD-JWT — [W3C](https://www.w3.org/TR/vc-data-model-2.0/).

**Local differential privacy**
- RAPPOR randomizes at the client so analysts see population patterns only — [arXiv](https://arxiv.org/abs/1407.6981).
- Apple's per-datum privacy loss was 1 or 2, but total loss reached up to 16 per day; Apple disputed the values — [Tang et al.](https://arxiv.org/pdf/1709.02753); [Wired repost](https://www.unwantedwitness.org/how-one-of-apples-key-privacy-safeguards-falls-short/). Google's RAPPOR reportedly uses about 2, lifetime 8–9 (same repost).
- Local DP only works with large populations — [Access Now](https://www.accessnow.org/understanding-differential-privacy-matters-digital-rights/).
- LDP on matrix factorization has known utility problems from high dimensionality and iterative estimation — [TKDE 2018 paper record](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c293t-c8847f4de3986ddb350ec384caee72a81a5a2f4c67c7af0720f96d7389bfdcdf3). Federated MF with secure aggregation offers better accuracy under a similar threat model — [VLDB](https://mail.vldb.org/pvldb/volumes/15/paper/Federated%20Matrix%20Factorization%20with%20Privacy%20Guarantee). Differentially private MF exists — [Hua, Xia, Zhong, IJCAI 2015](https://www.ijcai.org/Abstract/15/251).

**Calculated for this memo (randomized response, binary answers).**
- The question for each privacy level is how many people are needed for one item's share at ±1.5 points standard error, and for a pairwise correlation at ±0.01.
- At ε = 1 per item (40 items, ε = 40 total): about 5,200 people per item share, about 219,000 per correlation.
- At ε = 0.1 per item (ε = 4 total): about 445,000 per item share, about 1.6 billion per correlation.
- Clustering needs correlations, so honest LDP on 40 items cannot build the map at a small scale.

**Secure aggregation**
- Bonawitz et al.: a server gets the sum of user vectors without seeing any one of them, survives dropouts, and costs about 1.7–2× communication — [ePrint](https://eprint.iacr.org/2017/281).
- Prio keeps privacy if at least one server is honest, and limits malicious clients — [Stanford](https://crypto.stanford.edu/prio/).

**MACI**
- Private, receipt-free voting, using a coordinator: a dishonest coordinator cannot censor or tamper, but collusion resistance depends on its honesty — [MACI](https://maci.pse.dev/); [v0.x docs](https://maci.pse.dev/docs/v0.x/introduction).

**Fit against the two scorers.** Ratings are keyed to a rater ID in Community Notes' data — [docs](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/download-data.md).

| Design | Team cost | Works with Polis-style map? | Works with Community Notes-style scorer? | Verdict |
|---|---|---|---|---|
| On-device fingerprint, published fixed loadings | Low | Yes for placing a person; map must come from elsewhere | Yes: scorer never sees it | **Do first** |
| Encrypted backup held by the user (passkey or exported file) | Low | n/a | n/a | **Do first** |
| No third-party scripts, no logs of IPs on fingerprint pages | Low | n/a | n/a | **Do first** |
| Seasonal pseudonyms and sunset | Low to medium | Yes | Yes, with lost long history | **Do** |
| Volunteer panel with its own consent for building the map | Medium | Yes: this is the map's input | n/a | **Do** |
| Coarse cluster attestation at rating time | Medium | n/a | Partial: gives viewpoint groups | **Do if D-31.1 keeps clusters as viewpoint** |
| Semaphore or anonymous credentials | Medium to high | Fair | Fair: per-season nullifier acts as pseudonym | **Pilot after launch** |
| Prio or secure aggregation for covariance | High; needs a second independent server operator | Yes, in principle | Weak: MF is iterative | **Later, with a partner** |
| Federated matrix factorization | High | n/a | Possible, research-grade | **Not now** |
| Local DP | Medium to build, needs huge population | Poor: see calculation | Poor | **Not for the map; fine for simple counts at scale** |
| MACI | High | No: wrong tool | No: wrong tool | **Skip**, except possibly a ratification vote later |

### Inferences
- **The two scoring needs can be separated.** A person's map position is private and device-held. Their rating history is a pseudonymous public act. The scorer needs the second, not the first. Matrix factorization learns its own viewpoint factor from ratings, so the fingerprint is not needed for scoring.
- **The conflict to flag:** spec step 6 uses "the map's clusters as the viewpoint dimension". For ordinary people this would force a cluster claim per rater, and D-31.1 already has an open conflict on it. Recommendation: use the learned factor for raters. If cluster groups are required, make the rater's attestation optional, coarse and self-submitted, in groups above the size floor.
- **A pseudonym is not protection if the rating history is published.** A season's ratings are themselves a fingerprint. Pseudonyms must go with a no-per-rater-export rule.
- **Reputation and unlinkability pull against each other.** Long-term reputation needs a stable identity; privacy needs rotation. Middle path: rotate each season and carry over only a coarse tier via a credential, so the score survives without the history. The full version needs anonymous credentials, so a simple start is to rotate and carry a single tier signed by the project, accepting that the project can link at the moment of transfer.
- **Device-held data can be seized or lost.** It moves the risk from a mass breach to one person's phone: an abusive partner, an employer laptop, a border check. Offer "don't save it" as a default option, and a quick delete.
- **How the map gets built without user data:** placing people needs only published loadings. Those can come from landmarks' public output (the current plan) plus a separately consented volunteer panel. People using the map don't feed it unless they opt in. Opt-in submission should be a one-off donation with no account ID.
- **A sunset is cheap and strong.** A rule such as deleting raw records after a fixed period, with a public statement, limits what any subpoena, breach or acquisition can reach.

### Gaps
- No Polis-specific client-side or DP implementation found.
- Did not benchmark browser proving times for 2026, or find a Semaphore or MACI 2026 audit.
- Parts of this analysis rest on my reading of matrix factorization, not a test. A quick experiment could measure scoring quality with seasonal pseudonym rotation.
- I could not confirm federated analytics tooling suited to a tiny team. No cloud or paid option should be chosen without Benjamin's approval.

---

## Sybil resistance and manipulation: identity needs in a reputation system

### Takeaway
Bot checks in a survey no longer work, so a free fingerprint quiz cannot be trusted as evidence about the public. But identity is only needed where something is at stake. Viewing and self-mapping need none. Rating that counts needs one-person-one-account, at the lowest-data strength that works. Anything raising an ID is a new list of who is here, so credentials must be separated from viewpoint data.

### Cited Findings
- Westwood (PNAS 2025): an autonomous LLM survey-taker reportedly evaded detection 99.8% of the time, at about $0.05 per response versus $1.50 for a human. As few as 10–52 fake responses could have flipped seven national pre-2024 polls — [404 Media](https://www.404media.co/a-researcher-made-an-ai-that-completely-breaks-the-online-surveys-scientists-rely-on/); [Dartmouth](https://fas.dartmouth.edu/news/2026/04/sean-westwood-wins-pnas-prize-ai-polling-study). The paper itself was not read.
- Community Notes requires an account at least 6 months old, a verified phone from a trusted carrier not tied to another Notes account, and no recent rule violations — [Community Notes docs](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/contributing/signing-up.md).
- Aliases are auto-generated and "not publicly associated" with X accounts. Profiles still show notes and impact — [aliases doc](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/contributing/aliases.md).
- A 5–20% minority of bad raters can suppress targeted notes in simulation. The scorer is sensitive to polarization and in-group preference — [arXiv 2511.02615](https://arxiv.org/pdf/2511.02615). 30.2% of displayed notes later lost helpful status, in part from later ratings by dissimilar raters — [arXiv 2601.14002](https://arxiv.org/pdf/2601.14002). (B5 covers the separate Selvam result.)
- Taiwan's Alignment Assembly invited people by 200,000 text messages to random numbers, combined with Polis and facilitated in-person sessions — [Tang transcript](https://archive.tw/speech/63852928); [transcript](https://archive.tw/speech/616678).
- Personhood credentials let someone prove they are a person, one credential per person, via zero-knowledge proofs and without revealing identity. CAPTCHAs are inadequate; strict ID is insufficiently private — [Adler et al.](https://arxiv.org/pdf/2408.07892).
- Human Passport (formerly Gitcoin Passport, acquired by Holonym) aggregates many independent signals into a score, default threshold 20. It reported work with 120+ projects — [Biometric Update](https://www.biometricupdate.com/202502/holonym-acquires-gitcoin-passport-in-proof-of-personhood-expansion); [Human Passport](https://passport.human.tech/blog/human-passport-proof-of-personhood-and-sybil-resistance-for-web3).
- BrightID verifies through "connection party" meets and says it records no personally identifying information — [BrightID](https://www.brightid.org/) (project claim).
- World ID: avoid for now, given the orders listed above.
- Group-based proof-of-personhood has its own attack: random groups may contain only an attacker's identities — [arXiv 2011.02412](https://arxiv.org/pdf/2011.02412).

**Tier design (mine):**

| Action | Identity needed | Mechanism |
|---|---|---|
| Read map, take fingerprint on device | None | Nothing sent |
| Donate answers to the volunteer panel | Light | Invited by random sample (Taiwan-style), or a one-time token. Treat open-web donations as unverified. |
| Rate notes, unrewarded | One-person, soft | Email or account age, low weight until track record |
| Rate notes, counted in MOVE | One-person, strong | Phone or personhood credential; the credential check is kept separate from ratings |
| Ratify a representation of a cluster | Strongest, plus cluster standing | Personhood credential, human only; no agents |

### Inferences
- **The fingerprint cannot be used as a sampling instrument.** Open-web answers can be mass-produced for pennies. Any claim about "what Americans think" needs recruited samples. The Westwood mitigation points the same way: address-based or voter-file recruitment.
- **Phone numbers are a compromise.** They are cheap and familiar but leave a subpoena-able link. Store only a salted check, or better, discard after issuing a token. This keeps the "one person" property with no retained list.
- **Each identity method excludes someone.** Passports exclude people without them. Phones exclude shared-phone households. Crypto-native tools exclude most Americans. Offer two or more routes to avoid skewing the map toward the well-documented.
- **Sybil defence also means rate limits in time:** new accounts get low weight, and coordinated bursts are held back, because identity alone does not stop real people colluding.

### Gaps
- Could not confirm any Polis-level sybil control or a Taiwan digital signature integration. Search results did not cover Join, TW FidO or the "digital signature" claim. Do not repeat that claim without a primary source.
- Self Protocol was not reached. No independent audit of zkPassport or BrightID was read. Population coverage of each method for the US is unknown.

---

## Behavioral and identity harms: labels, exposure, and nudges

### Takeaway
There is a plausible, evidence-backed risk that giving someone a worldview type hardens the very identity the project wants to soften. The direct evidence on quiz labels is thin, but a strong analogue exists: a simple mail reminder about party registration raised party identification. Exposure to out-groups can backfire when unstructured. The EU's manipulation ban is narrower than people assume; the stricter ethical line is covertness. Fingerprint-tailored persuasion should be off by default.

### Cited Findings

**Labels and looping**
- Hacking's "looping effect": classifying people changes how they see themselves and behave, which changes the category. "Sometimes, our sciences create kinds of people that in a certain sense did not exist before." — [Hacking, LRB](https://www.lrb.co.uk/the-paper/v28/n16/ian-hacking/making-up-people).
- Gerber, Huber and Washington (2010): a mailing about party registration led to 8.1 points greater identification with the latent party and stronger partisanship — [Yale ISPS](https://isps.yale.edu/research/publications/isps10-038); [J-PAL](https://www.povertyactionlab.org/print/pdf/node/1804).
- Kahan's work: people selectively credit information to fit group values, and trust experts seen as sharing them — [Cultural cognition overview](https://en.wikipedia.org/wiki/Cultural_cognition) (the "identity-protective cognition" citation is in its further reading; I did not read the 2007 paper).
- Iyengar et al.: affective polarization stems from partisanship as a social identity and reaches well outside politics — [Annual Review](https://annualreviews.org/doi/pdf/10.1146/annurev-polisci-051117-073034).
- Type quizzes: a 1989 thesis found feedback could shift self-perception, with situational limits — [Richmond](https://scholarship.richmond.edu/masters-theses/522) (fragments only). A 2024 study argues MBTI as a social label may mark people as "deviants" when behaviour departs from type, though it found no strong correlation with social anxiety — [Frontiers via PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11408848/).

**Out-group exposure**
- Bail et al. (2018): after a month following a bot sharing opposing elites, Republicans moved more conservative; Democrats moved slightly liberal, not significant — [PNAS record](https://scholars.duke.edu/publication/1346854); [phys.org](https://phys.org/news/2018-09-caught-political-echo-chamber-opposition.pdf).
- The Strengthening Democracy Challenge tested 25 of 252 submitted interventions — [site](https://www.strengtheningdemocracychallenge.org/). The specifics could not be read (see Gaps).

**Manipulation and nudges**
- Susser, Roessler and Nissenbaum: manipulation is covert influence that targets decision-making vulnerabilities; persuasion offers reasons a person can weigh. Nudges are not automatically manipulative: open ones such as nutrition labels are not — [Internet Policy Review](https://policyreview.info/articles/analysis/technology-autonomy-and-manipulation).
- Yeung: "hypernudges" are networked, continually updated and pervasive. Notice and consent do not adequately fix the legitimacy concerns — [paper](https://sts.wisc.edu/wp-content/uploads/sites/328/2019/06/%E2%80%98Hypernudge%E2%80%99-Big-Data-as-a-Mode-of-Regulation-by-Design-Yeung.pdf).
- AI Act Art. 5(1)(a) bans subliminal or purposefully manipulative techniques that distort behaviour and likely cause significant harm. 5(1)(b) covers exploiting age or disability vulnerabilities. 5(1)(c) bans social scoring leading to unrelated or disproportionate detriment. 5(1)(g) bans *biometric* categorisation inferring political opinions — [Art. 5](https://artificialintelligenceact.eu/article/5/).
- The Commission's non-binding guidelines say transparent persuasion with informed consent is likely lawful — [Covington](https://www.insideprivacy.com/artificial-intelligence/european-commission-guidelines-on-prohibited-ai-practices-under-the-eu-artificial-intelligence-act/); [Arthur Cox](https://www.arthurcox.com/knowledge/the-eu-commission-guidelines-on-prohibited-ai-practices/).
- Annex III 8(b) lists as high-risk AI intended to influence election outcomes or voting behaviour, when people are directly exposed to its output — [Annex III](https://artificialintelligenceact.eu/annex/3/).

### Inferences
- **The fingerprint's main output should not be a type.** Prefer:
  - per-issue positions with stated uncertainty;
  - "you resemble this cluster on these 12 items, and differ on these 8";
  - no team name, badge, or shareable card;
  - retaking encouraged, and the display of change over time held on the device.
- **Show the distance from the cluster, not membership in it.** People with a mixed profile should see that they are mixed, not be forced into a nearest group. This also protects nuance.
- **Run the experiment before launch.** Randomly compare type labels with continuous displays, and measure identity strength, out-group warmth, and accuracy of describing the other side. Evidence here is too thin to assume. It would be a useful public contribution.
- **The MEET layer should keep its structure.** Bail's result concerned unstructured elite messages from a bot. It does not show that structured, disclosed, reciprocal dialogue backfires. This is a caution, not a refutation.
- **Article 5(1)(a) likely does not reach most disclosed tools; ethics should go further.** Article 5(1)(c) is the sleeper risk. A public MOVE score that an employer or platform uses for an unrelated purpose looks like what it covers. Terms should forbid this, and the design should avoid an exportable personal score. **[LEGAL REVIEW]**
- **Annex III 8(b) hinges on intent to influence voting.** Dialogos does not aim at that, but a fingerprint that nudges people before an election could look that way. **[LEGAL REVIEW]**

**Proposed bounds for any nudge (my synthesis of the above):**
1. Disclosed each time, at the moment it happens, with the reason.
2. User-started: the person asks to be challenged or shown the other side.
3. Reasons, not weak spots: it never uses a measured vulnerability.
4. Symmetric: the same nudge is offered to all clusters.
5. No directional goal: the target is understanding, measured by whether the other side signs the description, never moving someone's opinion.
6. Runs on the device from data the person holds, with no server-side profile.
7. Off before elections unless shown to be neutral; a quiet period seems sensible.
8. Publishable: any rule that the team would be embarrassed to show users is banned.

### Gaps
- No direct RCT found on whether a political type quiz hardens identity. Political typology quiz effects (Pew and similar) were not found.
- MBTI test-retest instability appeared only in an unsourced blog, so it is not used here.
- Results of the Voelkel *Science* 2024 megastudy could not be read (HTTP 403), and meta-perception correction evidence (PNAS 2020) was also blocked. My memory is that correcting exaggerated views of the other side reduced animosity. Treat that as **unverified**; this finding matters a great deal to whether showing out-group views helps, and it needs reading first.
- No search results on Thaler and Sunstein's own ethical bounds; only the Susser et al. account of nudges was read.
- Status of the EU "Digital Omnibus" delays to AI Act dates was not checked.

---

## Agents as participants: representing or simulating a fingerprint

### Takeaway
A 40-answer fingerprint is close to enough to build a working model of a person's opinions. That makes it more than a record: a stolen fingerprint is a rehearsal dummy for tailoring persuasion to that person. Agents may help a person prepare, but they must never stand in for a person's signature.

### Cited Findings
- Park et al.: agents built from 1,052 Americans predicted held-out General Social Survey answers at 83% (interview only), 82% (survey only), 86% (combined), and 74% (demographics only), normalized to each person's own two-week test-retest consistency — [arXiv 2411.10109](https://arxiv.org/abs/2411.10109).
- Personhood paper: AI agents may misrepresent whose goals they serve — [Adler et al.](https://arxiv.org/pdf/2408.07892).
- Westwood: LLM agents pass current survey checks at negligible cost — [404 Media](https://www.404media.co/a-researcher-made-an-ai-that-completely-breaks-the-online-surveys-scientists-rely-on/).

### Inferences
- **Survey answers already do most of the work.** In Park's data, survey-only agents nearly matched two-hour interviews. Though those were GSS items, not a 40-item fingerprint, the risk carries over.
- **New risk not in B6: the fingerprint as attack material.** Anyone holding it can pre-test messages on a twin of that person, then deliver the winner. This is another reason for device-only storage.
- **Why agents never ratify, in addition to B6's A6:**
  - Ratification is valuable because a person accepts responsibility for a description of their side. A simulation only extends their past answers.
  - The success test is meta-consensus. If an agent can sign, the test measures model fit, not understanding.
  - Agents fail silently: a model could sign something the person would reject. Nobody would know.
  - An agent can be run many times, so one fingerprint could yield many votes.
- **A person's delegate should carry a fingerprint only inside their own session.** Scope should be set per use; output is labelled; the person reviews before anything is sent. Nothing the agent says counts as the person's position until they confirm it.
- **Never sell or offer "talk to a simulation of this cluster" built on private fingerprints.** Build cluster stand-ins from public landmark material only, and label them.
- **Conflict to flag:** project instructions mention agents "on a separate leaderboard", while B6 A7 says no public agent leaderboard. The spine's adopted safeguards likely settle this, but I did not check. Benjamin should confirm.

### Gaps
- The 2026 literature on digital twins in deliberation was not reached.
- No data on how accurately a fingerprint of exactly 40 items yields a twin. Disclosure law is covered by B6 and was not re-examined.

---

## Threat model and design list ordered by cost

### Takeaway
The cheapest controls are also the strongest: do not hold the data, do not publish per-person data, and do not name people's type. Build the first group before any public fingerprint exists. Hold back from anything that requires a server-side list of ordinary people and their worldviews.

### Cited Findings

Threat model. The evidence is in the sections above; the right column is my recommendation.

| # | Adversary | What they want | How | Evidence | Main control |
|---|---|---|---|---|---|
| T1 | Government (any party in power) | Names of people with a given view | Subpoena, including no-judge administrative demands | [DHS 2026](https://www.hawaiitribune-herald.com/2026/02/14/nation-world-news/homeland-security-wants-social-media-sites-to-expose-anti-ice-accounts/?nonamp=1) | Hold nothing linkable; publish a policy and transparency report; notify users |
| T2 | Hacker or careless vendor | Bulk dump | Misconfigured database | [L2](https://fedscoop.com/exposed-u-s-voter-database-poses-extreme-danger-researcher-says/); [RNC](https://www.upguard.com/breaches/the-rnc-files); [Tea](https://en.wikipedia.org/wiki/Tea_(app)) | No central fingerprint store |
| T3 | Third-party script or ad network | Answers as they are typed | Trackers on the page | [Finnish VAAs](https://link.springer.com/chapter/10.1007/978-981-97-1313-4_30) | No third-party code; strict content security policy; self-hosted fonts |
| T4 | Campaign, broker, advertiser | Link answers to voter file | Fuzzy matching | [Voter files with modelled issues](https://www.upguard.com/breaches/the-rnc-files); [TTPA fallout](https://about.fb.com/news/2025/07/ending-political-electoral-and-social-issue-advertising-in-the-eu/) | No exports; no demographics; no sale ever |
| T5 | Harasser or doxxer | Public shame | Map people with labels | [Eightmaps](https://nextcity.org/daily/entry/mapping-proposition-8) | No public person-level labels; no public list of who has a fingerprint |
| T6 | Intimate partner, parent, employer | One person's views | Device access, pressure to reveal | Reasoning only | Don't-save default, quick delete, no shareable proof |
| T7 | Researcher or open-data user | Re-identify | Join released vectors or rater histories | [Netflix](https://arxiv.org/abs/cs/0610105); [CN data](https://raw.githubusercontent.com/twitter/communitynotes/main/documentation/under-the-hood/download-data.md); tests above | Aggregates only, size floor |
| T8 | Sybil farm or state troll | Skew the map or score | Cheap LLM accounts | [Westwood](https://www.404media.co/a-researcher-made-an-ai-that-completely-breaks-the-online-surveys-scientists-rely-on/); [arXiv 2511.02615](https://arxiv.org/pdf/2511.02615) | Recruited panels; identity tiers; low weight for new accounts |
| T9 | Persuader with a twin | Tailor messages to a person | Simulate from fingerprint | [Park et al.](https://arxiv.org/abs/2411.10109) | Device-only; no fingerprint for hosted agents |
| T10 | Project itself: mission drift, sale, new owner, bankruptcy | Monetize or repurpose | Change of terms | B5 threat list; [FTC order on data deletion](https://www.ftc.gov/news-events/news/press-releases/2019/12/ftc-issues-opinion-order-against-cambridge-analytica-deceiving-consumers-about-collection-facebook) | Sunset; charter barring sale; nothing to sell |
| T11 | The design itself | Hardened tribes | Type labels and badges | [Hacking](https://www.lrb.co.uk/the-paper/v28/n16/ian-hacking/making-up-people); [Gerber et al.](https://isps.yale.edu/research/publications/isps10-038) | Continuous display, no team names, RCT before launch |
| T12 | Third parties using MOVE | Decisions about jobs, access | Scraping a public score | [AI Act 5(1)(c)](https://artificialintelligenceact.eu/article/5/) | No exportable personal score; terms; **[LEGAL REVIEW]** |

### Inferences

**Design list, cheapest first.** Cost is my rough estimate for a very small team using open-source tools.

*Tier 0: policy and data-shape decisions (days, no spend)*
1. Write a rule that no server stores an answer vector, and no ordinary person's cluster, under any ID. Add it to the red lines.
2. Do not publish per-rater data, unlike Community Notes. Publish note-level aggregates.
3. Do not collect demographics with answers. Screen items for "revealing" religion, health, sexuality, immigration status.
4. Cut the question count to the fewest that place people well. This reduces burden and sensitive-item exposure, but do not count it as anonymity: 25 answers are as identifying as 40.
5. No type names, badges, or share cards as defaults. Show per-issue position and uncertainty.
6. Bar third-party use of scores in the terms. Add a charter clause: no sale of data, in any form, even in acquisition.
7. Plain-language promises checked against what the code does, learning from the FTC's Cambridge Analytica finding. Never say "anonymous" for a vector.
8. Set a data sunset and a subpoena policy, and publish both.

*Tier 1: simple engineering (1–3 weeks)*
9. Compute placement in the browser from published loadings; save nothing by default.
10. Offer an encrypted export the person holds, with one-click delete.
11. No third-party scripts, strict content security policy, IPs not logged on these pages.
12. Neutral 18+ gate kept on the device. **[LEGAL REVIEW]**
13. Size floor on any displayed cluster.
14. Agents: fingerprint stays in a person's session; reviewed output only.

*Tier 2: moderate engineering (1–2 months)*
15. Seasonal rater pseudonyms, with only a coarse tier carried over.
16. Separate volunteer panel, with explicit consent and its own recruited sample, to build and refresh the map.
17. Identity tiers, with credential checks stored apart from ratings. Start with phone and discard the raw number, plus one non-phone route.
18. Pre-registered label test (type versus continuous display).
19. Voluntary external ethics review.

*Tier 3: cryptography and partners (a quarter or more; needs a specialist)*
20. Semaphore or anonymous credentials for per-season rating rights and optional cluster attestation.
21. Selective-disclosure credentials (VC 2.0 with BBS or SD-JWT) for carrying a tier.
22. Prio-style or secure aggregation for optional population statistics, with an independent second operator.

*Do not build now*
- Local DP for the map, MACI for scoring, federated matrix factorization, World ID, or hosted fingerprint twins.

**Decisions needed from Benjamin:**
- Accept "server never holds an answer vector" as a red line? It means ordinary users do not feed the map unless they separately opt in.
- Resolve D-31.1: learned rater factor (better for privacy) or map clusters as viewpoint?
- Launch US-only, avoiding EU targeting, until a lawyer confirms the approach?
- Pay for one legal review? This is the one spend I would recommend, and needs his approval under project rules.

### Gaps
- Effort estimates are judgment, not measured.
- Design has not been reviewed by a security specialist or lawyer. Any public launch of a fingerprint should have both.
- Vault write-back was not done here because the task limits changes to this notes file.
