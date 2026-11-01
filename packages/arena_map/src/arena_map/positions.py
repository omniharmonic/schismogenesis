"""Compare people by the positions they hold, not by exact claim matches (D-31.13).

Only questions both people addressed count. A blank never counts as disagreement.
"""

from dataclasses import dataclass
from itertools import combinations

# question key -> position keys
Holdings = dict[str, set[str]]


@dataclass(frozen=True)
class Alignment:
    a: str
    b: str
    shared_questions: int
    same_position: int

    @property
    def score(self) -> float | None:
        return self.same_position / self.shared_questions if self.shared_questions else None


def align(holdings: dict[str, Holdings]) -> list[Alignment]:
    """Each pair: on questions both addressed, how many had a position in common."""
    pairs = []
    for a, b in combinations(sorted(holdings), 2):
        shared = holdings[a].keys() & holdings[b].keys()
        same = sum(bool(holdings[a][q] & holdings[b][q]) for q in shared)
        pairs.append(Alignment(a, b, len(shared), same))
    return pairs


def groups(pairs: list[Alignment], min_shared: int = 3, min_score: float = 0.75) -> list[list[str]]:
    """Connected groups over well-evidenced, strong alignments. Not yet clusters."""
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for pair in pairs:
        find(pair.a), find(pair.b)
        if pair.shared_questions >= min_shared and (pair.score or 0) >= min_score:
            parent[find(pair.a)] = find(pair.b)
    found: dict[str, list[str]] = {}
    for name in parent:
        found.setdefault(find(name), []).append(name)
    return sorted((sorted(g) for g in found.values() if len(g) > 1), key=len, reverse=True)
