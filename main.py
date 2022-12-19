import time
from multiprocessing import Process

from dotenv import load_dotenv

load_dotenv(".env")

from apps.decisiontree.services import DecisionTreeService

from fastapi import FastAPI, Depends
import uvicorn

from database.models import Greenhouse
from project.utils.const import Constants

from apps.sensor.services import resubscribe_sensor, on_available_sensor_detected

from apps.actuator.services import on_available_actuator_detected
import argparse

from loguru import logger
from sqlalchemy.orm import Session

from database.base import scoped_session, Session_, get_session
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


class IotService:
    def __init__(self):
        self.running_flag = True
        self.client = MqttClient()
        self.process = Process(target=self.client.loop_start())

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

    def mqtt_listener(self):
        logger.info("run mqtt listener")
        self.client.on_connect = on_connect
        self.client.message_callback_add(EChannel.available, on_available_sensor_detected)
        self.client.message_callback_add(EChannel.actuator_available, on_available_actuator_detected)

        self.client.connect(broker.host, broker.port)
        self.client.subscribe(EChannel.available, qos=1)
        self.client.subscribe(EChannel.actuator_available, qos=1)


app = FastAPI(
    docs_url="/",
    redoc_url="/redoc"
)
iot_service = IotService()


@app.on_event("startup")
async def startup():
    s: Session = Session_()
    gh = s.query(Greenhouse).filter(Greenhouse.label == "default").first()
    Constants.greenhouse_id = gh.id
    # only for test
    ser = DecisionTreeService()
    z = ser.create_tree(s)
    print(z)
    # only for test
    s.close()
    # iot_service.run()


@app.on_event("shutdown")
async def shutdown():
    ...
    # iot_service.stop()


@app.post("/decision/tree")
async def post_decision_tree(decision_tree_service: DecisionTreeService = Depends(DecisionTreeService), session=Depends(get_session)):
    decision_tree_service.create_tree(session)


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
    uvicorn.run("main:app", host="127.0.0.1", port=8001, env_file=".env")
