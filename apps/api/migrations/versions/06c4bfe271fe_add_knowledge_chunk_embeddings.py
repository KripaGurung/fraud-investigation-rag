"""add knowledge chunk embeddings

Revision ID: 06c4bfe271fe
Revises: 078a70f0956b
Create Date: 2026-09-21 13:26:18.112735
"""

from typing import Sequence, Union

from alembic import op
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "06c4bfe271fe"
down_revision: Union[str, Sequence[str], None] = "078a70f0956b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "knowledge_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "knowledge_chunks",
        "embedding",
    )