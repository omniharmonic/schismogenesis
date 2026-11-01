# ADR-033: Argument-role gate

Status: accepted for the pilot. Date: 2026-11-01.

Quote and entailment checks confirm words, not their job in an argument. Both blind audits found
that a concession, or a reconstruction of someone else's view, can pass as an assertion. A separate
reader now labels every accepted claim with the surrounding paragraphs in view, and records
`claim.argument_role` and `claim.role_fair`.

A claim leaves `accepted` if it is unfair, or if its role is `others_view`, `setup`, `ironic` or
`unclear`. Fair concessions, conditionals and hypotheticals stay, because their proposition keeps
the limit.

Context is clipped to 500 characters either side, so distant qualifications stay invisible, and the
reader is a Claude agent, not a calibrated instrument. The rate of about 3% is a floor. For
authors who reconstruct others at length (Thiel, Land), this gate should get whole-essay context.
