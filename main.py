from dotenv import load_dotenv

from database.models import Greenhouse
from project.utils.const import Constants

load_dotenv(".env")
from apps.sensor.services import resubscribe_sensor, on_available_sensor_detected

from apps.actuator.services import on_available_actuator_detected
import argparse
import sys

from loguru import logger
from pre_commit.errors import FatalError
from sqlalchemy.orm import Session

from database.base import scoped_session, Session_
from project.configs import BrokerConfigs
from project.settings.logger import init_logging
from project.utils.mqtt import EChannel, MqttClient

__version__ = "0.0.1"
init_logging()

broker = BrokerConfigs()


@scoped_session
def on_connect(c: MqttClient, userdata, flags, rc, session: Session):
    if rc == 0:
        logger.info(broker.host, broker.port)
        logger.success(f"{str(c)} connected")
        resubscribe_sensor(c, session)
    else:
        logger.error("Connect failed. Reconnecting...")
        c.connect(broker.host, broker.port)


def main():
    # with Session_.begin() as session:
    #     session.add(
    #         SensorRecord(
    #             greenhouse_id=1,
    #             sensor_id=8,
    #             weather="",
    #             number_of_week=str(datetime.now().isoweekday()),
    #             sensor_data="100"
    #         )
    #     )
    #     session.commit()
    client = MqttClient()

    client.on_connect = on_connect
    client.message_callback_add(EChannel.available, on_available_sensor_detected)
    client.message_callback_add(EChannel.actuator_available, on_available_actuator_detected)

    client.connect(broker.host, broker.port)
    client.subscribe(EChannel.available, qos=1)
    client.subscribe(EChannel.actuator_available, qos=1)
    # client.subscribe("ESP8266/4")
    # interval task
    # interval task -->
    print("looping...")
    client.loop_forever()


def startup():
    s: Session = Session_()
    gh = s.query(Greenhouse).filter(Greenhouse.label == "default").first()
    print("default greenhouse {}".format(gh.id))
    Constants.greenhouse_id = gh.id
    s.close()


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

    startup()
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
