"""enable pgvector extension

Revision ID: 91bd59b7a5e9
Revises: 
Create Date: 2026-09-16 15:26:01.937979

"""
from typing import Sequence, Union

from alembic import op



# revision identifiers, used by Alembic.
revision: str = '91bd59b7a5e9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """Downgrade schema."""
    pass
