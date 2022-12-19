from apps.enums.enums import Temperature, Humidity, SoilMoisture, ERun, EDayCycle, Water


class DecisionData:
    # dayc: EDayCycle = "dayc"
    # temperature: Temperature = "temperature"
    # humidity: Humidity = "humidity"
    # soil: Soil = "soil"
    # run: ERun = "run"
    __annotations__ = {
        "dayc": EDayCycle,
        "temperature": Temperature,
        "humidity": Humidity,
        "soil": SoilMoisture,
        "water": Water,
        "run": ERun,
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
