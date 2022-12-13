"""Fix token int to str 2

Revision ID: f2a1cee0c854
Revises: 07ebaaabc403
Create Date: 2022-12-13 22:22:01.878710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2a1cee0c854'
down_revision = '07ebaaabc403'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'oauth_tokens', ['token'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'oauth_tokens', type_='unique')
    # ### end Alembic commands ###
