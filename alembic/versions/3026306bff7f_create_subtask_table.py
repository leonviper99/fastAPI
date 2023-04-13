"""create subtask table

Revision ID: 3026306bff7f
Revises: 678a2e7f0cdf
Create Date: 2023-04-13 12:54:14.756182

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.orm as orms

# revision identifiers, used by Alembic.
revision = '3026306bff7f'
down_revision = '678a2e7f0cdf'
branch_labels = None
depends_on = None

# op.add_column('subtasks',
#     sa.Column('taskid', sa.Integer())
# )
op.alter_column('subtasks', 'task_id', new_column_name='task_id')


def upgrade() -> None:
    pass
    # op.create_table(
    #     'subtasks',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('Title', sa.String(50), nullable=False),
    #     sa.Column('flag', sa.Boolean, default = False),
    #     sa.Column('status', sa.Boolean, default = False),
    #     orms.relationship('Task', backref='tasks', lazy='dynamic')
        
    # )

    



def downgrade() -> None:
    op.drop_table('tasks'),
    op.drop_table('subtasks'),
