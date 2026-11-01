# B5 — Platform Access, Data Governance and Ethics

> **Design update (2026-10-30).** The Design Dialogue Memo of 2026-10-30 (`design/DESIGN-MEMO-2026-10-30.md`) records decisions that supersede earlier research recommendations where they conflict; see `synthesis/SYNTHESIS.md` §2. The research below is unchanged. For this brief:
> - **Superseded: the data strategy** (AT Protocol primary for the open graph; X archive primary for X users; X OAuth secondary). The map is now built from **landmark public output** (YouTube and podcast transcripts, Substacks, posts) plus first-party **statement reactions**; AT Protocol is one channel and demographically skewed; X archive and OAuth are **optional enrichment** (SYNTHESIS §2 D11–D17; §11.1).
> - **Lower priority: the legal read on X's political-inference clause.** Still required before any X OAuth feature, but the core map no longer depends on X (Q36).
> - **Modified: red line 1 and the "landmark / public-figure policy".** Public intellectuals may be placed **from their public output** as worldview clustering, not political categorization, under conditions: the cluster is described, the person is not scored; quotes link to sources; a dispute / annotate affordance; a published selection method. **Private individuals remain opt-in only**, and red line 2 is restated as no inference about private individuals who have not reacted or consented (SYNTHESIS §11.2). This brief's GDPR caution for EU landmarks still stands: counsel before any EU landmark.
> - **New risk this brief did not cover: transcript copyright and platform ToS** (YouTube, podcast hosts) for ingesting ~500 landmarks' archives (R49, Q34).
> - **Retained:** aggregate-only release (k ≥ 50, DP), re-identification red-team, no scraping or rate-limit circumvention, no friends'-data pattern, the consent screen and per-layer consent for reactors.

Wave 1 research brief for the Dialogos Arena (author of record: Benjamin Life). Researched 2026-10-30.

---

## Summary

The SEE layer's main input, the X social graph, is now expensive to collect at network scale and contractually hostile to this use case. X moved to pay-per-use credits in February 2026. Reading accounts and follow edges costs about $0.01 per user object, which is affordable for one person's own graph and ruinous for a network crawl. More decisively, X's Developer Policy forbids deriving or storing inferences about a user's political affiliation or beliefs. The only carve-out is aggregate analysis that keeps no personal identifiers. A worldview map placed on top of X API data runs straight into that clause.

Two routes avoid it:
1. **The user-uploaded X archive.** This is the person's own data, obtained under data-portability rights, so the Developer Agreement does not govern it.
2. **AT Protocol (Bluesky).** Its whole social graph is public, free to stream through Jetstream, and natively able to host a map as a labeler or feed generator.

The legal picture points the same way:
- **GDPR** treats inferred political opinion as Art. 9 special-category data. The CJEU reads "manifestly made public" narrowly. Explicit, opt-in consent is the workable lawful basis.
- **Prior abuse cases** show where the harm comes from. Cambridge Analytica, influence-operation mapping and graph de-anonymization all show that a memetic map is also a targeting map.

**Recommendation:**
- Data sources: consent-only placement, with AT Protocol native ingestion and X archive upload as the two main intake paths. Use X OAuth only for the narrow case of a user reading their own data.
- Publication: aggregate-only. No individual inference about people who have not consented.

---

## Findings

### 1. X / Twitter API (state as of October 2026)

**Pricing model.** X launched pay-per-use, credit-based API access on 6 Feb 2026. Legacy Basic plans move to pay-per-use at the end of their billing cycle (June 2026) and Pro plans follow in September 2026. Enterprise continues at unpublished prices. A third-party summary reports these read prices:

| Read | Price |
|---|---|
| Posts | $0.005 per resource |
| Users | $0.010 per resource |
| Followers/following | $0.010 per resource |
| Likes, mutes, blocks | $0.001 per resource |

Other reported terms:
- The same resource is billed only once per UTC day.
- Pay-per-use accounts are capped at 3M post reads per month.
- Rate limits stay fixed regardless of spend; recent search is 450 requests per 15 minutes per app.

These figures are partly UNVERIFIED: docs.x.com/x-api/getting-started/pricing was blocked for fetching, and the per-resource prices above come from Upload-Post's 28 Sep 2026 summary.

**Owned Reads.** The official changelog (16 Apr 2026, effective 20 Apr) sets "Owned Reads" at $0.001 per resource. They cover these `GET /2/users/{id}/…` endpoints: bookmarks, blocking, muting, pinned_lists, tweets, mentions, liked_tweets, followers, following, owned_lists, followed_lists and list_memberships.
- Owned Reads appear to apply to the authenticated account's own data.
- UNVERIFIED: whether an OAuth end user's reads of their own data count as "owned" for a third-party app, or whether only the developer's own account does. This decides whether a self-map costs about $1 or about $10 per user.

**What was removed.** On 16 Apr 2026, "Following, Likes, and Quote-Posts via the API" were removed from all self-serve tiers. These are write actions, such as following an account on a user's behalf. The read lookups (/followers, /following, /liked_tweets) remain.
- Quote-tweet *lookup* availability under pay-per-use is UNVERIFIED.
- Since 4 May 2026, keyword search no longer returns retweets.
- The home timeline endpoint (`/timelines/reverse_chronological`) is not on the Owned Reads list. Its current availability and price are UNVERIFIED.

**OAuth for "offer up your feed".** X uses the OAuth 2.0 Authorization Code flow with PKCE. The relevant scopes are `tweet.read`, `users.read`, `follows.read`, `like.read`, `list.read`, `bookmark.read` and `offline.access`.
- Access tokens last 2 hours.
- A refresh token is issued only when `offline.access` is requested.
- The authorization code must be exchanged within 30 seconds.

This technically supports "connect your X and see yourself" at roughly $1–$15 per user for the ego graph plus likes.

**Cost wall: second-degree graphs.** Placing one person well needs the graph *around* them, for example who their 1,000 follows themselves follow. At about $0.01 per user object, that is on the order of $10,000 per ego network (back-of-envelope; my own calculation). Network-scale crawling is therefore not viable on self-serve. Enterprise pricing is unpublished.

**Developer Policy restrictions.** These are the binding constraints (docs.x.com/developer-terms/restricted-use-cases):
- **No sensitive inferences.** Developers may not derive, infer or store inferred data about users' political affiliation or beliefs, religion, race or ethnicity, sexual orientation, health, union membership and similar categories. The one exception is aggregate analysis that stores no personal identifiers.
  - The page does not mention a user-consent exception (UNVERIFIED whether one exists elsewhere).
  - A per-person worldview position derived from X API data plausibly violates this clause even when the person consents. **This is the single biggest platform risk to the brief's stated entry point.**
- **No surveillance or profiling.** Prohibited uses include tracking users, monitoring protests or rallies, tracking activist groups or unions, individual profiling and psychographic segmentation. Violations can lead to loss of access.
- **Linking an X account to an off-X identity** requires express opt-in consent.
- **Redistribution.** IDs are the preferred way to share data. Hydrated objects may be shared non-automatically, up to 50,000 per recipient per day, and must not be published publicly. Up to 1.5M post IDs may go to one entity per 30 days. Academic institutions may share IDs without limit for non-commercial research.
- **Other limits:**
  - No measuring X's aggregate platform metrics.
  - No using X content to train or fine-tune foundation or frontier models (Grok excepted). Fine-tuning a cheap stance classifier on X content is probably not a "foundation model"; that reading is UNVERIFIED and needs legal review.
  - One app per use case.

**Terms of Service on scraping.** X's terms, effective 15 Nov 2024, set $15,000 in liquidated damages for accessing more than 1M posts in 24 hours in violation of the terms. The Knight Institute called this a chill on independent research.

**The X data archive (user export).**
- **How it is obtained.** The user requests it in settings, verifies with an email or phone code, and receives a ZIP of HTML plus JSON "in a few days".
- **What it contains:**
  - The user's profile and posts.
  - DMs and media.
  - Followers and following lists.
  - Address book.
  - Lists created, followed or belonged to.
  - X's inferred interests and demographics about the user.
  - Ads seen and engaged with.
- **File-level detail** (Princeton Community Notes study protocol):
  - `following.js` holds **numeric account IDs only**.
  - `like.js` holds the IDs, links and **text** of liked posts.
  - `personalization.js` holds X's inferred interests.
  - `ad-impressions.js` holds targeting criteria.
- **Implications for the Arena:**
  - The archive is free and fairly complete for the *ego* view: own posts, the text of everything liked, and the follow list.
  - Because the user exercises their own data right, the Developer Agreement does not govern it.
  - Handles for followed accounts must still be resolved. That means either API lookups at $0.01 each, or matching against the IDs of accounts that have already consented (see the design section).
  - The archive also contains highly sensitive material: DMs, address book, X's inferred demographics and ad targeting. **Parse client-side and discard everything except the allow-listed files.**

### 2. AT Protocol / Bluesky, Farcaster, Mastodon

**AT Protocol is open by architecture.**
- All repository records are public and replicated through relays: posts, follows, likes, reposts, list memberships and even blocks.
- Jetstream re-serves the firehose as lightweight JSON. A filtered stream (posts only, zstd-compressed) runs to about 1% of the firehose's bandwidth. Running an instance can cost as little as a $5/month VPS.
- Bluesky runs four free public instances (jetstream1/2, us-east/us-west).
- Filters: `wantedCollections` (for example `app.bsky.graph.follow`, with prefix wildcards supported) and `wantedDids` (up to 10,000).
- No authentication is documented.
- Trade-off: Jetstream events are not cryptographically verified. The full firehose or Tap (released Dec 2025) gives verifiable sync.
- The unauthenticated AppView API serves follows and likes lookups. The rate limit was historically about 3,000 requests per 5 minutes; the current figure is UNVERIFIED.
- **Cost of a full Bluesky follow graph: effectively bandwidth plus storage.** It is about 46M registered accounts, with mobile MAU of about 10.4M in June 2026, down roughly 50% from the Q4 2024 peak.

**Labelers.**
- Anyone can run one by publishing an `app.bsky.labeler.service` record.
- Labels target accounts, profiles or individual records. Users subscribe to up to about 9 third-party labelers and choose hide, warn or ignore for each label.
- Labels are signed and distributed openly, so **any label is effectively public**.
- A worldview-cluster labeler would therefore attach a public political-tribe tag to accounts. **That is a targeting list.** It must only label accounts that have opted in, and preferably only at the user's own request.
- Feed generators are lower risk. A "bridge feed" serves posts from adjacent or opposing clusters to a subscriber without publishing anyone's cluster assignment.

**Permissioned data is coming but not ready.**
- The AT Protocol Spring 2026 roadmap names "non-public data with explicit access control" a major focus through summer 2026. At that stage it was a sketch proposal.
- OAuth permission sets shipped between late 2025 and early 2026.
- Implication: today, anything the Arena writes to a user's PDS is public. Private per-user map state must live in Arena storage or on the user's device until permissioned data lands.

**Farcaster.**
- The protocol was acquired by Neynar in January 2026. Daily active users "never surpassed the low-tens of thousands".
- Neynar's APIs give full follower and following lists. Pricing:

| Tier | Price | Credits |
|---|---|---|
| Free | $0 | 10M |
| Scale | $249/month | 60M |

- The graph is open but small and crypto-skewed. **Farcaster is useful as a pilot community, not as a representative map.**

**Mastodon / fediverse.**
- The API is open but the norms are hostile. Some instances explicitly refuse to be researched or indexed.
- The Mastodon API has no terms of service of its own, so consent is set per instance.
- A 2019 Mastodon network study was retracted after an open letter from admins and users. The complaints were an instance-terms violation, GDPR, and weak de-identification.
- Opt-in indexing (FEP-5feb) is the emerging norm.
- **Opt-in only. Never crawl.**

**Feasibility comparison:**

| Platform | Graph access | Cost | Terms fit for worldview mapping | Population |
|---|---|---|---|---|
| X API | Ego graph via OAuth; network crawl impractical | ~$1–15 per user ego; ~$10k per 2-hop ego | **Poor**: political-inference clause | Largest; the political center of gravity |
| X archive upload | Ego only (IDs, likes text, posts) | Free (UX friction: days of waiting) | Good: the user's own data | Same as X, but only motivated users |
| Bluesky / AT Proto | Entire public graph via Jetstream | ~Bandwidth | Good legally; labels are public, so a design risk | Mid-size, left-skewed and shrinking |
| Farcaster | Entire graph | Free to $249/month | Good | Tiny, crypto-skewed |
| Mastodon | Per instance | Free | Norms hostile to unconsented mapping | Small, fragmented |

### 3. Privacy law: inferred political opinion

**GDPR Art. 9.**
- "Political opinions" are special-category data. Processing them is prohibited unless an exception applies, such as explicit consent (9(2)(a)) or data "manifestly made public" by the person (9(2)(e)).
- *Meta v Bundeskartellamt* (C-252/21, 4 Jul 2023): sensitive data cannot be treated as manifestly made public merely because a user visits sites or apps. Processing that *reveals* special categories counts as special-category processing.
- *Schrems v Meta* (C-446/21, 4 Oct 2024):
  - 9(2)(e) requires that the person intended, by a clear affirmative act, to make the data public. It covers only what they actually made public.
  - A public statement about one's orientation does not license profiling from other data.
  - Data minimisation forbids open-ended aggregation for targeting.
- **Implication:** posting publicly on X does *not* make an inferred cluster position "manifestly public". For EU residents, placement needs explicit Art. 9(2)(a) consent. A DPIA (Art. 35) is near-certainly required for large-scale special-category profiling.
- Profiling rules (Art. 21 objection, Art. 22) also apply.

**EU political advertising regulation (TTPA, Reg. 2024/900).**
- Applies from 10 Oct 2025.
- Bans political-ad targeting that uses special-category data, such as inferred political opinion.
- The Arena is not an ad system. But **a map whose outputs feed campaign targeting would put downstream users in breach.** That is another reason never to export individual cluster assignments.

**EU DSA Art. 40.**
- The delegated act on researcher data access took effect 29 Oct 2025.
- Art. 40(12) gives researchers, including those at not-for-profit bodies, direct access to *publicly accessible* platform data for research on EU systemic risks. Civic discourse and electoral processes are among those risks.
- This could be a lawful route to X public data for an affiliated research partner. The conditions are independence, funding disclosure and publishing results. Eligibility for this project is UNVERIFIED.

**US law.**
- **CCPA/CPRA.**
  - Its "sensitive personal information" list includes religious or philosophical beliefs but **not political opinions**.
  - Inferences about SPI categories count as SPI.
  - Consumers have a "limit the use" right.
- **Colorado Privacy Act** (relevant to Benjamin in Boulder). Per the NatLawReview chart, its sensitive-data list covers religion, ethnicity, sexual orientation, health, citizenship and children's data, **not political opinion**. Colorado's rules also restrict "sensitive data inferences" (UNVERIFIED detail). Applicability thresholds and nonprofit coverage are UNVERIFIED.
- **Bottom line:** US law is weaker than GDPR on political opinion. Design to the GDPR standard anyway: the user base will be global, and the ethical stakes do not depend on jurisdiction.

**Scraping case law.**
- **hiQ v. LinkedIn.** The Ninth Circuit held that scraping public data likely does not violate the CFAA (reaffirmed after *Van Buren*). But LinkedIn won on breach of contract in Nov 2022, because hiQ had agreed to the user agreement and used fake profiles. The case ended in a consent judgment: $500k, a permanent injunction, and destruction of scraped data and models.
- **X v. Bright Data** (N.D. Cal.).
  - 2024 dismissal: contract claims over *public* data were preempted by copyright, since users own the content. The court warned against platform "information monopolies".
  - Nov 2024: X was allowed to amend. Trespass (server-load theory), access-based contract claims, and new CFAA/DMCA claims survived.
  - Bright Data counterclaimed on antitrust grounds.
  - Status in 2026: ongoing (UNVERIFIED final outcome).
- **Meta v. Bright Data (2024).** Logged-out scraping was not "use" under Meta's terms.
- **2025–26.** The frontier has moved to DMCA §1201 anti-circumvention theories (Google v. SerpApi; Reddit v. SerpApi et al.).
- **Lesson:** logged-out scraping of public X data may survive in court. But it is litigation-exposed, especially in X's preferred venues, and logging in creates a contract. And even where scraping is lawful, it does not cure the GDPR Art. 9 problem. **Do not scrape.**

### 4. Weaponization: a memetic map is a targeting map

- **Cambridge Analytica.** The FTC (6 Dec 2019) found that GSRApp deceived users about collecting identifiable data, harvested data from users *and their friends*, and did so for voter profiling and targeting. Up to 87M people were affected.
  - The structural lesson: **one person's consent was used to extract their friends' data.** Pulling a consenting user's follow graph is the same pattern unless the non-consenting nodes are kept anonymous.
- **Inference power.** Kosinski, Stillwell and Graepel (PNAS 2013) predicted Democrat vs. Republican with about 85% accuracy from Facebook Likes alone (n ≈ 58k). Sexual orientation and ethnicity were similarly predictable. Likes and follows *are* sensitive data once modelled.
- **Influence-operation mapping.** Graphika's business is mapping "communities" and "amplification dynamics" from public data. Its listed sectors include government and defense. The same cluster maps serve trust-and-safety work, brand targeting and state intelligence.
  - An open, high-resolution cluster map with named members is a free version of this product **for any state actor or harassment campaign.**
- **De-anonymization.** Narayanan and Shmatikov (2009) re-identified about one third of users in an *anonymized* Twitter graph, using Flickr as auxiliary data, with a 12% error rate. Graph structure alone fingerprints people. **Publishing an "anonymized" graph is not anonymization.**
- **Harassment surfaces on open protocols.** Bluesky blocks are public, and third-party tools (e.g., Clearsky) have used them to expose block relations. Any public cluster label becomes a brigading index.

**Threat model:**
- States and parties: targeting and repression.
- Harassers: cluster-wide doxxing or brigades.
- Advertisers: microtargeting.
- Employers or vetting services: X itself bans "extreme vetting".
- Researchers: unconsented reuse.
- The operator: mission drift or acquisition.

### 5. Manipulation of the arena and legitimacy

- **Bridging algorithms are gameable.** Community Notes' matrix-factorization bridging could be manipulated in production data: up to 10.7% of lower-quality notes could be pushed over consensus thresholds with fewer than 10 coordinated ratings (Selvam, Baxter et al., arXiv 2607.01824, 2026). X deployed mitigations. MOVE-layer rewards for cross-tribe "metabolizing" invite the same synthetic-consensus attack: tribes colluding to fake bridging.
- **Polis** (PCA plus k-means over agree/disagree votes) structurally limits flame wars by having no replies. Published descriptions do not claim robust sybil resistance.
- **Sybils and bots** distort the map, because cluster centroids shift under injected accounts, and they farm rewards. Mitigations:
  - Proof-of-personhood or stake on reward-eligible actions (not on viewing).
  - Account-age and activity priors.
  - Coordination detection, meaning the same ABC (actors, behaviors, content) heuristics used for influence operations.
  - Rate-limited, quadratic-weighted influence.
  - Keeping the bridging algorithm open but its parameters periodically re-fit.
- **Brigading and entryism into dialogue (MEET).** Mitigations: invitation by matched pairs or small groups, and no public thread pile-ons (the Anti-Debate format helps).
- **Legitimacy.** Whoever defines the axes and the cluster names holds a lot of power: naming a tribe is a political act.
  - Who governs the taxonomy, the model choices and data retention needs a credible answer. Options include a commons charter, an independent ethics board with veto, published model cards and cluster definitions, and member-elected stewards.
  - Contestability is essential: users must be able to dispute their placement and the label of their cluster.
  - Do not position the map as an "authoritative" depiction of a person.

---

## How this answers the governing question (layering + validation)

**Consent changes which layers are available.**
- The *social-graph* layer, the most powerful signal of belonging, is only legitimately buildable from:
  - (a) the consenting user's own ego graph (from the archive or OAuth);
  - (b) the fully public AT Protocol graph, used **in aggregate only**;
  - (c) edges *between* consenting users.
- *Embeddings* and *claims extraction* work on the user's own posts and liked-post text, which the archive provides. These are first-party data.
- *Classifiers* that infer stance about non-consenting people are a red line, not a layer.

**Recommended layering under these constraints:**
1. **Background terrain (aggregate, non-identifying).** Build cluster structure from the public AT Protocol graph and from consented X ego graphs.
   - Publish only cluster-level statistics.
   - Apply minimum-size thresholds (k ≥ 50 suggested) and differential-privacy noise to edge counts between clusters.
   - Prominent public accounts, such as officials and outlets, may be shown as *landmarks* only if a "public figure" policy is adopted. That policy is UNVERIFIED for GDPR safety: even public figures' inferred politics is Art. 9 data, so a safer variant shows landmarks only with their consent.
2. **Self-placement (private to the user).** Project the consenting user's ego graph, embeddings and claims onto the terrain. The result is shown only to them and stored locally or encrypted by default.
3. **Opt-in visibility.** The user may choose to appear to others, at a granularity they pick:
   - cluster only;
   - region;
   - an exact point;
   - a named node available for MEET matching.

**Validation within ethical bounds:**
- Self-report agreement. Ask placed users whether the placement "feels right", and whether its *reasons* feel right, so the inference is legible.
- Held-out stance surveys, for example a short values instrument at onboarding.
- Cross-layer agreement: graph-based versus claim-based placement for the same consenting person.
- Test-retest stability.
- Ground-truth validation can never use non-consenting people's private attributes.
- A **re-identification red-team** must pass before any aggregate release. Attempt Narayanan–Shmatikov style matching against public data.

---

## Reusable assets / design implications

**Recommended data strategy, in priority order:**

1. **AT Protocol native (primary for the open graph).**
   - Ingest Jetstream (`app.bsky.graph.follow`, `feed.like`, `feed.repost`, `feed.post`), or Tap for verifiable sync.
   - Users sign in with atproto OAuth to claim and see their placement.
   - Deliver the MEET layer as a **feed generator** ("bridge feeds"): low risk, nothing is published about anyone.
   - Offer a **labeler** only as self-applied, opt-in labels (for example "open to dialogos with X-cluster"). Never label by inference.
   - Honor deletes: unfollows, record deletions and account deactivation propagate within 24 hours.
   - Watch for permissioned data (2026) to hold private map state on users' own PDSes.
2. **X archive upload (primary for X users).**
   - Parse **in the browser** (local-first). Allow-list `tweets`, `like`, `following`, `follower` and `profile`. Drop DMs, address book, ad files and X's inferred demographics before anything leaves the device.
   - Upload only derived features: hashed follow IDs, embeddings and extracted claims. Or keep everything client-side.
   - Resolve follow IDs only against (a) other consenting users and (b) a small curated landmark set. Represent all other follows as salted-hash "dark matter" that shapes similarity but is never displayed or resolved.
3. **X OAuth (secondary, narrow).**
   - For users who will not wait days for an archive.
   - Use the scopes `follows.read`, `like.read`, `tweet.read`, `users.read` and `offline.access` (or skip offline access and refresh nothing).
   - Before relying on this path, **get legal review of the political-inference clause.** Possible compliance shape: the user's position is computed on device or shown only to them, and the server stores no identifier-linked inference. Whether that satisfies X is UNVERIFIED. Without a clear yes, launch with the archive path only.
4. **Farcaster** as an optional pilot community. **Mastodon** opt-in only, via user OAuth, honoring instance policies.
5. **Research partner route.** An EU-affiliated non-profit research partner could apply under DSA Art. 40(12) for public X data to validate aggregate terrain, published openly.

**Architecture patterns:**
- Local-first, user-held data.
- An explicit Art. 9(2)(a) consent screen that names "political opinions and beliefs".
- Per-layer consent toggles.
- One-click delete and export.
- A DPIA before launch.
- Retention limits: raw archives are never retained server-side; derived features expire after 12 months unless renewed.
- Aggregate releases pass both k-threshold and DP gates.
- A "why am I here" explanation for every placement.
- A dispute/correct affordance.
- Sybil-resistant identity only on MOVE (reward) actions.
- Open-source models and published cluster definitions.

**Existing alignment.** Ontography's PRD already states "NFR-3 Privacy: private by default; external fingerprints of real people labeled as machine inference" (/home/claude/auto-ontography-archive/docs/PRD.md:114). The Arena should *tighten* this: no external fingerprints of non-consenting real people at all, except opt-in landmarks.

## Red-line list for the spec

1. **No placement of any identifiable person on the map without their explicit, informed, revocable opt-in.** This covers inference, labels and named nodes.
2. **No inference of political opinion, religion, ethnicity, sexuality, health or union membership about non-consenting people.** Not even internally, and not even "just for the model". Non-consenting accounts exist only as aggregate or hashed signal.
3. **No public release of individual-level cluster assignments, edge lists or "anonymized" graphs.** Aggregates only, behind k-thresholds and DP noise, after a re-identification red-team.
4. **No scraping.** No logged-out crawling of X, no fake or sock-puppet accounts, no circumvention of rate limits or anti-bot measures.
5. **No use of X API data to derive or store identifier-linked political inferences** unless X's written terms or legal counsel clearly permit it.
6. **No sale, licensing or API export of cluster membership** to campaigns, advertisers, employers, vetting services, data brokers, law enforcement or intelligence agencies. Includes no TTPA-style political-ad targeting use. Publish a warrant canary or transparency report.
7. **No inferred labels published through AT Protocol labelers.** Self-applied, opt-in labels only.
8. **No server-side retention of raw archives, DMs, address books or X's ad and inference files.** Allow-list parsing, on device.
9. **No "friends' data" pattern (the Cambridge Analytica lesson).** One user's consent never exposes their connections' identities or inferred positions.
10. **No training or fine-tuning on X content in ways barred by X's terms.** No reuse of user data for unrelated model training.
11. **No reward eligibility in the MOVE layer without sybil resistance and coordination detection.** Bridging scores are audited for synthetic consensus.
12. **No unaccountable taxonomy.** Cluster names, axes and models are published, contestable and governed by a body that includes mapped communities. Users can dispute their placement and delete themselves at any time.
13. **No dark patterns in consent.** Separate consents per layer (graph / posts / likes / visibility). Declining keeps core access where possible.
14. **No mapping of minors.** Age-gate at 18, or apply the strictest regime available.

---

## Risks & open questions

- **The X political-inference clause** may make even consented, user-visible-only placement from API data non-compliant. Legal reading needed. (UNVERIFIED whether a consent exception exists.)
- **Owned Reads pricing scope** for third-party OAuth users. (UNVERIFIED)
- **Availability of the home timeline and quote lookups** under pay-per-use. (UNVERIFIED; docs.x.com pricing page blocked)
- **Archive friction.** A multi-day wait and a ZIP upload will cut conversion sharply. Consider an email-me-when-ready flow.
- **Representativeness.** Bluesky skews left and is shrinking. Opt-in X users self-select. The map will be biased toward the reflective, the curious and the already-bridging. Weight and caveat accordingly, and say so on the map.
- **Landmark / public-figure policy** under GDPR is unresolved.
- **Governance.** Who stewards the map is open: a commons charter, an ethics board, or member election. Acquisition or capture risk can be addressed with purpose-trust or steward-ownership structures (aligns with Benjamin's purpose-trust work; not researched here).
- **X v. Bright Data final outcome** and the 2026 DMCA §1201 cases. (UNVERIFIED)
- **Colorado Privacy Act** coverage of political inference and nonprofits. (UNVERIFIED)
- **Blocked pages** (permission timeouts):
  - docs.x.com/x-api/getting-started/pricing
  - docs.bsky.app/blog/jetstream
  - docs.bsky.app moderation
  - github.com/bluesky-social/jetstream
  - Bluesky developer guidelines (bsky.network/docs/support/developer-guidelines)
  - Bluesky block-implementation post

  Their facts were taken from secondary or mirror sources noted below.

---

## Sources

**X / Twitter**
- X Developer changelog (pay-per-use 6 Feb 2026; Owned Reads and removed write actions 16 Apr 2026; retweets out of search 4 May 2026; OAuth notes) — https://docs.x.com/updates/changelog
- X restricted use cases (sensitive inference, surveillance, redistribution, training) — https://docs.x.com/developer-terms/restricted-use-cases
- X OAuth 2.0 Authorization Code with PKCE (scopes, token lifetimes) — https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code
- Upload-Post, "X API pricing in 2026" (per-resource prices, caps, legacy migration; vendor source, checked 28 Sep 2026) — https://www.upload-post.com/x-api-pricing/
- X Help, "How to download your X archive" — https://help.x.com/articles/20170320
- Princeton Community Notes study, archive file details — https://communitynotes.cs.princeton.edu/data_collection_details_prol.pdf
- Knight Institute on X ToS liquidated damages (17 Oct 2024) — https://knightcolumbia.org/content/knight-institute-says-xs-new-terms-of-service-will-stifle-independent-research

**AT Protocol, Farcaster, fediverse**
- Jaz (Bluesky), "Jetstream" (2024) — https://jazco.dev/2024/09/24/jetstream/
- Jetstream API description (params, public hosts) — https://apis.io/apis/bluesky/bluesky-jetstream/
- Bluesky docs, Labels and moderation — https://www.docs.bsky.app/docs/advanced-guides/moderation
- AT Protocol Spring 2026 Roadmap (24 Mar 2026) — https://atproto.com/blog/2026-spring-roadmap
- Bluesky API rate limits discussion — https://github.com/bluesky-social/atproto/discussions/697
- Gigazine on Bluesky active users (Aug 2026) — https://gigazine.net/gsc_news/en/20260812-blueskys-active-user/
- Neynar developer pricing — https://neynar.com/developer
- Pulse, Neynar acquires Farcaster (21 Jan 2026) — https://www.pulse.bot/crypto/news/farcaster-founders-step-back-as-neynar-acquires-struggling-crypto-social-app-c18ce121-b2ec-4ab1-8985-409a46f07c15/
- Lisker & Mihaljević, "Data Ethics in the Fediverse" (2025) — https://arxiv.org/html/2505.07606v1

**Law and regulation**
- DLA Piper on CJEU C-252/21 — https://privacymatters.dlapiper.com/2023/07/eu-cjeus-landmark-decision-in-meta-vs-bundeskartellamt/
- Columbia GFoE on CJEU C-446/21 Schrems v Meta — https://globalfreedomofexpression.columbia.edu/cases/maximilian-schrems-v-meta-platforms-ireland-limited-schrems-iii/
- EU TTPA (Reg. 2024/900) overview — https://en.wikipedia.org/wiki/Transparency_and_Targeting_of_Political_Advertising_Regulation ; official text — https://eur-lex.europa.eu/eli/reg/2024/900/oj
- EC FAQ on DSA researcher data access — https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en
- Bastion, CCPA sensitive personal information — https://bastion.tech/learn/ccpa/sensitive-personal-information
- NatLawReview, sensitive data across states (Colorado) — https://natlawreview.com/article/updated-colorado-what-considered-sensitive-personal-information
- ZwillGen, hiQ v. LinkedIn wrap-up — https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/
- NatLawReview, X Corp loses vs Bright Data (2024) — https://natlawreview.com/article/x-corp-loses-battle-over-public-data-access
- Goldman blog, X v. Bright Data procedural history (Jan 2025) — https://blog.ericgoldman.org/archives/2025/01/catching-up-on-the-heavyweight-scraping-battle-between-x-and-bright-data-guest-blog-post.htm
- Web scraping legal landscape wiki (Meta v. Bright Data; 2025–26 DMCA cases) — https://publish.obsidian.md/twsc-public/Web+Scraping/Wiki/concepts/web-scraping-legal-landscape

**Weaponization and manipulation**
- CBS News, FTC finds Cambridge Analytica deceived users (6 Dec 2019) — https://www.cbsnews.com/news/ftc-finds-cambridge-analytica-deceived-facebook-users-2019-12-06 ; FTC opinion — https://www.ftc.gov/system/files/documents/cases/d09389_comm_final_opinionpublic.pdf
- Kosinski, Stillwell & Graepel, PNAS 2013 — https://pubmed.ncbi.nlm.nih.gov/23479631/
- Narayanan & Shmatikov, "De-anonymizing Social Networks" (2009) — https://arxiv.org/abs/0903.3276
- Graphika, How it works — https://graphika.com/how-it-works
- Selvam, Baxter et al., "Gaming Consensus" (arXiv 2607.01824, 2026) — https://tldr.takara.ai/p/2607.01824
- Gigazine on Polis 2.0 (Feb 2026) — https://www.gigazine.net/gsc_news/en/20260216-polis/

**Internal**
- Ontography PRD NFR-3 — /home/claude/auto-ontography-archive/docs/PRD.md
