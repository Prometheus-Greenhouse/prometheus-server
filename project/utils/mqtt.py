from enum import auto

import paho.mqtt.client
from fastapi_utils.enums import StrEnum


class MqttClient(paho.mqtt.client.Client):
    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        return super().publish(topic, payload, qos, retain, properties)


class EChannel(StrEnum):
    allow = auto()
    available = auto()
    actuator_available = auto()
