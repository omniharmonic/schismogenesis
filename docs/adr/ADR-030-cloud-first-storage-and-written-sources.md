# ADR-030: Light source storage and written works as sources

Status: accepted (D-31.10). Date: 2026-10-31.

## Source storage
Raw sources go on plain disk under `ARENA_SOURCE_DIR`, stored by content hash through
`arena_core.storage.FileSourceStore`. `transcript.storage_ref` holds the returned reference. Moving
to S3-compatible storage later means one new class and a file copy. No object-store service runs
for now. Postgres keeps the `private` schema, since it already exists and costs nothing.

The system still needs the full text, because quote anchoring must find each exact quote in its
source. What stays restricted is republication, for copyright and platform-terms reasons, not
secrecy.

## Written sources
Migration `0003_written_sources` keeps the pipeline's shape. An episode is any content item, a
transcript is its text, and a segment is a located span.
- `episode.format` adds book, book_chapter, blog_post, op_ed, lecture, letter, dissertation, filing.
- `channel.platform` adds blog, book_publisher, journal, filing.
- `transcript.route` adds `written_source`.
- `appearance_role` adds author and co_author.
- `segment` and `chunk` timing becomes optional. Each needs timing or a `locator`, and a database
  constraint enforces that. `claim` also gains `locator`.
- `episode.authorship` records own_name, pseudonymous, co_authored, corporate or
  ghostwritten_or_edited.

Claim extraction, quote anchoring and the NLI gate apply unchanged.

## Needed before written extraction runs (P2)
- **Voice:** extraction must separate the author's position from what they quote, report or
  caricature. Speech-act rules and gold examples need to cover this.
- **Esoteric and ironic writing:** a literal reading of a deliberately layered text can state the
  opposite of its intent. Such claims stay `stated` only for what the sentence says; any deeper
  reading is `inferred`, which is never scored and always labelled.
- **Co-authors:** `segment.person_id` holds one person. Co-authored and corporate texts need a rule
  for who holds the stance. The default is to record every author in `appearance` and leave those
  stances unassigned to one person until reviewed.
- **Time:** `stance.as_of` already holds the publication date, so a 1995 book reads as a 1995
  position. Clustering must decide how old stances count.
- **Volume:** prolific writers produce far more claims. Clustering must normalize per person.
- **Language:** a non-English source needs a rule for quoting the original beside a translated
  proposition. The anchor always stays on the original text.
- **Lawful copies:** books and paywalled texts are used only from copies Benjamin lawfully holds,
  are never committed to git, and appear publicly only as short quotes with citations.
