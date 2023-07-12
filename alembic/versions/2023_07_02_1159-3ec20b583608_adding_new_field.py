"""adding new field

Revision ID: 3ec20b583608
Revises: 1a4ef0ea6013
Create Date: 2023-07-02 11:59:56.488784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ec20b583608'
down_revision = '1a4ef0ea6013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('priority', sa.Column('number', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'priority', ['number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'priority', type_='unique')
    op.drop_column('priority', 'number')
    # ### end Alembic commands ###