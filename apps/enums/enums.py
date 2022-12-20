from enum import Enum


class EDayCycleValue(str, Enum):
    DAY = "DAY"
    NIGHT = "NIGHT"


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
            EDayCycleValue: ESensorType.DAYC,
            EWaterValue: ESensorType.WATER,
            ESoilMoistureValue: ESensorType.SOIL_MOISTURE,
            EHumidityValue: ESensorType.HUMIDITY,
            ETemperatureValue: ESensorType.TEMPERATURE,
            ERunValue: ESensorType.RUN
        }.get(type)
