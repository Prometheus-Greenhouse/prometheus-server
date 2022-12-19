from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from apps.enums.enums import ESensorType, EDayCycle
from database.models import SensorRecord, Sensor


# from database.base import scoped_session

class DecisionTreeDataModel:
    def __init__(self,
                 day_cycle,
                 water,
                 temperature,
                 humidity,
                 soil,
                 run,
                 ):
        self.dayc = day_cycle
        self.water = water
        self.temperature = temperature
        self.humidity = humidity
        self.soil = soil
        self.run = run

    def __repr__(self):
        return "dayc {} water {} temp {} hum {} soil {} run {}".format(self.dayc, self.water, self.temperature, self.humidity, self.soil, self.run)


class DecisionTreeService:
    def create_tree(self, session: Session):
        return self.consumeDataRecord(datetime.now() - timedelta(days=1), datetime.now(), session)

    def consumeDataRecord(self, from_: datetime, to: datetime, session: Session) -> List[DecisionTreeDataModel]:
        result = []
        cursor = from_
        while cursor < to:
            cright = cursor + timedelta(hours=1)
            not_in = ("NULL", "NAN", "NaN")
            water = session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_water")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.WATER,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            humidity = session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_humidity")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.HUMIDITY,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            temperature = session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_temperature")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.TEMPERATURE,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            soil = session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_temperature")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.SOIL_MOISTURE,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            data = DecisionTreeDataModel(
                day_cycle=EDayCycle.DAY if (0 < cursor.hour < 12) else EDayCycle.NIGHT,
                water=water,
                temperature=temperature,
                humidity=humidity,
                soil=soil,
                run=""
            )
            result.append(data)

            cursor = cursor + timedelta(hours=1)
        return result
