from database.models import Sensor
from project.core import repos


@repos(Sensor, 1)
class SensorRepos:
    ...
