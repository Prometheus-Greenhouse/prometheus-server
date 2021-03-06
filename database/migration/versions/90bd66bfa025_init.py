"""init

Revision ID: 90bd66bfa025
Revises: 
Create Date: 2022-07-09 15:27:59.364687

"""
from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision = '90bd66bfa025'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actuator',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(length=255), nullable=True),
                    sa.Column('unit', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('document',
                    sa.Column('los_id', sa.String(length=30), nullable=False),
                    sa.Column('state_id', sa.String(length=30), nullable=True),
                    sa.Column('state_name', sa.String(length=255), nullable=True),
                    sa.Column('content', sa.CLOB(), nullable=True),
                    sa.PrimaryKeyConstraint('los_id')
                    )
    op.create_table('farm_information',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('region', sa.String(length=255), nullable=True),
                    sa.Column('are_of_farm', sa.Float(), nullable=True),
                    sa.Column('number_of_greenhouse', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Farm info'
                    )
    op.create_table('sensor',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('address', sa.String(length=255), nullable=False),
                    sa.Column('type', sa.String(length=255), nullable=True),
                    sa.Column('unit', sa.String(length=255), nullable=True, comment='Đơn vị đo'),
                    sa.PrimaryKeyConstraint('id'),
                    comment='sensor description'
                    )
    op.create_table('user',
                    sa.Column('username', sa.String(length=100), nullable=False),
                    sa.Column('fullname', sa.String(length=255), nullable=True),
                    sa.Column('role_hierarchy', sa.CLOB(), nullable=True),
                    sa.PrimaryKeyConstraint('username')
                    )
    op.create_table('greenhouse_information',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('farm_id', sa.Integer(), nullable=True),
                    sa.Column('type', sa.String(length=100), nullable=True),
                    sa.Column('area', sa.Float(), nullable=True),
                    sa.Column('height', sa.Float(), nullable=True),
                    sa.Column('width', sa.Float(), nullable=True),
                    sa.Column('length', sa.Float(), nullable=True),
                    sa.Column('cultivation_area', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['farm_id'], ['farm_information.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='greenhouse_information'
                    )
    op.create_table('actuator_allocation',
                    sa.Column('greenhouse_id', sa.Integer(), nullable=False),
                    sa.Column('actuator_id', sa.Integer(), nullable=False),
                    sa.Column('north', sa.Float(), nullable=True),
                    sa.Column('west', sa.Float(), nullable=True),
                    sa.Column('height', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['actuator_id'], ['actuator.id'], ),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse_information.id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'actuator_id')
                    )
    op.create_table('basic_growth_information',
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
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse_information.id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'line_number')
                    )
    op.create_table('nutrient_irrigator',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('greenhouse_id', sa.Integer(), nullable=True),
                    sa.Column('type', sa.String(length=100), nullable=True),
                    sa.Column('position_north', sa.Float(), nullable=True),
                    sa.Column('position_west', sa.Float(), nullable=True),
                    sa.Column('position_height', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse_information.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='nutrient_irrigator'
                    )
    op.create_table('sensor_allocation',
                    sa.Column('greenhouse_id', sa.Integer(), nullable=False),
                    sa.Column('sensor_id', sa.Integer(), nullable=False),
                    sa.Column('north', sa.Float(), nullable=True),
                    sa.Column('west', sa.Float(), nullable=True),
                    sa.Column('height', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['greenhouse_id'], ['greenhouse_information.id'], ),
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
                    sa.Column('lint_number', sa.String(length=200), nullable=True),
                    sa.ForeignKeyConstraint(['greenhouse_id', 'sensor_id'], ['sensor_allocation.greenhouse_id', 'sensor_allocation.sensor_id'], ),
                    sa.PrimaryKeyConstraint('greenhouse_id', 'sensor_id', 'date'),
                    comment='Sensor'
                    )

    table_names = (
        "actuator",
        "farm_information",
        "sensor",
        "greenhouse_information",
        "nutrient_irrigator",
    )
    for name in table_names:
        op.execute(f"""
    CREATE SEQUENCE {name}_seq START WITH 1
        """)
        op.execute(f"""
    CREATE OR REPLACE TRIGGER {name}_ins
    BEFORE INSERT ON {name}
    FOR EACH ROW
    BEGIN
      SELECT {name}_seq.nextval
      INTO \\:new.id
      FROM dual;
    END;
    """)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor_record')
    op.drop_table('nutrient_irrigator_record')
    op.drop_table('sensor_allocation')
    op.drop_table('nutrient_irrigator')
    op.drop_table('basic_growth_information')
    op.drop_table('actuator_allocation')
    op.drop_table('greenhouse_information')
    op.drop_table('user')
    op.drop_table('sensor')
    op.drop_table('farm_information')
    op.drop_table('document')
    op.drop_table('actuator')
    # ### end Alembic commands ###
