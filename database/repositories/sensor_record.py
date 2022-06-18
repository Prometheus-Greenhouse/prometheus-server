from database.models import SensorRecord
from project.core import Repository


class SensorRecordRepos(Repository[SensorRecord, int]):
    ...
