"""add postgis extension

Revision ID: a5a3eaecd65e
Revises: 55491cb2bd08
Create Date: 2026-06-18 18:32:09.683406

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a5a3eaecd65e"
down_revision: Union[str, Sequence[str], None] = "55491cb2bd08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS postgis")
