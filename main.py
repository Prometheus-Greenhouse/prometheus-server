import sys
from datetime import datetime

from loguru import logger
from paho.mqtt.client import MQTTMessage
from pre_commit.errors import FatalError
from sqlalchemy.orm import Session

from database.base import scoped_session
from database.models import SensorRecord, Sensor
from project.configs import BrokerConfigs
from project.settings.logger import init_logging
from project.utils.mqtt import EChannel, MqttClient

__version__ = "0.0.1"
init_logging()

client = MqttClient()
broker = BrokerConfigs()


@client.connect_callback()
def on_connect(c: MqttClient, userdata, flags, rc):
    if rc == 0:
        # c.publish("available", {"address": "address", "type": "hihi", "unit": "unit"}, 1)
        logger.info(broker.host, broker.port)
        logger.success(f"{str(c)} connected")
    else:
        logger.error("Connect failed. Reconnecting...")
        c.connect(broker.host, broker.port)


@scoped_session
def on_sensor_data(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    logger.success(f"received {msg.payload}")
    sensor_id = msg.topic.split("/")[1]
    session.add(
        SensorRecord(
            greenhouse_id=1,
            sensor_id=sensor_id,
            weather="",
            number_of_week=str(datetime.now().isoweekday()),
            sensor_data=msg.payload.decode("utf8"),
        )
    )


@client.topic_callback(EChannel.available)
@scoped_session
def on_available_sensor_detected(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    register_topic = msg.payload.decode("utf8")
    # update sensor
    sensor = session.query(Sensor).filter(Sensor.local_id == register_topic).one_or_none()
    if sensor:
        ...
    else:
        # insert new sensor
        sensor = Sensor(
            address="random_string",
            local_id=register_topic,
            type="",
            unit=""
        )
        session.add(sensor)
        session.flush()

    sensor_topic = f"sensor/{sensor.id}"
    c.message_callback_add(sensor_topic, on_sensor_data)
    c.subscribe(sensor_topic)
    logger.debug(register_topic)
    c.publish(register_topic, sensor_topic, 1)

    logger.info("new topic {}".format(sensor_topic))


def main():
    @client.topic_callback("ESP8266/4")
    def on_sensor(c: MqttClient, userdata, msg: MQTTMessage):
        print("recieved")
        print(msg.payload)

    client.connect(broker.host, broker.port)
    client.subscribe(EChannel.available, qos=1)
    # client.subscribe("ESP8266/4")
    # interval task
    # interval task -->
    client.loop_forever()


if __name__ == "__main__":
    # uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True, env_file=".env")
    while True:
        try:
            main()
            print("run main")
        except FatalError as e:
            logger.error('A fatal error occurred: %s' % e)
            sys.exit(2)
        except KeyboardInterrupt:
            logger.info("Exit...")
            sys.exit(2)
        except Exception as e:
            logger.exception(e)
            continue
