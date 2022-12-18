from enum import Enum


class EDayCycle(str, Enum):
    DAY = "DAY"
    NIGHT = "NIGHT"


class Temperature(str, Enum):
    HOT = "HOT"
    COOL = "COOL"
    MID = "MID"


class Humidity(str, Enum):
    HIGH = "HIGH"
    NORMAL = "NORMAL"


class Soil(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"


class ERun(str, Enum):
    Y = "Y"
    N = "N"


class ESensorType(str, Enum):
    HUMIDITY = "HUMIDITY"
    TEMPERATURE = "TEMPERATURE"
    SOIL_MOISTURE = "SOIL_MOISTURE"
    WATER = "WATER"
    NaN = "NaN"
