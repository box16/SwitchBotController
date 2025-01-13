from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int
