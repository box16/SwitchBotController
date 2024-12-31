from dataclasses import dataclass


# TODO ルールを内包させる
@dataclass(frozen=True)
class Group:
    id: str
    name: str
