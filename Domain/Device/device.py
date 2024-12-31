from dataclasses import dataclass


# TODO ルールを内包させる
@dataclass(frozen=True)
class Device:
    id: str
    name: str
    type: str
