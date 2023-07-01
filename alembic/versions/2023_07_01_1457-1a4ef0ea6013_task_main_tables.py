"""task main tables

Revision ID: 1a4ef0ea6013
Revises: 0d038214965c
Create Date: 2023-07-01 14:57:27.466386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a4ef0ea6013'
down_revision = '0d038214965c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('priority',
    sa.Column('code_name', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code_name')
    )
    op.create_table('task',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('deadline', sa.DateTime(timezone=True), nullable=False),
    sa.Column('finished', sa.DateTime(timezone=True), nullable=False),
    sa.Column('is_project', sa.Boolean(), nullable=False),
    sa.Column('priority_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['priority_id'], ['priority.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_priority_id'), 'task', ['priority_id'], unique=False)
    op.create_table('tag',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'name')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=False)
    op.create_index(op.f('ix_tag_user_id'), 'tag', ['user_id'], unique=False)
    op.create_table('task_to_tag',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id', 'tag_id')
    )
    op.create_index(op.f('ix_task_to_tag_tag_id'), 'task_to_tag', ['tag_id'], unique=False)
    op.create_index(op.f('ix_task_to_tag_task_id'), 'task_to_tag', ['task_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_to_tag_task_id'), table_name='task_to_tag')
    op.drop_index(op.f('ix_task_to_tag_tag_id'), table_name='task_to_tag')
    op.drop_table('task_to_tag')
    op.drop_index(op.f('ix_tag_user_id'), table_name='tag')
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_table('tag')
    op.drop_index(op.f('ix_task_priority_id'), table_name='task')
    op.drop_table('task')
    op.drop_table('priority')
    # ### end Alembic commands ###
