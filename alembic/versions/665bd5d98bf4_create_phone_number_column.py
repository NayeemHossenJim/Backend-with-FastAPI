"""Create phone number column

Revision ID: 665bd5d98bf4
Revises: 
Create Date: 2025-11-16 16:26:01.441266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '665bd5d98bf4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('User', sa.Column('phone_number', sa.String(length=11), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
