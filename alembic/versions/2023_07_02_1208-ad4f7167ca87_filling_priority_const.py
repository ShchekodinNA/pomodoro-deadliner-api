"""filling priority const

Revision ID: ad4f7167ca87
Revises: 3ec20b583608
Create Date: 2023-07-02 12:08:57.156843

"""
from alembic import op
import sqlalchemy as sa
from src.constant_to_table import tabels_constants

# revision identifiers, used by Alembic.
revision = 'ad4f7167ca87'
down_revision = '3ec20b583608'
branch_labels = None
depends_on = None
priority_table = tabels_constants[1]

def upgrade() -> None:
    op.bulk_insert(priority_table.table, priority_table.content)


def downgrade() -> None:
    op.execute(priority_table.table.delete())
