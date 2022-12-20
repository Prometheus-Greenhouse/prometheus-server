from typing import Any

from apps.enums.enums import EDayCycleValue, EWaterValue, ETemperatureValue, EHumidityValue, ESoilMoistureValue, ERunValue, ESensorType


class DecisionTreeDataModel:
    __metadata__ = {}
    _map = {
        EDayCycleValue: "dayc",
        EWaterValue: "water",
        ETemperatureValue: "temperature",
        EHumidityValue: "humidity",
        ESoilMoistureValue: "soil",
        ERunValue: "run",
    }

    def __init__(self,
                 day_cycle: EDayCycleValue,
                 water: EWaterValue,
                 temperature: ETemperatureValue,
                 humidity: EHumidityValue,
                 soil: ESoilMoistureValue,
                 run: ERunValue,
                 ):
        self.dayc = day_cycle
        self.water = water
        self.temperature = temperature
        self.humidity = humidity
        self.soil = soil
        self.run = run

    @classmethod
    def from_raw_value(cls,
                       day_cycle: EDayCycleValue,
                       water: float,
                       temperature: float,
                       humidity: float,
                       soil: float,
                       run: ERunValue,
                       ):
        return cls(day_cycle,
                   cls.get_value_group(water, ESensorType.WATER),
                   cls.get_value_group(temperature, ESensorType.TEMPERATURE),
                   cls.get_value_group(humidity, ESensorType.HUMIDITY),
                   cls.get_value_group(soil, ESensorType.SOIL_MOISTURE),
                   run)

    @staticmethod
    def get_value_group(raw_value, type) -> Any:
        for key, item in DecisionTreeDataModel.__metadata__[type].items():
            try:
                if item["cLeft"] <= raw_value <= item["cRight"]:
                    return key
            except Exception:
                continue

    def get(self, type):
        if type not in self._map:
            raise ValueError("type not in _map {}".format(type))
        return getattr(self, self._map.get(type))

    def __repr__(self):
        return "[dayc: {} water: {} temp: {} hum: {} soil: {} run: {}]".format(self.dayc, self.water, self.temperature, self.humidity, self.soil, self.run)
