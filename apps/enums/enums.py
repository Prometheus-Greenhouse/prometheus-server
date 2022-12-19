from enum import Enum, auto
from fastapi_utils.enums import StrEnum


class EDayCycle(str, Enum):
    DAY = "DAY"
    NIGHT = "NIGHT"


class Water(StrEnum):
    HIGH = auto()
    MID = auto()
    LOW = auto()


class SoilMoisture(str, Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Humidity(str, Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Temperature(str, Enum):
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class ERun(str, Enum):
    Y = "Y"
    N = "N"


class ESensorType(str, Enum):
    WATER = "WATER"
    SOIL_MOISTURE = "SOIL_MOISTURE"
    HUMIDITY = "HUMIDITY"
    TEMPERATURE = "TEMPERATURE"
    NaN = "NaN"
