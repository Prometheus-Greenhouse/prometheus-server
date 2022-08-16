from typing import Dict

from fastapi import APIRouter, Depends, Body
from fastapi_utils.cbv import cbv

from database.models import Sensor
from database.repositories.sensor import SensorRepos

router = APIRouter()


@cbv(router)
class SensorAPI:
    repos: SensorRepos = Depends(SensorRepos)

    @router.post(
        path="/sensors"
    )
    async def post_sensor(self, sensor: Dict = Body(...)):
        self.repos.insert(Sensor(**sensor))
