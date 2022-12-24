import time
from multiprocessing import Process

from loguru import logger

from apps.actuator.services import on_available_actuator_detected
from apps.sensor.services import on_available_sensor_detected, resubscribe_sensor
from database.base import scoped_session
from sqlalchemy.orm import Session

from project.configs import BrokerConfigs
from project.utils.mqtt import MqttClient, EChannel


class IotService:
    def __init__(self):
        self.running_flag = True
        self.client = MqttClient()
        self.process = Process(target=self.client.loop_start())
        self.broker = BrokerConfigs()

    def run(self):
        self.mqtt_listener()
        self.process.start()
        logger.info("mqtt client looping...")

    def stop(self):
        self.client.loop_stop()
        logger.info("mqtt client loop stop")
        time.sleep(0.1)
        self.process.join()
        logger.info("shutdown iot service")

    @scoped_session
    def on_connect(self, c: MqttClient, userdata, flags, rc, session: Session):
        if rc == 0:
            logger.info(self.broker.host, self.broker.port)
            logger.success(f"{str(c)} connected")
            resubscribe_sensor(c, session)
            c.message_callback_add(EChannel.available, on_available_sensor_detected)
            c.message_callback_add("actuator_available", on_available_actuator_detected)

            c.subscribe(EChannel.available, qos=1)
            c.subscribe("actuator_available", qos=1)
        else:
            logger.error("Connect failed. Reconnecting...")
            c.connect(self.broker.host, self.broker.port)

    def mqtt_listener(self):
        logger.info("run mqtt listener")
        logger.info(EChannel.actuator_available)
        self.client.on_connect = self.on_connect

        self.client.connect(self.broker.host, self.broker.port)
