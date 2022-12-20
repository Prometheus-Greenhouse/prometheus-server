from apps.enums.enums import ETemperatureValue, EHumidityValue, ESoilMoistureValue, ERunValue, EDayCycleValue, EWaterValue


class DecisionData:
    # dayc: EDayCycle = "dayc"
    # temperature: Temperature = "temperature"
    # humidity: Humidity = "humidity"
    # soil: Soil = "soil"
    # run: ERun = "run"
    __annotations__ = {
        "dayc": EDayCycleValue,
        "temperature": ETemperatureValue,
        "humidity": EHumidityValue,
        "soil": ESoilMoistureValue,
        "water": EWaterValue,
        "run": ERunValue,
    }

    def __init__(self,
                 day_cycle,
                 temperature,
                 humidity,
                 soil,
                 run,
                 ):
        self.dayc = day_cycle
        self.temperature = temperature
        self.humidity = humidity
        self.soil = soil
        self.run = run

    def __str__(self):
        return f"{chr(123)}{self.dayc}, {self.temperature}, {self.humidity}, {self.soil}, {self.run}{chr(125)}"

    def __repr__(self):
        return f"{chr(123)}{self.dayc}, {self.temperature}, {self.humidity}, {self.soil}, {self.run}{chr(125)}"
