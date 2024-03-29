"""Nonnullmarks

Revision ID: 153ada62087c
Revises: 71e75558909e
Create Date: 2023-09-03 14:43:45.013731

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '153ada62087c'
down_revision = '71e75558909e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contests', 'mark5',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('contests', 'mark4',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('contests', 'mark3',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contests', 'mark3',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('contests', 'mark4',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('contests', 'mark5',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###