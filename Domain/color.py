from dataclasses import dataclass
from utility.exception import ColorException


@dataclass(frozen=True)
class ColorCode:
    value: int

    def __post_init__(self):
        try:
            if not (0 <= self.value <= 255):
                raise ColorException("カラーコードは0~255で指定してください")
        except Exception as e:
            raise ColorException(e)

    def get(self):
        return self.value


@dataclass(frozen=True)
class Color:
    red: ColorCode
    green: ColorCode
    blue: ColorCode

    def __post_init__(self):
        object.__setattr__(self, "red", self._to_color_code(self.red))
        object.__setattr__(self, "green", self._to_color_code(self.green))
        object.__setattr__(self, "blue", self._to_color_code(self.blue))

    @staticmethod
    def _to_color_code(value):
        if isinstance(value, ColorCode):
            return value
        elif isinstance(value, int):
            return ColorCode(value)
        else:
            raise ColorException(f"ColorCodeかintで指定してください")
