"""

Revision ID: e58677b07b7c
Revises: 0e7ec05efe82
Create Date: 2023-08-17 21:36:33.372271

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'e58677b07b7c'
down_revision = '0e7ec05efe82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contests',
    sa.Column('tasks', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('forGroups', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('authorId', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['authorId'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_contests_uuid'), 'contests', ['uuid'], unique=True)
    op.create_table('tasks',
    sa.Column('tests', sa.JSON(), nullable=True),
    sa.Column('types', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('authorId', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('timeLimit', sa.Integer(), nullable=False),
    sa.Column('memoryLimit', sa.Integer(), nullable=False),
    sa.Column('dayChallenge', sa.Boolean(), nullable=False),
    sa.Column('functionName', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['authorId'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_tasks_uuid'), 'tasks', ['uuid'], unique=True)
    op.create_table('submit',
    sa.Column('testsResults', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('current_timestamp(0)'), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('userId', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('taskId', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('source', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('referedContest', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('gitCommitId', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('solved', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['taskId'], ['tasks.uuid'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_submit_uuid'), 'submit', ['uuid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_submit_uuid'), table_name='submit')
    op.drop_table('submit')
    op.drop_index(op.f('ix_tasks_uuid'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_contests_uuid'), table_name='contests')
    op.drop_table('contests')
    # ### end Alembic commands ###