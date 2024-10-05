"""Add Device model

Revision ID: 70e453fcaef5
Revises: 4b7f6475faab
Create Date: 2024-10-05 17:46:51.088063

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '70e453fcaef5'
down_revision = '4b7f6475faab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('provider_device_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('device_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('last_reported_latitude', sa.Float(), nullable=True),
    sa.Column('last_reported_longitude', sa.Float(), nullable=True),
    sa.Column('is_online', sa.Boolean(), nullable=False),
    sa.Column('last_online_timestamp', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('telemetrydata', sa.Column('provider_device_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.alter_column('telemetrydata', 'device_id',
               existing_type=sa.VARCHAR(),
               type_=sa.Uuid(),
               nullable=False)
    op.drop_index('ix_telemetrydata_device_id', table_name='telemetrydata')
    op.drop_index('ix_telemetrydata_ident', table_name='telemetrydata')
    op.drop_index('telemetrydata_timestamp_idx', table_name='telemetrydata')
    op.create_foreign_key(None, 'telemetrydata', 'device', ['device_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'telemetrydata', type_='foreignkey')
    op.create_index('telemetrydata_timestamp_idx', 'telemetrydata', [sa.text('timestamp DESC')], unique=False)
    op.create_index('ix_telemetrydata_ident', 'telemetrydata', ['ident', 'timestamp'], unique=False)
    op.create_index('ix_telemetrydata_device_id', 'telemetrydata', ['device_id', 'timestamp'], unique=False)
    op.alter_column('telemetrydata', 'device_id',
               existing_type=sa.Uuid(),
               type_=sa.VARCHAR(),
               nullable=True)
    op.drop_column('telemetrydata', 'provider_device_id')
    op.drop_table('device')
    # ### end Alembic commands ###
