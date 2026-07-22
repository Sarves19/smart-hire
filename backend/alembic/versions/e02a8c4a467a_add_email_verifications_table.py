"""Add email_verifications table

Revision ID: e02a8c4a467a
Revises: f46fb93c507d
Create Date: 2026-07-20 06:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e02a8c4a467a'
down_revision: Union[str, Sequence[str], None] = 'f46fb93c507d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    
    # Check if table already exists before creating it
    inspector = sa.inspect(conn)
    if 'email_verifications' not in inspector.get_table_names():
        # Create ENUM type with error handling
        try:
            conn.execute(sa.text("CREATE TYPE otppurpose AS ENUM ('EMAIL_VERIFICATION', 'PASSWORD_RESET')"))
        except Exception:
            # Type already exists, that's fine - continue
            pass
        
        op.create_table(
            'email_verifications',
            sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.BigInteger(), nullable=False),
            sa.Column('otp_hash', sa.String(length=255), nullable=False),
            sa.Column('purpose', postgresql.ENUM('EMAIL_VERIFICATION', 'PASSWORD_RESET', name='otppurpose', create_type=False), nullable=False),
            sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
            sa.Column('is_used', sa.Boolean(), server_default=sa.literal(False), nullable=False),
            sa.Column('attempts', sa.Integer(), server_default=sa.literal(0), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(
            op.f('ix_email_verifications_user_id'),
            'email_verifications',
            ['user_id'],
            unique=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'email_verifications' in inspector.get_table_names():
        op.drop_index(
            op.f('ix_email_verifications_user_id'),
            table_name='email_verifications',
        )
        op.drop_table('email_verifications')
    
    # Drop ENUM type if it exists
    try:
        conn.execute(sa.text("DROP TYPE otppurpose"))
    except Exception:
        # Type doesn't exist or couldn't be dropped, that's fine
        pass
