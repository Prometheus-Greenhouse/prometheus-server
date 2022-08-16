import sys

from loguru import logger
from paho.mqtt.client import MQTTMessage
from pre_commit.errors import FatalError
from sqlalchemy.orm import Session

from database.base import scoped_session
from project.configs import BROKER
from project.settings.logger import init_logging
from project.utils.mqtt import EChannel, to_dict, MqttClient

__version__ = "0.0.1"

init_logging()


@scoped_session
def on_sensor_data(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
    try:
        logger.success(f"received {msg.payload}")
        # sensor_record = SensorRecord(
        #     **to_dict(msg.payload)
        # )
        # session.add(sensor_record)
        # session.flush()
    except Exception as e:
        logger.exception(e)


def main():
    client = MqttClient()

    @client.topic_callback(EChannel.available)
    @scoped_session
    def on_available_sensor_detected(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
        sensor_dict = to_dict(msg.payload)
        print(sensor_dict)

        # sensor = Sensor(**sensor_dict)
        # session.add(sensor)
        # session.flush()
        new_topic = f"sensor/{1}"
        c.message_callback_add(new_topic, on_sensor_data)
        c.subscribe(new_topic)
        c.publish(EChannel.allow, new_topic, 1)

        logger.info("new topic {}".format(new_topic))

    @client.connect_callback()
    def on_connect(c: MqttClient, userdata, flags, rc):
        if rc == 0:
            # c.publish("available", {"address": "address", "type": "hihi", "unit": "unit"}, 1)
            logger.success(f"{str(c)} connected")
        else:
            logger.error("Connect failed. Reconnecting...")
            c.connect(BROKER.host, BROKER.port)

    @client.topic_callback("ESP8266/4")
    def on_sensor(c: MqttClient, userdata, msg: MQTTMessage, session: Session):
        print("recieved")
        print(msg.payload)

    client.connect(BROKER.host, BROKER.port)
    client.subscribe(EChannel.available, qos=1)
    # interval task
    # def run(c:MqttClient):
    #     while True:
    #         print("--->")
    #         c.publish("")
    #         time.sleep(4)
    # p = Process()
    # interval task -->
    client.loop_forever()


# @app.post("/on")
# def on():
#     client.publish("ESP8266/4", "1")
#
#
# @app.post("/off")
# def off():
#     client.publish("ESP8266/4", "0")
#
#
# client.loop_start()

if __name__ == "__main__":
    # uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True, env_file=".env")
    try:
        main()
    except FatalError as e:
        logger.error('A fatal error occurred: %s' % e)
        sys.exit(2)
    except KeyboardInterrupt:
        logger.info("Exit...")
        sys.exit(2)
