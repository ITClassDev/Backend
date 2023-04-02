"""

Revision ID: ee896adea958
Revises: 65ecb7ac85c8
Create Date: 2023-04-02 22:25:22.986036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee896adea958'
down_revision = '65ecb7ac85c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'polls_answers', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'polls_answers', type_='unique')
    # ### end Alembic commands ###