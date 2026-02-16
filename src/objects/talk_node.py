"""Class representation of a Geneforge talk node."""

import dataclasses

@dataclasses.dataclass(frozen=True)
class TalkNode:
    node_id: int
    tag: int
    state: int
    next_state: int
    condition: str
    text: list[str]
    action: str
