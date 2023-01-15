"""Add db.tasks func_name

Revision ID: c5afab822b56
Revises: acf65fc8391f
Create Date: 2023-01-15 18:41:43.720825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5afab822b56'
down_revision = 'acf65fc8391f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('func_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'func_name')
    # ### end Alembic commands ###
