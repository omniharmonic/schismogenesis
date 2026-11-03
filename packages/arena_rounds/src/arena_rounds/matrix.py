"""The room's vote matrix: participants by statements, +1 agree, -1 disagree, 0 pass, nan unseen."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class VoteMatrix:
    participants: list[str]
    statements: list[str]
    values: np.ndarray

    @classmethod
    def from_rows(cls, rows: list[tuple[str, str, int]]) -> "VoteMatrix":
        participants = sorted({r[0] for r in rows})
        statements = sorted({r[1] for r in rows})
        p_index = {p: i for i, p in enumerate(participants)}
        s_index = {s: j for j, s in enumerate(statements)}
        values = np.full((len(participants), len(statements)), np.nan)
        for participant, statement, vote in rows:
            values[p_index[participant], s_index[statement]] = vote
        return cls(participants, statements, values)

    def votes_per_participant(self) -> np.ndarray:
        return (~np.isnan(self.values)).sum(1)

    def subset(self, rows: np.ndarray) -> "VoteMatrix":
        kept = [p for p, keep in zip(self.participants, rows, strict=True) if keep]
        return VoteMatrix(kept, self.statements, self.values[rows])
