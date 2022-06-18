class ESP8266:
    topic: str = "ESP8266/4"


class DeviceRepository:
    def get_esp8266(self):
        return ESP8266()
