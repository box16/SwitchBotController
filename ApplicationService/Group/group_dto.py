from dataclasses import dataclass


@dataclass(frozen=True)
class Group:
    id: str
    name: str
