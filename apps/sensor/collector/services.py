from project.configs import BROKER
from project.utils import mqtt


class CollectorService:
    def __init__(self):
        self.client = mqtt.MqttClient()

    def run(self):
        self.client.connect(BROKER.host, BROKER.port)
        self.client.message