"""

Revision ID: 1e6cc1f4505a
Revises: 717d0856a002
Create Date: 2023-04-02 22:56:56.420149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e6cc1f4505a'
down_revision = '717d0856a002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('polls_answers', sa.Column('answer_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('polls_answers', 'answer_date')
    # ### end Alembic commands ###
