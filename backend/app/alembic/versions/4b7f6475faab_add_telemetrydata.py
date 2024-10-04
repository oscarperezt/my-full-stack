"""Add TelemetryData

Revision ID: 4b7f6475faab
Revises: 1a31ce608336
Create Date: 2024-09-28 17:52:56.905686

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '4b7f6475faab'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telemetrydata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('storage_server_timestamp_utc', sa.DateTime(), nullable=False),
    sa.Column('ident', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('position_altitude', sa.Float(), nullable=True),
    sa.Column('position_hdop', sa.Float(), nullable=True),
    sa.Column('position_latitude', sa.Float(), nullable=True),
    sa.Column('position_longitude', sa.Float(), nullable=True),
    sa.Column('position_satellites', sa.Integer(), nullable=True),
    sa.Column('server_timestamp', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('device_type_id', sa.Integer(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('protocol_id', sa.Integer(), nullable=True),
    sa.Column('engine_ignition_status', sa.Boolean(), nullable=True),
    sa.Column('device_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('device_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('din', sa.Integer(), nullable=True),
    sa.Column('event_enum', sa.Integer(), nullable=True),
    sa.Column('event_seqnum', sa.Integer(), nullable=True),
    sa.Column('gnss_antenna_status', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('gsm_network_roaming_status', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('message_type_enum', sa.Integer(), nullable=True),
    sa.Column('peer', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('position_direction', sa.Float(), nullable=True),
    sa.Column('position_speed', sa.Float(), nullable=True),
    sa.Column('position_valid', sa.Boolean(), nullable=True),
    sa.Column('timestamp_key', sa.Integer(), nullable=True),
    sa.Column('accumulator_0', sa.Float(), nullable=True),
    sa.Column('accumulator_1', sa.Float(), nullable=True),
    sa.Column('accumulator_2', sa.Float(), nullable=True),
    sa.Column('accumulator_3', sa.Float(), nullable=True),
    sa.Column('accumulator_4', sa.Float(), nullable=True),
    sa.Column('accumulator_5', sa.Float(), nullable=True),
    sa.Column('accumulator_6', sa.Float(), nullable=True),
    sa.Column('accumulator_7', sa.Float(), nullable=True),
    sa.Column('accumulator_8', sa.Float(), nullable=True),
    sa.Column('accumulator_9', sa.Float(), nullable=True),
    sa.Column('accumulator_10', sa.Float(), nullable=True),
    sa.Column('accumulator_11', sa.Float(), nullable=True),
    sa.Column('accumulator_12', sa.Float(), nullable=True),
    sa.Column('accumulator_13', sa.Float(), nullable=True),
    sa.Column('accumulator_14', sa.Float(), nullable=True),
    sa.Column('accumulator_15', sa.Float(), nullable=True),
    sa.Column('raw_data', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    # Convert the table to a hypertable, using the 'timestamp' column
    op.execute("""
        SELECT create_hypertable('telemetrydata', 'timestamp', if_not_exists => TRUE);
    """)

    # Add indexes on frequently queried columns
    op.create_index('ix_telemetrydata_ident', 'telemetrydata', ['ident', 'timestamp'])
    op.create_index('ix_telemetrydata_device_id', 'telemetrydata', ['device_id', 'timestamp'])


    # Enable compression on the hypertable with segment by device_id, order by timestamp
    op.execute("""
        ALTER TABLE telemetrydata SET (
            timescaledb.compress,
            timescaledb.compress_segmentby = 'device_id'
        );
    """)
    op.execute("""
        SELECT add_compression_policy('telemetrydata', INTERVAL '90 days');
    """)

    # Set retention policy to 720 days (2 years)
    op.execute("""
        SELECT add_retention_policy('telemetrydata', INTERVAL '720 days');
    """)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_telemetrydata_ident', table_name='telemetrydata')
    op.drop_index('ix_telemetrydata_device_id', table_name='telemetrydata')
    op.drop_index('ix_telemetrydata_timestamp', table_name='telemetrydata')
    op.drop_table('telemetrydata')
    # ### end Alembic commands ###
