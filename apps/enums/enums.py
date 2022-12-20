from datetime import datetime
from enum import Enum


class EDayCycleValue(str, Enum):
    DAY = "DAY"
    NIGHT = "NIGHT"

    @classmethod
    def from_current_time(cls, timestamp: datetime) -> 'EDayCycleValue':
        return EDayCycleValue.DAY if (5 <= timestamp.hour <= 17) else EDayCycleValue.NIGHT


class EWaterValue(str, Enum):
    HIGH = "HIGH"
    # MID = "MID"
    LOW = "LOW"


class ESoilMoistureValue(str, Enum):
    HIGH = "HIGH"
    # MID = "MID"
    LOW = "LOW"


class EHumidityValue(str, Enum):
    HIGH = "HIGH"
    # MID = "MID"
    LOW = "LOW"


class ETemperatureValue(str, Enum):
    HIGH = "HIGH"
    # MID = "MID"
    LOW = "LOW"


class ERunValue(str, Enum):
    Y = "Y"
    N = "N"


class ESensorType(str, Enum):
    DAYC = "DAYC"
    WATER = "WATER"
    SOIL_MOISTURE = "SOIL_MOISTURE"
    HUMIDITY = "HUMIDITY"
    TEMPERATURE = "TEMPERATURE"
    RUN = "RUN"
    NaN = "NaN"

    @staticmethod
    def get_sensor_type(type):
        return {
            EDayCycleValue: "dayc",
            EWaterValue: "water",
            ESoilMoistureValue: "soil",
            EHumidityValue: "humidity",
            ETemperatureValue: "temperature",
            ERunValue: "run"
        }.get(type)
