from paho.mqtt.client import MQTTMessage
from sqlalchemy.orm import Session

from database.base import scoped_session
from database.models import Actuator, ActuatorAllocation
from project.utils import functions
from project.utils.const import Constants
from project.utils.mqtt import MqttClient


@scoped_session
def on_available_actuator_detected(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    register_topic = msg.payload.decode("utf8")
    print("actuator detected")
    print(register_topic)
    actuator = session.query(Actuator).filter(Actuator.local_id == register_topic).one_or_none()
    if actuator:
        ...
    else:
        actuator = Actuator(
            local_id=register_topic,
            type="NaN",
            unit=None,
            is_running=False
        )
        session.add(actuator)
        session.flush()
        actuator_allocate = ActuatorAllocation(
            greenhouse_id=Constants.greenhouse_id,
            actuator_id=actuator.id,
            north=0,
            west=0,
            height=0,
        )
        session.add(actuator_allocate)
        session.flush()

    actuator_topic = f"actuator/{actuator.id}"
    c.publish(register_topic, actuator_topic, 1)
    functions.info("new topic {}".format(actuator_topic))
