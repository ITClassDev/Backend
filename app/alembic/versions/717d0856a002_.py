"""

Revision ID: 717d0856a002
Revises: ee896adea958
Create Date: 2023-04-02 22:35:18.299828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '717d0856a002'
down_revision = 'ee896adea958'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('polls_answers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('polls_answers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###