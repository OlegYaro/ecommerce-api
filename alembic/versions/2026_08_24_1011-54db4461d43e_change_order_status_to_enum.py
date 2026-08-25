"""change order status to enum

Revision ID: 54db4461d43e
Revises: befb3230c818
Create Date: 2026-08-24 10:11:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '54db4461d43e'
down_revision: Union[str, None] = 'befb3230c818'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TYPE IF EXISTS orderstatus CASCADE")

    op.execute("CREATE TYPE orderstatus AS ENUM ('pending', 'approved', 'rejected')")

    op.execute(
        "ALTER TABLE orders "
        "ALTER COLUMN status TYPE orderstatus "
        "USING LOWER(status)::orderstatus"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE orders "
        "ALTER COLUMN status TYPE VARCHAR(16) "
        "USING status::text"
    )

    op.execute("DROP TYPE IF EXISTS orderstatus CASCADE")
