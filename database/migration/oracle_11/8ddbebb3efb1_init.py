"""init

Revision ID: 8ddbebb3efb1
Revises: 
Create Date: 2022-08-31 23:11:46.771608

"""
import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy.exc import DatabaseError

revision = '8ddbebb3efb1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    for table in [
        'sensor_record',
        'nutrient_irrigator_record',
        'sensor_allocation',
        'nutrient_irrigator',
        'basic_growth_info',
        'actuator_allocation',
        'greenhouse',
        'sensor',
        'farm',
        'actuator',
    ]:
        try:
            op.drop_table(table)
        except:
            continue

    op.create_table('actuator',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(length=255), nullable=True),
                    sa.Column('unit', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('farm',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('region', sa.String(length=255), nullable=True),
                    sa.Column('are_of_farm', sa.Float(), nullable=True),
                    sa.Column('number_of_greenhouse', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Farm info'
                    )
    op.create_table('sensor',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('local_id', sa.String(length=255), nullable=True),
                    sa.Column('address', sa.String(length=255), nullable=False),
                    sa.Column('type', sa.String(length=255), nullable=True),
                    sa.Column('unit', sa.String(length=255), nullable=True, comment='Đơn vị đo'),
                    sa.PrimaryKeyConstraint('id'),
                    comment='sensor description'
                    )
    op.create_table('greenhouse',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('type', sa.String(length=100), nullable=True),
                    sa.Column('area', sa.Float(), nullable=True),
                    sa.Column('height', sa.Float(), nullable=True),
                    sa.Column('width', sa.Float(), nullable=True),
                    sa.Column('length', sa.Float(), nullable=True),
                    sa.Column('cultivation_area', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['farm_id'], ['farm.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='greenhouse'
                    )
    op.create_table('actuator_allocation',
                    sa.Column('greenhouse_id', sa.Integer(), nullable=False),
                    sa.Column('actuator_id', sa.Integer(), nullable=False),
                    sa.Column('north', sa.Float(), nullable=True),
                    sa.Column('west', sa.Float(), nullable=True),
                    sa.Column('height', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['actuator_id'], ['actuator.id'], ),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse.id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'actuator_id')
                    )
    op.create_table('basic_growth_info',
                    sa.Column('greenhouse_id', sa.Integer(), nullable=False),
                    sa.Column('line_number', sa.Integer(), nullable=False),
                    sa.Column('cultivation_state_date', sa.DateTime(), nullable=True, comment='Ngày gieo hạt'),
                    sa.Column('cultivation_end_date', sa.DateTime(), nullable=True, comment='Ngày thu hoạch'),
                    sa.Column('specie', sa.String(length=500), nullable=True, comment='Giống cây'),
                    sa.Column('cultivation_method', sa.String(length=500), nullable=True, comment='Phương thức canh tác'),
                    sa.Column('number_of_crop', sa.Integer(), nullable=True, comment='Tổng số cay canh tác'),
                    sa.Column('number_of_crop_per_slab', sa.Integer(), nullable=True, comment='Số cây trên mỗi tấm trồng trọt'),
                    sa.Column('sow_date', sa.DateTime(), nullable=True, comment='Ngày gieo hạt'),
                    sa.Column('transplanting_date', sa.DateTime(), nullable=True, comment='Ngày cấy'),
                    sa.Column('species_of_graft_seeding', sa.String(length=255), nullable=True, comment='Các loài ghép hạt'),
                    sa.Column('species_of_graft_understock', sa.String(length=255), nullable=True, comment='Các loài ghép gốc'),
                    sa.Column('sow_date_of_seedling', sa.DateTime(), nullable=True),
                    sa.Column('transplanting_date_of_seedling', sa.DateTime(), nullable=True),
                    sa.Column('planting_density', sa.String(length=500), nullable=True, comment='Mật độ cây trồng'),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse.id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'line_number')
                    )
    op.create_table('nutrient_irrigator',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('greenhouse_id', sa.Integer(), nullable=True),
                    sa.Column('type', sa.String(length=100), nullable=True),
                    sa.Column('position_north', sa.Float(), nullable=True),
                    sa.Column('position_west', sa.Float(), nullable=True),
                    sa.Column('position_height', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='nutrient_irrigator'
                    )
    op.create_table('sensor_allocation',
                    sa.Column('greenhouse_id', sa.Integer(), nullable=False),
                    sa.Column('sensor_id', sa.Integer(), nullable=False),
                    sa.Column('north', sa.Float(), nullable=True),
                    sa.Column('west', sa.Float(), nullable=True),
                    sa.Column('height', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse.id'], ),
                    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'sensor_id'),
                    comment='sensor description'
                    )
    op.create_table('nutrient_irrigator_record',
                    sa.Column('irrigator_id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.DateTime(), nullable=False),
                    sa.Column('line_number', sa.String(length=100), nullable=False),
                    sa.Column('weather', sa.String(length=500), nullable=True),
                    sa.Column('number_of_week', sa.Integer(), nullable=True),
                    sa.Column('single_supply', sa.String(length=100), nullable=True),
                    sa.Column('ec', sa.String(length=100), nullable=True, comment='dS/m'),
                    sa.ForeignKeyConstraint(['irrigator_id'], ['nutrient_irrigator.id'], ),
                    sa.PrimaryKeyConstraint('irrigator_id', 'date', 'line_number'),
                    comment='nutrient_irrigator_record'
                    )
    op.create_table('sensor_record',
                    sa.Column('greenhouse_id', sa.Integer(), nullable=False),
                    sa.Column('sensor_id', sa.Integer(), nullable=False),
                    sa.Column('date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('weather', sa.String(length=500), nullable=True),
                    sa.Column('number_of_week', sa.String(length=200), nullable=True),
                    sa.Column('sensor_data', sa.String(length=500), nullable=True),
                    sa.Column('line_number', sa.String(length=200), nullable=True),
                    sa.ForeignKeyConstraint(['greenhouse_id', 'sensor_id'], ['sensor_allocation.greenhouse_id', 'sensor_allocation.sensor_id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'sensor_id', 'date'),
                    comment='Sensor'
                    )
    op.execute('INSERT INTO farm(id, number_of_greenhouse) VALUES (1, 10)')
    op.execute("INSERT INTO greenhouse(id, farm_id) VALUES (1, 1)")
    table_names = (
        "actuator",
        "farm",
        "sensor",
        "greenhouse",
        "nutrient_irrigator",
    )
    for name in table_names:
        try:
            op.execute(f"DROP SEQUENCE {name.upper()}_SEQ")
        except DatabaseError:
            ...
        op.execute(f"""
    CREATE SEQUENCE {name.upper()}_SEQ START WITH 2
        """)
        op.execute(f"""
    CREATE OR REPLACE TRIGGER {name.upper()}_INS
    BEFORE INSERT ON {name.upper()}
    FOR EACH ROW
    BEGIN
      SELECT {name}_SEQ.nextval
      INTO \\:new.ID
      FROM dual;
    END;
    """)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor_record')
    op.drop_table('nutrient_irrigator_record')
    op.drop_table('sensor_allocation')
    op.drop_table('nutrient_irrigator')
    op.drop_table('basic_growth_info')
    op.drop_table('actuator_allocation')
    op.drop_table('greenhouse')
    op.drop_table('sensor')
    op.drop_table('farm')
    op.drop_table('actuator')
    # ### end Alembic commands ###
