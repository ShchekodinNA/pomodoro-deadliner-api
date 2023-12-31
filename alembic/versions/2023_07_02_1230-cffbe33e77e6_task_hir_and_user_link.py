"""task hir and user link

Revision ID: cffbe33e77e6
Revises: ad4f7167ca87
Create Date: 2023-07-02 12:30:02.170012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cffbe33e77e6'
down_revision = 'ad4f7167ca87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('task', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_task_parent_id'), 'task', ['parent_id'], unique=False)
    op.create_index(op.f('ix_task_user_id'), 'task', ['user_id'], unique=False)
    op.drop_constraint('task_priority_id_fkey', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'task', ['parent_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'task', 'priority', ['priority_id'], ['id'])
    op.create_foreign_key(None, 'task', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_priority_id_fkey', 'task', 'priority', ['priority_id'], ['id'], ondelete='SET NULL')
    op.drop_index(op.f('ix_task_user_id'), table_name='task')
    op.drop_index(op.f('ix_task_parent_id'), table_name='task')
    op.drop_column('task', 'parent_id')
    op.drop_column('task', 'user_id')
    # ### end Alembic commands ###
