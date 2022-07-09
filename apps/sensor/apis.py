from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from paho.mqtt.client import Client

from project.configs import BROKER

router = APIRouter()


@cbv(router)
class SensorAPI:

    @router.get(
        path="/scan"
    )
    async def scan_sensors(self):
        ...
