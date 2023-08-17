"""

Revision ID: 8e6f973c3361
Revises: e58677b07b7c
Create Date: 2023-08-17 21:36:52.184918

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e6f973c3361'
down_revision = 'e58677b07b7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submits',
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
    op.create_index(op.f('ix_submits_uuid'), 'submits', ['uuid'], unique=True)
    op.drop_index('ix_submit_uuid', table_name='submit')
    op.drop_table('submit')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submit',
    sa.Column('testsResults', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP(0)'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP(0)'), autoincrement=False, nullable=False),
    sa.Column('uuid', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('userId', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('taskId', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('source', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('referedContest', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('gitCommitId', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('solved', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['taskId'], ['tasks.uuid'], name='fk_submit_taskId_tasks'),
    sa.ForeignKeyConstraint(['userId'], ['users.uuid'], name='fk_submit_userId_users'),
    sa.PrimaryKeyConstraint('uuid', name='pk_submit')
    )
    op.create_index('ix_submit_uuid', 'submit', ['uuid'], unique=False)
    op.drop_index(op.f('ix_submits_uuid'), table_name='submits')
    op.drop_table('submits')
    # ### end Alembic commands ###