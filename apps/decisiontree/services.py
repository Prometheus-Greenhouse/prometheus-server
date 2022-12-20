from datetime import datetime, timedelta
from typing import List, Any, Dict

import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apps.decisiontree.core.decison_tree_v2 import DecisionTreeCore
from apps.decisiontree.core.model import DecisionTreeDataModel
from apps.decisiontree.core.node import Node
from apps.enums.enums import ESensorType, EDayCycleValue, ERunValue, ETemperatureValue, EWaterValue, EHumidityValue, ESoilMoistureValue
from database.base import get_session
from database.models import SensorRecord, Sensor, NutrientIrrigatorRecord, SensorTypeMetadata, DecisionTree


class DecisionTreeService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.sensor_meta = dict()

    def create_tree(self) -> Node:
        data = self.consumeDataRecord(datetime.now() - timedelta(days=1), datetime.now())
        TARGET = ERunValue
        props = [EDayCycleValue,
                 ETemperatureValue,
                 EWaterValue,
                 EHumidityValue,
                 ESoilMoistureValue]
        core = DecisionTreeCore(TARGET)
        return core.create_node(props, data, None)

    def make_decision(self, sensor_data: float) -> Any:
        self.loadMetadata()
        water_q = self.session.query(SensorRecord.sensor_data.label(ESensorType.WATER.value)).join(
            Sensor, Sensor.id == SensorRecord.sensor_id
        ).filter(
            Sensor.type == ESensorType.WATER
        ).order_by(
            sa.desc(SensorRecord.id)
        ).subquery()

        temp_q = self.session.query(SensorRecord.sensor_data.label(ESensorType.TEMPERATURE.value)).join(
            Sensor, Sensor.id == SensorRecord.sensor_id
        ).filter(
            Sensor.type == ESensorType.TEMPERATURE
        ).order_by(
            sa.desc(SensorRecord.id)
        ).subquery()

        humidity_q = self.session.query(SensorRecord.sensor_data.label(ESensorType.HUMIDITY.value)).join(
            Sensor, Sensor.id == SensorRecord.sensor_id
        ).filter(
            Sensor.type == ESensorType.HUMIDITY
        ).order_by(
            sa.desc(SensorRecord.id)
        ).subquery()

        soil_q = self.session.query(SensorRecord.sensor_data.label(ESensorType.SOIL_MOISTURE.value)).join(
            Sensor, Sensor.id == SensorRecord.sensor_id
        ).filter(
            Sensor.type == ESensorType.SOIL_MOISTURE
        ).order_by(
            sa.desc(SensorRecord.id)
        ).subquery()

        rs = dict(self.session.query(water_q, temp_q, humidity_q, soil_q).first())
        decision_data = DecisionTreeDataModel.from_raw_value(
            day_cycle=EDayCycleValue.from_current_time(datetime.now()),
            water=float(rs[ESensorType.WATER.value]),
            temperature=float(rs[ESensorType.TEMPERATURE.value]),
            humidity=float(rs[ESensorType.HUMIDITY.value]),
            soil=float(rs[ESensorType.SOIL_MOISTURE.value]),
            run=None
        )
        d_tree: DecisionTree = self.session.query(DecisionTree).order_by(sa.desc(DecisionTree.id)).first()
        root_node: Dict = d_tree.tree
        return self.travel_tree(root_node, decision_data)

    def travel_tree(self, node: Dict, decision_data: DecisionTreeDataModel) -> Any:
        if not node["is_leaf"]:
            decision_value = decision_data.__getattribute__(node["name"])
            next_node = node["values"][decision_value]
            return self.travel_tree(next_node, decision_data)
        else:
            return node["decision"]

    def loadMetadata(self):
        for sensor_type in self.session.query(SensorTypeMetadata).all():
            DecisionTreeDataModel.__metadata__[sensor_type.type] = sensor_type.content

    def consumeDataRecord(self, from_: datetime, to: datetime) -> List[DecisionTreeDataModel]:
        self.loadMetadata()

        result = []
        cursor = from_
        while cursor < to:
            cright = cursor + timedelta(hours=1)
            not_in = ("NULL", "NAN", "NaN")
            water = self.session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_water")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.WATER,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            humidity = self.session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_humidity")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.HUMIDITY,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            temperature = self.session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_temperature")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.TEMPERATURE,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            soil = self.session.query(func.avg(func.to_number(SensorRecord.sensor_data)).label("avg_temperature")).join(
                Sensor, Sensor.id == SensorRecord.sensor_id
            ).filter(
                SensorRecord.created_at.between(cursor, cright),
                Sensor.type == ESensorType.SOIL_MOISTURE,
                SensorRecord.sensor_data.not_in(not_in),
            ).scalar()

            is_irrigator_run = bool(self.session.execute(
                select(1).where(
                    NutrientIrrigatorRecord.run_date.between(cursor, cright)
                )
            ).scalar())

            data = DecisionTreeDataModel.from_raw_value(
                day_cycle=EDayCycleValue.from_current_time(cursor),
                water=water,
                temperature=temperature,
                humidity=humidity,
                soil=soil,
                run=ERunValue.Y if is_irrigator_run else ERunValue.N
            )
            result.append(data)
            cursor = cursor + timedelta(hours=1)
        return result
