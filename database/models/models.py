from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, func, ForeignKeyConstraint, CLOB

from database.models.base import Base


class FarmInformation(Base):
    __tablename__ = "farm_information"
    __table_args__ = {
        "comment": "Farm info"
    }

    id = Column(Integer, primary_key=True)
    region = Column(String(255))
    are_of_farm = Column(Float)
    number_of_greenhouse = Column(String(100))


class GreenhouseInformation(Base):
    __tablename__ = "greenhouse_information"
    __table_args__ = {
        "comment": "greenhouse_information"
    }
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farm_information.id"))
    type = Column(String(100))
    area = Column(Float)
    height = Column(Float)
    width = Column(Float)
    length = Column(Float)
    cultivation_area = Column(Float)


class NutrientIrrigator(Base):
    __tablename__ = "nutrient_irrigator"
    __table_args__ = {
        "comment": "nutrient_irrigator"
    }
    id = Column(Integer, primary_key=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse_information.id"))
    type = Column(String(100))
    position_north = Column(Float)
    position_west = Column(Float)
    position_height = Column(Float)


class NutrientIrrigatorRecord(Base):
    __tablename__ = "nutrient_irrigator_record"
    __table_args__ = {
        "comment": "nutrient_irrigator_record"
    }
    irrigator_id = Column(Integer, ForeignKey("nutrient_irrigator.id"), primary_key=True)
    date = Column(DateTime, primary_key=True)
    line_number = Column(String(100), primary_key=True)
    weather = Column(String(500))
    number_of_week = Column(Integer)
    single_supply = Column(String(100))
    ec = Column(String(100), comment="dS/m")


class Sensor(Base):
    __tablename__ = "sensor"
    __table_args__ = {
        "comment": "sensor description"
    }
    id = Column(Integer, primary_key=True, )
    address = Column(String(255), nullable=False)
    type = Column(String(255), )
    unit = Column(String(255), comment="????n v??? ??o", )


class SensorAllocation(Base):
    __tablename__ = "sensor_allocation"
    __table_args__ = {
        "comment": "sensor description"
    }
    greenhouse_id = Column(Integer, ForeignKey("greenhouse_information.id"), primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    north = Column(Float)
    west = Column(Float)
    height = Column(Float)


class SensorRecord(Base):
    __tablename__ = "sensor_record"
    __table_args__ = (ForeignKeyConstraint(("greenhouse_id", "sensor_id"), ("sensor_allocation.greenhouse_id", "sensor_allocation.sensor_id")), {
        "comment": "Sensor",
    })
    greenhouse_id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, primary_key=True)
    date = Column(DateTime, primary_key=True, server_default=func.now())

    weather = Column(String(500))
    number_of_week = Column(String(200))
    sensor_data = Column(String(500))
    lint_number = Column(String(200))


class BasicGrowthInformation(Base):
    __tablename__ = "basic_growth_information"
    greenhouse_id = Column(Integer, ForeignKey("greenhouse_information.id"), primary_key=True)
    line_number = Column(Integer, primary_key=True)
    cultivation_state_date = Column(DateTime, comment="Ng??y gieo h???t")
    cultivation_end_date = Column(DateTime, comment="Ng??y thu ho???ch")
    specie = Column(String(500), comment="Gi???ng c??y")
    cultivation_method = Column(String(500), comment="Ph????ng th???c canh t??c")
    number_of_crop = Column(Integer, comment="T???ng s??? cay canh t??c")
    number_of_crop_per_slab = Column(Integer, comment="S??? c??y tr??n m???i t???m tr???ng tr???t")
    sow_date = Column(DateTime, comment="Ng??y gieo h???t")
    transplanting_date = Column(DateTime, comment="Ng??y c???y")
    species_of_graft_seeding = Column(String(255), comment="C??c lo??i gh??p h???t")
    species_of_graft_understock = Column(String(255), comment="C??c lo??i gh??p g???c")
    sow_date_of_seedling = Column(DateTime, comment="")
    transplanting_date_of_seedling = Column(DateTime, comment="")
    planting_density = Column(String(500), comment="M???t ????? c??y tr???ng")


class Actuator(Base):
    __tablename__ = "actuator"
    id = Column(Integer, primary_key=True)
    type = Column(String(255))
    unit = Column(String(255))


class ActuatorAllocation(Base):
    __tablename__ = "actuator_allocation"
    greenhouse_id = Column(Integer, ForeignKey("greenhouse_information.id"), primary_key=True)
    actuator_id = Column(Integer, ForeignKey("actuator.id"), primary_key=True)
    north = Column(Float)
    west = Column(Float)
    height = Column(Float)


class User(Base):
    __tablename__ = "user"

    username = Column(String(100), primary_key=True)
    fullname = Column(String(255))
    role_hierarchy = Column(CLOB)


class DocumentModel(Base):
    __tablename__ = "document"
    los_id = Column(String(30), primary_key=True)
    state_id = Column(String(30))
    state_name = Column(String(255))
    content = Column(CLOB)
