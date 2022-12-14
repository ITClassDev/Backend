"""Add techstack field to user model

Revision ID: eb466fc3377b
Revises: df99a450cb06
Create Date: 2023-01-09 20:01:16.259553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb466fc3377b'
down_revision = 'df99a450cb06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('techStack', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'techStack')
    # ### end Alembic commands ###
