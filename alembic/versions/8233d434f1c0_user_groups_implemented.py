"""User groups implemented

Revision ID: 8233d434f1c0
Revises: eb466fc3377b
Create Date: 2023-01-11 19:05:38.959507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8233d434f1c0'
down_revision = 'eb466fc3377b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_groups', ['id'])
    op.add_column('users', sa.Column('groupId', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'groupId')
    op.drop_constraint(None, 'user_groups', type_='unique')
    # ### end Alembic commands ###
