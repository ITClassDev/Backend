"""

Revision ID: 32975d459587
Revises: 5b93bb4378a5
Create Date: 2023-08-20 15:11:11.913230

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '32975d459587'
down_revision = '5b93bb4378a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contests', sa.Column('forLearningClass', sa.Integer(), nullable=True))
    op.alter_column('contests', 'deadline',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contests', 'deadline',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('contests', 'forLearningClass')
    # ### end Alembic commands ###