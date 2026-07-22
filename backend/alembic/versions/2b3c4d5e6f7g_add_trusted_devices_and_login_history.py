"""Add trusted_devices and login_history tables

Revision ID: 2b3c4d5e6f7g
Revises: e02a8c4a467a
Create Date: 2026-07-22 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2b3c4d5e6f7g'
down_revision: Union[str, Sequence[str], None] = 'e02a8c4a467a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Create trusted_devices table if it doesn't exist
    if 'trusted_devices' not in inspector.get_table_names():
        op.create_table(
            'trusted_devices',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.BigInteger(), nullable=False),
            sa.Column('device_name', sa.String(length=255), nullable=False),
            sa.Column('device_fingerprint', sa.String(length=512), nullable=False),
            sa.Column('browser', sa.String(length=100), nullable=True),
            sa.Column('operating_system', sa.String(length=100), nullable=True),
            sa.Column('ip_address', sa.String(length=45), nullable=True),
            sa.Column('is_active', sa.Boolean(), server_default=sa.literal(True), nullable=False),
            sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('device_fingerprint'),
        )
        op.create_index(
            op.f('ix_trusted_devices_user_id'),
            'trusted_devices',
            ['user_id'],
            unique=False,
        )
        op.create_index(
            op.f('ix_trusted_devices_device_fingerprint'),
            'trusted_devices',
            ['device_fingerprint'],
            unique=True,
        )
    
    # Create login_history table if it doesn't exist
    if 'login_history' not in inspector.get_table_names():
        # Create LoginStatus enum
        try:
            conn.execute(sa.text("CREATE TYPE loginstatus AS ENUM ('SUCCESS', 'FAILED_INVALID_CREDENTIALS', 'FAILED_OTP_INVALID', 'FAILED_ACCOUNT_INACTIVE', 'FAILED_EMAIL_UNVERIFIED', 'FAILED_ACCOUNT_LOCKED')"))
        except Exception:
            pass
        
        op.create_table(
            'login_history',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.BigInteger(), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('ip_address', sa.String(length=45), nullable=True),
            sa.Column('browser', sa.String(length=255), nullable=True),
            sa.Column('operating_system', sa.String(length=255), nullable=True),
            sa.Column('device', sa.String(length=255), nullable=True),
            sa.Column('device_fingerprint', sa.String(length=512), nullable=True),
            sa.Column('location', sa.String(length=255), nullable=True),
            sa.Column('status', postgresql.ENUM('SUCCESS', 'FAILED_INVALID_CREDENTIALS', 'FAILED_OTP_INVALID', 'FAILED_ACCOUNT_INACTIVE', 'FAILED_EMAIL_UNVERIFIED', 'FAILED_ACCOUNT_LOCKED', name='loginstatus', create_type=False), server_default='SUCCESS', nullable=False),
            sa.Column('is_trusted_device', sa.Boolean(), server_default=sa.literal(False), nullable=False),
            sa.Column('failure_reason', sa.String(length=255), nullable=True),
            sa.Column('notification_sent', sa.Boolean(), server_default=sa.literal(False), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(
            op.f('ix_login_history_user_id'),
            'login_history',
            ['user_id'],
            unique=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'login_history' in inspector.get_table_names():
        op.drop_index(
            op.f('ix_login_history_user_id'),
            table_name='login_history',
        )
        op.drop_table('login_history')
        
        # Drop enum type
        try:
            conn.execute(sa.text("DROP TYPE loginstatus"))
        except Exception:
            pass
    
    if 'trusted_devices' in inspector.get_table_names():
        op.drop_index(
            op.f('ix_trusted_devices_device_fingerprint'),
            table_name='trusted_devices',
        )
        op.drop_index(
            op.f('ix_trusted_devices_user_id'),
            table_name='trusted_devices',
        )
        op.drop_table('trusted_devices')
