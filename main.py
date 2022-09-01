from dotenv import load_dotenv

load_dotenv(".env")
import argparse
import sys
from datetime import datetime

from loguru import logger
from paho.mqtt.client import MQTTMessage
from pre_commit.errors import FatalError
from sqlalchemy.orm import Session

from database.base import scoped_session
from database.models import SensorRecord, Sensor, SensorAllocation
from project.configs import BrokerConfigs
from project.settings.logger import init_logging
from project.utils.mqtt import EChannel, MqttClient

__version__ = "0.0.1"
init_logging()

client = MqttClient()
broker = BrokerConfigs()
GREENHOUSE_ID = 1


def resubscribe(c: MqttClient, session: Session):
    sensors = session.query(Sensor).all()
    for sensor in sensors:
        print("resubscribe" + str(sensor.id))
        sensor_topic = f"sensor/{sensor.id}"
        c.message_callback_add(sensor_topic, on_sensor_data)
        c.subscribe(sensor_topic)
        c.publish(sensor.local_id, sensor_topic, 1)


@client.connect_callback()
@scoped_session
def on_connect(c: MqttClient, userdata, flags, rc, session: Session):
    if rc == 0:
        # c.publish("available", {"address": "address", "type": "hihi", "unit": "unit"}, 1)
        logger.info(broker.host, broker.port)
        logger.success(f"{str(c)} connected")
        resubscribe(c, session)
    else:
        logger.error("Connect failed. Reconnecting...")
        c.connect(broker.host, broker.port)


@scoped_session
def on_sensor_data(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    logger.success(f"received {msg.payload}")
    sensor_id = msg.topic.split("/")[1]
    # sensor not allocate
    is_allocated = session.query(1).filter(
        SensorAllocation.sensor_id == sensor_id, SensorAllocation.greenhouse_id == GREENHOUSE_ID
    ).one_or_none()
    if not is_allocated:
        print("sensor not allocate")
        return
    # sensor allocate
    session.add(
        SensorRecord(
            greenhouse_id=GREENHOUSE_ID,
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
    print(register_topic)
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
        sensor_allocate = SensorAllocation(
            sensor_id=sensor.id,
            greenhouse_id=GREENHOUSE_ID,
        )
        session.add(sensor_allocate)
        session.flush()

    sensor_topic = f"sensor/{sensor.id}"
    c.message_callback_add(sensor_topic, on_sensor_data)
    c.subscribe(sensor_topic)
    logger.debug(register_topic)
    c.publish(register_topic, sensor_topic, 1)

    logger.info("new topic {}".format(sensor_topic))


def main():
    client.connect(broker.host, broker.port)
    client.subscribe(EChannel.available, qos=1)
    # client.subscribe("ESP8266/4")
    # interval task
    # interval task -->
    client.loop_forever()


if __name__ == "__main__":
    version = "0.0.1"
    banner = f"""
         _     ___  ____
        | |   / _ \\/ ___|
        | |  | | | \\___ \\
        | |__| |_| |___) |
        |_____\\___/|____/
         =========|_|==============
          :: Prometheus ::                (v{version})
        """
    parser = argparse.ArgumentParser(usage=banner)
    parser.add_argument("-e", "--env-file", help="Set env file, default=all")
    # parser.add_argument("-v", "--version", action="store_true", help="print the version number and exit")
    parser.add_argument("-v", "--version", action="store_true", help="print the version number and exit")
    args = parser.parse_args()
    if args.version:
        print(__version__)

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
