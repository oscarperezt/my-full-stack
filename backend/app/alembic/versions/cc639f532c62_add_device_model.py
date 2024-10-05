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
    # Decompress existing chunks for 'telemetrydata' hypertable
    op.execute("""
        DO $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT show_chunks('telemetrydata')) LOOP
                EXECUTE 'SELECT decompress_chunk(' || quote_literal(r.show_chunks) || ');';
            END LOOP;
        END $$;
    """)

    # Disable compression on hypertable
    op.execute("""
        ALTER TABLE telemetrydata SET (timescaledb.compress = FALSE);
    """)

    # Proceed with schema changes
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

    # Rename the existing `device_id` column to `provider_device_id`
    op.alter_column('telemetrydata', 'device_id',
                    new_column_name='provider_device_id')

    # Add a new `device_id` column with UUID type
    op.add_column('telemetrydata', sa.Column('device_id', sa.Uuid(), nullable=False))

    op.drop_index('ix_telemetrydata_device_id', table_name='telemetrydata')
    op.drop_index('ix_telemetrydata_ident', table_name='telemetrydata')
    op.drop_index('telemetrydata_timestamp_idx', table_name='telemetrydata')
    op.create_foreign_key(None, 'telemetrydata', 'device', ['device_id'], ['id'])

    # Re-enable compression after schema changes
    op.execute("""
        ALTER TABLE telemetrydata SET (timescaledb.compress = TRUE);
    """)
    # ### end Alembic commands ###


def downgrade():
    # Drop the foreign key on the new `device_id` column
    op.drop_constraint(None, 'telemetrydata', type_='foreignkey')

    # Revert the addition of the `device_id` column
    op.drop_column('telemetrydata', 'device_id')

    # Rename `provider_device_id` back to `device_id`
    op.alter_column('telemetrydata', 'provider_device_id',
                    new_column_name='device_id')

    # Recreate dropped indexes
    op.create_index('telemetrydata_timestamp_idx', 'telemetrydata', [sa.text('timestamp DESC')], unique=False)
    op.create_index('ix_telemetrydata_ident', 'telemetrydata', ['ident', 'timestamp'], unique=False)
    op.create_index('ix_telemetrydata_device_id', 'telemetrydata', ['device_id', 'timestamp'], unique=False)

    # Drop the `provider_device_id` column added earlier
    op.drop_column('telemetrydata', 'provider_device_id')

    # Drop the `device` table
    op.drop_table('device')
    # ### end Alembic commands ###
