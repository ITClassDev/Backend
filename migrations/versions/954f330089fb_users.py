"""Users

Revision ID: 954f330089fb
Revises: b487ff7c8e06
Create Date: 2023-06-04 21:13:53.163069

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '954f330089fb'
down_revision = 'b487ff7c8e06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'techStack',
               existing_type=sa.VARCHAR(length=800),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'techStack',
               existing_type=sa.VARCHAR(length=800),
               nullable=False)
    # ### end Alembic commands ###