"""Market table

Revision ID: 6c56f2483c62
Revises: 25433e2d0885
Create Date: 2022-10-07 16:47:07.578841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c56f2483c62'
down_revision = '25433e2d0885'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_telegram', sa.String(), nullable=True))
    op.add_column('users', sa.Column('user_github', sa.String(), nullable=True))
    op.add_column('users', sa.Column('user_about_text', sa.String(), nullable=True))
    op.add_column('users', sa.Column('user_avatar_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_avatar_path')
    op.drop_column('users', 'user_about_text')
    op.drop_column('users', 'user_github')
    op.drop_column('users', 'user_telegram')
    # ### end Alembic commands ###
