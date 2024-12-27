from dataclasses import dataclass


@dataclass(frozen=True)
class Device:
    id: str
    name: str
    type: str
