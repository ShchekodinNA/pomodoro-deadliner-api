"""Fill auth tabels

Revision ID: b618611a4984
Revises: 405f6c57e0c6
Create Date: 2023-06-21 17:49:09.722387

"""
from alembic import op
import sqlalchemy as sa
from src.auth.costants import BaseRolesEnum


# revision identifiers, used by Alembic.
revision = "b618611a4984"
down_revision = "405f6c57e0c6"
branch_labels = None
depends_on = None

user_role_table = sa.table(
    "user_role", sa.column("id", sa.Integer), sa.column("code_name", sa.String)
)

user_role_content = [{"code_name": item.value} for item in BaseRolesEnum]


def delete_content(table):
    op.execute(table.delete())


def upgrade() -> None:
    op.bulk_insert(user_role_table, user_role_content)


def downgrade() -> None:
    delete_content(user_role_table)
