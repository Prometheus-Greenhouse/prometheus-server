from loguru import logger
from paho.mqtt.client import MQTTMessage

from database.base import Session_
from database.models import Sensor
from project.configs import BROKER
from project.utils import mqtt


class DetectorServices:
    def __init__(self):
        self.client = mqtt.Client()

    def on_message(self, client, userdata, msg: MQTTMessage):
        sensor_dict = mqtt.to_dict(msg.payload)
        with Session_.begin() as session:
            session.add(Sensor(

            ))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.publish("available", {"name": "hihi"}, 1)
            logger.success(f"{str(client)} connected")
        else:
            logger.error("Connect failed. Reconnecting...")
            client.connect(BROKER.host, BROKER.port)

    def run(self):
        client = self.client

        client.on_message = self.on_message
        client.on_connect = self.on_connect

        client.connect(BROKER.host, BROKER.port)
        client.subscribe("available", qos=1)
        client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
