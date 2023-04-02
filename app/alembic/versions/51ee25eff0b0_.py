"""

Revision ID: 51ee25eff0b0
Revises: 2aef1ac39c5b
Create Date: 2023-04-01 22:45:50.774347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51ee25eff0b0'
down_revision = '2aef1ac39c5b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('polls', sa.Column('entries', sa.PickleType(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('polls', 'entries')
    # ### end Alembic commands ###