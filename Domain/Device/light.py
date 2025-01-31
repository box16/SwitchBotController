from Domain.Device.device import Device, DeviceID, DeviceName, DeviceType
from dataclasses import dataclass
from typing import Union
from utility.exception import LightException, ColorException


@dataclass(frozen=True)
class ColorCode:
    value: int

    def __post_init__(self):
        if not (0 <= self.value <= 255):
            raise ColorException("カラーコードは0~255で指定してください")

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


@dataclass(frozen=True)
class Brightness:
    value: int

    def __post_init__(self):
        if not self.value:
            raise LightException("空です")
        if isinstance(self.value, str):
            tmp = int(self.value)
            object.__setattr__(self, "value", tmp)
        if not isinstance(self.value, int):
            raise LightException("intかstrで指定してください")
        if (self.value < 0) or (self.value > 100):
            raise LightException(f"明るさは0~100の範囲です : {self.value}")

    def get(self):
        return self.value


@dataclass(frozen=True)
class ColorTemperature:
    value: int

    def __post_init__(self):
        if not self.value:
            raise LightException("空です")
        if not isinstance(self.value, int):
            raise LightException("intで指定してください")
        if (self.value < 2700) or (self.value > 6500):
            raise LightException(f"色温度は2700~6500の範囲です : {self.value}")

    def get(self):
        return self.value


class Light(Device):
    def __init__(
        self,
        id: Union[DeviceID, str, int],
        name: Union[DeviceName, str],
    ):
        super().__init__(id, name, DeviceType.LIGHT)
        self.brightness = Brightness(100)
        self.color = Color(255, 255, 255)
        self.color_temp = ColorTemperature(6500)

    def set_brightness(self):
        pass

    def set_color(self):
        pass

    def set_color_temperature(self):
        pass
