from datetime import datetime

from loguru import logger
from paho.mqtt.client import MQTTMessage
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.base import scoped_session
from database.models import SensorRecord, Sensor, SensorAllocation
from project.utils import functions
from project.utils.const import Constants
from project.utils.mqtt import MqttClient


@scoped_session
def on_sensor_data(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    sensor_id = msg.topic.split("/")[1]
    # sensor not allocate
    is_allocated = session.query(1).filter(
        SensorAllocation.sensor_id == sensor_id, SensorAllocation.greenhouse_id == Constants.greenhouse_id
    ).one_or_none()
    if not is_allocated:
        print("sensor not allocate")
        return
    # sensor allocate
    try:
        sensor_data = msg.payload.decode("ascii")
        logger.info("sensor: {}:{}", msg.topic, sensor_data)
        session.add(
            SensorRecord(
                greenhouse_id=Constants.greenhouse_id,
                sensor_id=sensor_id,
                weather="",
                number_of_week=str(datetime.now().isoweekday()),
                sensor_data=sensor_data
            )
        )
        session.flush()
    except UnicodeDecodeError as e:
        functions.logger.exception(e)
    except IntegrityError:
        pass


@scoped_session
def on_available_sensor_detected(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    register_topic = msg.payload.decode("utf8")
    logger.info(register_topic)
    # update sensor
    sensor = session.query(Sensor).filter(Sensor.local_id == register_topic).one_or_none()
    if sensor:
        ...
    else:
        # insert new sensor
        sensor = Sensor(
            address="random_string",
            local_id=register_topic,
            type="NaN",
            unit="NaN"
        )
        session.add(sensor)
        session.flush()
        sensor_allocate = SensorAllocation(
            sensor_id=sensor.id,
            greenhouse_id=Constants.greenhouse_id,
        )
        session.add(sensor_allocate)
        session.flush()

    sensor_topic = f"sensor/{sensor.id}"
    c.message_callback_add(sensor_topic, on_sensor_data)
    c.subscribe(sensor_topic)
    logger.debug(register_topic)
    c.publish(register_topic, sensor_topic, 1)

    logger.info("new topic {}".format(sensor_topic))


def resubscribe_sensor(c: MqttClient, session: Session):
    sensors = session.query(Sensor).all()
    for sensor in sensors:
        logger.info("resubscribe sensor topic {}", sensor.id)
        sensor_topic = f"sensor/{sensor.id}"
        c.message_callback_add(sensor_topic, on_sensor_data)
        c.subscribe(sensor_topic)
        c.publish(sensor.local_id, sensor_topic, 1)
