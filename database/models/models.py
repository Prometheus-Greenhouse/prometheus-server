from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, ForeignKeyConstraint, Identity, TIMESTAMP, text

from database.models.base import Base
from database.types import JSONLob, Boolean


class Actuator(Base):
    __tablename__ = "actuator"
    id = Column(Integer, Identity(), primary_key=True)
    local_id = Column(String(255))
    label = Column(String(255))
    type = Column(String(255))
    unit = Column(String(255))
    is_running = Column(Boolean(1))


class Farm(Base):
    __tablename__ = "farm"
    __table_args__ = {
        "comment": "Farm info"
    }

    id = Column(Integer, Identity(), primary_key=True)
    label = Column(String(255))
    region = Column(String(255))
    are_of_farm = Column(Float)
    number_of_greenhouse = Column(String(100))


class Greenhouse(Base):
    __tablename__ = "greenhouse"
    __table_args__ = {
        "comment": "greenhouse"
    }
    id = Column(Integer, Identity(), primary_key=True)
    farm_id = Column(Integer, ForeignKey("farm.id"))
    label = Column(String(255))
    type = Column(String(100))
    area = Column(Float)
    height = Column(Float)
    width = Column(Float)
    length = Column(Float)
    cultivation_area = Column(Float)
    is_default = Column(Boolean(1))


class NutrientIrrigator(Base):
    __tablename__ = "nutrient_irrigator"
    __table_args__ = {
        "comment": "nutrient_irrigator"
    }
    id = Column(Integer, Identity(), primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"))
    type = Column(String(100))
    position_north = Column(Float)
    position_west = Column(Float)
    position_height = Column(Float)


class Sensor(Base):
    __tablename__ = "sensor"
    __table_args__ = {
        "comment": "sensor description"
    }
    id = Column(Integer, Identity(), primary_key=True, )
    local_id = Column(String(255))
    label = Column(String(255))
    address = Column(String(255), nullable=False)
    type = Column(String(255), )
    unit = Column(String(255), comment="Đơn vị đo", )


class SensorAllocation(Base):
    __tablename__ = "sensor_allocation"
    __table_args__ = {
        "comment": "sensor description"
    }
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    north = Column(Float)
    west = Column(Float)
    height = Column(Float)


class SensorRecord(Base):
    __tablename__ = "sensor_record"
    __table_args__ = (ForeignKeyConstraint(("greenhouse_id", "sensor_id"), ("sensor_allocation.greenhouse_id", "sensor_allocation.sensor_id")), {
        "comment": "Sensor",
    })
    id = Column(Integer, Identity(), primary_key=True, )
    greenhouse_id = Column(Integer)
    sensor_id = Column(Integer)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    weather = Column(String(500))
    number_of_week = Column(String(255))
    sensor_data = Column(String(255))
    line_number = Column(String(255))
    update_ts = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class BasicGrowthInfo(Base):
    __tablename__ = "basic_growth_info"
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), primary_key=True)
    line_number = Column(Integer, primary_key=True)
    cultivation_state_date = Column(DateTime, comment="Ngày gieo hạt")
    cultivation_end_date = Column(DateTime, comment="Ngày thu hoạch")
    specie = Column(String(500), comment="Giống cây")
    cultivation_method = Column(String(500), comment="Phương thức canh tác")
    number_of_crop = Column(Integer, comment="Tổng số cay canh tác")
    number_of_crop_per_slab = Column(Integer, comment="Số cây trên mỗi tấm trồng trọt")
    sow_date = Column(DateTime, comment="Ngày gieo hạt")
    transplanting_date = Column(DateTime, comment="Ngày cấy")
    species_of_graft_seeding = Column(String(255), comment="Các loài ghép hạt")
    species_of_graft_understock = Column(String(255), comment="Các loài ghép gốc")
    sow_date_of_seedling = Column(DateTime, comment="")
    transplanting_date_of_seedling = Column(DateTime, comment="")
    planting_density = Column(String(500), comment="Mật độ cây trồng")


class ActuatorAllocation(Base):
    __tablename__ = "actuator_allocation"
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"), primary_key=True)
    actuator_id = Column(Integer, ForeignKey("actuator.id"), primary_key=True)
    north = Column(Float)
    west = Column(Float)
    height = Column(Float)


class NutrientIrrigatorRecord(Base):
    __tablename__ = "nutrient_irrigator_record"
    __table_args__ = {
        "comment": "nutrient_irrigator_record"
    }
    id = Column(Integer, primary_key=True)
    run_date = Column(DateTime)
    actuator_id = Column(Integer)


class ActuatorTask(Base):
    __tablename__ = "actuator_task"
    actuator_id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, primary_key=True)
    task_type = Column(String(255))
    start_value = Column(Float)
    limit_value = Column(Float)


class SensorTypeMetadata(Base):
    __tablename__ = 'sensor_type_metadata'

    type = Column(String(100), primary_key=True)
    content = Column(JSONLob)


class DecisionTree(Base):
    __tablename__ = "decision_tree"

    id = Column(Integer, Identity(), primary_key=True)
    actuator_id = Column(Integer)
    tree = Column(JSONLob)
